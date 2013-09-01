import mechanize
import bs4
import re
from bs4 import BeautifulSoup
from blog_model import DanielFood_blog
from Options import Options
class DanielFood:
    def __init__(self):
        self.url = 'http://danielfooddiary.com/'
        self.options = []
        self.blogs = []

    def get_options(self, br):
        r = br.open(self.url)
        html = r.read()
        soup = BeautifulSoup(html)
        month_selector = soup.body.find("select",attrs={"name":"archive-dropdown"})
        opts = month_selector.contents
        for o in opts:
            if type(o) == bs4.element.Tag:
                url = o['value']
                month_size = o.string
                if url != '' and re.match(r'^http.*',url):
                    month = re.findall(r'\w+ \d+',month_size)[0]
                    opt = Options(url,month)
                    self.options.append(opt)
    
    def parse_one_blog(self, br, link):
        req = br.follow_link(link)
        html = req.read()
        soup = BeautifulSoup(html)
        daniel_blog = DanielFood_blog()
        daniel_blog.parse(soup.body)
        return daniel_blog

    def parse_one_page(self, br, url):
        result = []
        
        #if there is url, means the first time go in the page, 
        #else just click the older page text to get new page
        r = br.open(url)
        
        links = list(br.links(text_regex=re.compile("Continue Reading")))
        for link in links:
            blog = self.parse_one_blog(br,link)
            br.back()
            result.append(blog)
        #get next page context
        links = list(br.links(text_regex=re.compile(r'\w*Older posts')))
        if len(links) >= 1:
            result.extend(self.parse_one_page(br,links[0].url))
        return result

    def parse_one_opt(self,br,opt):
        results = self.parse_one_page(br, opt.url)
        for r in results:
            print r.date
            print r.title
            print r.content

    def parse(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        self.get_options(br)
        #check update

        for opt in self.options:
            self.parse_one_opt(br, opt)
            #break