#!/usr/bin/env bats


@test "data import followed by delete" {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pb import "$datafile"
    [ $status -eq 0 ]
    job_id=$(echo ${output} | grep JobId | awk '{print $NF}')
    run pb rest -d $job_id
    [ $status -eq 0 ]
}
