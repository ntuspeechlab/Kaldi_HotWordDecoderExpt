#!/bin/bash

# we assume that kaldi path has been setup!
#source pathDesktop.sh
#source pathLaptop.sh

# Source this file, and then check ./DataLG
# The output should be self-explanatory
#
# Step 1.1: # Step 1.1, creating the hotword decoder's lexicon AND language model count
# Input IS ONLY the required hotwordRawList.txt


in_hotwordRawlist=$ExpDir/Input/hotwordRawList.txt 
in_MasterUnigramCount=$ExpDir/Input/unigram.count
op_hotWordLex=$ExpDir/dataLG/hotwordDecoderLex.txt
op_hotWordUnigram=$ExpDir/dataLG/hotwordDecoderUnigram.txt
op_hotWordUnigramArpa=$ExpDir/dataLG/hotwordDecoderUnigram.arpa


python3 ./local/run_createhotWordLexiconUnigram.py  --whichMethod=$methodID\
                                            --hotwordRawList  $in_hotwordRawlist  \
                                            --unigram_countFile $in_MasterUnigramCount \
                                            --topNunigram  $threshold_N_forMasterWord\
                                            --fixHotWord_position $threshold_N_forCountHotWord\
                                            --opHotDecoderLexicon $op_hotWordLex   \
                                            --opHotDecoderUnigram $op_hotWordUnigram 
                                            
# In the above example, we are taking 
# we will take the top 5000 (in this example =threshold_N_forMasterWord) words.
# we will use the top 300 (in this example =threshold_N_forCountHotWord) count 
# to initialize for ALL hotwords count into op Unigram containing master top N words and hotwords


#Step 1.3, creating the arpa file
ngram-count -read $op_hotWordUnigram   -lm $op_hotWordUnigramArpa

#
# you should NOW build your hotword decoder and score
# if you are successful, you will get 2 files,
# the hotword.ctm and the master.ctm
#
# We should NOW call Peng Yizhou's script to create a hotword decoder from our
#   ./exp/expX/dataLG/hotwordDecoderUnigram.arpa
#   ./exp/expX/dataLG/hotwordDecoderLex.txt



