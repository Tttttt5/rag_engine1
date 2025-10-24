# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from db import SessionLocal, Ingestion, Status
import uuid, datetime, requests, threading
from embedding import add_to_corpus, get_corpus_embeddings

app = FastAPI(title="Simple RAG Engine (No Redis, No Qdrant)")

# ----------- Models for Requests -----------
class IngestRequest(BaseModel):
    url: HttpUrl

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

# ----------- Background Process -----------
def process_url(ingestion_id: str, url: str):
    session = SessionLocal()
    try:
        # Mark status = PROCESSING
        job = session.get(Ingestion, ingestion_id)
        job.status = Status.PROCESSING
        session.commit()

        # Fetch content
        response = requests.get(url, timeout=10)
        text = response.text[:5000]  # limit for demo

        # Create simple embeddings (TF-IDF or custom)
        add_to_corpus([text])
        embeddings = get_corpus_embeddings()

        print(f"[Worker] Processed {url}, generated {len(embeddings)} embeddings")

        # Mark completed
        job.status = Status.COMPLETED
        job.completed_at = datetime.datetime.utcnow()
        session.commit()
    except Exception as e:
        job.status = Status.FAILED
        job.error = str(e)
        session.commit()
        print(f"[Worker] Error processing {url}: {e}")
    finally:
        session.close()

# ----------- Routes -----------
@app.post("/ingest-url", status_code=202)
async def ingest_url(req: IngestRequest):
    """Receive a URL and process it asynchronously."""
    ingestion_id = str(uuid.uuid4())
    session = SessionLocal()
    entry = Ingestion(id=ingestion_id, url=req.url, status=Status.PENDING)
    session.add(entry)
    session.commit()
    session.close()

    # Run in background thread instead of Redis
    threading.Thread(target=process_url, args=(ingestion_id, req.url), daemon=True).start()
    return {"ingestion_id": ingestion_id, "status": "PENDING"}

@app.get("/ingestion/{ingestion_id}")
async def get_status(ingestion_id: str):
    """Check ingestion status."""
    session = SessionLocal()
    job = session.get(Ingestion, ingestion_id)
    session.close()
    if not job:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": job.id,
        "url": job.url,
        "status": job.status,
        "submitted_at": job.submitted_at,
        "completed_at": job.completed_at,
        "error": job.error
    }

@app.post("/query")
async def query(req: QueryRequest):
    """Search within stored embeddings (simple demo)."""
    embeddings = get_corpus_embeddings()
    if not embeddings:
        raise HTTPException(status_code=400, detail="No data ingested yet.")
    return {"answer": f"Query received: {req.query}", "total_docs": len(embeddings)}

@app.get("/")
def home():
    return {"message": "RAG Engine running (no Redis, no Qdrant)!"}
