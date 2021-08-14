# various steps

# step1


source ./pathExpt.sh
# get the experiment parameters


python3 ./local/createExp.py --setup $ExpJSON
# lets create the directory
# you should change expX to exp(some number)
# see ./exp/expX.json for example


#  step2
#  you have to build your own data for L and G of the hotword decoder
#  populate ./exp/expX/dataLG
#  here we will run1_BuildLexiconLM.sh prepared in ./exp/expX as an example
source run_Step2_BuildLexiconLM.sh
# we would have created the hotword lexicon txt and the unigram arpa for the hotword decoder
#

# step3
# Build the HCLG -> put it in ./exp/dataLG
# and run the hotword decoder
# we expect 2 ctm files:  hotword.ctm and master.ctm
# the decoder should dump the data into the ./exp/expX/Output
# I am waiting for Yachao to integrate this
# run_Step3_buildAndRunHotWordDecoder.sh
# Lets hack this first:
#cp ./exp/TMP_OP_STEP3/yachao_mismatch/* ./exp/ExpX/Output/
#cp ./exp/TMP_OP_STEP3/yachao_best/* ./exp/ExpX/Output/
cp ./exp/TMP_OP_STEP3/yachao_old/* ./exp/ExpX/Output/



# step 4
# lets combine the hotword.ctm and master.ctm to form the dual.ctm
#
run_Step4_combineDual.sh
# This will generate the dual.ctm
# and also prepare the files for WER scoring
# the master, hotword and dual will produce 3 files each
#	hotwordONLY, word+hotWord and wordONLY
#	so we can score these 3 separately


# step5
# Generate the WER for the files
run_Step5_wer_scoring.sh








