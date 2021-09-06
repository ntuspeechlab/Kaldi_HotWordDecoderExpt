#!/usr/bin/env bash

#
# Author : Chng Eng Siong

# This is the script to run, to decode the audio files the hotword decoder - DEMO
# We will assume you have (required)
#	1) a master decoder
#	2) audio files
#
#

# Step 0:
# You must initialize hwSetup.json
# and setup all fields and path, then run
# we now use python3 (v3.6 greater) -> dependencies for subprocess, and others

#step0 , you must edit and put your own hwSetup.json!
#HWSETUP_FileName='hwSetup.json'
HWSETUP_FileName=$1

python3  S3_score_hotword_decoder.py --json $HWSETUP_FileName
python3  S4_combineCTM.py --json $HWSETUP_FileName
