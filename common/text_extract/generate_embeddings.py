import os
import json
from sqlalchemy import create_engine, text
from sentence_transformers import SentenceTransformer

# Load BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# DB setup
db_url = os.getenv("BRITANNICA_DB_URL")
if not db_url:
    raise RuntimeError("Missing $BRITANNICA_DB_URL")
if db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(db_url)

# Embedding pipeline
def embed_articles():
    with engine.begin() as conn:
        rows = conn.execute(
            text("SELECT id, content FROM articles_1911 WHERE embedding IS NULL")
        ).fetchall()

        print(f"Embedding {len(rows)} articles...")

        for idx, row in enumerate(rows, start=1):
            article_id = row.id
            content = row.content.strip().replace("\n", " ")

            embedding = model.encode(content, normalize_embeddings=True)
            embedding_json = json.dumps(embedding.tolist())

            conn.execute(
                text("UPDATE articles_1911 SET embedding = :embedding WHERE id = :id"),
                {"embedding": embedding_json, "id": article_id}
            )

            if idx % 100 == 0:
                print(f"Processed {idx} / {len(rows)} articles...")

        print("Done.")


if __name__ == "__main__":
    embed_articles()

