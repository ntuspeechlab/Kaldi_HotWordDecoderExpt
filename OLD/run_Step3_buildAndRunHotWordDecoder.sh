#!/bin/bash
# Note expX is a place holder, it should be which expt you are runing, and the appropriate directory

source pathExpt.sh   # This will tell you the parameters needed below

run_Step3a_BuildHotWordDecoder --ipDir $DirMaster --LGDir $ExpLGDir --opDir $ExpLGDir
# in this step, yachao should 
#    1) build the hotword decoder, e.g with the parameters
        # we need the above script to know where the Master Directory is, and where the
        # LG info are, and where to dump the hotword decoder model        

run_Step3b_RunDecoder_onTestFiles --modelDir $ExpLGDir --ipTestDir $DirTestData --opDir $ExpOutput/hotword.ctm
# Run the hotword decoder to create the hotword.ctm

run_Step3c_RunDecoder__onTestFiles --modelDir $DirMaster --ipTestDir $DirTestData --opDir $ExpOutput/master.ctm
# Run the master decoder (if needed) or just copy the master decoder op to create the master.ctm

# At $ExpOutput, you should Now have two file
#     hotword.ctm and master.ctm
# if not the next step will fail!!!



