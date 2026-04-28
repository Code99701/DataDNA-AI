"""
Embedding service using sentence-transformers for semantic similarity.

Uses a lazy-loaded singleton pattern to avoid reloading the model on every
request. The default model (all-MiniLM-L6-v2) produces 384-dim embeddings
and is fast enough for hackathon demos.
"""
import logging
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Singleton service for generating and comparing text embeddings.

    The sentence-transformer model is loaded on first use and cached
    for all subsequent calls within the same process.
    """

    _model = None

    @classmethod
    def get_model(cls):
        """Load the sentence-transformer model (lazy initialization)."""
        if cls._model is None:
            logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
            from sentence_transformers import SentenceTransformer
            cls._model = SentenceTransformer(EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully")
        return cls._model

    @classmethod
    def generate_embedding(cls, text: str) -> np.ndarray:
        """
        Generate a dense vector embedding for the given text.

        Args:
            text: Input text string.

        Returns:
            1-D numpy array of float32 values (384 dimensions for MiniLM).
        """
        model = cls.get_model()
        embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        return embedding.astype(np.float32)

    @classmethod
    def generate_embeddings_batch(cls, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts in a single batch call.

        More efficient than calling generate_embedding() in a loop.

        Args:
            texts: List of text strings.

        Returns:
            2-D numpy array of shape (len(texts), embedding_dim).
        """
        model = cls.get_model()
        embeddings = model.encode(
            texts, convert_to_numpy=True,
            show_progress_bar=False, batch_size=32
        )
        return embeddings.astype(np.float32)

    @classmethod
    def compute_similarity(cls, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            emb1: First embedding vector (1-D).
            emb2: Second embedding vector (1-D).

        Returns:
            Cosine similarity score between -1.0 and 1.0.
        """
        # Reshape to 2-D for sklearn
        sim = cosine_similarity(
            emb1.reshape(1, -1),
            emb2.reshape(1, -1)
        )
        return float(sim[0][0])

    @classmethod
    def compute_similarity_matrix(
        cls, query_embeddings: np.ndarray, stored_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute pairwise cosine similarity between two sets of embeddings.

        Args:
            query_embeddings: Shape (n, dim).
            stored_embeddings: Shape (m, dim).

        Returns:
            Similarity matrix of shape (n, m).
        """
        return cosine_similarity(query_embeddings, stored_embeddings)

    @staticmethod
    def serialize_embedding(emb: np.ndarray) -> bytes:
        """Serialize a numpy embedding to bytes for DB storage."""
        return emb.astype(np.float32).tobytes()

    @staticmethod
    def deserialize_embedding(data: bytes) -> np.ndarray:
        """Deserialize bytes from DB back to a numpy embedding."""
        return np.frombuffer(data, dtype=np.float32)
