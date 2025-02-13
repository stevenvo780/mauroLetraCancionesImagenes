import os
import lyrics
import llm_image

def main():
    song_title = input("Ingrese el título de la canción: ")
    lyric_text = lyrics.fetch_lyrics(song_title)
    print("Letra obtenida:")
    print(lyric_text)
    
    img_path = llm_image.generate_image_from_lyrics(lyric_text)
    if img_path:
        print("Imagen generada por modelo:", img_path)
    else:
        print("No se pudo generar la imagen con el modelo.")
    
if __name__ == "__main__":
    main()