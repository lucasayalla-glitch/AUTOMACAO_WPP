# language: pt

Funcionalidade: Enviar mensagem pelo WhatsApp Web

  Cenário: Usuário envia mensagem para um contato
    Dado que o WhatsApp Web está aberto
    E eu escaneio o QR Code para fazer login
    Quando eu buscar pelo contato "Programação"
    E eu digitar a mensagem "Mensagem de teste."
    Então a mensagem deve ser enviada com sucesso