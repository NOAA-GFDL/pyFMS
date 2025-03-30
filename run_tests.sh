#!/bin/bash

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
    if [ $? -ne 0 ] ; then exit 1 ; fi                                                                                                 }

run_test "pytest tests/test_build.py"

test="tests/test_pyfms.py"
create_input $test
run_test "pytest -m parallel $test"
remove_input $test

test="tests/py_mpp/test_define_domains.py"
create_input $test
run_test "mpirun -n 8 python -m pytest -m 'parallel' $test"
remove_input $test

test="tests/py_mpp/test_getset_domains.py"
create_input $test
run_test "mpirun -n 4 python -m pytest -m 'parallel' tests/py_mpp/test_getset_domains.py"
remove_input $test

test="tests/py_mpp/test_update_domains.py"
create_input $test
run_test "mpirun -n 4 python -m pytest -m 'parallel' tests/py_mpp/test_update_domains.py"

run_test "pytest tests/py_horiz_interp"

run_test "pytest tests/py_data_override/test_generate_files.py"
run_test "mpirun -n 6 python -m pytest -m 'parallel' tests/py_data_override/test_data_override.py"
remove_input "tests/py_data_override/test_data_override.py"

run_test "pytest tests/py_diag_manager/test_generate_files.py"
run_test "mpirun -n 1 python -m pytest tests/py_diag_manager/test_diag_manager.py"
remove_input "tests/py_diag_manager/test_diag_manager.py

rm -rf INPUT *logfile* *warnfile*
