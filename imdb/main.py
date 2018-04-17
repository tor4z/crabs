from crabs import Client, HTMLParser, StrParser, Set
import re

if __name__ == "__main__":
    url = "http://www.imdb.com"
    client = Client()
    client.get(url)
    parser = HTMLParser(client.text, "lxml")
    links = parser.find_all("a", href = re.compile(r"[.*title.*|.*name.*]"))
    title_parser = StrParser(r".*title/(\w*)/?")
    name_parser = StrParser(r".*name/(\w*)/?")
    title_set = Set()
    name_set = Set()

    for link in links:
        title_set.add(title_parser.find_one(link))
        name_set.add(name_parser.find_one(link))
    print(title_set)