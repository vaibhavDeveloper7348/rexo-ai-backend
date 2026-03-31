# Jack AI API - FIXED VERSION WITH CAMERA SAVE
# Properly returns URL and query data
# pip install flask flask-cors

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)

class JackAssistant:
    def __init__(self):
        # Extended FAQ database with all your questions
        self.faqs = {
            "what are the hostel facilities": "guru nanak dev engineering college provides well furnished rooms wifi common room mess gym and 24x7 security",
            "how can i apply for a hostel": "you need to fill out the hostel application form available on the college website or collect it from the hostel office",
            "what are the hostel fees": "fees vary based on room type and facilities it is best to check the official website or contact the hostel office",
            "is wifi available in the hostel": "yes wifi is provided but there may be usage restrictions",
            "what is your name":"i am jack ai",
            "are visitors allowed in the hostel": "only parents or guardians are allowed during visiting hours",
            "what are the hostel entry and exit timings": "entry and exit are restricted after 10 pm for security reasons",
            "is hostel mess food good": "the food quality is decent and the menu is planned with student preferences in mind",
            "are electric appliances allowed": "no most electric appliances are not allowed due to safety concerns",
            "is there 247 security in the hostel": "yes the hostel has cctv surveillance and security guards",
            "which programs are offered by it department": "the department offers btech in information technology and mtech in computer science and it full time",
            "what is the intake capacity for btech it": "the annual intake for btech it is 180 students as per website",
            "what postgraduate program is available": "mtech in computer science and information technology is offered full time",
            "who is the head of the it department": "the head of department is dr kulvinder singh mann",
            "how can i contact it department": "you can contact via email it at gndec ac in or phone number 9915507920",
            "does the department have nptel courses": "yes the department provides access to nptel moocs for honour degree",
            "what is the vision of the it department": "to groom technically competent it professionals especially from rural punjab",
            "what is the mission of the it department": "to uplift rural students and provide technical solutions to local society",
            "is gndec it ncat accredited": "yes the it department has nba accreditation till june 2025",
            "what facilities are available for students": "facilities include departmental library laboratories infrastructure central library training and placement sports",
            "where can i find time table": "class teacher and room time tables are available on the it department website under time tables section",
            "how can i view syllabus and study scheme": "you can download btech syllabus and study schemes on the website under programs section",
            "does the department organize training programs": "yes short induction programs and four week summer training ai ml iot are organized annually",
            "who is coordinator for summer training": "dr randeep kaur and prof himani sharma coordinate the summer training programme",
            "is there an induction program": "yes an induction program for new btech lateral entry and mtech students is organized in department library",
            "where to find archives and notices": "archives with notices such as datesheets and project notices are listed under the archives section",
            "does department organize technical workshops": "yes technical workshops hackathons leadership initiatives and career development programmes are organized",
            "how to download guidelines for training and project": "training guidelines formats and rubrics are available under guidelines section on website",
            "is the department involved in research": "yes faculty are active in ai ml iot image processing big data cloud computing and network security research",
            "where is the departmental lab located": "departmental laboratories and infrastructure details are available in the facilities section",
            "what courses are offered at gndec": "gndec offers undergraduate programs including btech in civil electrical mechanical electronics communication computer science information technology robotics and ai, barch, bca, bba, bvoc interior design; postgraduate mtech mba mca msc physics msc chemistry and doctoral programs",
            "how long is the btech program": "the btech program duration is four years divided into eight semesters",
            "what is the intake for civil engineering btech": "intake for civil engineering is 120 seats",
            "what is the intake for mechanical engineering btech": "intake for mechanical engineering is 150 seats",
            "what is the intake for cse btech": "intake for computer science and engineering is either 180 or 300 depending on intake year",
            "what is the intake for electrical engineering btech": "intake for electrical engineering is 90 seats",
            "what is the intake for electronics and communication engineering btech": "intake for ece is 90 seats",
            "what is the intake for information technology btech": "intake for information technology is 120 or 180 seats",
            "is robotics and ai offered at btech": "yes btech in robotics and artificial intelligence is available with 30 seats intake",
            "what postgraduate courses are available": "mtech in various specializations mba mca msc physics and msc chemistry are offered",
            "what is the mtech cse intake": "intake for mtech computer science and engineering is 12 seats",
            "what is the mtech ece intake": "intake for mtech electronics and communication engineering is 12 seats",
            "what is the mtech environmental intake": "intake for mtech environmental science and engineering is 6 or 12 depending on document",
            "what undergraduate commerce courses are available": "bba bca and bvoc interior design are offered at undergraduate level",
            "how many seats are there for bba": "bba has an intake of 60 students",
            "how many seats are there for bca": "bca intake is 60 or 180 depending on intake year",
            "what is the duration of mtech program": "mtech programs are two years full time or three years part time",
            "is doctorate phd offered": "yes phd admission is accepted under qip and ai in all engineering branches",
            "which authority is gndec affiliated to": "gndec is affiliated to ikg pt university and is an autonomous college under ugc act",
            "is gndec accredited": "yes accredited with naac a grade and most ug programs are nba accredited",
            "when was gndec established": "gndec was established in 1956 under nankana sahib education trust",
            "what is the vision of gndec": "its vision is excellence in rural india serving rural communities through technical education",
            "does gndec have hostels": "yes boys and girls hostel facilities are available",
            "does gndec hostels have wifi": "yes 24 hours internet facility with leased line backup",
            "is there security in hostels": "yes cctv surveillance and security guards are present",
            "does gndec have ncc and nss": "yes it has an ncc company and three and a half units of nss",
            "has gndec won sports championships": "yes it has been overall sports champion of ikgptu",
            "does gndec have an fm radio station": "yes gndec has an fm radio station under community fm scheme",
            "does gndec have central library": "yes central library with print journals and ebooks is available",
            "does gndec have auditorium and workshop": "yes there is an auditorium and well equipped workshops",
            "does gndec have a dispensary on campus": "yes a dispensary is available on campus",
            "does gndec have a bank and post office": "yes bank branch and post office are located on campus",
            "is gndec campus urban": "yes located in urban area at gill road ludhiana spanning about 88 acres",
            "how far is gndec from railway station": "the campus is approximately 2 km from ludhiana railway station",
            "does gndec offer scholarships": "yes scholarships are available details in brochure pages 17 18",
            "what is the fee for btech first year": "first year btech fee is approximately rupees 96400",
            "what is lateral entry in btech": "yes lateral entry is allowed for diploma holders under specific eligibility",
            "what is eligibility for btech": "10 plus 2 with physics and mathematics and one of chemistry biology cs biotech",
            "is diploma accepted for entry": "yes diploma holders are eligible for lateral entry under ptu guidelines",
            "what entrance exam is needed for btech": "admission via jee main and ptu online counselling",
            "is nata required for barch": "yes for barch nata score based counselling is followed",
            "how many rural seats are there": "70 percent seats reserved for rural area candidates",
            "what is the quota for state vs other": "85 percent seats are for punjab candidates 15 percent for other states",
            "does gndec have sports facilities": "yes sports ground gymnasium and indoor sports are available",
            "is transportation available": "yes college runs bus service and public transport is available nearby",
            "is there cafeteria or mess": "yes mess and cafeteria is available on campus",
            "does gndec have placement cell": "yes there is a training and placement cell with strong industry ties",
            "which companies visit for placements": "companies like tcs wipro infosys accenture amongst others recruit from gndec",
            "do alumni work abroad": "yes alumni are placed in companies in india usa uk germany canada etc"
        }
        
        self.questions = list(self.faqs.keys())
        
        # College FAQ shortcuts
        self.college_faq_answers = {
            "btech programs": "GNDEC offers UG, PG, and PhD programs in engineering, management, and sciences.",
            "btech duration": "The B.Tech program at GNDEC lasts for 4 years.",
            "mtech specializations": "M.Tech specializations include CSE, Mechanical, Electrical, Structural, and more.",
            "departments": "GNDEC has departments in Civil, Mechanical, Electrical, CS, IT, Business, and more.",
            "btech fees": "The first-year B.Tech fee is approximately rupees 96,400.",
            "lateral entry": "Yes, GNDEC allows lateral entry into B.Tech for diploma holders.",
            "hostel facilities": "Yes, GNDEC provides hostel facilities for students."
        }

    def get_answer(self, user_question):
        """Find best matching answer"""
        user_question = user_question.lower()
        
        best_match = None
        best_score = 0
        
        for question in self.questions:
            similarity = SequenceMatcher(None, user_question, question).ratio()
            user_words = set(user_question.split())
            question_words = set(question.split())
            word_overlap = len(user_words & question_words) / max(len(user_words), 1)
            score = (similarity * 0.6) + (word_overlap * 0.4)
            
            if score > best_score:
                best_score = score
                best_match = question
        
        if best_score >= 0.3:
            return self.faqs[best_match]
        else:
            return "Sorry, I don't have an answer to that question."

    def parse_command(self, command):
        """
        Parse command and return proper action with data
        Returns: dict with action, message, url, query
        """
        cmd = command.lower().strip()
        
        # Camera commands - WITH SAVE FUNCTIONALITY
        if "camera" in cmd:
            if "open" in cmd or "start" in cmd:
                return {
                    "action": "OPEN_CAMERA",
                    "message": "Opening camera on your mobile"
                }
            elif "close" in cmd or "stop" in cmd:
                return {
                    "action": "CLOSE_CAMERA",
                    "message": "Closing camera"
                }
            # NEW: Capture/Take photo command
            elif "capture" in cmd or "take" in cmd or "click" in cmd or "photo" in cmd or "picture" in cmd:
                return {
                    "action": "CAPTURE_PHOTO",
                    "message": "Capturing photo and saving to gallery",
                    "save_to_gallery": True
                }
        
        # NEW: Direct photo capture commands
        if ("take" in cmd or "click" in cmd or "capture" in cmd) and ("photo" in cmd or "picture" in cmd or "pic" in cmd):
            return {
                "action": "CAPTURE_PHOTO",
                "message": "Capturing photo and saving to gallery",
                "save_to_gallery": True
            }
        
        # YouTube - specific handling
        if "youtube" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening YouTube",
                    "url": "https://www.youtube.com"
                }
        
        # Facebook
        if "facebook" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening Facebook",
                    "url": "https://www.facebook.com"
                }
        
        # Instagram
        if "instagram" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening Instagram",
                    "url": "https://www.instagram.com"
                }
        
        # Twitter/X
        if "twitter" in cmd or " x " in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening Twitter",
                    "url": "https://www.twitter.com"
                }
        
        # LinkedIn
        if "linkedin" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening LinkedIn",
                    "url": "https://www.linkedin.com"
                }
        
        # GitHub
        if "github" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_WEBSITE",
                    "message": "Opening GitHub",
                    "url": "https://www.github.com"
                }
        
        # Browser opening
        if "browser" in cmd or ("open" in cmd and "google" in cmd):
            return {
                "action": "OPEN_BROWSER",
                "message": "Opening browser",
                "url": "https://www.google.com"
            }
        
        if "close" in cmd and "browser" in cmd:
            return {
                "action": "CLOSE_BROWSER",
                "message": "Closing browser"
            }
        
        # Search commands - FIXED
        if "search" in cmd:
            # Extract search query
            query = cmd.replace("search", "").replace("for", "").strip()
            
            # Remove common words
            query = query.replace("on google", "").replace("google", "").strip()
            
            if query:
                return {
                    "action": "SEARCH_GOOGLE",
                    "message": f"Searching for {query}",
                    "query": query
                }
            else:
                return {
                    "action": "FAQ_ANSWER",
                    "answer": "What do you want me to search for?"
                }
        
        # Website opening - general pattern
        if "open" in cmd:
            words = cmd.split()
            try:
                open_index = words.index("open")
                if open_index + 1 < len(words):
                    website = words[open_index + 1]
                    
                    # Handle common websites
                    if website in ["google", "youtube", "facebook", "instagram", 
                                   "twitter", "linkedin", "github", "amazon", "netflix"]:
                        url = f"https://www.{website}.com"
                        return {
                            "action": "OPEN_WEBSITE",
                            "message": f"Opening {website}",
                            "url": url
                        }
                    # Handle URLs
                    elif "." in website:
                        url = website if website.startswith("http") else f"https://{website}"
                        return {
                            "action": "OPEN_WEBSITE",
                            "message": f"Opening {website}",
                            "url": url
                        }
            except:
                pass
        
        # Application commands
        if "calculator" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_APP",
                    "message": "Opening calculator",
                    "app": "calculator"
                }
            elif "close" in cmd:
                return {
                    "action": "CLOSE_APP",
                    "message": "Closing calculator",
                    "app": "calculator"
                }
        
        if "settings" in cmd and "open" in cmd:
            return {
                "action": "OPEN_APP",
                "message": "Opening settings",
                "app": "settings"
            }
        
        if "contacts" in cmd and "open" in cmd:
            return {
                "action": "OPEN_APP",
                "message": "Opening contacts",
                "app": "contacts"
            }
        
        if "gallery" in cmd or "photos" in cmd:
            if "open" in cmd:
                return {
                    "action": "OPEN_APP",
                    "message": "Opening gallery",
                    "app": "gallery"
                }
        
        # Default: treat as FAQ question
        answer = self.get_answer(command)
        return {
            "action": "FAQ_ANSWER",
            "answer": answer
        }

# Initialize Jack Assistant
jack = JackAssistant()

# ============= API ENDPOINTS =============

@app.route('/jack/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Jack AI is running',
        'version': '3.2',
        'mode': 'mobile_first_with_camera_save',
        'features': ['faq', 'camera', 'camera_capture', 'browser', 'search', 'applications', 'websites']
    })

@app.route('/jack/ask', methods=['POST'])
def ask_question():
    """Ask Jack a question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        answer = jack.get_answer(question)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'action': 'FAQ_ANSWER',
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/jack/command', methods=['POST'])
def process_command():
    """
    Process natural language commands
    Returns properly formatted response with action, message, url, query
    """
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        # Parse command and get result
        result = jack.parse_command(command)
        
        # Build response
        response = {
            'command': command,
            'status': 'success'
        }
        
        # Add all fields from parse result
        if 'action' in result:
            response['action'] = result['action']
        
        if 'message' in result:
            response['message'] = result['message']
        
        if 'answer' in result:
            response['answer'] = result['answer']
        
        if 'url' in result:
            response['url'] = result['url']
        
        if 'query' in result:
            response['query'] = result['query']
        
        if 'app' in result:
            response['app'] = result['app']
        
        if 'save_to_gallery' in result:
            response['save_to_gallery'] = result['save_to_gallery']
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': str(e), 
            'status': 'failed'
        }), 500

@app.route('/jack/add_faq', methods=['POST'])
def add_faq():
    """Add new FAQ"""
    try:
        data = request.get_json()
        question = data.get('question', '').lower()
        answer = data.get('answer', '')
        
        if not question or not answer:
            return jsonify({'error': 'Question and answer required'}), 400
        
        jack.faqs[question] = answer
        jack.questions = list(jack.faqs.keys())
        
        return jsonify({
            'message': 'FAQ added successfully',
            'question': question,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/jack/get_all_faqs', methods=['GET'])
def get_all_faqs():
    """Get all FAQs"""
    try:
        return jsonify({
            'faqs': jack.faqs,
            'total_count': len(jack.faqs),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
