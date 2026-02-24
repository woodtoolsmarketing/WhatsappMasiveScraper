1. Verificar que Python responde
En tu misma terminal de VS Code, probá ejecutar esto para ver si Windows reconoce a Python:

PowerShell
python --version
(Nota: Si te vuelve a dar un error de "no se reconoce", probá escribiendo py --version. Si ambos fallan, significa que cuando instalaste Python en esa compu te olvidaste de marcar la casilla que dice "Add Python to PATH". En ese caso, hay que volver a ejecutar el instalador de Python y marcarla).

2. Crear el Entorno Virtual
Si el comando anterior te devolvió un número de versión (ej: Python 3.12.1), vamos a crear la burbuja aislada para este proyecto. Ejecutá:

PowerShell
python -m venv venv
(Si en el paso anterior te funcionó py, usá py -m venv venv). Vas a notar que se crea una carpetita nueva llamada venv en tu explorador de archivos a la izquierda.

3. Activar el Entorno
Ahora le decimos a la terminal de VS Code que empiece a usar esa burbuja. Ejecutá este comando:

PowerShell
.\venv\Scripts\activate
Si todo salió bien, vas a notar que la línea de tu terminal cambia y ahora tiene un (venv) verde al principio.

4. Instalar Selenium (Ahora sí)
Una vez que ves el (venv), tu terminal ya tiene a pip configurado y listo para la acción. Ejecutá:

PowerShell
pip install selenium
O, si ya habías creado el archivo de texto:

PowerShell
pip install -r requirements.txt
