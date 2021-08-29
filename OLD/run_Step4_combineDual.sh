#!/bin/bash

# After you have run this file, and then check ./TestDataOp
# The output should be self-explanatory
#

# This script combines the output of master and hotword decoder
# Step 4.1)  combine hotword and master decoder ctm file.
# The following command generates the dual ctm file from master and hotword ctm
#

#Parameters for step4.1
in_hotwordRawlist=$ExpDir/Input/hotwordRawList.txt 
in_masterCTM=$ExpDir/Output/master.ctm
in_hotwordCTM=$ExpDir/Output/hotword.ctm
threshold_collar_rate=0.25
out_dualCTM=$ExpDir/Output/dual.ctm

#step4.1 : combinining the CTM files to form the dual ctm output
python3.7 ./local/run_combineCTM.py   --hotwordRawList $in_hotwordRawlist \
                            --master_ctm  $in_masterCTM \
                            --hotword_ctm $in_hotwordCTM \
                            --collar_rate $threshold_collar_rate \
                            --dual_ctm    $out_dualCTM 
                            




outRefWord=$ExpDir/Output/WER_refword
outMaster=$ExpDir/Output/WER_master
outHotWord=$ExpDir/Output/WER_hotword
outDual=$ExpDir/Output/WER_dual



# We will generate the files for scoring
# this is the sentence level CTM withput time information, 2 fields, uttID and uttString
# 3 types of uttString
#  1) Reference         -> this is a text version of ctm file, left most field == file ID followed by text string
#  2) HotWordONLY       -> all none hotword removed, e.g __Orchard_Road
#  3) WordandHotWord    -> words mixed with hotword labels i visited __Orchard_Road today   (hotword labels == __hotword_label)
#  4) WordONLY       -> words only, e.g  i visited Orchard Road today


#step4.2 : generating the WER for the CTM files
python3.7 ./local/run_convertCTM_toWERscoringText.py  --ctm $in_refText     --hotwordRawList $in_hotwordRawlist  --opFileName $outRefWord
python3.7 ./local/run_convertCTM_toWERscoringText.py  --ctm $in_masterCTM   --hotwordRawList $in_hotwordRawlist   --opFileName $outMaster
python3.7 ./local/run_convertCTM_toWERscoringText.py  --ctm $in_hotwordCTM  --hotwordRawList $in_hotwordRawlist   --opFileName $outHotWord
python3.7 ./local/run_convertCTM_toWERscoringText.py  --ctm $out_dualCTM    --hotwordRawList $in_hotwordRawlist   --opFileName $outDual

