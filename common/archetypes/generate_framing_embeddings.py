import os
import json
import mysql.connector
from urllib.parse import urlparse
from sentence_transformers import SentenceTransformer

# Load BERT model (can be swapped for others like 'all-mpnet-base-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load DB credentials from environment
db_url = os.environ.get("BRITANNICA_DB_URL")
if not db_url:
    raise ValueError("BRITANNICA_DB_URL not set")

parsed = urlparse(db_url)
DB_CONFIG = {
    'user': parsed.username,
    'password': parsed.password,
    'host': parsed.hostname,
    'port': parsed.port or 3306,
    'database': parsed.path.lstrip('/')
}

# Connect
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

# Select framing entries with content and no embedding
cursor.execute("SELECT id, content FROM framing WHERE content IS NOT NULL AND embedding IS NULL")

rows = cursor.fetchall()
print(f"🔍 Found {len(rows)} entries to embed.")

for row in rows:
    framing_id = row["id"]
    text = row["content"]

    try:
        embedding = model.encode(text, normalize_embeddings=True)
        embedding_json = json.dumps(embedding.tolist())

        cursor.execute(
            "UPDATE framing SET embedding = %s WHERE id = %s",
            (embedding_json, framing_id)
        )
        print(f"✅ Embedded ID {framing_id}")
    except Exception as e:
        print(f"❌ Error embedding ID {framing_id}: {e}")

conn.commit()
cursor.close()
conn.close()
print("🎯 Embeddings generated and saved.")

