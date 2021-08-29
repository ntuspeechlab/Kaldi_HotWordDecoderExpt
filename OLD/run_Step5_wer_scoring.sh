#!/bin/bash
# After you have run this file, and then check ./TestDataOp
# The output should be self-explanatory
#

# This script scores the WER of the master, hotword, and dual decoder's output
#

# if the reference ctm in the 3 format does not exist, we must create them
inRefWord=$ExpOutput/WER_refword



#Parameters for step5.1
inDual=$ExpOutput/WER_dual
inMaster=$ExpOutput/WER_master
inHotWord=$ExpOutput/WER_hotword

outWERDualResult=$ExpOutput/WER_result
outWERMasterResult=$ExpOutput/WER_result
outWERHotWordResult=$ExpOutput/WER_result
opWER=$ExpOutput/WER_result.txt

python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inDual --opFileName $outWERDualResult --remarkStr "DualDecoder Result" > $opWER
python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inMaster --opFileName $outWERMasterResult --remarkStr "MasterDecoder Result" >> $opWER
python3.7 ./local/run_scoreWER.py --ref $inRefWord --hyp $inHotWord --opFileName $outWERHotWordResult --remarkStr "HotWordDecoder Result" >> $opWER

echo "Step5: saving results in:"
echo $opWER

  

