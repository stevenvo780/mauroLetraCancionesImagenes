from flask import Flask, request, render_template, redirect, url_for
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
        return render_template("error.html", error=error)
    
    img_path = llm_image.generate_image_from_lyrics(lyric_text)
    if img_path:
        return render_template("generate.html", img_path=img_path)
    else:
        return render_template("error.html", error="No se pudo generar la imagen.")

if __name__ == "__main__":
    app.run(debug=True)
