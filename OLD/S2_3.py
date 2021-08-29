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
    

    exptDir=config['ExptInfo']['exptDir']
    outputDir=config['ExptInfo']['outputDir'].replace('$exptDir',exptDir)
    IpDir = './exp/expClean/Output/*'
    cmdStr = 'cp -r '+IpDir+' '+outputDir
    os.system(cmdStr)

    print('S2: build hotword decoder')
    print('S3: run hotword decoder')
    print('To simulate: We will copy past output from '+IpDir+'to '+outputDir)

    
if __name__ == "__main__":
    main()
