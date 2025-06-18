from pymongo import MongoClient

# Update with your actual MongoDB connection string
MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["society_issue_tracker"]

# Export collections
tickets_collection = db["tickets"]
technicians_collection = db["technicians"]
