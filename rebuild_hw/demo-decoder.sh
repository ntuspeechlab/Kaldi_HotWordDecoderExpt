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
audiodata_dir=$1
expId=$2
env_file=$3
exp_output_dir=$4

set -e

. $env_file $expId
. $KALDI_PATH
. parse_options.sh || { echo "parse_options.sh expected ..." && exit 1; }

if [ $# -ne 4 ]; then
  echo -e "\nusage: $0 [options] <experiment-id> <env-file>\n"
 usage=$(cat<<EOF
EOF

  Example:  $0  exp123 env.sh
    
EOF
)
  echo "$usage" && exit 1
 fi

# 1. Clean and Prepare Kaldi data
rm -rf $HW_DATA
mkdir -p $HW_DATA $HW_DATA/wav $HW_DATA/kaldi-formatted
cp $audiodata_dir/*.wav $HW_DATA/wav
counter=1

# create wav.scp, utt2spk and spk2utt
for wavf in $HW_DATA/wav/*.wav; do 
	echo "utt-$counter /usr/bin/sox -t wav $wavf -t wav -c 1 -b 16 -t wav - rate 8000 |" >> $HW_DATA/kaldi-formatted/wav.scp
	echo "utt-$counter utt-$counter" >> $HW_DATA/kaldi-formatted/utt2spk
	echo "utt-$counter utt-$counter" >> $HW_DATA/kaldi-formatted/spk2utt
	counter=$((counter+1))
done

# Paths for features extraction
source_data=$HW_DATA/kaldi-formatted
data=$HW_DATA/mfcc-hires
log=$HW_DATA/feats/log
feat=$HW_DATA/feats/data
ivector_dev=$HW_DATA/ivector

# 2. Extract Features
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

## 3. Decode and score

# Decoding and scoring output
decode_ID=$(basename $TDNNF)
DECODE_DIR_HW=$TDNNF/decode-${expId}-${decode_ID}-HW
DECODE_DIR_MST=$TDNNF/decode-${expId}-${decode_ID}-MST


# Decode Master
steps/nnet3/decode.sh --nj $NUM_JOB --cmd "$CMD" --acwt 1.0 --post-decode-acwt 10.0 --online-ivector-dir \
$ivector_dev $MASTER_GRAPH $data $DECODE_DIR_MST || exit 1

# Decode Hotword
steps/nnet3/decode.sh --nj $NUM_JOB --cmd "$CMD" --acwt 1.0 --post-decode-acwt 10.0 --online-ivector-dir \
$ivector_dev $HW_GRAPH $data $DECODE_DIR_HW || exit 1
        
# log
echo $TDNNF "\n" $HW_GRAPH "\n" $TESTDATA_DIR "\n" >> $DECODE_DIR_HW/version.txt

# extract ctm
steps/get_ctm_fast.sh $data $MASTER_GRAPH $DECODE_DIR_MST $DECODE_DIR_MST/ctm
steps/get_ctm_fast.sh $data $HW_GRAPH $DECODE_DIR_HW $DECODE_DIR_HW/ctm

# export results
mkdir -p $HW_RESULT

cp -r $DECODE_DIR_MST $EXP_DIR
cp -r $DECODE_DIR_MST/ctm/ctm $HW_RESULT/master.ctm

# Hotword
cp -r $DECODE_DIR_HW $EXP_DIR
cp -r $DECODE_DIR_HW/ctm/ctm $HW_RESULT/hotword.ctm

cp $HW_RESULT/master.ctm $exp_output_dir
cp $HW_RESULT/hotword.ctm $exp_output_dir
