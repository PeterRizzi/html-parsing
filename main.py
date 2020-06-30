import requests
from collections import defaultdict
from html.parser import HTMLParser

words = defaultdict(int)
tags = defaultdict(int)

recent_starttag = None

non_code_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'li', 'ul']
code_tags = ['script', 'style']

sites = ['http://www.foxnews.com', 'https://www.nytimes.com', 'https://www.wsj.com',
         'https://www.msnbc.com']

f = open("a.txt", "w+")


class MyHTMLParser(HTMLParser):  # encapsulate storage within class
    def handle_data(self, data):
        code_flag = recent_starttag in code_tags  # or recent_starttag not in non_code_tags
        for word in data.split():  # what about two-word joins like first and last names?
            if not code_flag:
                words[word.lower()] += 1
        global f
        f.write('data: ')
        f.write(data[:200].encode('ascii', 'ignore'))
        f.write('\n')

    def handle_starttag(self, tag, attrs):
        tags[tag] += 1
        global recent_starttag
        recent_starttag = tag
        global f
        f.write("tag: ")
        f.write(tag.encode('ascii', 'ignore'))
        f.write('\n')


parser = MyHTMLParser()

for site in sites:
    r = requests.get(site)
    parser.feed(r.text)

    site_words = sum(words.values())

    print '\n' + site + '\n'

    for w in words:
        if (words[w] / float(site_words)) > .005 and len(w) > 3:
            print w
    # print words['juneteenth']

    # for t in tags:
    #     if tags[t] > 15:
    #         print t

    words = defaultdict(int)
    tags = defaultdict(int)



"""
Losing words due to missing them when they are attributes in a scrolling image
script or something like that
"""







