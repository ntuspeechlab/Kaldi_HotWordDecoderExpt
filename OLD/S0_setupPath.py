"""
FileName:  S0_setupPath.py
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
import os,sys
#import shutil
import argparse

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))

def real_main(ipJsonFileName):        

   log.info("{}".format("S0_setupPath: creating the experiment folder"))
   with open(ipJsonFileName, mode="r") as j_object:
      config = json.load(j_object)
   # Lets check the required directories
   log.info("{}".format("model="+config['model_name']))


   exptDir=config['ExptInfo']['exptDir']
   result = subprocess.run(["mkdir", exptDir], capture_output=True, text=True)
   log.info("{}".format("creating the experiment folder:"+exptDir))

   configLGDir=config['ExptInfo']['configLGDir'].replace('$exptDir',exptDir)
   result = subprocess.run(["mkdir", configLGDir], capture_output=True, text=True)

   inputDir=config['ExptInfo']['inputDir'].replace('$exptDir',exptDir)
   result = subprocess.run(["mkdir", inputDir], capture_output=True, text=True)

   outputDir=config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
   result = subprocess.run(["mkdir", outputDir], capture_output=True, text=True)
   
   result=subprocess.run(['cp',ipJsonFileName,exptDir+'/'+ipJsonFileName], capture_output=True, text=True)

   # lets copy the master decoder unigram count
   masterDir  = config['MasterDecoder']['masterDir']
   masterUnigramName = config['MasterDecoder']['unigram_master'].replace('$masterDir',masterDir)
   savedUnigramName  = inputDir+'/unigram_master.count'
   result=subprocess.run(['cp',masterUnigramName, savedUnigramName], capture_output=True, text=True)
   if result.returncode != 0:
       log.exception("{}".format(result))


   ipFileName =  config['ExptInfo']['ipHotWordList']
   opFileName =  inputDir+"/hotwordRawList.txt"
   result=subprocess.run(['cp',ipFileName, opFileName], capture_output=True, text=True)
   if result.returncode != 0:
       log.info("{}".format(result))



def main():

    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    real_main(args.json)
    
if __name__ == "__main__":
    main()

