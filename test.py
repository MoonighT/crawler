import mechanize
import os
import bs4
import re
from twisted.internet import defer, reactor
from twisted.web.client import getPage
from bs4 import BeautifulSoup
from dateutil import parser
from time import time
#from nltk.tokenize import sent_tokenize

def strip_lower(s):
    return s.lower().strip()

class Options:
    def __init__(self, url = "", title = "", size = 0):
        self.url = url
        self.title = title
        self.size = size

class SGfood_blog:
    def __init__(self):
        self.date = None 
        self.title = ''
        self.content = ''

    def parse(self,blog):
        date_tag = blog.find("h2","date-header")
        self.date = parser.parse(date_tag.string)
        self.title = blog.find("h3","post-title entry-title").a.string.strip().encode('utf-8', 'ignore')
        self.content = blog.find("div","post-body entry-content").text.strip().encode('utf-8', 'ignore')

class DanielFood_blog:
    def __init__(self):
        self.date = None
        self.title = ''
        self.content = ''

    def parse(self, blog):
        date_tag = blog.find("span","post-date")
        self.date = parser.parse(date_tag.string[:-3])
        title_tag = blog.find("h1","title")
        self.title = title_tag.a['title'].strip().encode('utf-8','ignore')
        content_tag = blog.find("div","entry")
        for par in content_tag.find_all("p"):
            self.content += par.text.strip().encode('utf-8','ignore')
        

class SGfood:
    def __init__(self):
        self.url = "http://www.sgfoodonfoot.com/"
        self.options = []
        self.blogs = []
    
    def get_options(self,br):
        r = br.open(self.url)
        html = r.read()
        soup = BeautifulSoup(html)
        month_selector = soup.body.find("select",id="BlogArchive1_ArchiveMenu")
        opts = month_selector.contents
        for o in opts:
            if type(o) == bs4.element.Tag:
                url = o['value']
                month_size = o.string
                if url != '' and re.match(r'^http.*',url):
                    size = re.findall(r'\(\d+\)',month_size)[0][1:-1]
                    month = re.findall(r'\w+ \d+',month_size)[0]
                    opt = Options(url,month,int(size))
                    self.options.append(opt)

    def parse_one_page(self,br,count,url=""):
        if count <= 0:
            return None
        result = []
        
        #if there is url, means the first time go in the page, 
        #else just click the older page text to get new page
        if url == "":
            req = br.click_link(text="Older Posts")
            r = br.open(req)
        else:
            r = br.open(url)
        html = r.read()
        soup = BeautifulSoup(html)
        blog_div = soup.find_all("div","date-outer")
        
        if count > len(blog_div):
            #crawl whole page and go to next page
            for blog in blog_div:
                #crawl one blog item
                sg_blog = SGfood_blog()
                sg_blog.parse(blog)
                result.append(sg_blog)
            #go to next page with count = count - len(blog_div) 
            next_result = self.parse_one_page(br,count-len(blog_div))
            if next_result != None:
                result.extend(next_result)
            else:
                pass
        else:
            #crawl only this page with count item
            for i,blog in enumerate(blog_div):
                if i>= count:
                    break
                else:
                    sg_blog = SGfood_blog()
                    sg_blog.parse(blog)
                    result.append(sg_blog)
        return result    
           
       
    def parse_one_opt(self,opt,br):
        opt_result = self.parse_one_page(br, opt.size, opt.url)
        for blog in opt_result:
            print blog.title
            print blog.date
            print blog.content

    def parse_sgfood(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        self.get_options(br)
        for opt in self.options:
            #check if there is new blogs
            pass
        #crawl new stuff
        for opt in self.options:
            self.parse_one_opt(opt,br)
        #    break

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
def crawl():
    #crawl sgfood website
    #sgfood = SGfood()
    #sgfood.parse_sgfood() 
    danielfood = DanielFood() 
    danielfood.parse()

if __name__ == "__main__":
    t0 = time()
    crawl() 
    t1 = time()
    print 'function crawl takes %f' %(t1-t0)
