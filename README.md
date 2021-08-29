#Filename: readme.md
#Author: Chng Eng SIong
#This directory contains HOW we are going to do the hotword decoder experiment

Requirements:
1) kaldi to be setup
2) python3 and some libraries: words (nltk), pandas

3) Read hwSetup.json
	-> this is the json file specifiying all the parameters and folders for the 
	-> hotword expt
	-> each expt will create a folder and dump the hotword decoder and results there

4) You can run.sh and follow the steps
  -> goto ./exp/Exp6/ to see whats happening in this example
  -> the decoded data simulation came from ./exp/expClean
  

python3  S0_setupPath.py  --json $HWSETUP_FileName
python3  S1_createhotWordLexiconUnigram.py --json $HWSETUP_FileName
python3  S2_3.py --json $HWSETUP_FileName
python3  S4_combineCTM.py --json $HWSETUP_FileName
python3  S5a_CTM_toWERscoring_Text.py --json $HWSETUP_FileName
python3  S5b_scoreCTM_WER.py --json $HWSETUP_FileName
python3  S5c_scorePenalySettings_WER.py --json $HWSETUP_FileName

