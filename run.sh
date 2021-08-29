#!/bin/bash0
#
# Author : Chng Eng Siong

# This is the script to run, to create the hotword decoder expt
# We will assume you have (required)
#	1) a master decoder
#	2) unigram count of master
#	3) a hotword list
#
#	Optional:
#	4) testfolder and reffile of test
#

# Step 0:
# You must initialize hwSetup.json
# and setup all fields and path, then run
# we now use python3 (v3.6 greater) -> dependencies for subprocess, and others

#step0 , you must edit and put your own hwSetup.json!
HWSETUP_FileName='hwSetup.json'


python3  S0_setupPath.py  --json $HWSETUP_FileName
python3  S1_createhotWordLexiconUnigram.py --json $HWSETUP_FileName
python3  S2_3.py --json $HWSETUP_FileName
python3  S4_combineCTM.py --json $HWSETUP_FileName
python3  S5a_CTM_toWERscoring_Text.py --json $HWSETUP_FileName
python3  S5b_scoreCTM_WER.py --json $HWSETUP_FileName
python3  S5c_scorePenalySettings_WER.py --json $HWSETUP_FileName




