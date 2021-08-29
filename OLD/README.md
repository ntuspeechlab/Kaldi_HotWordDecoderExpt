#Filename: readme.md
#Author: Chng Eng SIong
#~/HardWordDecoderExp

#This directory contains HOW we are going to do the hotword decoder experiment


Requirements:
1) kaldi to be setup
2) python3 and some libraries: words (nltk), pandas


Step1) modify pathExpt.sh
a) update to use correct setup:
   source pathDesktop.sh  or source pathLaptop.sh or your own
b) setup the output directory and expt ID
	 methodID=4  # this will affect the opDir, and Step2 (Build Lexicon)
     ExpID=./exp/Exp$methodID  #initialise this if its gone
c) setup the testfile's ref file:  inRefWord=$ExpID/Output/WER_refword


Directory description:
1) ~/HotWordDecoderExp/data
	a) MasterDecoder (the files needed to create the Master decoder
	b) The testdata (wavefiles, etc) we going to test


2) ~/HotWordDecoderExp/utils
	a) the scripts (python,bash) to support the experiments


3) ~/HotWordDecoderExp/exp
	a) exp output
	



Steps:
1) python3 local/createExp.py --setup exp/exp3.json
	// create the directory using exp3.json information

	