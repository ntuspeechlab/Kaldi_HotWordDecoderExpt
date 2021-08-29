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
Usage: python3 run_remove_WB_inNonHotWordLex.py --infile inLexName --opFileName opLexName
"""

import logging
import argparse
import subprocess
import sys,os

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))



#run_remove_WB_inNonHotWord.py --infile inLexFIle

def real_main():        
    log.info("{}".format("Removing _WB_ in non HotWord"))
    parse = argparse.ArgumentParser()
    parse.add_argument('--infile', required=True,  help="input file ")
    parse.add_argument('--opFileName', required=True,  help="opfilename to be saved")
    args = parse.parse_args()

    inFileName   = args.infile;
    opFileName   = args.opFileName


    inFile = open(inFileName)
    lines = inFile.readlines()

    opFile = open(opFileName,'w')
    for line in lines:
        tok = list(line.strip().split(' '))
        print(tok[0],tok[1],tok[-1])
        if (tok[0][0:2] == '__'):
            pass
        else:
            tok[1]  = tok[1].replace('_WB_','_')
            tok[-1] = tok[-1].replace('_WB_','_')

        opStr = ''
        for t in tok:    
            opStr = opStr+str(t)+' '

        opStr=opStr+'\n'
        print('P1:',opStr)    
        opFile.write(opStr)

    inFile.close()
    opFile.close()


    
def main():
    real_main()
    
if __name__ == "__main__":
    main()
