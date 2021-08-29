# This is the pathExpt of every experiment
## Global variables

# remember to set your Kaldi path to the appropriate one
# check for !!! to find where needs your attention
#source pathLapTop.sh 	#!!!
source pathDesktop.sh  #!!!

# You must change run_Step2_BuildLexiconLM.sh to use this methodID
methodID=5  #!!!
export ExpDescription="method 5 chosen - from YaChao lexicon and count"
# this will affect the opDir, and Step2 (Build Lexicon)



PWD=$(pwd)                          # we should be in this directory to run
export PATH=$PATH:$PWD/local/		# we need the scripts here to run the expt

#===========================
# To run the experiment, you must know where thlse master directory is
# and the master directoy files needed
#
export DirMaster=$PWD/data/MasterDecoder
export DirTestData=$PWD/data/TestData
export IpHotWordList=$PWD/exp/hotwordRawList.txt

	# the path to where the Master Decoder is
	# the Master decoder directory contains the unigram.count of the master decoder
	# and the HCLG of the master decoder
	# and files like H and C  and other files required to build hotword decoder
	# and the directory of the test wavefiles

#Parameter for step 4.2
#To test, you must provide the appropriate test file ground truth
export in_refText=$DirTestData/groundTruth_WordOnly.txt   #!!!
# the filename of the reference file MUST end with .txt

	
#============================================
# To run an experiment, 
#	1) create the following directories
#	2) generate expInfo.json
#  ever experiment we conduct will be dumped into ExpDir


export ExpJSON=./expInfo.json   # This contains a string to remember the setting of the expt
export ExpDir=./exp/Exp$methodID        # to build the lex and arpa
export ExpLGDir=$ExpDir/dataLG	 # where we will put the arpa and lex to build the decoder
export ExpInput=$ExpDir/Input
export ExpOutput=$ExpDir/Output

# Step 2's settings   #!!!
export threshold_N_forMasterWord=80000
export threshold_N_forCountHotWord=200

echo "okExportExp"