"""
FileName:  S4_combineCTM.py
Author: Chng Eng Siong
Date: 28 Aug 2021

This file setups the directories needed for the experiments using json file,
unlike bash used traditionally in kaldi
hence to run the scripts, all paths MUST be put into the json file, e.g, hwSetup.json

% requires python 3.6 and above as we use subprocess

    """
import json
import logging
import subprocess
import os, sys, io
import argparse

sys.path.append('./local')  # for my own library
import libCTM
from   libCTM  import C_ArrayUttCTM   # eng siong's library 
from   libCTM  import C_UttCTM
from   libWord import C_WordList


logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))

def real_main(ipJsonFileName):        

   log.info("{}".format("S4_combineCTM: Combining Master and Hotword CTM filesgenerated by KALDI ..."))
   with open(ipJsonFileName, mode="r") as j_object:
      config = json.load(j_object)
   # Lets check the required directories
   log.info("{}".format("combining the CTM of Master and Hotword decoder"))

   # parameters settings  extracted from json file
   hotwordRawList = config['ExptInfo']['ipHotWordList']

   exptDir=config['ExptInfo']['exptDir']
   outputDir=config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
   master_ctm     = config['CombineCTM']['master_ctm'].replace('$outputDir',outputDir)
   hotword_ctm    = config['CombineCTM']['hotword_ctm'].replace('$outputDir',outputDir)
   dual_ctm       = config['CombineCTM']['dual_ctm'].replace('$outputDir',outputDir)
   collar_rate    = config['CombineCTM']['collar_rate']  # default = 0.25
                                                       #"Overlapping time to insert hotword (%) between Master and Keyword"
   print(master_ctm,hotword_ctm,collar_rate, dual_ctm)
   uttFileMasterCTM = C_ArrayUttCTM()
   uttFileMasterCTM.readCTMFile(master_ctm) 

   uttFileHotWordCTM = C_ArrayUttCTM()
   uttFileHotWordCTM.readCTMFile(hotword_ctm)  

   # This is for the future! :) 
   listHotWord = C_WordList()
   listHotWord.read_WordList( hotwordRawList, True)  # we must tell the function that we are reading HOTLIST

   dualDecoderCTM = C_ArrayUttCTM()
   for eachMasterUtt in uttFileMasterCTM.arrayUttCTM:
        uttName          = eachMasterUtt.uttName
        found_hotWordUtt = uttFileHotWordCTM.getCTMfromUttName(uttName)
        if ( found_hotWordUtt == 0):
            log.info("{}".format('warning, hotword ctm does not have this utt'+uttName+'\n'))
            # since there is no hotword utt, just add the master utt as dual!
            # This is possible (when the hotword decoder outputs nothing for this utterance)
            retCTM = eachMasterUtt
        else:
            oneUttHotWordONLYCTM  = libCTM.fn_retainOnlyHotWord(listHotWord, found_hotWordUtt)
            retCTM                = libCTM.fn_combineMasterCTM_HotWordCTM(eachMasterUtt, 
                                                  oneUttHotWordONLYCTM, collar_rate)
        dualDecoderCTM.addUttCTM(retCTM)
    
   # lets save All the utterances        
   dualDecoderCTM.writeCTMFile(dual_ctm)
   print('===============  completed ===================')
    


def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    real_main(args.json)
    
if __name__ == "__main__":
    main()

