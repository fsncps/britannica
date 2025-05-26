import sys
import re
import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# --- DB Setup ---
DB_URL = os.getenv("BRITANNICA_DB_URL")
if not DB_URL:
    print("Error: environment variable $BRITANNICA_DB_URL not set.")
    sys.exit(1)
if DB_URL.startswith("mysql://"):
    DB_URL = DB_URL.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles_1911"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

# --- Parsing Functions ---

def is_article_start(lines, index):
    if index == 0 or lines[index - 1].strip() != "":
        return False
    line = lines[index].strip()
    if len(line) <= 30:
        return False
    if not re.match(r'^[A-Z]{2}', line):
        return False
    if re.match(r'^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI|XVII|XVIII|XIX|XX)\.', line):
        return False
    if not re.search(r'[a-z]{2,}', line):
        return False
    if re.search(r'[^a-z],', line) or '(' in line:
        return True
    return False

def is_meaningful_article_line(line):
    line = line.strip()
    if not line:
        return False
    if re.match(r'^\d{1,4}\s', line):
        return False
    if re.match(r'^Fig\.', line):
        return False
    if re.match(r'^[IVXLCDM]{1,4}[\.\s]', line):
        return False
    if re.match(r'^[A-Z]{2,}\s*[=+\-*/]', line):
        return False
    if not re.search(r'\b[a-z]{2,}\b', line):
        return False
    return True

def extract_articles(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    articles = []
    current_article = ""
    in_article = False

    for i, line in enumerate(lines):
        if is_article_start(lines, i):
            if current_article.strip():
                articles.append(current_article.strip())
            current_article = lines[i].strip()
            in_article = True
        elif in_article:
            if is_meaningful_article_line(line):
                clean = line.strip()
                if current_article.endswith("-"):
                    current_article = current_article[:-1] + clean
                else:
                    current_article += " " + clean

    if current_article.strip():
        articles.append(current_article.strip())

    return articles

# --- Insertion ---

def insert_articles_to_db(articles):
    db = SessionLocal()
    try:
        for content in articles:
            article = Article(title="", content=content)
            db.add(article)
        db.commit()
        print(f"Inserted {len(articles)} articles into articles_1911.")
    except Exception as e:
        db.rollback()
        print("Error inserting into database:", e)
    finally:
        db.close()

# --- Entry Point ---

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python insert_articles.py input.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    parsed_articles = extract_articles(input_file)
    insert_articles_to_db(parsed_articles)

