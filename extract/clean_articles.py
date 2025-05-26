import sys
import re

def is_article_start(lines, index):
    """
    Detects if a line is an article start:
    - Follows a blank line.
    - Starts with two capital letters.
    - Length > 30.
    - Contains at least one lowercase word.
    - Contains a comma not preceded by lowercase OR an opening parenthesis.
    - Does not start with a Roman numeral (I. ... XX.)
    """
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
    """
    Heuristic to detect meaningful article body text:
    - Not empty.
    - Doesn't start with 'Fig.' or a number + space.
    - Doesn't start with Roman numerals.
    - Doesn't look like a formula or all-caps code.
    - Must contain a lowercase word.
    """
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

def clean_articles_from_file(input_path, output_path):
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

    # Save final article
    if current_article.strip():
        articles.append(current_article.strip())

    with open(output_path, "w", encoding="utf-8") as f:
        for article in articles:
            f.write(article + "\n\n")

    print(f"Extracted {len(articles)} articles.")

# --- Entry Point ---
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_articles.py input.txt output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    clean_articles_from_file(input_path, output_path)

