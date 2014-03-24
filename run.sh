#!/bin/bash

# Enable chatty mode if --debug.
if [ $3 ] && [ $3 == "--debug" ]
then
  #debug_cflags='--alsologtostderr --log_network'
  #debug_pyflags='--verbose'
  debug_cflags='--alsologtostderr'
fi

# make a logs directory
mkdir -p logs

# Start the launcher and sleep a moment to make sure it is listening.
./scripts/nodemanager_local.py $debug_pyflags 8668 --log_dir=logs $debug_cflags $configflags &

nodemanager_pid=$!
sleep .5

# Start the master and sleep a moment to make sure it is listening.
./master.exe --max_workers $1 --address=$(hostname):15418 --log_dir=logs $debug_cflags $(hostname):8668 &
master_pid=$!
sleep .5

./scripts/workgen.py $debug_pyflags $(hostname):15418 $2

success=$?

# Tell the master to die by sending it the tagged message (shutdown, 0).
#python -c 'import comm; import sys; sys.stdout.write(comm.TaggedMessage(comm.SHUTDOWN, 0).to_bytes())' | nc $(hostname) 15418
printf "\x06\x00\x00\x00\x00\x00\x00\x00" | nc $(hostname) 15418
trap "kill -9 $master_pid; kill -9 $nodemanager_pid; exit $success" SIGINT
wait $master_pid

# Kill the the launcher to clean up.
kill -9 $nodemanager_pid

# Return successfully iff the all work was accepted correctly.
exit $success
