from mongoengine import Document, StringField, ReferenceField, ListField, CASCADE
from mongoengine import connect
from dotenv import load_dotenv
import os
import urllib

# Завантаження змінних з .env
load_dotenv()

# Database connection parameters
DB_USERNAME = urllib.parse.quote_plus(os.getenv('DB_USERNAME'))
DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))
DB_DOMAIN = urllib.parse.quote_plus(os.getenv('DB_DOMAIN'))

uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_DOMAIN}/?retryWrites=true&w=majority"
connect(host=uri, db='test', ssl=True)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50, required=True)
    born_location = StringField(max_length=150, required=True)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)
    meta = {"collection": "quotes"}
