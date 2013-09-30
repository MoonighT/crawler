from dateutil import parser
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize,sent_tokenize
def generate_token(content):
    return [word_tokenize(t) for t in sent_tokenize(content)]

class DanielFood_blog:
    def __init__(self):
        self.date = None
        self.title = ''
        self.content = ''

    def parse(self, blog):
        date_tag = blog.find("span","post-date")
        self.date = parser.parse(date_tag.string[:-3])
        title_tag = blog.find("h1","title")
        self.title = title_tag.a['title'].strip().encode('ascii','ignore')
        content_tag = blog.find("div","entry")
        for par in content_tag.find_all("p"):
            self.content += par.text.strip().encode('ascii','ignore')


class SGfood_blog:
    def __init__(self):
        self.date = None 
        self.title = ''
        self.content = []

    def parse(self,blog):
        date_tag = blog.find("h2","date-header")
        self.date = parser.parse(date_tag.string)
        self.title = blog.find("h3","post-title entry-title").a.string.strip().encode('ascii', 'ignore')
        #self.content = blog.find("div","post-body entry-content").text.strip().encode('ascii', 'ignore')
        

        text = blog.find("div","post-body entry-content")

        content_list = str(text).split('</div>')
        for c in content_list:
            text = BeautifulSoup(c).text.strip().encode('ascii', 'ignore')
            if len(text) > 0:
                self.content.extend(generate_token(text))
