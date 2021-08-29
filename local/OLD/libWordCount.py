#!/usr/bin/env python3
"""
Filename: libWordCount.py (to be imported as a module)
Author: Chng Eng Siong
Date: 6 Aug 2021
Last edited: 3rd Aug 2021 (CES), 11:07pm
Objective: Libraries supporting count of unigram
"""
#
import re
import logging
import os, sys, io
from   libWord import C_WordList, C_OneWord
from   dataclasses import dataclass
import pandas as pd
import numpy as np
from nltk.corpus import words
# we need this to check if the token is a english word
# to speed things up, we define a set on the words
# see: https://stackoverflow.com/questions/57842654/is-there-any-faster-way-to-check-from-a-words-list-with-nltk-with-python



logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))

"""
word1 count
word2 count
"""
def wordIsRomanChars(w):
    return w[0].upper() and all([ord(c) <128 or (ord(c) >= 65313 and ord(c) <= 65339) or (ord(c) >= 65345 and ord(c) <= 65371) for c in w])


@dataclass
class C_WordSortedCountDict:
    fileName: str
    test: str
    dictSortedIdxToStr = {}
    dictStrToSortedCount = {}

    def __init__(self):
        self.fileName = ''
        self.test = "ABC"
        self.dictSortedIdxToStr = {}
        self.dictStrToSortedCount = {}
 

    def readUnigramCount(self, unigram_countFile, topNunigram):
    # Lets read the given unigram of Master first
    # we will use pandas, and assume that the unigram count has 2 fields
    # The first row must NOT be ignored, hence header = none
    # see how to use pandas in: https://re-thought.com/pandas-value_counts/
        df = pd.read_csv(unigram_countFile, header=None, encoding='utf8', dtype={'token':'str', 'count':'int'}, sep='\t')
        # BUT pandas require 1st row to have the field ID
        # we can replocate it by the following, BUT we must save the original first!
        df.columns = ['token','count']
        sorted_df = df.sort_values('count',ascending=False)
        print('Reading unigram file: num of elements read in ',unigram_countFile,' = ', len(df))

        # we will save those unique english-only  words!!!
        numFound=0
        setWords =set(words.words()) # if we dont use set, its very slow!!!
        self.filename = unigram_countFile
        self.dictSortedIdxToStr = {}
        self.dictStrToSortedCount = {}
        for tok,count in zip(sorted_df['token'].values, sorted_df['count'].values):
            if wordIsRomanChars(str(tok)) == 1 and numFound< topNunigram and (tok in setWords):
                self.dictStrToSortedCount[tok] = count
                self.dictSortedIdxToStr[numFound]=tok
                numFound=numFound+1
        print('Reading unigram file: found english words=',numFound)        


    def SaveFile(self, fileName, mode):
        log.info("Writing SortedCountDict File : ({})".format(fileName))
        opfile = open(fileName,mode,encoding='utf8')
        for i in range(0,len(self.dictSortedIdxToStr)):
            tok   = self.dictSortedIdxToStr[i]
            count = self.dictStrToSortedCount[tok]
            opfile.write("{0} {1}\n".format(tok, count))
        opfile.close()
        log.info("Completed Writing Sorted File ({}) has ({}) entries".format(fileName,len(self.dictSortedIdxToStr)))


    def SqrtRootCount(self):
        for i in range(0,len(self.dictSortedIdxToStr)):
            tok   = self.dictSortedIdxToStr[i]
            count = self.dictStrToSortedCount[tok]
            self.dictStrToSortedCount[tok] = int(np.sqrt(count))
                
    def SquareCount(self):
        for i in range(0,len(self.dictSortedIdxToStr)):
            tok   = self.dictSortedIdxToStr[i]
            count = self.dictStrToSortedCount[tok]
            self.dictStrToSortedCount[tok] = int(count*count)
                





@dataclass
class C_WordUnSortedCountDict:
    dictStrToCount: dict

    def __init__(self):
        self.dictStrToCount = {}
 

    def addWordCount(self, wordStr, wordCount):
        self.dictStrToCount[wordStr] = wordCount


    def SaveFile(self, fileName, mode):
        log.info("Writing UNSortedCountDict File : ({})".format(fileName))
        opfile = open(fileName,mode,encoding='utf8')
        for tok in self.dictStrToCount:
            count = self.dictStrToCount[tok]
            opfile.write("{0} {1}\n".format(tok, count))
        opfile.close()
        log.info("Completed Writing Sorted File ({}) has ({}) entries".format(fileName,len(self.dictStrToCount)))

    def SqrtRootCount(self):
        for tok in self.dictStrToCount:
            count = self.dictStrToCount[tok]
            self.dictStrToCount[tok] = int(np.sqrt(count))

    def SquareCount(self):
        for tok in self.dictStrToCount:
            count = self.dictStrToCount[tok]
            self.dictStrToCount[tok] = int(count*count)



def unit_test():

    myMasterCount = C_WordSortedCountDict()
    topN = 20
    myMasterCount.readUnigramCount('./exp/ExpX/Input/unigram.count',topN)   # reading topN entries
    myMasterCount.SaveFile('./exp/ExpX/dataLG/testCount.txt','w')



  # Lets read the hot word first
    listHotWord = C_WordList()
    listHotWord.read_WordList( './exp/ExpX/Input/hotwordRawList.txt', True)
    # we must use above class, as we need the label of the hotword in __Tanjong_Pagar_Way
    # we must pass it a flag to tell HIM if of if not hotWord
    myHotWordCount = C_WordUnSortedCountDict()
    for oneWordStr in listHotWord.listWordStr:
        oneWord = listHotWord.dictWStrToCWord[oneWordStr]
        myHotWordCount.addWordCount(oneWord.wordLabel, 99)
        #inserting the hotword and label into the myHotWordCount

    myHotWordCount.SaveFile('./exp/ExpX/dataLG/testCount.txt','a')
    
if __name__ == "__main__":
    unit_test()
