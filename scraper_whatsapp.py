from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # NUEVO: Importamos las teclas del teclado
import time
import csv

def iniciar_extraccion():
    print("Iniciando navegador...")
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")

    input("Escaneá el código QR. Cuando veas tus chats cargados, presioná ENTER en esta consola...")
    time.sleep(3) 

    datos_extraidos = []
    chats_procesados = set() 
    intentos_sin_nuevos = 0 

    try:
        panel_chats = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pane-side"))
        )
        print("Comenzando la lectura masiva... (podés soltar el mouse)")

        while intentos_sin_nuevos < 3:
            chats_en_pantalla = panel_chats.find_elements(By.XPATH, './/div[@role="row"]')
            hubo_nuevos_en_esta_pasada = False

            for chat in chats_en_pantalla:
                try:
                    elementos_titulo = chat.find_elements(By.XPATH, './/span[@title]')
                    if not elementos_titulo:
                        continue
                        
                    nombre = elementos_titulo[0].get_attribute("title")
                    
                    if not nombre or nombre in chats_procesados:
                        continue 
                        
                    # IGNORAR GRUPOS Y DIFUSIONES
                    iconos_grupo = chat.find_elements(By.XPATH, './/span[@data-icon="default-group"] | .//span[@data-icon="default-broadcast"]')
                    if iconos_grupo:
                        print(f"⏩ Grupo/Difusión ignorado: {nombre}")
                        chats_procesados.add(nombre)
                        continue

                    # ENTRAR AL CHAT
                    chat.click()
                    time.sleep(2) 
                    
                    mensajes = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@dir="ltr"]')
                    
                    motivo = "Sin mensaje de texto (posible audio/imagen)"
                    if mensajes:
                        motivo = mensajes[0].text 
                    
                    datos_extraidos.append([nombre, motivo])
                    chats_procesados.add(nombre)
                    hubo_nuevos_en_esta_pasada = True
                    print(f"✅ Extraído: {nombre} | Total guardados: {len(datos_extraidos)}")
                    
                    time.sleep(1) 
                    
                except Exception as e:
                    continue

            # --- NUEVO SISTEMA DE SCROLL (SIMULA TECLADO) ---
            if not hubo_nuevos_en_esta_pasada:
                intentos_sin_nuevos += 1
                print(f"Buscando más chats en el fondo... (Intento {intentos_sin_nuevos}/3)")
            else:
                intentos_sin_nuevos = 0 

            # Hacemos clic en el último chat que vimos para asegurarnos de tener la lista seleccionada
            if chats_en_pantalla:
                chats_en_pantalla[-1].click()
                time.sleep(1)
                # Simulamos apretar la tecla "Page Down" (Av Pág) varias veces para bajar de golpe
                chats_en_pantalla[-1].send_keys(Keys.PAGE_DOWN)
                chats_en_pantalla[-1].send_keys(Keys.PAGE_DOWN)
            
            time.sleep(3) # Pausa para que WhatsApp cargue los de abajo

    except Exception as e:
        print(f"Error crítico durante el scraping: {e}")

    finally:
        print("Finalizado. Cerrando navegador y ordenando los datos...")
        driver.quit()
        guardar_en_csv_ordenado(datos_extraidos)

def guardar_en_csv_ordenado(datos):
    nombre_archivo = 'extraccion_masiva.csv'
    
    datos.sort(key=lambda x: x[0].lower())
    
    with open(nombre_archivo, 'w', newline='', encoding='utf-8-sig') as archivo:
        writer = csv.writer(archivo, delimiter=';')
        writer.writerow(['Nombre o Número', 'Primer Mensaje del Cliente']) 
        writer.writerows(datos)
        
    print(f"¡Listo! Se extrajeron {len(datos)} chats individuales. Guardados en {nombre_archivo}")

if __name__ == "__main__":
    iniciar_extraccion()