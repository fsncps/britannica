import subprocess
from pathlib import Path

input_files = ["1.djvu", "2.djvu", "3.djvu"]
output_file = "principia_combined.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    for fname in input_files:
        path = Path(fname)
        if path.exists():
            print(f"Extracting: {fname}")
            try:
                result = subprocess.run(
                    ["djvutxt", str(path)],
                    capture_output=True,
                    check=True,
                    text=True
                )
                outfile.write(f"--- START OF {fname} ---\n\n")
                outfile.write(result.stdout)
                outfile.write(f"\n\n--- END OF {fname} ---\n\n")
            except subprocess.CalledProcessError as e:
                print(f"Error extracting {fname}: {e}")
        else:
            print(f"File not found: {fname}")

print(f"\nCombined output written to: {output_file}")

