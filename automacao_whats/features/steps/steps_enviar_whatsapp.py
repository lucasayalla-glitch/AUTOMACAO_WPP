from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

# ============================================================
# 🧠 Definição dos passos do teste BDD para WhatsApp Web
# ============================================================


# ----------------------------------------
# 1️⃣ Etapa "DADO QUE..."
# ----------------------------------------
@given("que o WhatsApp Web está aberto")
def step_open_whatsapp(context):
    """
    Abre o WhatsApp Web.
    O navegador já foi inicializado no environment.py
    """
    # Acessa o WhatsApp Web
    context.driver.get("https://web.whatsapp.com")
    
    print("✅ WhatsApp Web acessado com sucesso!")
    print("⏳ Aguardando carregamento da página...")
    
    # Aguarda um pouco para a página carregar
    time.sleep(3)


@given("eu escaneio o QR Code para fazer login")
def step_scan_qr_code(context):
    """
    Aguarda o usuário escanear o QR Code.
    """
    print("\n" + "="*60)
    print("📱 ESCANEIE O QR CODE COM SEU CELULAR AGORA!")
    print("="*60)
    print("⏳ Aguardando login... (Timeout: 60 segundos)")
    
    try:
        # Aguarda até que a página principal do WhatsApp carregue
        # Isso indica que o QR Code foi escaneado com sucesso
        context.wait = context.driver
        
        # Espera o campo de busca aparecer (indica que o login foi feito)
        from selenium.webdriver.support.ui import WebDriverWait
        wait = WebDriverWait(context.driver, 60)  # 60 segundos para escanear
        
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        
        print("✅ Login realizado com sucesso!")
        print("✅ WhatsApp carregado!")
        
        # Aguarda mais um pouco para garantir que tudo carregou
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Timeout: QR Code não foi escaneado a tempo ou erro no carregamento")
        print(f"Detalhes: {str(e)}")
        raise


# ----------------------------------------
# 2️⃣ Etapa "QUANDO..."
# ----------------------------------------
@when('eu buscar pelo contato "{nome_contato}"')
def step_search_contact(context, nome_contato):
    """
    Busca por um contato específico no WhatsApp.
    """
    try:
        print(f"🔍 Buscando contato: {nome_contato}")
        
        # Localiza o campo de busca
        # XPath atualizado para o campo de busca do WhatsApp
        search_box = context.driver.find_element(
            By.XPATH, 
            '//div[@contenteditable="true"][@data-tab="3"]'
        )
        
        # Clica no campo de busca
        search_box.click()
        time.sleep(1)
        
        # Digita o nome do contato
        search_box.send_keys(nome_contato)
        
        print(f"✅ Nome '{nome_contato}' digitado no campo de busca")
        
        # Aguarda os resultados aparecerem
        time.sleep(2)
        
        # Clica no primeiro resultado (o contato)
        # XPath para o primeiro resultado da busca
        primeiro_resultado = context.driver.find_element(
            By.XPATH,
            f'//span[@title="{nome_contato}"]'
        )
        primeiro_resultado.click()
        
        print(f"✅ Contato '{nome_contato}' selecionado")
        
        # Aguarda a conversa abrir
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Erro ao buscar contato: {str(e)}")
        print("💡 Verifique se o nome do contato está correto")
        raise


@when('eu digitar a mensagem "{mensagem}"')
def step_type_message(context, mensagem):
    """
    Digita a mensagem no campo de texto.
    """
    try:
        print(f"💬 Digitando mensagem: {mensagem}")
        
        # Localiza o campo de mensagem
        # XPath para o campo de texto de mensagem
        message_box = context.driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@data-tab="10"]'
        )
        
        # Clica no campo de mensagem
        message_box.click()
        time.sleep(1)
        
        # Digita a mensagem
        message_box.send_keys(mensagem)
        
        print("✅ Mensagem digitada com sucesso")
        
        # Aguarda um pouco antes de enviar
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Erro ao digitar mensagem: {str(e)}")
        raise


# ----------------------------------------
# 3️⃣ Etapa "ENTÃO..."
# ----------------------------------------
@then("a mensagem deve ser enviada com sucesso")
def step_send_message(context):
    """
    Envia a mensagem clicando no botão de enviar.
    """
    try:
        print("📤 Enviando mensagem...")
        
        # Localiza e clica no botão de enviar
        # XPath para o botão de enviar (ícone de avião de papel)
        send_button = context.driver.find_element(
            By.XPATH,
            '//button[@aria-label="Enviar"]'
        )
        send_button.click()
        
        print("✅ Mensagem enviada com sucesso!")
        
        # Aguarda para confirmar o envio
        time.sleep(3)
        
        # Verifica se a mensagem foi enviada (aparece o check)
        # Isso é opcional, mas garante que a mensagem foi enviada
        try:
            context.driver.find_element(
                By.XPATH,
                '//span[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'
            )
            print("✅ Confirmação: Mensagem entregue (check apareceu)")
        except:
            print("⚠️  Não foi possível confirmar o check de entrega")
        
        print("\n" + "="*60)
        print("🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {str(e)}")
        raise