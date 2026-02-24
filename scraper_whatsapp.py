from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def iniciar_extraccion():
    # 1. Iniciar Chrome
    print("Iniciando navegador...")
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")

    # 2. Esperar al escaneo del QR
    input("Escaneá el código QR en WhatsApp Web. Cuando veas tus chats cargados, presioná ENTER en esta consola...")

    datos_extraidos = []

    try:
        # 3. Buscar el panel lateral de chats
        # Usamos WebDriverWait para darle tiempo a la página a reaccionar
        panel_chats = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pane-side"))
        )
        
        # Buscar los contenedores de cada chat
        chats = panel_chats.find_elements(By.XPATH, './/div[@role="listitem"]')
        print(f"Se detectaron {len(chats)} chats en pantalla. Iniciando lectura...")

        # 4. Iterar sobre los primeros 10 chats (podés aumentar este número luego)
        for chat in chats[:10]:
            try:
                chat.click()
                time.sleep(2) # Pausa clave para no ser bloqueados y dejar cargar el chat
                
                # Extraer nombre o número
                elemento_nombre = driver.find_element(By.XPATH, '//header//span[@dir="auto"]')
                nombre = elemento_nombre.text
                
                # Extraer los mensajes recibidos (message-in)
                mensajes = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@dir="ltr"]')
                
                motivo = "Sin mensaje de texto (posible audio/imagen)"
                if mensajes:
                    motivo = mensajes[0].text # Tomamos el primer mensaje visible del historial
                
                datos_extraidos.append([nombre, motivo])
                print(f"✅ Contacto extraído: {nombre}")
                
                time.sleep(1) # Pausa humana
                
            except Exception as e:
                print(f"⚠️ No se pudo procesar un chat. Saltando al siguiente...")
                continue

    except Exception as e:
        print(f"Error crítico durante el scraping: {e}")

    finally:
        # 5. Cerrar navegador y guardar
        print("Cerrando navegador y guardando datos...")
        driver.quit()
        
        # Generar el CSV
        guardar_en_csv(datos_extraidos)

def guardar_en_csv(datos):
    nombre_archivo = 'extraccion_masiva.csv'
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow(['Nombre_Numero', 'Primer_Mensaje_Visible']) # Encabezados
        writer.writerows(datos)
    print(f"¡Listo! Los datos se guardaron en {nombre_archivo}")

# Ejecutar el script
if __name__ == "__main__":
    iniciar_extraccion()