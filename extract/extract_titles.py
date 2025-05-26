import os
import re
from sqlalchemy import create_engine, text

def extract_title_from_article(text: str) -> str:
    text = text.strip().replace("\n", " ")

    p_start = text.find("(")
    if 0 <= p_start <= 20:
        p_end = text.find(")", p_start)
        if p_end != -1:
            for match in re.finditer(r',\s+(\w+)', text[p_end:]):
                following_word = match.group(1)
                if not following_word.isupper() and following_word.lower() != "or":
                    cutoff = p_end + match.start()
                    title = text[:cutoff].rstrip(",")
                    break
            else:
                title = text
        else:
            title = text
    else:
        for match in re.finditer(r',\s+(\w+)', text):
            following_word = match.group(1)
            if not following_word.isupper() and following_word.lower() != "or":
                title = text[:match.start()].rstrip(",")
                break
        else:
            title = text

    title = title.strip()
    return title[:97] + "..." if len(title) > 100 else title

# --- DB Setup ---
db_url = os.getenv("BRITANNICA_DB_URL")
if not db_url:
    print("Environment variable $BRITANNICA_DB_URL is not set.")
    exit(1)
if db_url.startswith("mysql://"):
    db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(db_url)

# --- Update Logic ---
def update_titles():
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id, content FROM articles_1911 WHERE title = ''")).fetchall()
        print(f"Processing {len(rows)} articles...")

        for row in rows:
            article_id = row.id
            content = row.content
            title = extract_title_from_article(content)

            conn.execute(
                text("UPDATE articles_1911 SET title = :title WHERE id = :id"),
                {"title": title, "id": article_id}
            )

        print("Done.")

# --- Run ---
if __name__ == "__main__":
    update_titles()

