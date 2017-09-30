#!/usr/bin/env bats


setup() {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pfb import "$datafile"
    [ $status -eq 0 ]
    [[ $output =~ id...([0-9]+), ]]
    job_id=${BASH_REMATCH[1]}
}

@test "jobs listing" {
    out=$(pfb list | grep '"id": ')
    [[ "$out" =~ $job_id ]]
}

@test "job detail" {
    out=$(pfb show $job_id | grep '"jobId": ')
    [[ "$out" =~ $job_id ]]
}

teardown() {
    run pfb del $job_id
}
