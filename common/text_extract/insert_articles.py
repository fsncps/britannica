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
    __tablename__ = "articles_1911_2"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    short_title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    embedding = Column(Text, nullable=True)
    volume = Column(Integer, nullable=True)
    page = Column(Integer, nullable=True)

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
    line = line.rstrip("\n")
    if not line.strip():
        return False
    if re.match(r'^\d{1,4}\s*$', line):
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

def find_page_number(lines, start_index):
    for i in range(start_index - 1, 4, -1):
        if (
            lines[i].strip().isdigit() and
            lines[i-1].strip() == "" and
            lines[i-2].strip() == "" and
            lines[i+1].strip() == "" and
            lines[i+2].strip() == ""
        ):
            return int(lines[i].strip())
    return None

def extract_volume_number(filename):
    match = re.search(r'VOL(\d{2})', filename.upper())
    return int(match.group(1)) if match else None

def extract_articles(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    articles = []
    current_lines = []
    in_article = False
    volume = extract_volume_number(os.path.basename(input_path))
    page = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        if is_article_start(lines, i):
            if current_lines:
                joined = "\n".join(current_lines).strip()
                joined = re.sub(r"\n{3,}", "\n\n", joined)  # collapse triple+ newlines
                articles.append({
                    "title": "",
                    "content": joined,
                    "volume": volume,
                    "page": page
                })
            current_lines = [stripped]
            page = find_page_number(lines, i)
            in_article = True
            continue

        if not in_article:
            continue

        if is_meaningful_article_line(line) or stripped == "":
            clean = line.rstrip("\n")
            if current_lines and current_lines[-1].endswith("-") and clean:
                current_lines[-1] = current_lines[-1][:-1] + clean.lstrip()
            else:
                current_lines.append(clean)

    if current_lines:
        joined = "\n".join(current_lines).strip()
        joined = re.sub(r"\n{3,}", "\n\n", joined)
        articles.append({
            "title": "",
            "content": joined,
            "volume": volume,
            "page": page
        })

    return articles




# --- Insertion ---

def insert_articles_to_db(articles):
    db = SessionLocal()
    try:
        for item in articles:
            article = Article(
                title=item["title"],
                short_title=None,
                content=item["content"],
                embedding=None,
                volume=item["volume"],
                page=item["page"]
            )
            db.add(article)
        db.commit()
        print(f"Inserted {len(articles)} articles into articles_1911_2.")
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

