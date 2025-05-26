import os
import re
import mysql.connector
from urllib.parse import urlparse
from pathlib import Path

# Read DB URL from environment
db_url = os.environ.get("BRITANNICA_DB_URL")
if not db_url:
    raise ValueError("BRITANNICA_DB_URL not set in environment.")

# Parse the URL
parsed = urlparse(db_url)
DB_CONFIG = {
    'user': parsed.username,
    'password': parsed.password,
    'host': parsed.hostname,
    'port': parsed.port or 3306,
    'database': parsed.path.lstrip('/')
}

# Framing data
framing_entries = [
    {
        "filename": "trump.txt",
        "title": "Political Populism",
        "sample_source": "Donald J. Trump: Inauguration Speech (2017)"
    },
    {
        "filename": "hells_best_kept_secret.txt",
        "title": "Apocalyptic Protestant Fundamentalism",
        "sample_source": "Ray Comfort: Hell’s Best Kept Secret (1989)"
    },
    {
        "filename": "sokal.txt",
        "title": "Pretentious Humbug",
        "sample_source": "Sokal & Co.: Quantum Gravity Hoax and The Conceptual Penis as a Social Construct (1996, 2017)"
    },
    {
        "filename": "einstein.txt",
        "title": "Einstein's Relativity",
        "sample_source": "Albert Einstein: The Theory of Relativity and Other Essays (1946)"
    },
    {
        "filename": "milestones.txt",
        "title": "Salafist Jihadism",
        "sample_source": "Sayyid Qutb: Milestones (1964)"
    },
    {
        "filename": "gender_trouble.txt",
        "title": "Feminism",
        "sample_source": "Judith Butler: Gender Trouble (1990)"
    },
    {
        "filename": "story_of_our_colonies.txt",
        "title": "Colonial Eurocentrism",
        "sample_source": "H. R. Fox Bourne: The Story of Our Colonies (1882)"
    },
    {
        "filename": "kapital.txt",
        "title": "Purple Marxism",
        "sample_source": "Karl Marx: Das Kapital Vol. I (1867)"
    },
    {
        "filename": "mein_kampt.txt",
        "title": "Fascist Authoritarianism",
        "sample_source": "Adolf Hitler: Mein Kampf (1925)"
    },
    {
        "filename": "principia_combined.txt",
        "title": "Analytical Formalism",
        "sample_source": "Whitehead & Russell: Principia Mathematica (1910–13)"
    }
]

# Resolve path relative to this script
base_path = Path(__file__).resolve().parent / "textfiles"

# Cleaning function
def clean_text_for_embedding(raw_text: str) -> str:
    lines = raw_text.splitlines()
    lines = [line for line in lines if not re.match(r"^\s*\d{1,3}\s*$", line)]
    lines = [line for line in lines if not re.match(r"^[A-Z ,.'\-]{10,}$", line)]
    lines = [line for line in lines if not re.search(r"[^\x00-\x7F]", line)]
    lines = [line for line in lines if not re.search(r"[^a-zA-Z0-9.,;:'\"?!()\[\] \n\t\-]", line)]
    lines = [re.sub(r"\s{2,}", " ", line).strip() for line in lines if line.strip()]

    text = "\n".join(lines)
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)

    return text.strip()

# Connect and insert
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

for entry in framing_entries:
    path = base_path / entry["filename"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_content = f.read()
            cleaned = clean_text_for_embedding(raw_content)

        cursor.execute(
            """
            INSERT INTO framing (title, sample_source, content)
            VALUES (%s, %s, %s)
            """,
            (entry["title"], entry["sample_source"], cleaned)
        )
        print(f"Inserted: {entry['title']} from {entry['filename']}")
    except Exception as e:
        print(f"❌ Error for {entry['filename']}: {e}")

conn.commit()
cursor.close()
conn.close()
print("✅ All framing entries inserted with cleaned content.")

