import warnings
from pathlib import Path
from sentence_transformers import SentenceTransformer
import torch.nn

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

HOME = Path.home()
CACHE_DIR = HOME / ".config/opencode" / "memoria-superior" / "embeddings"

def cargar_modelo():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = SentenceTransformer(MODEL_NAME, cache_folder=str(CACHE_DIR))
    model.eval()
    model = torch.ao.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )
    return model
