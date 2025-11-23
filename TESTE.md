# Instruções para Testar o WhatsApp Bot

## URL do Webhook
```
https://73a3794f-43fe-4a23-9e0f-fd0eedcdc5c2-00-2co9wgm41y5ry.worf.replit.dev/webhook/whatsapp
```

## Passo a Passo para Configurar no Twilio

### 1. Acessar o Console Twilio
- Acesse: https://console.twilio.com/

### 2. Configurar WhatsApp Sandbox
1. No menu lateral, vá em **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Ou acesse diretamente: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

### 3. Conectar seu WhatsApp
1. Você verá um número Twilio (geralmente +1 415 523 8886)
2. Envie uma mensagem do seu WhatsApp pessoal para esse número
3. A mensagem deve ser: `join <código>` (o código aparece na tela)
4. Você receberá uma confirmação de que está conectado ao sandbox

### 4. Configurar o Webhook
1. Na mesma página do Sandbox, procure por **Sandbox Configuration**
2. Em **"When a message comes in"**:
   - Cole a URL: `https://73a3794f-43fe-4a23-9e0f-fd0eedcdc5c2-00-2co9wgm41y5ry.worf.replit.dev/webhook/whatsapp`
   - Método: **POST**
3. Clique em **Save**

### 5. Testar o Bot
1. Envie qualquer mensagem para o número Twilio do seu WhatsApp
2. Aguarde alguns segundos
3. Você deve receber uma resposta inteligente gerada pelo Gemini AI!

## Exemplos de Mensagens para Testar

```
Olá! Como você está?
```

```
Qual é a capital do Brasil?
```

```
Me conte uma piada
```

```
Explique o que é inteligência artificial em termos simples
```

## Verificar Status do Servidor

### Endpoint Raiz
```bash
curl https://73a3794f-43fe-4a23-9e0f-fd0eedcdc5c2-00-2co9wgm41y5ry.worf.replit.dev/
```

Resposta esperada:
```json
{
  "status": "online",
  "service": "WhatsApp Bot com Gemini AI",
  "endpoints": {
    "webhook": "/webhook/whatsapp",
    "health": "/health"
  }
}
```

### Endpoint de Saúde
```bash
curl https://73a3794f-43fe-4a23-9e0f-fd0eedcdc5c2-00-2co9wgm41y5ry.worf.replit.dev/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "services": {
    "gemini": true,
    "twilio": true
  }
}
```

## Monitorar Logs

Os logs do servidor mostrarão:
- Mensagens recebidas (com números mascarados)
- Respostas geradas
- Mensagens enviadas
- Qualquer erro (sem expor dados sensíveis)

## Solução de Problemas

### Bot não responde?
1. Verifique se o endpoint `/health` retorna `"status": "healthy"`
2. Confirme que a URL do webhook foi configurada corretamente no Twilio
3. Verifique se você está enviando mensagens do número conectado ao sandbox
4. Veja os logs do servidor para identificar erros

### Erro 403 (Não autorizado)?
- A assinatura Twilio não está sendo validada corretamente
- Verifique se a URL configurada no Twilio é exatamente a mesma do servidor

### Serviços não disponíveis?
1. Verifique se a `GEMINI_API_KEY` está configurada nos Secrets
2. Confirme se a integração Twilio está ativa
3. Reinicie o servidor se necessário

## Notas Importantes

- O Twilio Sandbox é **gratuito** mas tem limitações
- Apenas números que enviaram `join <código>` podem interagir com o bot
- Para produção, você precisa de um número Twilio aprovado para WhatsApp Business
- O Gemini AI tem cotas gratuitas, mas pode ter limites de uso

## Próximos Passos

Depois de testar e validar, você pode:
1. Personalizar as respostas do Gemini editando `services/gemini_service.py`
2. Adicionar comandos especiais (ex: /ajuda, /sobre)
3. Implementar histórico de conversas
4. Adicionar suporte para imagens e mídia
5. Publicar a aplicação para produção no Replit
