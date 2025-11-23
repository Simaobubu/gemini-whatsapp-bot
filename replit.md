# WhatsApp Bot com Flask, Gemini AI e Twilio

## Visão Geral
Backend Flask production-ready que integra a API Gemini para gerar respostas inteligentes e a API Twilio para receber e enviar mensagens do WhatsApp automaticamente.

## Funcionalidades
- ✅ Webhook Twilio para receber mensagens do WhatsApp
- ✅ Validação de assinatura Twilio para segurança
- ✅ Integração com Gemini API para gerar respostas inteligentes
- ✅ Envio automático de respostas via Twilio WhatsApp API
- ✅ Gerenciamento seguro de variáveis de ambiente via integração Replit
- ✅ Tratamento robusto de erros e logging para produção
- ✅ Mascaramento de dados sensíveis nos logs
- ✅ Lazy initialization com recuperação automática de falhas
- ✅ Health endpoint para monitoramento
- ✅ Configuração Gunicorn para produção

## Arquitetura do Projeto
```
/
├── app.py                      # Aplicação Flask principal
├── services/
│   ├── __init__.py
│   ├── gemini_service.py       # Serviço de integração Gemini AI
│   └── twilio_service.py       # Serviço de integração Twilio
├── .env.example                # Exemplo de configuração
├── .gitignore                  # Arquivos ignorados
├── README.md                   # Documentação completa
└── replit.md                   # Este arquivo
```

## Variáveis de Ambiente Necessárias
- `GEMINI_API_KEY`: Chave de API do Google Gemini (configurada via Replit Secrets)
- Twilio: Gerenciado via integração Replit (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER)
- `SESSION_SECRET`: Chave secreta para sessões Flask (opcional)

## Como Funciona
1. Usuário envia mensagem para o número WhatsApp configurado no Twilio
2. Twilio envia a mensagem para o webhook `/webhook/whatsapp` via POST com assinatura
3. O servidor valida a assinatura da requisição Twilio
4. Se válida, processa a mensagem e envia para Gemini AI
5. Gemini gera uma resposta inteligente
6. A resposta é enviada de volta ao usuário via Twilio WhatsApp API

## Configuração do Twilio
Para conectar o webhook:
1. Acesse o console Twilio
2. Vá em Messaging > Settings > WhatsApp sandbox settings
3. Configure o webhook URL: `https://73a3794f-43fe-4a23-9e0f-fd0eedcdc5c2-00-2co9wgm41y5ry.worf.replit.dev/webhook/whatsapp`
4. Selecione método POST
5. Teste enviando uma mensagem para o número Twilio

## Recursos de Segurança
- ✅ Validação de assinatura X-Twilio-Signature em todas as requisições do webhook
- ✅ Reconstrução de URL com headers de proxy (X-Forwarded-Proto, X-Forwarded-Host)
- ✅ Mascaramento de números de telefone e conteúdo de mensagens nos logs
- ✅ Respostas de erro genéricas sem exposição de detalhes internos
- ✅ Logging apenas com tipos de exceção, sem stack traces completas
- ✅ Gerenciamento seguro de credenciais via integração Replit

## Mudanças Recentes
- **2025-11-21**: Projeto criado com estrutura completa Flask + Gemini + Twilio
- **2025-11-21**: Implementada validação de assinatura Twilio
- **2025-11-21**: Adicionado mascaramento de dados sensíveis nos logs
- **2025-11-21**: Implementado lazy initialization com recuperação automática
- **2025-11-21**: Health endpoint atualizado para refletir estado em tempo real
- **2025-11-21**: Código revisado e aprovado como production-ready

## Preferências do Usuário
- Idioma: Português (Brasil)
- Stack: Python, Flask, Gemini AI, Twilio
- Segurança: Máxima prioridade com validação de webhooks e proteção de dados
