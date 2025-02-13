from dotenv import load_dotenv 
load_dotenv() 

from flask import Flask, request, render_template, jsonify, send_from_directory
import lyrics
import llm_image

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    song_title = request.form.get("song_title", "").strip()
    error = None
    if not song_title or " - " not in song_title:
        error = "Formato incorrecto. Use 'Artista - Título'."
    else:
        lyric_text = lyrics.fetch_lyrics(song_title)
        if not lyric_text or "No se encontraron letras" in lyric_text:
            error = "No se encontraron letras para la canción ingresada."
    if error:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": error})
        return render_template("error.html", error=error)
    
    try:
        steps = int(request.form.get("steps", 50))
    except:
        steps = 50
    try:
        guidance = float(request.form.get("guidance", 8.0))
    except:
        guidance = 8.0
    try:
        gen_width = int(request.form.get("gen_width", 512))
        gen_height = int(request.form.get("gen_height", 512))
    except:
        gen_width, gen_height = 512, 512

    img_path = llm_image.generate_image_from_lyrics(lyric_text, steps, guidance, gen_width, gen_height)
    if img_path:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"img_path": img_path})
        return render_template("generate.html", img_path=img_path)
    else:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "No se pudo generar la imagen."})
        return render_template("error.html", error="No se pudo generar la imagen.")

@app.route('/output/<path:filename>')
def output_file(filename):
    return send_from_directory('output', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
