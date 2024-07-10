import redis
from redis_lru import RedisLRU
from dotenv import load_dotenv
from models import Quote, Author
import os

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

connect_redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


cache = RedisLRU(connect_redis)
@cache
def find_quotes_by_name(name: str) -> list:
    print(f"Function call: find_quotes_by_name ")
    list_quotes = []
    author = Author.objects(fullname__iregex=name).first()
    if not author:
        print(f"Автор '{name}' не знайдений.")
        return
    quotes = Quote.objects(author=author)
    for quote in quotes:
        # print(quote.quote)
        list_quotes.append(quote.quote)
    return list_quotes
@cache
def find_quotes_by_tag(tag: str) -> list:
    list_quotes = []
    quotes = Quote.objects(tags__iregex=tag)
    if not quotes:
        print(f"Тег '{tag}' не знайдений.")
        return
    for quote in quotes:
        print(quote.quote)
        list_quotes.append(quote.quote)

    return list_quotes
@cache
def find_quotes_by_tags(tags_list: str) -> list:
    list_quotes = []
    quotes = Quote.objects(tags__in=[name.strip() for name in tags_list])
    if not quotes:
        print(f"Цитати з тегами '{', '.join(tags_list)}' не знайдені.")
        return
    for quote in quotes:
        print(quote.quote)
        list_quotes.append(quote.quote)

    print(f"Function call : find_quotes_by_tags ")
    return list_quotes

def parse_input(user_input):
    cmd, *args = user_input.split(':')
    cmd = cmd.strip().lower()
    return cmd, *args


commands = {
    'name': find_quotes_by_name,
    'tag': find_quotes_by_tag,
    'tags': find_quotes_by_tags
}

def main():
    while True:
        user_input = input("Введіть команду (author:ім'я або tag:тег або tags:тег1,тег2,...): ")
        command, value = parse_input(user_input)
        if command in ['close', 'quit', 'exit']:
            print('Goodbye!')
            break
        else:
            if command in commands:
                if command == 'tags':
                    tags = value.split(',')
                    print(tags)
                    print(commands[command](tags))
                else:
                    print(commands[command](value.strip()))
            else:
                print("Невідома команда. Будь ласка, використовуйте 'name:', 'tag:' або 'tags:'.")



if __name__ == '__main__':
    main()
