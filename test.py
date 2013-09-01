import os
from time import time
from sgfood import SGfood
from danielfood import DanielFood


        
def crawl():
    #crawl sgfood website
    sgfood = SGfood()
    sgfood.parse_sgfood() 
    #danielfood = DanielFood() 
    #danielfood.parse()

if __name__ == "__main__":
    t0 = time()
    crawl() 
    t1 = time()
    print 'function crawl takes %f' %(t1-t0)
