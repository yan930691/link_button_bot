# database.py
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.users = self.db.users
        self.buttons = self.db.buttons
        self.scripts = self.db.scripts
        self.files = self.db.files

    def get_user(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def create_user(self, user_id, lang="my"):
        if not self.get_user(user_id):
            self.users.insert_one({"user_id": user_id, "lang": lang})
            return True
        return False

    def get_user_lang(self, user_id):
        user = self.get_user(user_id)
        return user.get("lang", "my") if user else "my"

    def set_user_lang(self, user_id, lang):
        self.users.update_one({"user_id": user_id}, {"$set": {"lang": lang}}, upsert=True)

    def get_buttons(self, user_id):
        data = self.buttons.find_one({"user_id": user_id})
        return data.get("buttons", []) if data else []

    def set_buttons(self, user_id, buttons):
        self.buttons.update_one(
            {"user_id": user_id},
            {"$set": {"buttons": buttons}},
            upsert=True
        )

    def delete_buttons(self, user_id):
        self.buttons.delete_one({"user_id": user_id})

    def set_script_state(self, user_id, state, data=None):
        self.scripts.update_one(
            {"user_id": user_id},
            {"$set": {"state": state, "data": data or {}}},
            upsert=True
        )

    def get_script_state(self, user_id):
        doc = self.scripts.find_one({"user_id": user_id})
        if doc:
            return doc.get("state", "idle"), doc.get("data", {})
        return "idle", {}

    def clear_script_state(self, user_id):
        self.scripts.delete_one({"user_id": user_id})

db = Database()
