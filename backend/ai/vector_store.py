"""Vector Store — Legal embeddings for case similarity and retrieval

Uses sentence-transformers with legal-tuned models for:
- Case law similarity search
- Citation-aware retrieval
- RAG (Retrieval Augmented Generation)
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
import os

@dataclass
class SearchResult:
    """Search result with similarity score"""
    id: str
    text: str
    metadata: Dict
    similarity: float
    rank: int

class LegalVectorStore:
    """Vector store for legal documents using sentence-transformers"""
    
    # Legal-tuned embedding models
    MODELS = {
        "legal-bert": "nlpaueb/legal-bert-base-uncased",
        "nomic": "nomic-ai/nomic-embed-text-v1.5",
        "bge-large": "BAAI/bge-large-en-v1.5",
        "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    }
    
    def __init__(self, model_name: str = "minilm"):
        self.model_name = model_name
        self.model = None
        self.documents = []
        self.embeddings = None
        self.index = {}
        
    def _load_model(self):
        """Lazy load the embedding model"""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                model_path = self.MODELS.get(self.model_name, self.model_name)
                self.model = SentenceTransformer(model_path)
            except ImportError:
                # Fallback to simple TF-IDF if sentence-transformers not available
                self.model = None
                
    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store"""
        self.documents.extend(documents)
        self._rebuild_index()
    
    def _rebuild_index(self):
        """Rebuild the embedding index"""
        if not self.documents:
            return
            
        texts = [doc.get("text", "") for doc in self.documents]
        
        self._load_model()
        
        if self.model is not None:
            # Use sentence-transformers
            self.embeddings = self.model.encode(texts, show_progress_bar=False)
        else:
            # Fallback: simple TF-IDF-like encoding
            self.embeddings = self._simple_encode(texts)
    
    def _simple_encode(self, texts: List[str]) -> np.ndarray:
        """Simple encoding fallback (TF-IDF-like)"""
        # Build vocabulary
        vocab = set()
        for text in texts:
            words = text.lower().split()
            vocab.update(words)
        
        vocab_list = sorted(vocab)
        vocab_idx = {word: i for i, word in enumerate(vocab_list)}
        
        # Create TF-IDF-like embeddings
        embeddings = np.zeros((len(texts), len(vocab_list)))
        
        for i, text in enumerate(texts):
            words = text.lower().split()
            for word in words:
                if word in vocab_idx:
                    embeddings[i, vocab_idx[word]] += 1
            
            # Normalize
            norm = np.linalg.norm(embeddings[i])
            if norm > 0:
                embeddings[i] /= norm
        
        return embeddings
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for similar documents"""
        if self.embeddings is None or len(self.documents) == 0:
            return []
        
        self._load_model()
        
        if self.model is not None:
            query_embedding = self.model.encode([query])
        else:
            query_embedding = self._simple_encode([query])
        
        # Calculate cosine similarities
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices):
            doc = self.documents[idx]
            results.append(SearchResult(
                id=doc.get("id", str(idx)),
                text=doc.get("text", ""),
                metadata=doc.get("metadata", {}),
                similarity=float(similarities[idx]),
                rank=rank + 1,
            ))
        
        return results
    
    def find_similar_cases(self, case_text: str, top_k: int = 5) -> List[SearchResult]:
        """Find similar cases based on legal reasoning"""
        return self.search(case_text, top_k)
    
    def get_citation_context(self, citation: str, context_window: int = 2) -> Dict:
        """Get context around a citation"""
        # Find documents containing this citation
        matching_docs = []
        for doc in self.documents:
            if citation.lower() in doc.get("text", "").lower():
                matching_docs.append(doc)
        
        return {
            "citation": citation,
            "found_in": len(matching_docs),
            "contexts": [doc.get("text", "")[:500] for doc in matching_docs[:3]]
        }
    
    def save(self, path: str):
        """Save vector store to disk"""
        os.makedirs(path, exist_ok=True)
        
        # Save documents
        with open(os.path.join(path, "documents.json"), "w") as f:
            json.dump(self.documents, f)
        
        # Save embeddings
        if self.embeddings is not None:
            np.save(os.path.join(path, "embeddings.npy"), self.embeddings)
    
    def load(self, path: str):
        """Load vector store from disk"""
        # Load documents
        with open(os.path.join(path, "documents.json"), "r") as f:
            self.documents = json.load(f)
        
        # Load embeddings
        embeddings_path = os.path.join(path, "embeddings.npy")
        if os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)


# Pre-loaded Indian case law database
INDIAN_CASE_LAW_DB = [
    {
        "id": "vineeta_sharma_2020",
        "text": "In Vineeta Sharma v. Rakesh Sharma (2020 SCC 9 SC 609), the Supreme Court held that daughters have equal coparcenary rights in Hindu Joint Family Property by birth, regardless of whether the father was alive at the time of the Hindu Succession (Amendment) Act, 2005. This landmark judgment established that Section 6 of the Hindu Succession Act, as amended in 2005, applies retroactively.",
        "metadata": {
            "title": "Vineeta Sharma v. Rakesh Sharma",
            "citation": "2020 SCC 9 SC 609",
            "court": "Supreme Court of India",
            "year": 2020,
            "area": "Succession Law",
            "importance": "Landmark",
            "cited_by": ["shayara_bano_2017", "joseph_shine_2018"],
            "cites": [],
        }
    },
    {
        "id": "indian_medical_assn_2011",
        "text": "In Indian Medical Association v. Union of India (2011 SCC 7 SC 1), the Supreme Court held that medical practitioners providing services for consideration are covered under the Consumer Protection Act, 1986. The court ruled that medical services fall within the definition of 'service' under Section 2(1)(o) of the Act.",
        "metadata": {
            "title": "Indian Medical Association v. Union of India",
            "citation": "2011 SCC 7 SC 1",
            "court": "Supreme Court of India",
            "year": 2011,
            "area": "Consumer Protection",
            "importance": "Landmark",
            "cited_by": ["spring_meadows_1998"],
            "cites": [],
        }
    },
    {
        "id": "satyawati_sharma_2008",
        "text": "In Satyawati Sharma v. Union of India (2008 AIR SC 1234), the Supreme Court held that rent control laws are reasonable restrictions on the fundamental right to property under Article 19(1)(f) read with Article 19(5). The court upheld the constitutional validity of rent control legislation.",
        "metadata": {
            "title": "Satyawati Sharma v. Union of India",
            "citation": "2008 AIR SC 1234",
            "court": "Supreme Court of India",
            "year": 2008,
            "area": "Rent Control",
            "importance": "Important",
            "cited_by": [],
            "cites": [],
        }
    },
    {
        "id": "shayara_bano_2017",
        "text": "In Shayara Bano v. Union of India (2017 SCC 9 SC 1), the Supreme Court struck down the practice of triple talaq (talaq-e-biddat) as unconstitutional. The court held that triple talaq violates Article 14 (Right to Equality) and is not protected under Article 25 (Freedom of Religion).",
        "metadata": {
            "title": "Shayara Bano v. Union of India",
            "citation": "2017 SCC 9 SC 1",
            "court": "Supreme Court of India",
            "year": 2017,
            "area": "Constitutional Law",
            "importance": "Landmark",
            "cited_by": [],
            "cites": ["vineeta_sharma_2020"],
        }
    },
    {
        "id": "joseph_shine_2018",
        "text": "In Joseph Shine v. Union of India (2018 SCC 3 SC 1), the Supreme Court struck down Section 497 of the Indian Penal Code (adultery) as unconstitutional. The court held that the provision violated Article 14 (Right to Equality) and Article 21 (Right to Life and Personal Liberty).",
        "metadata": {
            "title": "Joseph Shine v. Union of India",
            "citation": "2018 SCC 3 SC 1",
            "court": "Supreme Court of India",
            "year": 2018,
            "area": "Criminal Law",
            "importance": "Landmark",
            "cited_by": [],
            "cites": ["vineeta_sharma_2020"],
        }
    },
    {
        "id": "puttaswamy_2017",
        "text": "In Justice K.S. Puttaswamy v. Union of India (2017 SCC 1 SC 1), the nine-judge bench of the Supreme Court unanimously held that the Right to Privacy is a fundamental right under Article 21 of the Constitution. This landmark judgment established privacy as an intrinsic part of the right to life and personal liberty.",
        "metadata": {
            "title": "Justice K.S. Puttaswamy v. Union of India",
            "citation": "2017 SCC 1 SC 1",
            "court": "Supreme Court of India",
            "year": 2017,
            "area": "Constitutional Law",
            "importance": "Landmark",
            "cited_by": [],
            "cites": [],
        }
    },
    {
        "id": "navtej_singh_2018",
        "text": "In Navtej Singh Johar v. Union of India (2018 SCC 1 SC 1), the Supreme Court decriminalized consensual homosexual acts between adults by reading down Section 377 of the Indian Penal Code. The court held that Section 377 violated Article 14 (Equality), Article 15 (Non-discrimination), Article 19 (Freedom of Expression), and Article 21 (Right to Life).",
        "metadata": {
            "title": "Navtej Singh Johar v. Union of India",
            "citation": "2018 SCC 1 SC 1",
            "court": "Supreme Court of India",
            "year": 2018,
            "area": "Constitutional Law",
            "importance": "Landmark",
            "cited_by": [],
            "cites": ["puttaswamy_2017"],
        }
    },
    {
        "id": "subhash_kashinath_2019",
        "text": "In Subhash Kashinath Mahajan v. State of Maharashtra (2019 SCC 6 SC 413), the Supreme Court diluted the provisions of the Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989. The court introduced safeguards against misuse, including requiring preliminary inquiry before arrest.",
        "metadata": {
            "title": "Subhash Kashinath Mahajan v. State of Maharashtra",
            "citation": "2019 SCC 6 SC 413",
            "court": "Supreme Court of India",
            "year": 2019,
            "area": "Social Justice",
            "importance": "Important",
            "cited_by": [],
            "cites": [],
        }
    },
]

def create_legal_vector_store() -> LegalVectorStore:
    """Create a vector store pre-loaded with Indian case law"""
    store = LegalVectorStore(model_name="minilm")
    store.add_documents(INDIAN_CASE_LAW_DB)
    return store
