#!/bin/bash

#####################
# Zin MICL@NTU  
# Aug 27, 2021
# for decoding and scoring
#####################



echo 
echo "$0 $@"
echo

# inputs
testdata_dir=$1
expId=$2
env_file=$3





set -e

. $env_file $expId
. $KALDI_PATH
. parse_options.sh || { echo "parse_options.sh expected ..." && exit 1; }

if [ $# -ne 2 ]; then
  echo -e "\nusage: $0 [options] <experiment-id> <env-file>\n"
 usage=$(cat<<EOF
EOF

  Example:  $0  exp123 env.sh
    
EOF
)
  echo "$usage" && exit 1
 fi


source_data=$TESTDATA_DIR/kaldi-formatted
data=$TESTDATA_DIR/mfcc-hires
log=$TESTDATA_DIR/feats/log
feat=$TESTDATA_DIR/feats/data
ivector_dev=$TESTDATA_DIR/ivector

model_ID=$(basename $TDNNF)
test_ID=$(basename $testdata_dir)
decode_ID="$model_ID-$test_ID"
DECODE_DIR=$TDNNF/decode-${expId}-${decode_ID}-HW

# Extract Features
if $EXTRACT_FEATURE; then
	utils/data/copy_data_dir.sh $source_data $data || exit 1;
	steps/make_mfcc.sh --mfcc-config ./conf/mfcc_hires_8k.conf --cmd "$CMD" \
            --nj $NUM_JOB $data $log $feat || exit 1
	steps/compute_cmvn_stats.sh $data $log $feat || exit 1
	utils/fix_data_dir.sh $data || exit 1
	echo -e "\n ##LOG(STEP05) extract mfcc hiresolution features @$data done @`date`"

	steps/nnet2/extract_ivectors_online.sh --cmd "$CMD" \
            --nj $NUM_JOB $data $IVECTOR_EXTRACTOR \
            $ivector_dev || exit 1;
	echo -e "\n ##LOG(STEP03) extract ivector-online @$ivector_dev done @`date`"
fi

## Decode and score
steps/nnet3/decode.sh --nj $NUM_JOB --cmd "$CMD" --acwt 1.0 --post-decode-acwt 10.0 --online-ivector-dir \
$ivector_dev $HW_GRAPH $data $DECODE_DIR || exit 1
        
# log
echo $TDNNF "\n" $HW_GRAPH "\n" $TESTDATA_DIR "\n" >> $DECODE_DIR/version.txt

# extract ctm
steps/get_ctm_fast.sh $data $HW_GRAPH $DECODE_DIR $DECODE_DIR/ctm

# export results
mkdir -p $HW_RESULT
cp -r $DECODE_DIR $EXP_DIR
cp -r $DECODE_DIR/ctm $HW_RESULT/hotword.ctm
cp -r $DECODE_DIR/scoring_kaldi/{penalty_0.0,penalty_0.5,penalty_1.0} $HW_RESULT
