from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import re
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_sql_injection_patterns():
    """Return regex patterns for SQL injection detection"""
    return [
        r"(?i)(?:union.*select|select.*from|insert.*into|update.*set|delete.*from|drop.*table)",
        r"(?i)(?:'\s*or\s*'|\"\s*or\s*\"|\bor\b\s*\d+\s*=\s*\d+)",
        r"(?i)(?:'\s*--|\"\s*--|;\s*--|#|/\*)",
        r"(?i)(?:\bwaitfor\s+delay\b|\bsleep\b)"
    ]

def analyze_sql_query(query):
    """
    Analyze a single SQL query for injection patterns
    Returns: (is_vulnerable, matched_patterns)
    """
    sql_patterns = detect_sql_injection_patterns()
    matched_patterns = []
    
    for i, pattern in enumerate(sql_patterns):
        if re.search(pattern, query):
            pattern_names = [
                "SQL Command Injection",
                "Boolean-based Injection",
                "Comment-based Injection",
                "Time-based Injection"
            ]
            matched_patterns.append(pattern_names[i])
    
    return len(matched_patterns) > 0, matched_patterns

def load_csv_data(csv_filename):
    """Load data from CSV file"""
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def find_sql_injection_attempts(data, sql_patterns):
    """Find SQL injection attempts in CSV data"""
    attacker_ip = None
    sql_attempts = []
    formatted_symbol_count = 0
    
    for row in data:
        info = row.get('Info', '')
        
        if any(re.search(pattern, info) for pattern in sql_patterns):
            if not attacker_ip:
                attacker_ip = row.get('Source')
            
            if row.get('Source') == attacker_ip:
                sql_attempts.append((row.get('Time'), info))
                if ':' in info:
                    formatted_symbol_count += 1
    
    return attacker_ip, sql_attempts, formatted_symbol_count

def process_csv_file(filepath):
    """Process uploaded CSV file for SQL injection analysis"""
    data = load_csv_data(filepath)
    sql_patterns = detect_sql_injection_patterns()
    attacker_ip, sql_attempts, formatted_symbol_count = find_sql_injection_attempts(data, sql_patterns)
    sql_attempts.sort()
    
    first_payload = sql_attempts[0][1] if sql_attempts else "NULL"
    last_payload = sql_attempts[-1][1] if sql_attempts else "NULL"

    results = {
        'attacker_ip': attacker_ip if attacker_ip else 'NULL',
        'attempt_count': len(sql_attempts),
        'first_payload': first_payload,
        'last_payload': last_payload,
        'formatted_symbol_count': formatted_symbol_count,
        'all_attempts': [{'time': t, 'payload': p} for t, p in sql_attempts[:10]]  # First 10 attempts
    }
    return results

# ============= API ENDPOINTS =============

@app.route('/sql/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'SQL Injection Detection API is running'
    })

@app.route('/sql/scan_query', methods=['POST'])
def scan_query():
    """
    Scan a single SQL query for vulnerabilities
    Request: {"query": "SELECT * FROM users WHERE id = 1"}
    Response: {"is_vulnerable": false/true, "patterns": [...]}
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        is_vulnerable, matched_patterns = analyze_sql_query(query)
        
        response = {
            'query': query,
            'is_vulnerable': is_vulnerable,
            'vulnerability_level': 'HIGH' if is_vulnerable else 'SAFE',
            'matched_patterns': matched_patterns,
            'pattern_count': len(matched_patterns),
            'status': 'success'
        }
        
        if is_vulnerable:
            response['recommendation'] = 'This query contains potential SQL injection patterns. Use parameterized queries.'
        else:
            response['recommendation'] = 'No SQL injection patterns detected in this query.'
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sql/scan_file', methods=['POST'])
def scan_file():
    """
    Scan uploaded CSV file for SQL injection attempts
    Expects multipart/form-data with 'file' field
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process file
        results = process_csv_file(filepath)
        
        # Clean up - remove file after processing
        os.remove(filepath)
        
        return jsonify({
            'results': results,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sql/test_examples', methods=['GET'])
def test_examples():
    """Get example queries for testing"""
    examples = {
        'vulnerable_queries': [
            "SELECT * FROM users WHERE username = 'admin' OR '1'='1'",
            "SELECT * FROM products WHERE id = 1; DROP TABLE users--",
            "SELECT * FROM accounts WHERE id = 1 UNION SELECT username, password FROM admin"
        ],
        'safe_queries': [
            "SELECT * FROM users WHERE id = ?",
            "SELECT name, email FROM customers WHERE status = 'active'",
            "INSERT INTO logs (action, timestamp) VALUES (?, NOW())"
        ]
    }
    
    return jsonify({
        'examples': examples,
        'status': 'success'
    })

@app.route('/sql/batch_scan', methods=['POST'])
def batch_scan():
    """
    Scan multiple queries at once
    Request: {"queries": ["query1", "query2", ...]}
    """
    try:
        data = request.get_json()
        queries = data.get('queries', [])
        
        if not queries:
            return jsonify({'error': 'No queries provided'}), 400
        
        results = []
        vulnerable_count = 0
        
        for query in queries:
            is_vulnerable, matched_patterns = analyze_sql_query(query)
            if is_vulnerable:
                vulnerable_count += 1
            
            results.append({
                'query': query,
                'is_vulnerable': is_vulnerable,
                'matched_patterns': matched_patterns
            })
        
        return jsonify({
            'total_queries': len(queries),
            'vulnerable_count': vulnerable_count,
            'safe_count': len(queries) - vulnerable_count,
            'results': results,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=False)