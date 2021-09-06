#!/usr/bin/env python3

"""
Filename: S2_3.py

# This  step is to 

S2) build the hotword decoder from the dircetory
    ./exp/Exp???/configLG folder
    and put the decoder into ./exp/Exp???/Output

S3) Run the hotword decoder and then put the results
    ./exp/Exp???/Output/hotword.ctm
    ./exp/Exp???/Output/master.ctm
    ./exp/Exp???/Output/penalty_0.0-> with different settings from 7_17
    ./exp/Exp???/Output/penalty_0.5-> with different settings from 7_17
    ./exp/Exp???/Output/penalty_1.0-> with different settings from 7_17

"""



import os
import argparse
import json

    

def main():


    parse = argparse.ArgumentParser()
    parse.add_argument('--json', required=True,  help="json file to setup experiment")
    args = parse.parse_args()
    ipJsonFileName = args.json
    
    with open(ipJsonFileName, mode="r") as j_object:
      config = json.load(j_object)
    # Lets check the required directories
    
    currentWD=config['ExptInfo']['currentWD']
    audioDir=config['ExptInfo']['audioDir'].replace('$currentWD',currentWD)
    exptDir=config['ExptInfo']['exptDir'].replace('$currentWD',currentWD)
    outputDir=config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
    hwBuildDir=config['ExptInfo']['hwBuildDir'].replace('$currentWD',currentWD)
    env_path_hw= config['hwBuildDir']['env_path'].replace('$hwBuildDir',hwBuildDir)
    expID=os.path.splitext(os.path.basename(exptDir))[0]
    
    print('S3: decode with hotword decoder')

    cmdStr = 'bash demo-decoder.sh ' +  audioDir + " " +  expID + " " +  env_path_hw + " " + outputDir
    print(cmdStr)
    cwd = os.getcwd()
    os.chdir(hwBuildDir)
    os.system(cmdStr)
    os.chdir(cwd)
    
    print('S3: decode with hotword decoder ... DONE')

if __name__ == "__main__":
    main()
