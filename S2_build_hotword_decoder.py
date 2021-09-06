#!/usr/bin/env python3
"""
Filename: S2_build_hortowrd_decoder.py

# This  step is to 

S2) build the hotword decoder from the dircetory
    ./exp/Exp???/configLG folder
    and put the decoder into ./exp/rebuildLM/exp/Exp???/graph

"""



import os
import sys
import argparse
import json
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
log = logging.getLogger("{}".format(os.path.basename(sys.argv[0])))    

def main():


    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    ipJsonFileName = args.json
    
    with open(ipJsonFileName, mode="r") as j_object:
      config = json.load(j_object)
    
    
    scriptDir=config['ExptInfo']['currentWD']
    exptDir=config['ExptInfo']['exptDir'].replace('$currentWD',scriptDir)
    dataLGDir=config['ExptInfo']['dataLGDir'].replace('$exptDir',exptDir)
    
    lexicon_hw=dataLGDir+'/'+config["dataLGDir"]["hwLex"]
    lm_hw=dataLGDir+'/'+config['dataLGDir']['hwUnigram_arpa_gz']
    hwBuildDir=config['ExptInfo']['hwBuildDir'].replace('$currentWD',scriptDir)
    env_path_hw= config['hwBuildDir']['env_path'].replace('$hwBuildDir',hwBuildDir)
    expID=os.path.splitext(os.path.basename(exptDir))[0]
    
    log.info("{}".format("Building the hotword decoder"))
    cmdStr = 'bash build-hotword-decoder.sh ' + lexicon_hw + " " + lm_hw + " " +  expID + " " +  env_path_hw
    
    cwd = os.getcwd()
    os.chdir(hwBuildDir)
    os.system(cmdStr)
    os.chdir(cwd)
    log.info("{}".format("Building the hotword decoder ... DONE"))
    
if __name__ == "__main__":
    main()
