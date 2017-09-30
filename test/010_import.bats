#!/usr/bin/env bats


@test "data import followed by delete" {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pfb import "$datafile"
    [ $status -eq 0 ]
    [[ $output =~ id...([0-9]+), ]]
    job_id=${BASH_REMATCH[1]}
    run pfb del $job_id
    [ $status -eq 0 ]
}
