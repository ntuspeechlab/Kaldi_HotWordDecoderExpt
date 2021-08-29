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

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))

       
def real_main(ipJsonFileName):

    with open(ipJsonFileName, mode="r") as j_object:
        config = json.load(j_object)
        # Lets check the required directories
    log.info("{}".format("s5B: WER scoring for CTM for (file_WordONLY.txt, file_HotONLY.txt, file_HotAndWord.txt"))

    exptDir      = config['ExptInfo']['exptDir']
    outputDir    = config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)

    master_ctm   = config['CombineCTM']['master_ctm'].replace('$outputDir',outputDir)
    hotword_ctm  = config['CombineCTM']['hotword_ctm'].replace('$outputDir',outputDir)
    dual_ctm     = config['CombineCTM']['dual_ctm'].replace('$outputDir',outputDir)
    test_dir     = config['TestDir']['dir']
    test_ref_txt = config['TestDir']['test_ref_txt'].replace('$testDir',test_dir)


    compute_wer_cmd = config['KaldiDir']['KALDI_ROOT']+'/src/bin/cmpute-wer '

    # remember that test_ref (although it is a ctm file MUST end with.txt since it has NO word boundary timing)

    list_ctm = [dual_ctm, master_ctm, hotword_ctm]
    typeExtension = ['_HotONLY.txt', '_HOTAndWord.txt', '_WordONLY.txt']
    
    refFile  = test_ref_txt[0:len(test_ref_txt)-4]
    for ctm in list_ctm:
        hypFile  = ctm[0:len(ctm)-4]
        opFileName   = hypFile+'_WER.txt'
        opWER = open(opFileName,'w')
        for ext in typeExtension:
            refFileExt = refFile+ext
            hypFileExt = hypFile+ext

            opStr = compute_wer_cmd+" --text --mode=present ark:"+refFileExt+ \
            " ark:"+hypFileExt+" capture_output=True, text=True"

            result = subprocess.run(["compute-wer", "--text", "--mode=present",
                "ark:"+refFileExt,"ark:"+hypFileExt], capture_output=True, text=True)
            opStr = "WER:"+hypFile+"\nType:"+ext+"\n"+result.stdout+'\n'
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

