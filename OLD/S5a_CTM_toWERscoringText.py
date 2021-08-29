# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 20:11:03 2021

@author: aseschng
"""
#!/usr/bin/env python3
"""
Author: Chng Eng Siong
Date: 29 Aug 2021
Objective: to convert the ctm file to text file ready for WER
This function allows CTM files to saved as text files so that WER can be called
we will  need a hotword list to convert as well

"""
#
import logging
import os, sys, io
import argparse
import json
sys.path.append('./local')  # for my own library
from   libCTM     import C_ArrayUttCTM   # eng siong's CTM library 
from   libWord    import C_WordList

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))




def real_main(ipJsonFileName):        

    with open(ipJsonFileName, mode="r") as j_object:
        config = json.load(j_object)
        # Lets check the required directories
    log.info("{}".format("S5a: Save CTM as text file for WER scoring ..."))

    exptDir      = config['ExptInfo']['exptDir']
    outputDir    = config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
    master_ctm   = config['CombineCTM']['master_ctm'].replace('$outputDir',outputDir)
    hotword_ctm  = config['CombineCTM']['hotword_ctm'].replace('$outputDir',outputDir)
    dual_ctm     = config['CombineCTM']['dual_ctm'].replace('$outputDir',outputDir)

    test_dir     = config['TestDir']['dir']
    test_ref_txt = config['TestDir']['test_ref_txt'].replace('$testDir',test_dir)
    # remember that test_ref (although it is a ctm file MUST end with.txt since it has NO word boundary timing)

    hotwordRawList = config['ExptInfo']['ipHotWordList']
    listHotWord = C_WordList()
    listHotWord.read_WordList(hotwordRawList, True)  # we must remember to tell the function that this is HOTWORDS

    list_ctm = [dual_ctm, master_ctm, hotword_ctm, test_ref_txt]
    for ctm in list_ctm:
        uttFileCTM = C_ArrayUttCTM()

        # This is to deal with event that ctm is txt (from reference!)
        if (ctm[-4:len(ctm)] == '.txt'):
            uttFileCTM.readTextFile(ctm) 

        if (ctm[-4:len(ctm)] == '.ctm'):
            uttFileCTM.readCTMFile(ctm) 

        opFileName = ctm[0:len(ctm)-4]  # extract ONLY the name and directory
        # the CTM class .saveCTM_HotWordOnly returns a uttArrayCTM class that have each utterance with ONLY hotwords!
        uttArrayHotWordONLY = uttFileCTM.saveCTM_HotWordOnly(listHotWord)
        uttArrayHotWordONLY.writeTextFile(opFileName+'_HotONLY.txt')

        # the CTM class .saveCTM_WordOnly returns a uttArrayCTM class that have each utterance with ONLY words!
        uttArrayWordONLY = uttFileCTM.saveCTM_WordOnly(listHotWord)
        uttArrayWordONLY.writeTextFile(opFileName+'_WordONLY.txt')

    
        # the CTM class .saveCTM_WordOnly returns a uttArrayCTM class that have each utterance with words + hotwords!
        uttArrayWordAndHotWordLabel = uttArrayWordONLY.saveCTM_WordAndHotWordLabel(listHotWord)
        uttArrayWordAndHotWordLabel.writeTextFile(opFileName+'_HotAndWord.txt')

    
    
def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    real_main(args.json)
    
if __name__ == "__main__":
    main()

