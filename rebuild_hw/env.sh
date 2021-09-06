#!/usr/bin/env bash

# This is the main environment variable file 
# set the values here before 
# 1) building Hotword  or 2) decoding+scoring



EXPID=$1

# Main directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# baseline system
BASE_DIR=$SCRIPT_DIR/baseline
ORIG_DICT=$BASE_DIR/orig_dict
TDNNF=$BASE_DIR/tdnnf
MASTER_GRAPH=$TDNNF/graph_base_en
KALDI_PATH=$SCRIPT_DIR/path.sh

# exp directory
EXP_DIR=$SCRIPT_DIR/exp/$EXPID
HW_DICT=$EXP_DIR/dict
HW_LANG=$EXP_DIR/lang
HW_LM=$EXP_DIR/lm
HW_GRAPH=$EXP_DIR/graph
HW_RESULT=$EXP_DIR/output
HW_DATA=$EXP_DIR/data
HW_VERBOSE=$EXP_DIR/verbose.txt
HW_LOG=$EXP_DIR/log.txt

# testset directory
#TESTDATA_DIR=$SCRIPT_DIR/data/imda-part2
#MODEL_ID=$(basename $TDNNF)
#TEST_ID=$(basename $TESTDATA_DIR)
#DECODE_ID="$MODEL_ID-$TEST_ID"
#DECODE_DIR=$TDNNF/decode-${EXPID}-${DECODE_ID}-HW

IVECTOR_EXTRACTOR=$SCRIPT_DIR/ivector-extractor


# decoding and scoring parameters
CMD="run.pl"
NUM_JOB=1
SELECTED_LM_WEIGHT=17
SELECTED_WIP=0.0
EXTRACT_FEATURE=true
SCORE_MODEL=1

