"""
Arquivo de configuração de ambiente do Behave
Gerencia hooks e configurações globais dos testes
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os


def before_all(context):
    """
    Executado UMA VEZ antes de todos os testes.
    Útil para configurações globais.
    """
    print("\n" + "="*60)
    print("🚀 INICIANDO SUITE DE TESTES DE AUTOMAÇÃO")
    print("="*60 + "\n")
    
    # Define configurações globais se necessário
    context.base_url = "https://www.google.com"
    context.timeout = 10


def before_scenario(context, scenario):
    """
    Executado ANTES de cada cenário (scenario).
    Ideal para inicializar o navegador.
    """
    print(f"\n▶️  Iniciando cenário: {scenario.name}")
    
    try:
        # Configurar as opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Opções adicionais para ambientes Linux/CI
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # ⭐ IMPORTANTE: Para WhatsApp Web - mantém sessão logada
        # Cria um diretório para armazenar os dados do perfil do usuário
        user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        
        # Desabilita notificações (opcional)
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        
        # Opção para rodar em modo headless (sem interface gráfica)
        # ⚠️ NÃO use headless para WhatsApp Web, pois precisa escanear QR Code
        # chrome_options.add_argument('--headless')
        
        # Usar webdriver-manager para gerenciar o ChromeDriver automaticamente
        service = Service(ChromeDriverManager().install())
        
        # Inicializar o navegador Chrome
        context.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configura timeout implícito
        context.driver.implicitly_wait(context.timeout)
        
        # Inicializa o WebDriverWait
        context.wait = WebDriverWait(context.driver, context.timeout)
        
        print("✅ Navegador inicializado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar navegador: {str(e)}")
        print("\n💡 DICAS DE SOLUÇÃO:")
        print("1. Instale o Chrome: sudo apt install google-chrome-stable")
        print("2. Instale webdriver-manager: pip install webdriver-manager")
        print("3. Ou use Firefox: sudo apt install firefox-geckodriver\n")
        raise


def after_scenario(context, scenario):
    """
    Executado DEPOIS de cada cenário.
    Garante que o navegador seja fechado.
    """
    # Verifica o status do cenário
    if scenario.status == "failed":
        print(f"❌ Cenário FALHOU: {scenario.name}")
        
        # Opcional: Tirar screenshot em caso de falha
        if hasattr(context, 'driver'):
            try:
                # Cria pasta de screenshots se não existir
                os.makedirs("screenshots", exist_ok=True)
                
                # Nome do arquivo com timestamp
                screenshot_name = f"screenshots/{scenario.name.replace(' ', '_')}_FAILED.png"
                context.driver.save_screenshot(screenshot_name)
                print(f"📸 Screenshot salvo em: {screenshot_name}")
            except Exception as e:
                print(f"⚠️  Erro ao salvar screenshot: {str(e)}")
    else:
        print(f"✅ Cenário passou: {scenario.name}")
    
    # Fecha o navegador
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
            print("🔒 Navegador fechado\n")
        except Exception as e:
            print(f"⚠️  Erro ao fechar navegador: {str(e)}\n")


def after_all(context):
    """
    Executado UMA VEZ após todos os testes.
    Útil para limpeza final ou relatórios.
    """
    print("\n" + "="*60)
    print("🏁 SUITE DE TESTES FINALIZADA")
    print("="*60 + "\n")

