# Generador de Imágenes a Partir de Letra de Canciones

Este proyecto permite generar imágenes artísticas basadas en la letra de una canción. Utiliza modelos de lenguaje para transformar la letra en un prompt creativo y emplea Stable Diffusion para generar la imagen artísticamente.

## Características

- **Generación de Prompts Creativos**: Utiliza modelos de lenguaje (Google API y modelo local como respaldo) para crear descripciones detalladas a partir de la letra de una canción.
- **Generación de Imágenes con AI**: Emplea Stable Diffusion para crear imágenes de alta calidad basadas en el prompt generado.
- **Progreso en Tiempo Real**: Muestra un overlay con una barra de progreso y mensajes informativos durante la generación de la imagen.
- **Historial y Galería de Imágenes**: Guarda todas las imágenes generadas en la carpeta "output" y las muestra en una galería con paginación.
- **Interfaz Web Moderna**: Implementada con Flask y estilizada con Bootstrap, adaptada para dispositivos móviles.
- **Personalización de Parámetros**: Permite ajustar el número de pasos de inferencia, guidance scale, y las dimensiones (ancho y alto) de la imagen.

## Requisitos

- Python 3.x
- Dependencias listadas en [requirements.txt](requirements.txt)

## Instalación

1. Instalar las dependencias:  
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar las variables de entorno, incluyendo GOOGLE_API_KEY y USE_GPU (opcional).
3. Ejecutar la aplicación:  
   ```bash
   python -m src.web_app
   ```
4. Acceder a [http://localhost:5000](http://localhost:5000) en el navegador.

## Estructura del Proyecto

- **/src**: Código fuente de la aplicación Flask y módulos para la generación de letras e imágenes.
- **/templates**: Plantillas HTML (index, generate, gallery, error) para la interfaz web.
- **/static**: Archivos estáticos como imágenes y hojas de estilo.
- **/output**: Carpeta donde se guardan las imágenes generadas.

## Uso

1. En la página principal ingrese el nombre de canción en el formato "Artista - Título".
2. Ajuste los parámetros de generación según sea necesario:
   - Pasos de inferencia (steps)
   - Guidance scale
   - Ancho y Alto de la imagen
3. Genere la imagen, observe la barra de progreso en tiempo real y espere a que finalice el proceso.
4. Acceda a la galería para revisar el historial de imágenes generadas.

## Notas Adicionales

- Los prompts se generan combinando la letra de la canción con un procesamiento creativo mediante Google API y, en su defecto, un modelo local.
- La aplicación utiliza Server-Sent Events para actualizar en tiempo real el progreso de la generación de la imagen.
- Se han integrado mejoras en la interfaz y funcionalidad, incluyendo soporte para paginación en la galería.
