from transformers import AutoTokenizer, AutoModelForSequenceClassification
from django.utils.deprecation import MiddlewareMixin

class EmotionModelMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
        print("Emotion model loaded")

    def process_request(self, request):
        request.emotion_tokenizer = self.tokenizer
        request.emotion_model = self.model
        response = self.get_response(request)
        return response
