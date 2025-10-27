#!/bin/bash -ex

oversubscribe=""
while getopts ":o" flag; do
    case $flag in
        o)
            oversubscribe="--oversubscribe"
            ;;
    esac
done

flags="--tb=long -s"

function create_input() {
    pytest $flags -m "create" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function remove_input() {
    pytest $flags -m "remove" $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

function run_test() {
    eval $1
    if [ $? -ne 0 ] ; then exit 1 ; fi
}

test="test_fms.py"
create_input $test
run_test "python -m pytest $flags -m parallel $test"
remove_input $test

test="py_mpp/test_define_domains.py"
create_input $test
run_test "mpirun -n 8 $oversubscribe pytest $flags -m 'parallel' $test::test_define_domains"
run_test "mpirun -n 8 $oversubscribe pytest $flags -m 'parallel' $test::test_optional_pelist"
remove_input $test

test="py_mpp/test_define_cubic_mosaic.py"
create_input $test
run_test "mpirun -n 30 $oversubscribe pytest $flags -m 'parallel' $test"
remove_input $test

test="py_mpp/test_getset_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe pytest $flags -m 'parallel' $test"
remove_input $test

test="py_mpp/test_update_domains.py"
create_input $test
run_test "mpirun -n 4 $oversubscribe pytest $flags -m 'parallel' $test"
remove_input $test

test="py_mpp/test_vector_update_domains.py"
create_input $test
run_test "mpirun -n 2 $oversubscribe pytest $flags -m 'parallel' $test"
remove_input $test

touch -a input.nml
test="py_mpp/test_gather.py"
run_test "mpirun -n 4 $oversubscribe pytest $flags $test"
rm -f input.nml

test="py_horiz_interp/test_horiz_interp.py"
create_input $test
run_test "pytest $flags  ${test}::test_create_xgrid"
run_test "mpirun -n 4 $oversubscribe pytest $flags ${test}::test_horiz_interp_conservative"
run_test "pytest $flags ${test}::test_horiz_interp_bilinear"
run_test "mpirun -n 2 $oversubscribe pytest $flags ${test}::test_horiz_interp_bilinear"
remove_input $test

#test temporarily turned off on Github Action
# test="py_data_override/test_data_override.py"
# run_test "python -m pytest $flags py_data_override/test_generate_files.py"
# run_test "mpirun -n 6 $oversubscribe pytest $flags -m 'parallel' $test"
# remove_input $test

run_test "pytest $flags py_diag_manager/test_generate_files.py"
run_test "mpirun -n 1 pytest $flags py_diag_manager/test_diag_manager.py"

run_test "pytest $flags utils/test_constants.py"

run_test "pytest $flags test_init.py"

rm -rf INPUT *logfile* *warnfile*
