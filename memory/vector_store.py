class SimpleVectorStore:
    def __init__(self):
        self.documents = []

    def add_document(self, text: str):
        self.documents.append(text)

    def search(self, query: str, top_k: int = 3):
        """Mock vector search. Returns dummy data."""
        return [doc for doc in self.documents if query.lower() in doc.lower()][:top_k]
