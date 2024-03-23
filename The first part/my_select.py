

from typing import Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def search_quotes():
    while True:
        command = input("Enter a command (eg, name: Steve Martin, tag: life, tags: life,live, або exit): ")

        if command.strip() == "exit":
            break

        parts = command.split(":")
        if len(parts) != 2:
            print("Invalid command format. Try again.")
            continue

        key, value = parts[0].strip(), parts[1].strip()

        if key == "name":
            print(find_by_author(value))

        elif key == "tag":
            print(find_by_tag(value))

        elif key == "tags":
            tags = value.split(",")
            quotes = Quote.objects(tags__in=tags)

            unique_quotes = set()

            for quote in quotes:
                unique_quotes.add(quote.quote)

            for unique_quote in unique_quotes:
                print(unique_quote)

        else:
            print("Unknown team. Try again.")


if __name__ == "__main__":
    search_quotes()

# if __name__ == '__main__':
#     print(find_by_tag('mi'))
#     print(find_by_tag('mi'))
#
#     print(find_by_author('in'))
#     print(find_by_author('in'))
#     quotes = Quote.objects().all()
#     print([e.to_json() for e in quotes])
