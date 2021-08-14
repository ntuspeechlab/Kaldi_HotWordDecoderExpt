#
# This is the pathExpt of every experiment
## Global variables

# remember to set your Kaldi path
source pathLapTop.sh
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
	
#============================================
# To run an experiment, 
#	1) create the following directories
#	2) generate expInfo.json
#  ever experiment we conduct will be dumped into ExpDir

export ExpJSON=./expInfo.json   # This contains a string to remember the setting of the expt
export ExpDir=./exp/ExpX        # to build the lex and arupa
export ExpLGDir=$ExpDir/dataLG	 # where we will put the arpa and lex to build the decoder
export ExpInput=$ExpDir/Input
export ExpOutput=$ExpDir/Output

echo "okExportExp"