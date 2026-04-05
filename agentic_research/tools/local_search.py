from pathlib import Path
from config import RESEARCH_DIR
def load_knowledge_base(path=RESEARCH_DIR):
    knowledge_base = {}
    base_path = Path(path)
    for file in base_path.glob("**/*.md"):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            knowledge_base[file.stem] = f.read()
    return knowledge_base