import os
import logging
import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


def get_twilio_credentials():
    """Obtém credenciais Twilio da integração Replit ou variáveis de ambiente"""
    hostname = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
    x_replit_token = None
    
    repl_identity = os.getenv('REPL_IDENTITY')
    web_repl_renewal = os.getenv('WEB_REPL_RENEWAL')
    
    if repl_identity:
        x_replit_token = 'repl ' + repl_identity
    elif web_repl_renewal:
        x_replit_token = 'depl ' + web_repl_renewal
    
    if hostname and x_replit_token:
        try:
            response = requests.get(
                f'https://{hostname}/api/v2/connection?include_secrets=true&connector_names=twilio',
                headers={
                    'Accept': 'application/json',
                    'X_REPLIT_TOKEN': x_replit_token
                }
            )
            data = response.json()
            connection_settings = data.get('items', [{}])[0]
            
            if connection_settings and connection_settings.get('settings'):
                settings = connection_settings['settings']
                return {
                    'account_sid': settings.get('account_sid'),
                    'api_key': settings.get('api_key'),
                    'api_key_secret': settings.get('api_key_secret'),
                    'phone_number': settings.get('phone_number')
                }
        except Exception as e:
            logger.warning(f"Não foi possível obter credenciais da integração Replit: {type(e).__name__}")
    
    return {
        'account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
        'auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
        'phone_number': os.getenv('TWILIO_WHATSAPP_NUMBER')
    }


class TwilioService:
    def __init__(self):
        creds = get_twilio_credentials()
        
        account_sid = creds.get('account_sid')
        
        if creds.get('api_key') and creds.get('api_key_secret'):
            api_key = creds.get('api_key')
            api_key_secret = creds.get('api_key_secret')
            self.client = Client(api_key, api_key_secret, account_sid=account_sid)
            self.auth_token = api_key_secret
            logger.info("TwilioService inicializado com API Key da integração Replit")
        elif creds.get('auth_token'):
            auth_token = creds.get('auth_token')
            self.client = Client(account_sid, auth_token)
            self.auth_token = auth_token
            logger.info("TwilioService inicializado com credenciais de ambiente")
        else:
            raise ValueError("Credenciais Twilio não configuradas")
        
        self.whatsapp_number = creds.get('phone_number')
        
        if not self.whatsapp_number:
            raise ValueError("TWILIO_WHATSAPP_NUMBER não configurado")
        
        if not self.whatsapp_number.startswith('whatsapp:'):
            self.whatsapp_number = f'whatsapp:{self.whatsapp_number}'
        
        logger.info(f"TwilioService pronto com número {self.whatsapp_number}")
    
    def send_whatsapp_message(self, to_number: str, message_body: str) -> bool:
        try:
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            masked_number = to_number[:14] + '****' if len(to_number) > 14 else 'whatsapp:****'
            logger.info(f"Enviando mensagem WhatsApp para {masked_number}")
            
            message = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message_body,
                to=to_number
            )
            
            logger.info(f"Mensagem enviada com sucesso. SID: {message.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"Erro Twilio ao enviar mensagem: Código {e.code}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar mensagem WhatsApp: {type(e).__name__}")
            return False
    
    def validate_webhook_signature(self, request_url: str, post_vars: dict, signature: str) -> bool:
        try:
            from twilio.request_validator import RequestValidator
            
            validator = RequestValidator(self.auth_token)
            
            return validator.validate(request_url, post_vars, signature)
            
        except Exception as e:
            logger.error(f"Erro ao validar assinatura do webhook: {type(e).__name__}")
            return False
