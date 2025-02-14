import os
import logging
import google.generativeai as genai
from typing import Optional, Dict, Any

class GoogleModel():
    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no encontrada en variables de entorno")
        self.api_key = api_key
        default_config = {'model_name': "gemini-2.0-flash-exp"}
        merged_config = {**default_config, **(config or {})}
        self.config = merged_config
        genai.configure(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)
    def get_response(self, query: str) -> str:
        try:
            model = genai.GenerativeModel(self.config['model_name'])
            generation_config = {'temperature': 0.7, 'top_p': 0.9, 'top_k': 40, 'max_output_tokens': 512, 'candidate_count': 1}
            prompt = (
                "Dada la siguiente letra compleja y rica en detalles, genera un prompt artístico y descriptivo, de al menos 200 palabras, "
                "para crear una imagen digital de altísima calidad. No repitas la letra textualmente; interpreta la atmósfera, los colores, "
                "la composición y las emociones evocadas. Letra: " + query
            )
            response = model.generate_content(prompt, generation_config=generation_config)
            if response.text:
                return response.text.strip()
            return "No se pudo obtener respuesta del modelo."
        except Exception as e:
            self.logger.error(f"Error en Google API: {str(e)}")
            return "No se pudo obtener respuesta del modelo."