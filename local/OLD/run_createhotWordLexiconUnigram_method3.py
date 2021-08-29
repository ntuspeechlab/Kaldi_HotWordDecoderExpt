#!/usr/bin/env python3
"""
#run_createhotWordLexiconUnigram_method 3
# will build a hotword lexicon, and a list of short syllables created by BPE
"""

import logging
import os, sys, io
from   libWord import C_WordList, C_OneWord
import argparse
from   libWordCount import C_WordSortedCountDict, C_WordUnSortedCountDict
import pandas as pd
# must install pandas, using bash cmd line:
# sudo apt-get install python3-pandas
# you can read about pandas here: 
# https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python

from nltk.corpus import words
# we need this to check if the token is a english word
# to speed things up, we define a set on the words
# see: https://stackoverflow.com/questions/57842654/is-there-any-faster-way-to-check-from-a-words-list-with-nltk-with-python

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))


def wordIsRomanChars(w):
    return w[0].upper() and all([ord(c) <128 or (ord(c) >= 65313 and ord(c) <= 65339) or (ord(c) >= 65345 and ord(c) <= 65371) for c in w])



def methodID_3(args):
    myMasterCount = C_WordSortedCountDict()
    topN = args.topNunigram
    myMasterCount.readUnigramCount(args.unigram_countFile,topN)   # reading topN entries
    foundTok = myMasterCount.dictSortedIdxToStr[args.fixHotWord_position-1]
    foundCountThreshold = myMasterCount.dictStrToSortedCount[foundTok]
    print("==============> Threshold for hotword ",foundCountThreshold)
    
  # Lets read the hot word first
    listWord = C_WordList()
    listWord.read_WordList( args.hotwordRawList,True)
    # we must use above class, as we need the label of the hotword in __Tanjong_Pagar_Way
    # we must pass it a flag to tell read_WordList if or if not hotWord
    myHotWordCount = C_WordUnSortedCountDict()
    for oneWordStr in listWord.listWordStr:
        oneWord = listWord.dictWStrToCWord[oneWordStr]
        countPron = 0
        for pronStr in oneWord.wordArrayPron:        
            if countPron == 0:
                myHotWordCount.addWordCount(oneWord.wordLabel, foundCountThreshold)
                countPron = countPron+1
            else:
                myHotWordCount.addWordCount(oneWord.wordLabel+'#'+str(countPron), foundCountThreshold)
                countPron=countPron+1

        #inserting the hotword and label into the myHotWordCount


    listOfWordToAdd = ['<s>','</s>','<unk>','<noise>','<v-noise>']
    for oneWordStr in  listOfWordToAdd:
        myHotWordCount.addWordCount(oneWordStr , foundCountThreshold)

        #sqrt root the count
        print('Square change in count')
        myMasterCount.SquareCount()
        myHotWordCount.SquareCount()



    # here we save the count files    
    myMasterCount.SaveFile(args.opHotDecoderUnigram,'w')
    myHotWordCount.SaveFile(args.opHotDecoderUnigram,'a')

    # here we save the lexicon
    list_englishWordsUnigram = sorted(set(myMasterCount.dictStrToSortedCount.keys()))
    listWord.add_WordList( list_englishWordsUnigram, False)  #MUST set second entry to False it is NOT a hotword
    listWord.write_WordLexicon(args.opHotDecoderLexicon)




#Example to run the code
"""
python3 run_createhotWordLexiconUnigram.py --whichMethod=$methodID --unigram_countFile ./TestData_Clean/unigram.count --topNunigram 1000 --hotwordRawList \
  ./TestData_Clean/hotwordRawList.txt  --opHotDecoderLexicon ./TestData_Op/hotwordDecoderLex.txt \
  --opHotDecoderUnigram ./TestData_Op/hotwordDecoderUnigram\
  --fixHotWord_position 300
"""

def real_main():        
    log.info("{}".format("reading given unigram count to create English lexicon for hotwords..."))
    parse = argparse.ArgumentParser()
    parse.add_argument('--whichMethod',    type=str, required=True,  help="which method to generate the unigramn count and lexicon")
    parse.add_argument('--unigram_countFile',    required=True,  help="unigram count of Master Kaldi ASR")
    parse.add_argument('--topNunigram',      type=int, default=5000, help="find topN unigrams (english words) will be retained")
    parse.add_argument('--hotwordRawList',   required=True,  help="hotword raw list file ")
    parse.add_argument('--opHotDecoderLexicon', required=True,  help="hotword decoder lexicon")
    parse.add_argument('--opHotDecoderUnigram', required=True,  help="hotword decoder unigramcount")
    parse.add_argument('--fixHotWord_position', type=int, default=300, help="fixing hotword into sorted unigram count at position xxx")
    
    
    args = parse.parse_args()

    print('At p1 ====================================')
    methodID_1(args)



def main():
    real_main()
    
if __name__ == "__main__":
    main()
