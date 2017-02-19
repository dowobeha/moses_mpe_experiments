#!/bin/bash

required_files="moses.ini static.pt static.lm client.py summary.txt log"

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


message="$(< ${dir}/summary.txt)"

echo "${message}"
rm -f ${dir}/*~

for file in ${required_files}; do
    git add ${dir}/${file}
done

git commit -m "${message}"

