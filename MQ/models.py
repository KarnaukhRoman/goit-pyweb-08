from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField
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
connect(host=uri, db='tasks', ssl=True)

class Contact(Document):
    fullname = StringField(required=True, max_length=200)
    email = EmailField(required=True, unique=True)
    phone_number = StringField(max_length=20, required=False)
    address = StringField(max_length=300, required=False)
    favor = BooleanField(default=False) # False - email, True - sms
    created_at = DateTimeField(auto_now_add=True) # Date and time of creation task
    message_sent = BooleanField(default=False) # False - not sent, True - sent
    processed_at = DateTimeField(auto_now_add=False, required=False) #
    consumer = StringField(max_length=30, required=False) # Name of consumer
    meta = {'collection': 'contacts'}