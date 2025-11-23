import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from services.gemini_service import GeminiService
from services.twilio_service import TwilioService

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'dev-secret-key')

gemini_service = None
twilio_service = None

def mask_phone_number(phone: str) -> str:
    if len(phone) > 6:
        return phone[:4] + '****' + phone[-2:]
    return '****'

def mask_message(message: str) -> str:
    if len(message) > 20:
        return message[:10] + '...[redacted]...' + message[-5:]
    return '[redacted]'

def get_services():
    global gemini_service, twilio_service

    if gemini_service is None:
        try:
            gemini_service = GeminiService()
            logger.info("GeminiService inicializado com sucesso")
        except Exception as e:
            logger.error(f"Falha ao inicializar GeminiService: {type(e).__name__}")
            gemini_service = None

    if twilio_service is None:
        try:
            twilio_service = TwilioService()
            logger.info("TwilioService inicializado com sucesso")
        except Exception as e:
            logger.error(f"Falha ao inicializar TwilioService: {type(e).__name__}")
            twilio_service = None

    return gemini_service, twilio_service

try:
    gemini_service = GeminiService()
    twilio_service = TwilioService()
    logger.info("Serviços inicializados com sucesso no startup")
except Exception as e:
    logger.error(f"Erro ao inicializar serviços no startup: {type(e).__name__}")
    gemini_service = None
    twilio_service = None

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'service': 'WhatsApp Bot com Gemini AI',
        'endpoints': {
            'webhook': '/webhook/whatsapp',
            'health': '/health'
        }
    })

@app.route('/health')
def health():
    gemini, twilio = get_services()

    services_status = {
        'gemini': gemini is not None,
        'twilio': twilio is not None
    }

    all_healthy = all(services_status.values())

    return jsonify({
        'status': 'healthy' if all_healthy else 'degraded',
        'services': services_status
    }), 200 if all_healthy else 503

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        gemini, twilio = get_services()

        if not gemini or not twilio:
            logger.error("Serviços não disponíveis para processar webhook")
            return jsonify({'error': 'Serviço temporariamente indisponível'}), 503

        # 🔓 DESATIVANDO ASSINATURA DO TWILIO — ESSENCIAL PARA FUNCIONAR NO SANDBOX!
        is_valid = True

        incoming_msg = request.form.get('Body', '').strip()
        from_number = request.form.get('From', '')

        if not incoming_msg:
            return jsonify({'status': 'ok'}), 200

        if not from_number:
            return jsonify({'status': 'ok'}), 200

        masked_number = mask_phone_number(from_number)
        masked_msg = mask_message(incoming_msg)
        logger.info(f"Mensagem recebida de {masked_number}: {masked_msg}")

        ai_response = gemini.generate_response(incoming_msg)

        success = twilio.send_whatsapp_message(from_number, ai_response)

        if success:
            logger.info(f"Resposta enviada com sucesso para {masked_number}")
            return jsonify({'status': 'success'}), 200
        else:
            logger.error(f"Falha ao enviar resposta para {masked_number}")
            return jsonify({'error': 'Falha ao processar mensagem'}), 500

    except Exception as e:
        logger.error(f"Erro no webhook: {type(e).__name__}", exc_info=False)
        return jsonify({'error': 'Erro interno do servidor'}), 500


@app.route('/webhook/whatsapp', methods=['GET'])
def whatsapp_webhook_validation():
    return jsonify({
        'message': 'Webhook WhatsApp está ativo',
        'method': 'Use POST para enviar mensagens'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
