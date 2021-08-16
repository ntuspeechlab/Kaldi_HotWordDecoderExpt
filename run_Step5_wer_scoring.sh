#!/bin/bash
#source pathDesktop.sh
source pathLaptop.sh

ExpID=./exp/ExpX  #initialise this if its gone

# After you have run this file, and then check ./TestDataOp
# The output should be self-explanatory
#

# This script scores the WER of the master, hotword, and dual decoder's output
#

# if the reference ctm in the 3 format does not exist, we must create them
inRefWord=$ExpID/Output/WER_refword


#Parameters for step5.1
inDual=$ExpID/Output/WER_dual
inMaster=$ExpID/Output/WER_master
inHotWord=$ExpID/Output/WER_hotword

outWERDualResult=$ExpID/Output/WER_result
outWERMasterResult=$ExpID/Output/WER_result
outWERHotWordResult=$ExpID/Output/WER_result
opWER=$ExpID/Output/WER_result.txt


python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inDual --opFileName $outWERDualResult --remarkStr "DualDecoder Result" > $opWER
python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inMaster --opFileName $outWERMasterResult --remarkStr "MasterDecoder Result" >> $opWER
python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inHotWord --opFileName $outWERHotWordResult --remarkStr "HotWordDecoder Result" >> $opWER



  

