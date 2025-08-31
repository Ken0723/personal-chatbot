import os
import json
import vertexai

from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
from typing import Dict, Optional
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class GeminiPortfolioService:
    def __init__(self):
        project_id = os.getenv('GCP_PROJECT_ID')
        location = os.getenv('GCP_LOCATION')
        
        vertexai.init(
            project=project_id,
            location=location
        )

        model_name = os.getenv('GEMINI_MODEL')

        self.model = GenerativeModel(model_name)

        with open('app/personal_data.json', 'r', encoding='utf-8') as f:
            self.personal_data = json.load(f)

        self.cache = {}
        
        logger.info(f"Initialized Gemini {model_name} in {location}")

    def _create_system_prompt(self, language: str) -> str:
        """system prompt"""
        data = self.personal_data.get(language, self.personal_data['en'])
        data_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        if language == 'zh_HK':
            return f"""你是 Ken 的個人網站聊天機器人。
嚴格規則：
1. 只能根據以下資料回答關於 Ken 的問題：
{data_str}

2. 對於任何與 Ken 無關的問題，必須回覆：
"我只能提供關於 Ken 的專業背景資訊。請問你想了解他的哪方面經驗？"

3. 絕對不能編造資料或回答資料以外的內容
4. 回答要簡潔專業，不超過 100 字
5. 用繁體中文回答"""
        
        else:
            return f"""You are Ken's portfolio chatbot assistant.

STRICT RULES:
1. You can ONLY answer questions about Ken based on this data:
{data_str}

2. For ANY unrelated questions, you MUST respond:
"I can only provide information about Ken's professional background. What would you like to know about his experience?"

3. NEVER make up information or answer beyond the provided data
4. Keep responses concise and professional, under 100 words
5. Respond in English"""
        
    def _check_cache(self, message_hash: str) -> Optional[str]:
        """cache checking"""
        if message_hash in self.cache:
            cached_data = self.cache[message_hash]
            time_diff = (datetime.now() - cached_data['time']).seconds
            if time_diff < 3600:  # 1 hour
                logger.info(f"Cache hit for hash: {message_hash}")
                return cached_data['response']
        return None
    
    def generate_response(self, user_message: str) -> Dict:
        """gen response"""
        try:
            # Language detection
            has_chinese = any(0x4e00 <= ord(c) <= 0x9fff for c in user_message)
            language = 'zh_HK' if has_chinese else 'en'
            
            # Check cache
            message_hash = hashlib.md5(
                user_message.lower().strip().encode()
            ).hexdigest()
            
            cached_response = self._check_cache(message_hash)
            if cached_response:
                return {
                    'success': True,
                    'message': cached_response,
                }
            
            # Prepare prompt    
            system_prompt = self._create_system_prompt(language)
            full_prompt = f"""{system_prompt}

User's Question: {user_message}

Response:"""
            
            # Gen Config
            generation_config = GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                top_k=40,
                max_output_tokens=200,
                candidate_count=1
            )
            
            # Gen response
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            # fetch text
            if response and response.text:
                response_text = response.text.strip()
                
                # Response checking
                if self._is_off_topic(user_message, response_text):
                    response_text = self._get_redirect_message(language)
                
                # Cache response
                self.cache[message_hash] = {
                    'response': response_text,
                    'time': datetime.now()
                }
                
                return {
                    'success': True,
                    'message': response_text,
                    'cached': False
                }
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            return {
                'success': False,
                'message': self._get_error_message(language),
                'error': str(e)
            }
        
    def _is_off_topic(self, user_message: str, response: str) -> bool:
        """Is it off topic"""
        # Blocked keyword
        forbidden_topics = [
            'weather', 'recipe', 'news', 'stock', 
            'movie', 'game', 'sports', 'politics'
        ]
        
        user_lower = user_message.lower()
        response_lower = response.lower()
        
        # no ken mentioned
        ken_mentioned = any(word in user_lower for word in ['ken', 'kenneth', '你', 'your'])
        
        if not ken_mentioned:
            for topic in forbidden_topics:
                if topic in response_lower and topic not in user_lower:
                    return True
        
        return False
    
    def _get_redirect_message(self, language: str) -> str:
        """Redirect msg"""
        if language == 'zh_HK':
            return "我只能提供關於 Ken 的專業背景資訊。請問你想了解他的工作經驗、技能還是項目？"
        else:
            return "I can only provide information about Ken's professional background. Would you like to know about his experience, skills, or projects?"
    
    def _get_error_message(self, language: str) -> str:
        """Error msg"""
        if language == 'zh_HK':
            return "抱歉，服務暫時不可用。請稍後再試。"
        else:
            return "Sorry, the service is temporarily unavailable. Please try again later."