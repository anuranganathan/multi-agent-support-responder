# agents/intent_classifier/agent.py

import os
from typing import Literal
import joblib
from google.cloud import firestore

# Set your service account key path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"

class IntentClassifierAgent:
    def __init__(self, model_path: str = "intent_model.pkl"):
        self.model = joblib.load(model_path)
        self.db = firestore.Client()

    def classify(self, email_text: str) -> Literal[
        "billing_issue", "order_delay", "product_issue", "general_query", "unknown"
    ]:
        try:
            return self.model.predict([email_text])[0]
        except Exception as e:
            print("⚠️ Prediction error:", e)
            return "unknown"

    def classify_all_emails(self):
        emails_ref = self.db.collection("emails")
        emails = emails_ref.where("intent", "==", None).stream()  # Only unclassified

        for doc in emails:
            data = doc.to_dict()
            email_text = data.get("body", "")
            intent = self.classify(email_text)
            print(f"📨 Email: {email_text}\n🎯 Intent: {intent}")

            # Update Firestore with detected intent
            emails_ref.document(doc.id).update({"intent": intent})
