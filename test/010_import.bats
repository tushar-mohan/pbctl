#!/usr/bin/env bats


@test "data import followed by delete" {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pfb --import "$datafile"
    [ $status -eq 0 ]
    job_id=$(echo ${output}|grep -w \"id\"|awk '{print $3}'|sed 's/,//')
    run pfb -D $job_id
    [ $status -eq 0 ]
}
