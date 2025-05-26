import sys
import re
import time

SLEEP_DELAY = 0.0

ROMAN_PREFIXES = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
]

def is_article_start(lines, index):
    """
    Enhanced article start detection:
    - Follows a blank line.
    - Starts with two caps.
    - Length > 30.
    - Contains a lowercase word.
    - Contains either: comma not after lowercase, OR parenthesis.
    - Does NOT start with a Roman numeral (e.g. 'IV. ...')
    """
    if index == 0 or lines[index - 1].strip() != "":
        return False

    line = lines[index].strip()

    if len(line) <= 30:
        return False

    if not re.match(r'^[A-Z]{2}', line):
        return False

    if re.match(r'^(' + '|'.join(ROMAN_PREFIXES) + r')\.', line):
        return False

    if not re.search(r'[a-z]{2,}', line):
        return False

    if re.search(r'[^a-z],', line) or '(' in line:
        return True

    return False

def detect_article_starts(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if is_article_start(lines, i):
            print(line.strip())
            time.sleep(SLEEP_DELAY)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python article_start.py <textfile>")
        sys.exit(1)

    detect_article_starts(sys.argv[1])

