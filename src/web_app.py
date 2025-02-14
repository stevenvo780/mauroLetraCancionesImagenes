import os
import queue
import threading
import uuid
import concurrent.futures
from flask import Flask, request, render_template, Response, stream_with_context, send_from_directory
from dotenv import load_dotenv 
load_dotenv() 

from . import lyrics
from . import llm_image

base_dir = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__,
            template_folder=os.path.join(base_dir, "templates"),
            static_folder=os.path.join(base_dir, "static"))

output_dir = os.path.join(base_dir, 'output')
history_images = []
history_images_lock = threading.Lock()

if os.path.exists(output_dir):
    for file in os.listdir(output_dir):
        if file.endswith(".png"):
            history_images.append(os.path.join("output", file))

executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())
jobs = {}  # Diccionario global para rastrear tareas

@app.route("/", methods=["GET"])
def index():
    page = request.args.get('page', 1, type=int)
    output_dir = os.path.join(base_dir, 'output')
    images = []
    if os.path.exists(output_dir):
        images = [os.path.join("output", f) for f in os.listdir(output_dir) if f.endswith(".png")]
        images.sort(key=lambda img: os.path.getmtime(os.path.join(base_dir, img)), reverse=True)
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = images[start:end]
    total_pages = (len(images) + per_page - 1) // per_page
    return render_template("index.html", images=paginated_images, page=page, total_pages=total_pages)

@app.route("/generate", methods=["GET"])
def generate():
    job_id = request.args.get("job_id")
    if job_id and job_id in jobs:
        job = jobs[job_id]
        future = job["future"]
        progress_queue = job["queue"]
    else:
        job_id = uuid.uuid4().hex
        progress_queue = queue.Queue()
    
        song_title = request.args.get("song_title", "").strip()
        error = None
        if not song_title or " - " not in song_title:
            error = "Formato incorrecto. Use 'Artista - Título'."
        else:
            progress_queue.put(("info", "Extrayendo la letra y creando prompt..."))
            lyric_text = lyrics.fetch_lyrics(song_title)
            if not lyric_text or "No se encontró la letra" in lyric_text:
                error = "No se encontró la letra para la canción ingresada."
        if error:
            return Response(f"data: error:{error}\n\n", mimetype="text/event-stream")
    
        try:
            steps = int(request.args.get("steps", 20))
        except:
            steps = 20
        try:
            guidance = float(request.args.get("guidance", 8.0))
        except:
            guidance = 8.0
        try:
            gen_width = int(request.args.get("gen_width", 512))
            gen_height = int(request.args.get("gen_height", 512))
        except:
            gen_width, gen_height = 512, 512
    
        result = {"img_path": None, "error": None}
    
        def callback(step, timestep, latents):
            progress = int((step / steps) * 100)
            progress_queue.put(("progress", progress))
    
        def background_task():
            progress_queue.put(("info", "Generando prompt..."))
            creative_prompt = lyrics.generate_creative_prompt(lyric_text)
            progress_queue.put(("info", "Generando imagen..."))
            img_path = llm_image.generate_image_from_lyrics(creative_prompt, steps, guidance, gen_width, gen_height, callback=callback)
            if img_path:
                img_path = img_path.replace(base_dir, '').lstrip('/')
                result["img_path"] = img_path
                with history_images_lock:
                    history_images.insert(0, img_path)
            else:
                result["error"] = "No se pudo generar la imagen."
            progress_queue.put(("done", result))
    
        future = executor.submit(background_task)
        jobs[job_id] = {"future": future, "queue": progress_queue}
    
    @stream_with_context
    def event_stream():
        yield f"data: job:{job_id}\n\n"
        while not future.done() or not progress_queue.empty():
            try:
                event, data = progress_queue.get(timeout=0.5)
                if event == "progress":
                    yield f"data: progress:{data}\n\n"
                elif event == "info":
                    yield f"data: info:{data}\n\n"
                elif event == "done":
                    if data["error"]:
                        yield f"data: error:{data['error']}\n\n"
                    else:
                        yield f"data: done:{data['img_path']}\n\n"
                    # Finalizado: limpiar el job
                    jobs.pop(job_id, None)
            except queue.Empty:
                continue
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/gallery', methods=["GET"])
def gallery():
    output_dir = os.path.join(base_dir, 'output')
    images = []
    if os.path.exists(output_dir):
        images = [os.path.join("output", f) for f in os.listdir(output_dir) if f.endswith(".png")]
        images.sort(key=lambda img: os.path.getmtime(os.path.join(base_dir, img)), reverse=True)
    
    page = request.args.get('page', 1, type=int)
    per_page = 6
    start = (page - 1) * per_page
    end = start + per_page
    paginated_images = images[start:end]
    total_pages = (len(images) + per_page - 1) // per_page
    return render_template("gallery.html", images=paginated_images, page=page, total_pages=total_pages)

@app.route('/output/<path:filename>')
def output_file(filename):
    output_dir = os.path.join(base_dir, 'output')
    return send_from_directory(output_dir, filename)
