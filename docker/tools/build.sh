#!/bin/bash
set -e

do_pull=0
do_build=0
do_push=0

while (($#))
do
    case $1 in
	--pull) do_pull=1; shift;;
	--build) do_build=1; shift;;
	--push) do_push=1; shift;;
	*) echo "usage: build.sh [--pull] [--build] [--push]" ; false 
    esac
done


pushd ../modules > /dev/null
module_names=(*)
popd  > /dev/null

if [ "$do_pull" -eq 1 ]
then
    for i in "${module_names[@]}"
    do
        echo ""
        echo "*** $i... ***"
        echo ""
        docker pull inferlink/ta1_$i
    done
fi

if [ "$do_build" -eq 1 ]
then
    for i in "${module_names[@]}"
    do
        echo ""
        echo "*** $i... ***"
        echo ""
        pushd ../modules/$i > /dev/null
        ./build.sh
        popd > /dev/null
    done
fi

if [ "$do_push" -eq 1 ]
then
    for i in "${module_names[@]}"
    do
        echo ""
        echo "*** $i... ***"
        echo ""
        docker push inferlink/ta_$i
    done
fi
