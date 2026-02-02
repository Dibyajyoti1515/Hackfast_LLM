from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter

# -------------------------
# Router
# -------------------------
router = APIRouter()

# -------------------------
# Load Embedding Model
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------
# Request Models
# -------------------------
class Product(BaseModel):
    id: int
    name: str
    about: List[str] = []
    reviews: List[str] = []

class RankRequest(BaseModel):
    user_profile: str
    products: List[Product]

# -------------------------
# Ranking Logic
# -------------------------
def rank_products(user_text: str, products: list) -> list[dict]:
    # ✅ Encode user profile
    user_embedding = model.encode(user_text)

    # ✅ Prepare product texts safely
    product_texts = []
    for product in products:
        name = str(product.get("name", "")).strip()
        about = " ".join(map(str, product.get("about", [])))
        reviews = " ".join(map(str, product.get("reviews", [])))

        text = " ".join([name, about, reviews]).strip()
        product_texts.append(text)

    # ✅ Encode products
    product_embeddings = model.encode(product_texts)

    # ✅ Compute cosine similarity
    similarities = cosine_similarity(
        [user_embedding],
        product_embeddings
    )[0]

    # ✅ Return only id + score
    scored_products = []
    for idx, product in enumerate(products):
        scored_products.append({
            "id": int(product["id"]),
            "score": round(float(similarities[idx]), 4)   # rounded for clean payload
        })

    # ✅ Sort by similarity score (descending)
    scored_products.sort(key=lambda x: x["score"], reverse=True)

    return scored_products

# -------------------------
# API Endpoint
# -------------------------
@router.post("/semantic/rank")
def rank_api(data: RankRequest):
    ranked_products = rank_products(
        data.user_profile,
        [p.dict() for p in data.products]
    )

    print("✅ Ranked Output:", ranked_products)
    return ranked_products
