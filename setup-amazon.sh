#!/usr/bin/env csh

mkdir -p $HOME/local/lib/python2.6/site-packages
setenv PYTHONPATH $HOME/local/lib/python2.6/site-packages:/afs/cs/academic/class/15418-s14/assignments
./easy_install --prefix=$HOME/local poster

echo $USER > scoreboard_token

echo "----------------------------------------------------------------"
echo "Please add the following line to your ~/.cshrc"
echo "setenv PYTHONPATH $HOME/local/lib/python2.6/site-packages:/afs/cs/academic/class/15418-s14/assignments"
