import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Offer, Post, Review

app = FastAPI(title="Travel Agency API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Travel Agency Backend is running"}

# Utility to convert Mongo documents

def serialize_doc(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    # Convert datetime to isoformat if present
    for k, v in list(doc.items()):
        try:
            import datetime
            if isinstance(v, (datetime.datetime, datetime.date)):
                doc[k] = v.isoformat()
        except Exception:
            pass
    return doc

# Offers Endpoints
@app.post("/api/offers", response_model=dict)
async def create_offer(offer: Offer):
    try:
        new_id = create_document("offer", offer)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/offers", response_model=List[dict])
async def list_offers(limit: Optional[int] = 50, featured: Optional[bool] = None):
    try:
        q = {}
        if featured is not None:
            q["is_featured"] = featured
        docs = get_documents("offer", q, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Posts Endpoints
@app.post("/api/posts", response_model=dict)
async def create_post(post: Post):
    try:
        new_id = create_document("post", post)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts", response_model=List[dict])
async def list_posts(limit: Optional[int] = 50):
    try:
        docs = get_documents("post", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reviews Endpoints
@app.post("/api/reviews", response_model=dict)
async def create_review(review: Review):
    try:
        new_id = create_document("review", review)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews", response_model=List[dict])
async def list_reviews(limit: Optional[int] = 50):
    try:
        docs = get_documents("review", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System/Test
@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
