import os
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash-exp"
        logger.info(f"GeminiService inicializado com modelo {self.model_id}")
    
    def generate_response(self, user_message: str) -> str:
        try:
            msg_preview = user_message[:20] + '...' if len(user_message) > 20 else user_message
            logger.info(f"Gerando resposta para mensagem (preview redacted)")
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=user_message,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            
            if response and response.text:
                logger.info(f"Resposta gerada com sucesso: {len(response.text)} caracteres")
                return response.text
            else:
                logger.warning("Resposta vazia do Gemini")
                return "Desculpe, não consegui gerar uma resposta no momento."
                
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com Gemini: {type(e).__name__}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
    
    def generate_contextual_response(self, user_message: str, context: str | None = None) -> str:
        try:
            if context:
                prompt = f"Contexto da conversa: {context}\n\nMensagem do usuário: {user_message}\n\nResponda de forma natural e útil:"
            else:
                prompt = user_message
            
            return self.generate_response(prompt)
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta contextual: {type(e).__name__}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."
