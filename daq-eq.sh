#!/bin/bash
# this declares that current user is a sudoer

sudo tee /etc/sudoers.d/$USER <<END
END

local DAQEQ_DIR = /home/rba/daqeq
local DAQEQ_TRUNK = $DAQEQ_DIR/trunk

if [[ -x $DAQEQ_TRUNK/RBA-DAQ_multisensor ]]; then
  exec $DAQEQ_TRUNK/RBA-DAQ_multisensor
else
  if [[ -e $DAQEQ_TRUNK/Makefile ]]; then
    $DAQEQ_TRUNK/make
  else
    echo RBA-DAQ_multisensor does not exist.
    exit
  fi
fi
