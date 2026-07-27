"""Multilingual embeddings. Record exact model/version and verify vector dimension."""
import numpy as np
def load_embedding_model():
    # Load once, not inside a row loop.
    raise NotImplementedError
def encode_event_texts(texts:list[str])->np.ndarray:
    # TODO: batch encode, normalize for cosine, expected shape n_events x embedding_dimension.
    raise NotImplementedError
