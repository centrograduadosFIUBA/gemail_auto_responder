# Gmail Auto Responder

Un sistema automatizado para enviar respuestas automáticas a correos electrónicos en Gmail utilizando Python y la API de Gmail.

## Descripción

Esta aplicación permite configurar y enviar respuestas automáticas a los correos electrónicos recibidos en tu cuenta de Gmail. Es especialmente útil durante períodos de ausencia, vacaciones o cuando necesitas gestionar un alto volumen de correos entrantes.

## Características

- Autenticación segura con la API de Gmail
- Detección automática de nuevos correos
- Configuración personalizable de respuestas automáticas
- Registro de correos respondidos para evitar duplicados
- Manejo seguro de credenciales

## Requisitos Previos

- Python 3.7 o superior
- Una cuenta de Gmail
- Credenciales de la API de Google (credenciales.json)

## Instalación

1. Asegúrate de tener todos los archivos necesarios:
   - `.env`: Archivo de configuración con las variables de entorno
   - `credenciales.json`: Archivo de credenciales de la API de Google
   - `requirements.txt`: Lista de dependencias del proyecto

2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
├── .env                  # Variables de entorno y configuración
├── env _ejemplo        # Ejemplo de configuración de variables de entorno
├── credenciales.json    # Credenciales de la API de Google
├── gmail_responder.py   # Script principal del auto respondedor
├── requirements.txt     # Dependencias del proyecto
├── token.json          # Token de autenticación generado (luego de conectar)
└── README.md           # Documentación del proyecto
```

## Configuración

1. Copia el archivo `env _ejemplo` a `.env`
2. Edita el archivo `.env` con tus configuraciones personales:
   - Configuración de la cuenta de Gmail
   - Mensaje de respuesta automática
   - Otras configuraciones necesarias

## Obtención de Credenciales

### Credenciales de Google (credenciales.json)

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Gmail:
   - En el menú lateral, ve a "APIs y servicios" > "Biblioteca"
   - Busca "Gmail API"
   - Haz clic en "Habilitar"

4. Configura la pantalla de consentimiento:
   - Ve a "APIs y servicios" > "Pantalla de consentimiento de OAuth"
   - Selecciona "Externo" y haz clic en "Crear"
   - Completa la información básica requerida
   - En los "Permisos", agrega los siguientes scopes:
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/gmail.send`
   - Agrega tu correo como usuario de prueba

5. Crea las credenciales:
   - Ve a "APIs y servicios" > "Credenciales"
   - Haz clic en "Crear credenciales" > "ID de cliente de OAuth"
   - Selecciona "Aplicación de escritorio"
   - Dale un nombre a tu aplicación
   - Haz clic en "Crear"
   - Descarga el archivo JSON
   - Renómbralo a `credenciales.json` y colócalo en la raíz del proyecto

### API Key de OpenAI

1. Ve a [OpenAI Platform](https://platform.openai.com/)
2. Inicia sesión o crea una cuenta
3. Ve a la sección "API Keys" en el menú
4. Haz clic en "Create new secret key"
5. Dale un nombre descriptivo a tu key
6. Copia la key generada (solo se mostrará una vez)
7. Agrégala a tu archivo `.env` como:
   ```
   OPENAI_API_KEY=tu_api_key_aquí
   ```

**Nota de Seguridad**: Nunca compartas o subas a repositorios públicos tus archivos de credenciales (`credenciales.json`, `.env` con la API key). Asegúrate de que estén incluidos en tu `.gitignore`.

## Uso

1. Ejecuta el script principal:
```bash
python gmail_responder.py
```

2. En el primer inicio, se utilizarán las credenciales proporcionadas en `credenciales.json` para autenticar la aplicación
3. Se generará automáticamente un `token.json` para mantener la sesión
4. El sistema comenzará a monitorear y responder automáticamente los correos nuevos

## Soporte

Si encuentras algún problema o tienes alguna pregunta, por favor:
1. Revisa la documentación proporcionada
2. Verifica que todos los archivos de configuración estén correctamente configurados
3. Asegúrate de tener los permisos necesarios en tu cuenta de Gmail

---
Última actualización: Febrero 2025
