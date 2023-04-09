import json

import redis
from redis_lru import RedisLRU

from models import Quote, Author, Tag
import connect

client = redis.Redis(
    host="redis-10520.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=10520,
    password="TatLFSUeL7aijGWc1Q48RRx2GTNdaaW3",
)
cache = RedisLRU(client)

while True:
    command = input("Enter your command: ")

    if command == "exit":
        break

    if command.startswith("tag:"):
        tag_name = command.split(":")[1].strip()
        cached_results_json = client.get(tag_name)
        if cached_results_json:
            cached_results = json.loads(cached_results_json)
            for quote in cached_results:
                print(quote)
                print("--------------")
        else:
            quotes = Quote.objects(tags__name__startswith=tag_name)
            results = []
            for quote in quotes:
                result = f"Quote: {quote.quote} | Author: {quote.author.fullname} | Tags: {[tag.name for tag in quote.tags]}"
                print(result)
                print("--------------")
                results.append(result)
            results_json = json.dumps(results)
            client.set(tag_name, results_json)

    elif command.startswith("name:"):
        author_name = command.split(":")[1].strip().title()
        cached_results_json = client.get(author_name)
        if cached_results_json:
            cached_results = json.loads(cached_results_json)
            print("From cache:")
            for quote in cached_results:
                print(quote)
                print("--------------")
        else:
            author = Author.objects(fullname__istartswith=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                results = []
                for quote in quotes:
                    result = f"Quote: {quote.quote} | Author: {quote.author.fullname} | Tags: {[tag.name for tag in quote.tags]}"
                    print(result)
                    print("--------------")
                    results.append(result)
                results_json = json.dumps(results)
                client.set(author_name, results_json)
            else:
                print(f"Author {author_name} not found")

    elif command.startswith("tags:"):
        tags = command.split(":")[1].strip().split(",")
        quotes = Quote.objects(tags__name__in=tags)
        for quote in quotes:
            print(
                f"Quote: {quote.quote} | Author: {quote.author.fullname} | Tags: {[tag.name for tag in quote.tags]}"
            )

    else:
        print("Not supported command")
