import os
import queue
import threading
from flask import Flask, request, render_template, Response, stream_with_context
from dotenv import load_dotenv 
load_dotenv() 

import lyrics
import llm_image

app = Flask(__name__)

history_images = []

output_dir = os.path.join(os.path.dirname(__file__), 'output')
if os.path.exists(output_dir):
    for file in os.listdir(output_dir):
        if file.endswith(".png"):
            history_images.append(os.path.join("output", file))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", images=history_images)

@app.route("/generate", methods=["GET"])
def generate():
    # Se obtienen los parámetros vía query string
    song_title = request.args.get("song_title", "").strip()
    error = None
    if not song_title or " - " not in song_title:
        error = "Formato incorrecto. Use 'Artista - Título'."
    else:
        lyric_text = lyrics.fetch_lyrics(song_title)
        if not lyric_text or "No se encontró la letra" in lyric_text:
            error = "No se encontró la letra para la canción ingresada."
    if error:
        return Response(f"data: error:{error}\n\n", mimetype="text/event-stream")

    try:
        steps = int(request.args.get("steps", 50))
    except:
        steps = 50
    try:
        guidance = float(request.args.get("guidance", 8.0))
    except:
        guidance = 8.0
    try:
        gen_width = int(request.args.get("gen_width", 512))
        gen_height = int(request.args.get("gen_height", 512))
    except:
        gen_width, gen_height = 512, 512

    progress_queue = queue.Queue()
    result = {"img_path": None, "error": None}

    def callback(step, timestep, latents):
        progress = int((step / steps) * 100)
        progress_queue.put(("progress", progress))

    def background_task():
        img_path = llm_image.generate_image_from_lyrics(lyric_text, steps, guidance, gen_width, gen_height, callback=callback)
        if img_path:
            result["img_path"] = img_path
            history_images.append(img_path)
        else:
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = history_images[start:end]
    total_pages = (len(history_images) + per_page - 1) // per_page
    return render_template("gallery.html", images=paginated_images, page=page, total_pages=total_pages)

@app.route('/output/<path:filename>')
def output_file(filename):
    return send_from_directory('output', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
