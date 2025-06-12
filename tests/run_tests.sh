#!/bin/bash

oversubscribe=""
while getopts ":o" flag; do
    case $flag in
        o)
            oversubscribe="--oversubscribe"
            ;;
    esac
done

function create_input() {
    pytest -m "create" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function remove_input() {
    pytest -m "remove" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function run_test() {
    eval $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

test="test_fms.py"
create_input $test
run_test "python -m pytest -m parallel $test"
remove_input $test

test="py_mpp/test_define_domains.py"
create_input $test
run_test "mpirun -n 8 $oversubscribe python -m pytest -m 'parallel' $test"
remove_input $test

test="tests/py_mpp/test_define_cubic_mosaic.py"
create_input $testAdd commentMore actions
run_test "mpirun -n 30 $oversubscribe python -m pytest -m 'parallel' $test"
remove_input $test

test="py_mpp/test_getset_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe python -m pytest -m 'parallel' py_mpp/test_getset_domains.py"
remove_input $test

test="py_mpp/test_update_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe python -m pytest -m 'parallel' py_mpp/test_update_domains.py"
remove_input $test

test="py_mpp/test_vector_update_domains.py"
create_input $test
run_test "mpirun -n 2 $oversubscribe python -m pytest -m 'parallel' py_mpp/test_vector_update_domains.py"
remove_input $test

run_test "python -m pytest py_horiz_interp"

run_test "python -m pytest py_data_override/test_generate_files.py"
run_test "mpirun -n 6 $oversubscribe python -m pytest -m 'parallel' py_data_override/test_data_override.py"
remove_input "py_data_override/test_data_override.py"

run_test "python -m pytest py_diag_manager/test_generate_files.py"
run_test "mpirun -n 1 python -m pytest py_diag_manager/test_diag_manager.py"

run_test "python -m pytest utils/test_constants.py"

run_test "python -m pytest test_init.py"

rm -rf INPUT *logfile* *warnfile*
