import json
from models import Author, Quote
from mongoengine.errors import NotUniqueError

if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as authors_file:
        authors = json.load(authors_file)
        for el in authors:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Author {el['fullname']} already exists")

    with open("quotes.json", encoding="utf-8") as quotes_file:
        quotes = json.load(quotes_file)
        for el in quotes:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()
