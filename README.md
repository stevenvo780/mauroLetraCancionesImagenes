# Generador de Imágenes a Partir de Letra de Canciones

Este proyecto permite generar imágenes artísticas basadas en la letra de una canción. Utiliza modelos de generación de imágenes (como Stable Diffusion) junto con servicios de modelos de lenguaje para transformar la letra en un prompt creativo que luego se utiliza para generar la imagen. Además, se guarda un historial de todas las imágenes generadas en la sesión.

## Características

- **Generación de Prompts Creativos**: Utiliza modelos de lenguaje para crear descripciones detalladas a partir de la letra de una canción.  
- **Generación de Imágenes con AI**: Emplea Stable Diffusion para generar imágenes de alta calidad basadas en el prompt.  
- **Historial de Imágenes**: Cada imagen generada se guarda con un identificador único, evitando sobreescrituras, y se muestra en una galería en la vista principal.  
- **Interfaz Web Amigable**: Implementada con Flask y estilizada con Bootstrap.  
- **Control de Progreso y Cancelación**: Muestra un overlay con barra de progreso durante la generación de la imagen que puede ser cancelada si es necesario.

## Requisitos

- Python 3.x
- Las dependencias listadas en [requirements.txt](requirements.txt):

## Instalación

1. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
   ```
2. Ajustar parámetros en `config.py` (tamaño, color de fondo, fuente, etc.).
3. Colocar la letra en `lyrics.txt`.
4. Ejecutar la aplicación:  
   ```bash
   python app.py
   ```
5. El resultado se guardará según el valor de `OUTPUT_FILENAME`.
