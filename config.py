from pymongo import MongoClient

# MongoDB connection string (make sure it's correct and encoded properly)
MONGO_URI = "mongodb+srv://society_user:Bank%401980@cluster0.sy8c2a5.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

# Use your desired DB and collection names
db = client["society_support"]
ticket_collection = db["tickets"]

# Predefined technicians (could be moved to DB if needed)
technicians = {
    "tech_1": {"name": "Tech 1", "mobile": "9000010001"},
    "tech_2": {"name": "Tech 2", "mobile": "9000010002"},
    "tech_3": {"name": "Tech 3", "mobile": "9000010003"},
    "tech_4": {"name": "Tech 4", "mobile": "9000010004"},
    "tech_5": {"name": "Tech 5", "mobile": "9000010005"},
    "tech_6": {"name": "Tech 6", "mobile": "9000010006"},
}
