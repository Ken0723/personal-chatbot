import os
import json
import re

from flask import Blueprint, request, jsonify, current_app
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime, timedelta
from app.services.gemini_service import GeminiPortfolioService

load_dotenv()
chatbot_service = GeminiPortfolioService()

api = Blueprint('api', __name__)

class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, ip):
        now = datetime.now()
        self.requests[ip] = [
            req_time for req_time in self.requests[ip]
            if now - req_time < timedelta(hours=1)
        ]
        
        # >= 30 per hours
        if len(self.requests[ip]) >= 30:
            return False
        
        # Log this request
        self.requests[ip].append(now)
        return True

rate_limiter = SimpleRateLimiter()

def sanitize_input(text):
    if not text or not isinstance(text, str):
        return None, "Invalid input"
    
    text = text.strip()
    
    if len(text) < 2:
        return None, "Message too short"
    
    if len(text) > 500:
        return None, "Message too long"
    
    dangerous_patterns = [
        # Prompt Injection
        r'ignore.{0,20}previous.{0,20}instructions',
        r'forget.{0,20}everything',
        r'disregard.{0,20}prior',
        r'override.{0,20}system',
        
        # Data Extraction
        r'system.{0,10}prompt',
        r'show.{0,10}all.{0,10}data',
        r'reveal.{0,10}instructions',
        
        # XSS (更嚴格)
        r'<[^>]*script',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe',
        r'<embed',
        r'<object',
        
        # Command Injection
        r'[;&|`]',
        r'\$\(',
        
        # Path Traversal
        r'\.\./',
        r'\.\.\\',
    ]
    
    text_lower = text.lower()
    
    # Compile patterns for better performance
    for pattern in dangerous_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return None, "Potentially harmful input detected"
    
    # Too Many Spec character
    special_char_count = sum(1 for c in text if not c.isalnum() and c not in ' .,!?')
    if special_char_count > len(text) * 0.3: # >30% number of character
        return None, "Too many special characters"
    
    return text, None

# API routes blue print
@api.route('/chat', methods=['POST'])
def chat():
    try:
        # Rate limiting
        user_ip = request.remote_addr
        if not rate_limiter.is_allowed(user_ip):
            return jsonify({
                'success': False,
                'message': 'Rate limit exceeded. Please try again later.'
            }), 429
        
        # Get and check the user's input
        user_message = request.json.get('message', '').strip()
        clean_message, error = sanitize_input(user_message)

        response = chatbot_service.generate_response(clean_message)

        return jsonify(response), 200 if response['success'] else 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error', 'error': str(e)}), 500
    
@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
    })

@api.route('/ci-cd-demo', methods=['GET'])
def ci_cd_demo():
    """CI/CD demo endpoint"""
    return jsonify({
        'success': True,
        'message': 'This is a demo api endpoint',
    })