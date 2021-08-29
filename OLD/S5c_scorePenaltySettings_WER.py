# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 20:11:03 2021

@author: aseschng
"""
#!/usr/bin/env python3
"""
Author: Chng Eng Siong
Date: 6 Aug 2021
Objective: This file scores WER
"""

import logging
import argparse
import subprocess
import sys,os
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
    log.info("{}".format("S5c: WER scoring for insertion penalty for (HotWord Decoder) _HotONLY.txt)"))

    exptDir         = config['ExptInfo']['exptDir']
    outputDir       = config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
    insPenaltyList  = config['WER_expts']['ins_penalty'].split(',')
    wtList          = config['WER_expts']['wt'].split(',')

    test_dir     = config['TestDir']['dir']
    test_ref_txt = config['TestDir']['test_ref_txt'].replace('$testDir',test_dir)

    compute_wer_cmd = config['KaldiDir']['KALDI_ROOT']+'/src/bin/cmpute-wer '

    # remember that test_ref (although it is a ctm file MUST end with.txt since it has NO word boundary timing)


    refFile  = test_ref_txt[0:len(test_ref_txt)-4]
    typeExtension = '_HotONLY.txt'
    refFileExt = refFile+typeExtension
    # We have assume step S5a has been runned!
    hotwordRawList = config['ExptInfo']['ipHotWordList']
    listHotWord = C_WordList()
    listHotWord.read_WordList(hotwordRawList, True)  # we must remember to tell the function that this is HOTWORDS


    for insPenalty in insPenaltyList:
        opFileName   = outputDir+'/'+insPenalty+'/WER_'+insPenalty+'.txt'
        opWER = open(opFileName,'w')

        for wt in wtList:

            # The hypothesis is a text file    
            hypTextFile    = outputDir+'/'+insPenalty+'/'+str(wt)+'.txt'
            hypTextFileExt = outputDir+'/'+insPenalty+'/'+str(wt)+typeExtension

            uttFileCTM = C_ArrayUttCTM()
            uttFileCTM.readTextFile(hypTextFile) 
            # the CTM class .saveCTM_HotWordOnly returns a uttArrayCTM class that have each utterance with ONLY hotwords!
            uttArrayHotWordONLY = uttFileCTM.saveCTM_HotWordOnly(listHotWord)
            uttArrayHotWordONLY.writeTextFile(hypTextFileExt)

            opStr = compute_wer_cmd+" --text --mode=present ark:"+refFileExt+ \
            " ark:"+hypTextFileExt+" capture_output=True, text=True"

            result = subprocess.run(["compute-wer", "--text", "--mode=present",
                "ark:"+refFileExt,"ark:"+hypTextFileExt], capture_output=True, text=True)
            opStr = "WER:"+hypTextFile+"\nType:"+typeExtension+"\n"+result.stdout+'\n'
            opWER.write(opStr)
            print(opStr)

        opWER.close()    

    print("===========================================\n")
    
  
def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    real_main(args.json)
    
if __name__ == "__main__":
    main()

