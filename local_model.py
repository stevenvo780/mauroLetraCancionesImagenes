import logging
import warnings
import torch
from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
try:
    from transformers import BitsAndBytesConfig
    BNB_AVAILABLE = True
except ImportError:
    BNB_AVAILABLE = False

warnings.filterwarnings('ignore', message='Input type into Linear4bit.*')

class LocalModel:
    DEFAULT_MODEL_NAME = "meta-llama/Llama-3.2-3B"
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        default_config = {'model_name': self.DEFAULT_MODEL_NAME}
        self.config = {**default_config, **(config or {})}
        self.model_name = self.config.get("model_name")
        logging.info(f"Cargando modelo: {self.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, padding_side="left", add_eos_token=True)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        device_map = "auto" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        if device_map == "cpu":
            logging.warning("GPU no disponible, usando CPU y sin cuantización.")
            quantization_config = None
        else:
            if BNB_AVAILABLE:
                try:
                    quantization_config = BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_quant_type="nf4",
                        bnb_4bit_use_double_quant=True,
                        llm_int8_enable_fp32_cpu_offload=True
                    )
                except Exception as e:
                    logging.error(f"Error configurando quantization_config: {e}")
                    quantization_config = None
            else:
                logging.warning("BitsAndBytes no disponible; se usará el modelo sin cuantización.")
                quantization_config = None
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map=device_map,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True
            )
            self.model.eval()
            self.model.config.pad_token_id = self.tokenizer.pad_token_id
        except Exception as e:
            logging.error(f"Error al cargar modelo: {e}")
            raise RuntimeError(f"No se pudo inicializar el modelo: {e}")
    def get_response(self, query: str) -> str:
        try:
            encoded = self.tokenizer(query, return_tensors="pt", truncation=True, max_length=256, padding=True, add_special_tokens=True)
            input_ids = encoded["input_ids"].to(self.model.device)
            attention_mask = encoded["attention_mask"].to(self.model.device)
            with torch.inference_mode():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=150,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    use_cache=True
                )
            response = self.tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True, clean_up_tokenization_spaces=True).strip()
            # Si la respuesta es muy corta, se solicita explícitamente un prompt más detallado.
            if len(response.split()) < 10:
                response = "Genera un prompt artístico y descriptivo, de al menos 50 palabras, basado en la siguiente letra: " + query
            for prefix in ["Respuesta:", "Jarvis:", "Usuario:", "Asistente:"]:
                if response.startswith(prefix):
                    response = response.replace(prefix, "", 1).strip()
            return response if response and len(response.split()) >= 10 else "¿En qué puedo ayudarte?"
        except Exception as e:
            logging.error(f"Error en el modelo local: {e}")
            return "Lo siento, hubo un error en el procesamiento. ¿Puedo ayudarte en algo más?"
    def __repr__(self):
        return f"<LocalModel: {self.model_name}>"
