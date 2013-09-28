import CRFPP
import copy
import sys
from collections import defaultdict
TEST_FILE = "test.data"
TAGS = ['B-ORG', 'I-ORG', 'B-F', 'I-F', 'B-LOC', 'I-LOC', 'O']

stat = defaultdict(int) 

class Feature:
    def __init__(self, feature):
        list = feature.split(' ')
        self.attr = list[:-1]
        self.tag = list[-1]

def cal_evaluation(stat):
    #Evaluation matrix
    print stat
    for i in TAGS:
        #Recall
        #Precision
        recall = 0.0
        precision = 0.0
        f_score = 0.0
        tp = 0
        p = 0
        f = 0
        for k,v in stat.items():
            if k[0] == i:
                p += 1
            if k[1] == i:
                f += 1
            if k[0] == i and k[1] == i:
                tp += 1
        if p > 0:
            recall = tp*1.0/p
            print i," recall= ",recall
        if f > 0:
            precision = tp*1.0/f
            print i," precision= ",precision
        if recall > 0 or precision > 0:
            f_score = 2 * precision * recall / ( precision + recall) 
            print i," f_score= ",f_score




try:
    tagger = CRFPP.Tagger("-m ../example/sgfood/model -v 3 -n2")
    #read test data
    parsed_blog = []    
    blog = []
    sent = []
    with open(TEST_FILE) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                blog.append(sent)
                sent = []
            else:
                x = Feature(line)
                sent.append(x)
           
    
    for sent in blog:
        tagger = CRFPP.Tagger("-m ../example/sgfood/model -v 3 -n2")
        for word in sent:
            tagger.add(" ".join(word.attr))
    
        print "column size: " , tagger.xsize()
        print "taken size: ", tagger.size()
        print "tag size: ", tagger.ysize()
        
        tagger.parse()
        print "conditional prob=" , tagger.prob()," log(Z)=" , tagger.Z()
        parsed_blog.append(tagger)
        for i, word in enumerate(sent):
            stat[(word.tag,tagger.y2(i))] += 1

    sorted_blog = sorted(parsed_blog, key = lambda k:k.prob())
    for sent in sorted_blog:
        print sent.prob()
    #cal_evaluation(stat)

except RuntimeError, e:
    print "Run time Error: ", e,
