import mechanize
import os
from bs4 import BeautifulSoup

br = mechanize.Browser()

r = br.open("http://danielfooddiary.com/2013/08/22/playkitchen/")
html = r.read()
soup = BeautifulSoup(html)

print soup.body.div.select("span.post-date")[0].contents

