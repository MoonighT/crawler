import mechanize
import os
import bs4
import re
from bs4 import BeautifulSoup
from dateutil import parser

class Options:
    def __init__(self, url = "", title = "", size = 0):
        self.url = url
        self.title = title
        self.size = size

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



def parse_one_page(br,count,url=""):
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
            date_tag = blog.find("h2","date-header")
            result.append(parser.parse(date_tag.string))
        #go to next page with count = count - len(blog_div) 
        next_result = parse_one_page(br,count-len(blog_div))
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
                date_tag = blog.find("h2","date-header")
                result.append(parser.parse(date_tag.string))
    return result    
       
   
def parse_one_opt(opt,br):
    opt_result = parse_one_page(br, opt.size, opt.url)
    print opt_result

def parse_sgfood(sgfood):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    sgfood.get_options(br)
    for opt in sgfood.options:
        #check if there is new blogs
        pass
    #crawl new stuff
    for opt in sgfood.options:
        parse_one_opt(opt,br)
        break

def crawl():
   #crawl sgfood website
   sgfood = SGfood()
   parse_sgfood(sgfood) 

if __name__ == "__main__":
    crawl() 
