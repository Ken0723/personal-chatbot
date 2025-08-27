import os
from dotenv import load_dotenv
from app.services.gemini_service import GeminiPortfolioService

load_dotenv()

def test_gemini():
    """Test Connection"""
    service = GeminiPortfolioService()
    
    # Test Question
    test_questions = [
        "Tell me about Ken's experience",
        "What programming languages does Ken know?",
        "Ken 有咩工作經驗？",
        "What's the weather today?",
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = service.generate_response(question)
        
        if response['success']:
            print(f"✅ Response: {response['message']}")
            if response.get('cached'):
                print("   (From cache)")
        else:
            print(f"❌ Error: {response.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_gemini()