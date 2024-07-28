import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from custom_exceptions import NoPageProtocoloManiobraException, NoProtocolosManiobrasException, NoDownloadProtManiException

# Ruta a tu navegador Chrome y al controlador de Chrome
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"  # Asegúrate de especificar la ruta correcta a tu navegador Chrome
CHROMEDRIVER_PATH = "Driver/chromedriver.exe"  # Asegúrate de especificar la ruta correcta al chromedriver
USER_DATA_DIR = r"C:/Path/To/Your/ChromeUserData"  # Asegúrate de especificar una ruta válida para el perfil de usuario

def init_variables():
    # Lanza Google Chrome con la depuración remota habilitada
    chrome_process = subprocess.Popen([
        CHROME_PATH,
        "--remote-debugging-port=9222",
        f"--user-data-dir={USER_DATA_DIR}"  # Asegúrate de especificar una ruta al perfil de usuario
    ])
    
    # Esperar un momento para que el navegador se inicie correctamente
    time.sleep(5)

    # Configura el servicio para el WebDriver de Chrome
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)

    # Configurar las opciones para Chrome
    chrome_options = ChromeOptions()
    chrome_options.debugger_address = "localhost:9222"

    # Inicializa el WebDriver para Chrome con el servicio y las opciones configuradas
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver, chrome_process
def check_for_element(driver, timeout=2):
    try:
        # Espera hasta que el elemento con el texto específico esté presente (máximo 15 segundos)
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'No hay cupos disponibles')]"))
        )
        return True
    except TimeoutException:
        return False

def check_for_button(driver, timeout=2):
    try:
        # Espera hasta que el botón con la clase específica esté presente (máximo 15 segundos)
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'botonEnlacePreinscripcion')]"))
        )
        # Extrae la URL de la propiedad onclick
        onclick_attribute = button.get_attribute("onclick")
        # Extrae la URL de la cadena onclick usando una expresión regular
        import re
        match = re.search(r"window.location = '([^']+)'", onclick_attribute)
        if match:
            return match.group(1)
        else:
            return False
    except TimeoutException:
        return False
    
def main(url):
    driver, chrome_process = init_variables()
    
    try:
        # Abre la página web donde se encuentra el elemento
        driver.get('https://estudiantes.portaloas.udistrital.edu.co/appserv/')
        button_url = None
        
        try:
            # Espera hasta que el título de la página sea el esperado (máximo 15 segundos)
            WebDriverWait(driver, 15).until(EC.title_is('Estudiantes'))
        except TimeoutException:
            raise NoPageProtocoloManiobraException()
        
        while True:
            # Abre la página web donde se encuentra el elemento
            driver.get(url)
            
            button_url = check_for_button(driver)

            # Verifica si el elemento con el texto específico está presente
            if not check_for_element(driver) and button_url:
                break  # Si el elemento no está presente, sale del bucle

            print("El elemento con el texto 'No hay cupos disponibles' está presente. Volviendo a intentar...")
            time.sleep(1)  # Espera antes de volver a intentar

        print(f"El elemento con el texto 'No hay cupos disponibles' ya no está presente.\nurl de inscripción:\n{button_url}")
        driver.get(button_url)
    finally:
        # Asegúrate de cerrar el proceso de Chrome cuando hayas terminado
        driver.quit()
        chrome_process.terminate()

if __name__ == "__main__":
    main(input('url de materia: '))
