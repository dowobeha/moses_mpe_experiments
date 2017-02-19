#!/bin/bash

required_files="client.py summary.txt"

if (( $# == 1 )); then

    if [[ ${1} =~ /$ ]] ; then
	dir="${1%/}"
	1>&2 echo -e "Warning:\tAssuming you meant ${prefix} instead of ${1}"
    else
	dir=${1}
    fi

    for file in ${required_files}; do
	if [ ! -e ${dir}/${file} ] ; then
	    1>&2 echo -e "${dir}/${file} is required, but was not found"
	    exit -1
	fi
    done
else
    1>&2 echo -e "Usage: $0 dir"
    exit -1
fi


message="$(echo Condition ${dir} && echo && cat ${dir}/summary.txt)"

echo "${message}"
rm -f ${dir}/*~

git add ${dir}

git commit -m "${message}"

