# -*- coding: utf-8 -*-
"""

This function reads directories of CTM files with different penailty and settings of the hotword decoder op
It will convert them to HOTWORD ONLY and score
The idea is to find the best setting

"""
#
import logging
import os, sys, io
import argparse
from   libCTM     import C_ArrayUttCTM   # eng siong's CTM library 
from   libWord    import C_WordList

       
def real_main(listHotWord, ipCTMTextFile, refFile):        
 
    print('\n======================\nExpt:\n'
        'Kaldi-CTM-File=', ipCTMTextFile,'\n'+refFile)

    uttFileCTM = C_ArrayUttCTM()
    uttFileCTM.readTextFile(ipCTMTextFile)
    opFileName = ipCTMTextFile[0:len(ipCTMTextFile)-4]; 

    # the CTM class .saveCTM_HotWordOnly returns a uttArrayCTM class that have each utterance with ONLY hotwords!
    uttArrayHotWordONLY = uttFileCTM.saveCTM_HotWordOnly(listHotWord)
    hypFile = opFileName+'_HOTWordONLY.txt'
    uttArrayHotWordONLY.writeTextFile(hypFile)
    print('saved:', hypFile)

    opStr = "/home/eschng/kaldi/src/bin/compute-wer --text --mode=present ark:"+refFile+ \
        " ark:"+hypFile
    os.system(opStr)    
    print('\n--------------')

#export DirTestData=$PWD/data/TestData

def main():
    ipHotWordFile = './../exp/hotwordRawList.txt'
    listHotWord = C_WordList()
    listHotWord.read_WordList( ipHotWordFile, True)  # we must remember to tell the function that this is HOTWORDS

    ipDir = ['penalty_0.0','penalty_0.5','penalty_1.0',]    
    for dirX in ipDir: 
        for wt in range(7,18):
            filename =    './../exp/Exp2/Output/'+dirX+'/'+str(wt)+'.txt'
            ipKaldiHotWordDecoderCTMFile = filename
            refFile =  './../data/TestData/groundTruth_HOTWordONLY.txt'
            real_main(listHotWord, ipKaldiHotWordDecoderCTMFile, refFile)
    
if __name__ == "__main__":
    main()
