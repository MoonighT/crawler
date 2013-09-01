from dateutil import parser
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
        self.content = ''

    def parse(self,blog):
        date_tag = blog.find("h2","date-header")
        self.date = parser.parse(date_tag.string)
        self.title = blog.find("h3","post-title entry-title").a.string.strip().encode('ascii', 'ignore')
        self.content = blog.find("div","post-body entry-content").text.strip().encode('ascii', 'ignore')