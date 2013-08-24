import mechanize
import os
import bs4
import re
from bs4 import BeautifulSoup
from dateutil import parser

class options:
    def __init__(self, url = "", title = "", size = 0):
        self.url = url
        self.title = title
        self.size = size

class SGfood:
    def __init__(self):
        self.options = []
        self.blogs = []


br = mechanize.Browser()

r = br.open("http://www.sgfoodonfoot.com/")
html = r.read()
soup = BeautifulSoup(html)

month_selector = soup.body.find("select",id="BlogArchive1_ArchiveMenu")

opts = month_selector.contents

sgfood = SGfood()


for o in opts:
    if type(o) == bs4.element.Tag:
        url = o['value']
        month_size = o.string
        if url != '' and re.match(r'^http.*',url):
            size = re.findall(r'\(\d+\)',month_size)[0][1:-1]
            month = re.findall(r'\w+ \d+',month_size)[0]
            opt = options(url,month,size)
            sgfood.options.append(opt)


for opt in sgfood.options:
#check if there is new blogs
    pass
#crawl new stuff

for opt in sgfood.options:
    r = br.open(opt.url)
    html = r.read()
    soup = BeautifulSoup(html)
    blog_div = soup.find_all("div","date-outer")
    for blog in blog_div:
        date_tag = blog.find("h2","date-header")
        print date_tag.string
        print parser.parse(date_tag.string)
    print html
    break


