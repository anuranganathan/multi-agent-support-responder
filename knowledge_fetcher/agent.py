from google.cloud import firestore

class KnowledgeFetcherAgent:
    def __init__(self, project_id="multi-agent-support-bot"):
        self.db = firestore.Client(project=project_id)
        self.collection = self.db.collection("faq_database")  # ← Collection name in Firestore

    def fetch_info(self, intent: str) -> str:
        doc_ref = self.collection.document(intent)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("response", "Response not found.")
        else:
            return "Sorry, no info available for this request."
