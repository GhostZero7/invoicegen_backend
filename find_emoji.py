
import os

def find_emoji():
    emoji_bytes = "🔑".encode("utf-8")
    for root, dirs, files in os.walk("."):
        if "venv" in root or ".git" in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                with open(path, "rb") as f:
                    content = f.read()
                    if emoji_bytes in content:
                        print(f"FOUND 🔑 in: {path}")
            except Exception:
                pass

if __name__ == "__main__":
    find_emoji()
