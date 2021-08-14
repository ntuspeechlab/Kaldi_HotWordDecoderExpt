#!/usr/bin/env python3
"""
Filename: createExp.py
Author: Chng Eng Siong
Date: 13 Aug 2021

	This python script setups the directory structure of the experiment
	it will take in a json file, which will describe the experiment, 
	and directory name
"""

import logging,os,sys
import shutil
import argparse
import subprocess
import json

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))

def real_main():        

    print("P1:",os.environ["ExpDir"])

    log.info("{}".format("creating the experiment folder"))
    parse = argparse.ArgumentParser()
    parse.add_argument('--setup',    required=True,  help="json file describing the experiment")
    args = parse.parse_args()

    
    # Save the json file used for the experiment
    with open(args.setup) as f:
        data = json.load(f)

   

    result = subprocess.run(["mkdir", os.environ["ExpDir"]], capture_output=True, text=True)
    print(result)
    result = subprocess.run(["mkdir", os.environ["ExpLGDir"]], capture_output=True, text=True)
    print(result)
    result = subprocess.run(["mkdir", os.environ["ExpInput"]], capture_output=True, text=True)
    print(result)
    result = subprocess.run(["mkdir", os.environ["ExpOutput"]], capture_output=True, text=True)
    print(result)

    openFileName = os.environ["ExpDir"]+"/expInfo.json"
    with open(openFileName, 'w') as outfile:
        json.dump(data, outfile)
        f.close()

    # step 2
    # we must put 2 files into the directory exp/expX/Input
    # the hotwordRawList.txt and the MasterDecoder/unigram.count
    # for our purpose, we will copy these from:
    # ./data/TestData/hotwordRawList.txt
    # and ./data/MasterDecoder/unigram.count
    src = os.environ["DirMaster"]+"/unigram.count"
    dst = os.environ["ExpInput"]+"/unigram.count"
    result=shutil.copyfile(src, dst)
    print("copied:",result)

    src =  os.environ["IpHotWordList"]
    dst =  os.environ["ExpInput"]+"/hotwordRawList.txt"
    result=shutil.copyfile(src, dst)
    print("copied:",result)

def main():
    real_main()
    
if __name__ == "__main__":
    main()

