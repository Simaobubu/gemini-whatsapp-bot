# WhatsApp Bot com Flask, Gemini AI e Twilio

Bot inteligente para WhatsApp que usa Gemini AI para gerar respostas automáticas via Twilio.

## 🚀 Funcionalidades

- ✅ Recebe mensagens do WhatsApp via webhook Twilio
- ✅ Gera respostas inteligentes usando Gemini AI
- ✅ Envia respostas automáticas de volta para o WhatsApp
- ✅ Tratamento de erros e logging completo
- ✅ Integração segura com credenciais Replit

## 📋 Pré-requisitos

1. **Conta Google AI Studio** - Para obter a chave GEMINI_API_KEY
2. **Conta Twilio** - Para usar o WhatsApp Business API
3. **Replit** - Para hospedar o bot

## 🔧 Configuração

### 1. Configurar Gemini API Key

A chave `GEMINI_API_KEY` já foi configurada nos secrets do Replit.

### 2. Configurar Twilio

A integração Twilio já foi configurada no Replit. Agora você precisa conectar o webhook:

#### Passo a passo:

1. **Acesse o Console Twilio:**
   - Vá para: https://console.twilio.com/

2. **Configure o WhatsApp Sandbox:**
   - Navegue para: **Messaging** → **Try it out** → **Send a WhatsApp message**
   - Ou acesse: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

3. **Conecte seu WhatsApp ao Sandbox:**
   - Siga as instruções para enviar uma mensagem do seu WhatsApp pessoal
   - Geralmente você precisa enviar uma mensagem como `join <código>` para o número Twilio

4. **Configure o Webhook URL:**
   - No console Twilio, vá para **WhatsApp Sandbox Settings**
   - Em **"When a message comes in"**, configure:
     - **URL:** `https://seu-dominio.replit.dev/webhook/whatsapp`
     - **Método:** `POST`
   - Clique em **Save**

### 3. Obter a URL do seu Replit

Sua aplicação está rodando em:
```
https://[seu-projeto].replit.dev
```

O endpoint do webhook é:
```
https://[seu-projeto].replit.dev/webhook/whatsapp
```

## 🧪 Testar o Bot

1. **Verifique se o servidor está rodando:**
   - Acesse: `https://seu-projeto.replit.dev/`
   - Deve retornar um JSON com status "online"

2. **Teste o webhook:**
   - Acesse: `https://seu-projeto.replit.dev/webhook/whatsapp`
   - Deve retornar uma mensagem indicando que o webhook está ativo

3. **Envie uma mensagem no WhatsApp:**
   - Envie qualquer mensagem para o número do Twilio Sandbox
   - O bot deve responder automaticamente usando Gemini AI

## 📡 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Status da aplicação |
| `/health` | GET | Verificação de saúde dos serviços |
| `/webhook/whatsapp` | POST | Recebe mensagens do Twilio |
| `/webhook/whatsapp` | GET | Informações sobre o webhook |

## 🔒 Variáveis de Ambiente

As seguintes variáveis são gerenciadas automaticamente:

- `GEMINI_API_KEY` - Chave da API Gemini (configurada via Replit Secrets)
- `TWILIO_ACCOUNT_SID` - ID da conta Twilio (via integração Replit)
- `TWILIO_AUTH_TOKEN` - Token de autenticação Twilio (via integração Replit)
- `TWILIO_WHATSAPP_NUMBER` - Número WhatsApp do Twilio (via integração Replit)

## 📁 Estrutura do Projeto

```
/
├── app.py                      # Aplicação Flask principal
├── services/
│   ├── __init__.py
│   ├── gemini_service.py       # Serviço Gemini AI
│   └── twilio_service.py       # Serviço Twilio WhatsApp
├── .env.example                # Exemplo de variáveis
├── .gitignore                  # Arquivos ignorados
├── README.md                   # Este arquivo
└── replit.md                   # Documentação do projeto
```

## 🛠️ Desenvolvimento

### Logs

Para ver os logs do servidor:
- No Replit, abra a aba de Console/Shell
- Os logs mostram todas as mensagens recebidas e enviadas

### Personalizar Respostas

Edite o arquivo `services/gemini_service.py` para ajustar:
- Temperatura da IA (criatividade)
- Tamanho máximo das respostas
- Instruções de contexto

## 🚀 Próximos Passos

Recursos que podem ser adicionados:

- [ ] Histórico de conversas por usuário
- [ ] Suporte para imagens e mídia
- [ ] Comandos especiais (ex: /ajuda, /info)
- [ ] Rate limiting
- [ ] Dashboard de métricas
- [ ] Respostas personalizadas por contexto

## 📝 Notas Importantes

- O Twilio Sandbox é **gratuito** mas tem limitações
- Para produção, você precisa de um **número Twilio aprovado** para WhatsApp
- O Gemini AI tem cotas gratuitas, mas pode ter limites de uso

## 🆘 Solução de Problemas

### Bot não responde:

1. Verifique se o servidor está rodando
2. Confirme se o webhook foi configurado corretamente no Twilio
3. Verifique os logs para ver se as mensagens estão chegando
4. Teste o endpoint `/health` para ver o status dos serviços

### Erro "Serviços não disponíveis":

1. Verifique se a GEMINI_API_KEY está configurada
2. Confirme se a integração Twilio está ativa
3. Reinicie o workflow

## 📄 Licença

Este projeto é de código aberto e está disponível para uso livre.
