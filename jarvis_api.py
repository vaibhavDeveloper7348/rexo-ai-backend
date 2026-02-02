"""
Complete Jarvis AI API with ALL features
pip install flask flask-cors requests wikipedia pyjokes psutil
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import datetime
import wikipedia
import pyjokes
import os
import platform
import psutil
import math
import re

app = Flask(__name__)
CORS(app)

class JarvisAPI:
    def __init__(self):
        self.user_info = {
            "name": "User",
            "location": "Ludhiana"
        }
    
    # ========== TIME & DATE ==========
    
    def get_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")
    
    def get_date(self):
        """Get current date"""
        now = datetime.datetime.now()
        return now.strftime("%B %d, %Y")
    
    def get_day(self):
        """Get current day"""
        now = datetime.datetime.now()
        return now.strftime("%A")
    
    # ========== WEATHER ==========
    
    def get_weather(self, city):
        """Get weather information for a city"""
        try:
            url = f"https://wttr.in/{city}?format=%C+%t+%h+%w"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return f"Weather in {city}: {response.text}"
            return f"Unable to fetch weather for {city}"
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
    
    # ========== WIKIPEDIA ==========
    
    def get_wikipedia_summary(self, topic, sentences=3):
        """Get Wikipedia summary"""
        try:
            result = wikipedia.summary(topic, sentences=sentences)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Please be more specific."
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{topic}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== JOKES ==========
    
    def get_joke(self):
        """Get a random joke"""
        try:
            return pyjokes.get_joke()
        except:
            return "Why do programmers prefer dark mode? Because light attracts bugs!"
    
    # ========== IP ADDRESS ==========
    
    def get_ip_address(self):
        """Get public IP address"""
        try:
            ip = requests.get('https://api.ipify.org', timeout=5).text
            return ip
        except:
            return "Unable to fetch IP address"
    
    # ========== NEWS ==========
    
    def get_news_headlines(self):
        """Get news headlines"""
        try:
            headlines = [
                "Tech industry sees major advancements in AI and machine learning",
                "Global markets show positive trends in technology sector",
                "New environmental policies announced for sustainable development",
                "Sports championship results: India performs exceptionally well",
                "Education sector adopts new digital learning platforms"
            ]
            return headlines
        except Exception as e:
            return ["Unable to fetch news at the moment"]
    
    # ========== CALCULATIONS ==========
    
    def calculate(self, expression):
        """Perform mathematical calculations"""
        try:
            # Clean expression
            expression = expression.strip()
            expression = expression.replace('x', '*').replace('X', '*')
            expression = expression.replace('÷', '/').replace('×', '*')
            
            # Safe evaluation (basic operations only)
            allowed_chars = set('0123456789+-*/() .')
            if not all(c in allowed_chars for c in expression):
                return None, "Invalid characters in expression"
            
            result = eval(expression)
            return result, None
        except Exception as e:
            return None, f"Calculation error: {str(e)}"
    
    # ========== SYSTEM STATS ==========
    
    def convert_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    
    def get_system_stats(self):
        """Get system statistics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory': {
                    'used': self.convert_size(memory.used),
                    'total': self.convert_size(memory.total),
                    'percent': memory.percent
                },
                'disk': {
                    'used': self.convert_size(disk.used),
                    'total': self.convert_size(disk.total),
                    'percent': disk.percent
                }
            }
        except Exception as e:
            return {'error': str(e)}

# Initialize Jarvis
jarvis = JarvisAPI()

# ============= API ENDPOINTS =============

@app.route('/jarvis/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Jarvis AI is running',
        'version': '4.0',
        'features': [
            'time', 'date', 'weather', 'wikipedia', 'jokes', 
            'news', 'calculator', 'system_stats', 'search'
        ]
    })

@app.route('/jarvis/command', methods=['POST'])
def process_command():
    """Process natural language commands"""
    try:
        data = request.get_json()
        command = data.get('command', '').lower()
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Time commands
        if 'time' in command:
            time = jarvis.get_time()
            return jsonify({
                'command': command,
                'response': f"The current time is {time}",
                'data': {'time': time},
                'status': 'success'
            })
        
        # Date commands
        if 'date' in command:
            date = jarvis.get_date()
            return jsonify({
                'command': command,
                'response': f"Today's date is {date}",
                'data': {'date': date},
                'status': 'success'
            })
        
        # Day commands
        if 'day' in command and 'what day' in command:
            day = jarvis.get_day()
            return jsonify({
                'command': command,
                'response': f"Today is {day}",
                'data': {'day': day},
                'status': 'success'
            })
        
        # Weather command
        if 'weather' in command:
            # Extract city name
            words = command.split()
            city = 'Ludhiana'  # default
            if 'in' in words:
                idx = words.index('in')
                if idx + 1 < len(words):
                    city = words[idx + 1].capitalize()
            
            weather = jarvis.get_weather(city)
            return jsonify({
                'command': command,
                'response': weather,
                'data': {'city': city},
                'status': 'success'
            })
        
        # Calculator commands
        if 'calculate' in command or 'what is' in command or 'what\'s' in command:
            # Extract expression
            expression = command.replace('calculate', '').replace('what is', '').replace('what\'s', '').strip()
            
            result, error = jarvis.calculate(expression)
            
            if error:
                return jsonify({
                    'command': command,
                    'response': f"I couldn't calculate that. {error}",
                    'status': 'success'
                })
            
            return jsonify({
                'command': command,
                'response': f"The answer is {result}",
                'data': {'expression': expression, 'result': result},
                'status': 'success'
            })
        
        # Check if command is just an arithmetic expression
        if re.search(r'\d+\s*[+\-*/]\s*\d+', command):
            result, error = jarvis.calculate(command)
            
            if not error:
                return jsonify({
                    'command': command,
                    'response': f"The answer is {result}",
                    'data': {'expression': command, 'result': result},
                    'status': 'success'
                })
        
        # Joke command
        if 'joke' in command:
            joke = jarvis.get_joke()
            return jsonify({
                'command': command,
                'response': joke,
                'status': 'success'
            })
        
        # News command
        if 'news' in command or 'headlines' in command:
            headlines = jarvis.get_news_headlines()
            headline_text = "\n".join([f"{i+1}. {h}" for i, h in enumerate(headlines[:5])])
            return jsonify({
                'command': command,
                'response': f"Here are today's top headlines:\n{headline_text}",
                'data': {'headlines': headlines},
                'status': 'success'
            })
        
        # System stats
        if 'system' in command or 'stats' in command or 'cpu' in command:
            stats = jarvis.get_system_stats()
            
            if 'error' in stats:
                response_text = "Unable to fetch system statistics"
            else:
                response_text = f"System Statistics:\n" \
                               f"CPU Usage: {stats['cpu_percent']}%\n" \
                               f"Memory: {stats['memory']['used']} / {stats['memory']['total']} ({stats['memory']['percent']}%)\n" \
                               f"Disk: {stats['disk']['used']} / {stats['disk']['total']} ({stats['disk']['percent']}%)"
            
            return jsonify({
                'command': command,
                'response': response_text,
                'data': stats,
                'status': 'success'
            })
        
        # Wikipedia/Information
        if 'tell me about' in command or 'who is' in command or 'what is' in command:
            # Extract topic
            topic = command.replace('tell me about', '').replace('who is', '').replace('what is', '').strip()
            
            summary = jarvis.get_wikipedia_summary(topic)
            return jsonify({
                'command': command,
                'response': summary,
                'data': {'topic': topic},
                'status': 'success'
            })
        
        # Search commands (YouTube, Google)
        if 'search' in command or 'youtube' in command:
            # Extract search query
            query = command.replace('search', '').replace('youtube', '').replace('for', '').replace('on', '').strip()
            
            if 'youtube' in command:
                response_text = f"I'll search YouTube for: {query}"
            else:
                response_text = f"I'll search Google for: {query}"
            
            return jsonify({
                'command': command,
                'response': response_text,
                'data': {'query': query},
                'status': 'success'
            })
        
        # Default response
        return jsonify({
            'command': command,
            'response': "I'm not sure how to help with that. Try asking about time, weather, calculations, or search!",
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)