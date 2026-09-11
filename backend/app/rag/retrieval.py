from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class RagDocument:
    source_scope: str
    business_id: str | None
    source_file: str
    content: str

class TextFileRetriever:
    def __init__(self, rag_root: str):
        self.rag_root = Path(rag_root).resolve()
        self.documents: list[RagDocument] = []
        self.reload()

    def reload(self) -> int:
        self.documents = []
        for path in self.rag_root.glob("generic/**/*.txt"):
            self.documents.append(RagDocument("common", None, str(path.relative_to(self.rag_root)), path.read_text(encoding="utf-8")))
        businesses_dir = self.rag_root / "businesses"
        for path in businesses_dir.glob("*/*.txt"):
            self.documents.append(RagDocument("business", path.parent.name, str(path.relative_to(self.rag_root)), path.read_text(encoding="utf-8")))
        return len(self.documents)

    def _search(self, query: str, scope: str, business_id: str | None = None) -> list[dict]:
        terms = {word for word in re.findall(r"[\w]+", query.lower()) if len(word) > 2}
        results = []
        for doc in self.documents:
            if doc.source_scope != scope or (business_id and doc.business_id != business_id):
                continue
            text = doc.content.lower()
            score = sum(1 for term in terms if term in text) / max(len(terms), 1)
            if score > 0:
                results.append({"source_file": doc.source_file, "content": doc.content, "score": round(score, 3)})
        return sorted(results, key=lambda item: item["score"], reverse=True)[:3]

    async def search_business(self, business_id: str, query: str) -> list[dict]:
        return self._search(query, "business", business_id)

    async def search_common(self, query: str) -> list[dict]:
        return self._search(query, "common")
