#!/bin/bash

#####################
# Zin MICL@NTU  
# Aug 27, 2021
# for buidling hotword decoder
#####################


echo 
echo "$0 $@"
echo


# inputs
hwLex=$1
hwUnigram_arpa_gz=$2
expId=$3
env_file=$4

set -e

. $env_file $expId
. $KALDI_PATH
. parse_options.sh || { echo "parse_options.sh expected ..." && exit 1; }


if [ $# -ne 4 ]; then
  echo -e "\nusage: $0 [options] <hotword-lexicon> <hotword-lm.gz> <experiment-id> <env-file>\n"
 usage=$(cat<<EOF
EOF

  Example:  $0 input/lexicon.txt input/lm.arpha.gz exp123 env.sh
    
EOF
)
  echo "$usage" && exit 1
 fi

## Step 0: Clear and Recreate Experiment Dir
if [ -d "$EXP_DIR" ]; then rm -Rf $EXP_DIR; fi
[ -d $HW_DICT ] || mkdir -p $HW_DICT
[ -d $HW_LM ] || mkdir -p $HW_LM
[ -d $HW_LANG ] || mkdir -p $HW_LANG

## Step 1: Create L.fst
cp $hwLex $HW_DICT/lexicon.txt
echo '<unk> <oov>' >> $HW_DICT/lexicon.txt
cp $ORIG_DICT/{nonsilence_phones.txt,silence_phones.txt,optional_silence.txt} $HW_DICT

# make lang
./utils/prepare_lang.sh --phone_symbol_table $TDNNF/phones.txt $HW_DICT '<unk>' $HW_LANG/tmp $HW_LANG &> $HW_VERBOSE
[ -f $HW_LANG/L.fst ] && echo "1. Creating L done" >> $HW_LOG

# Step 2: prepare lm
cp $hwUnigram_arpa_gz $HW_LM/lm1.gz
[ -f $HW_LM/lm1.gz ] && echo "2. Creating LM done" >> $HW_LOG

# Step 3: Create G.fst
./scripts/arpa2G.sh $HW_LM/lm1.gz $HW_LANG $HW_LANG &> $HW_VERBOSE
[ -f $HW_LANG/G.fst ] && echo "3. Creating G done" >> $HW_LOG

# Step 4: Create HCLG.fst graph
./utils/mkgraph.sh $HW_LANG $TDNNF $HW_GRAPH &> $HW_VERBOSE
[ -f $HW_GRAPH/HCLG.fst ] && echo "4. Creating Graph done" >> $HW_LOG
