#!/bin/bash -ex

oversubscribe=""
while getopts ":o" flag; do
    case $flag in
        o)
            oversubscribe="--oversubscribe"
            ;;
    esac
done

function create_input() {
    pytest -svm "create" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function remove_input() {
    pytest -svm "remove" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function run_test() {
    eval $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

test="test_fms.py"
create_input $test
run_test "python -m pytest -svm parallel $test"
remove_input $test

test="py_mpp/test_define_domains.py"
create_input $test
run_test "mpirun -n 8 $oversubscribe python -m pytest -svm 'parallel' $test"
remove_input $test

test="py_mpp/test_define_cubic_mosaic.py"
create_input $test
run_test "mpirun -n 30 $oversubscribe python -m pytest -svm 'parallel' $test"
remove_input $test

test="py_mpp/test_getset_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe python -m pytest -svm 'parallel' py_mpp/test_getset_domains.py"
remove_input $test

test="py_mpp/test_update_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe python -m pytest -svm 'parallel' py_mpp/test_update_domains.py"
remove_input $test

test="py_mpp/test_vector_update_domains.py"
create_input $test
run_test "mpirun -n 2 $oversubscribe python -m pytest -svm 'parallel' py_mpp/test_vector_update_domains.py"
remove_input $test

test="py_horiz_interp/test_horiz_interp.py"
create_input $test
run_test "python -m pytest -sv -k test_create_xgrid $test"
run_test "python -svm pytest -sv -k test_horiz_interp_conservative $test"
run_test "mpirun -n 4 $oversubscribe python -m pytest -sv -k test_horiz_interp_conservative $test"
run_test "python -m pytest -s -k test_horiz_interp_bilinear $test"
run_test "mpirun -n 2 $oversubscribe python -m pytest -sv -k test_horiz_interp_bilinear $test"
remove_input $test

#test temporarily turned off on Github Action
if [ ! -n $oversubscribe ] ; then
    run_test "python -m pytest py_data_override/test_generate_files.py"
    run_test "mpirun -n 6 $oversubscribe python -m pytest -svm 'parallel' py_data_override/test_data_override.py"
    remove_input "py_data_override/test_data_override.py"
fi

run_test "python -m pytest py_diag_manager/test_generate_files.py"
run_test "mpirun -n 1 python -svm pytest py_diag_manager/test_diag_manager.py"

run_test "python -svm pytest utils/test_constants.py"

run_test "python -svm pytest test_init.py"

rm -rf INPUT *logfile* *warnfile*
