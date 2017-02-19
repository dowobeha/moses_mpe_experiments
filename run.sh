#!/bin/bash

# A script to run experimental conditions

if (( $# == 1 )); then

    if [[ ${1} =~ /$ ]] ; then
	workingDir="${1%/}"
	1>&2 echo -e "Warning:\tAssuming you meant ${workingDir} instead of ${1}"
    else
	workingDir=${1}
    fi

    for file in moses.s.ini \
                moses.d.ini \
                static.pt \
                static.lm \
        ; do
        if [ ! -e ${workingDir}/${file} ] ; then
            1>&2 echo -e "${workingDir}/${file} is required, but was not found"
            exit -1
        fi
    done

else
    1>&2 echo -e "Usage: $0 workingDir"
    exit -1
fi

static_port_number=$(./get_free_port.py)
dynamic_port_number=$(./get_free_port.py)


cd ${workingDir}

1>&2 echo -e "Condition:\t${workingDir}"
1>&2 echo
1>&2 cat  summary.txt
1>&2 echo
1>&2 echo
1>&2 echo -e "Launching:\tmosesserver -v 1 -f moses.s.ini &> log.s"

../../bin/mosesserver -v 1 -f moses.s.ini --server-port ${static_port_number} &> log.s &
static_server_pid=${!}

sleep 0.5

1>&2 echo -e "Launching:\tmosesserver -v 1 -f moses.d.ini &> log.d"

../../bin/mosesserver -v 1 -f moses.d.ini --server-port ${dynamic_port_number} &> log.d &
dynamic_server_pid=${!}

sleep 0.5

1>&2 echo -e "Launching:\tmoses client.py"
1>&2 echo
./client.py ${static_port_number} ${dynamic_port_number} <<< "<s> ich kaufe sie eine katze </s>"


1>&2 echo
kill ${static_server_pid}  && (1>&2 echo "Killed static  Moses server (port ${static_port_number}, pid ${static_server_pid})")    || (1>&2 echo "Failed to kill static  Moses server (port ${static_port_number}, pid ${static_server_pid})")
kill ${dynamic_server_pid} && (1>&2 echo "Killed dynamic Moses server (port ${dynamic_port_number}, pid ${dynamic_server_pid})")  || (1>&2 echo "Failed to kill dynamic Moses server (port ${dynamic_port_number}, pid ${dynamic_server_pid})")
