#!/usr/bin/env bats


setup() {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pfb -i "$datafile"
    [ $status -eq 0 ]
    job_id=$(echo ${output}|grep -w \"id\"|awk '{print $3}'|sed 's/,//')
}

@test "jobs listing" {
    out=$(pfb -l | grep '"id": ')
    [[ "$out" =~ $job_id ]]
}

@test "job detail" {
    out=$(pfb -j $job_id | grep '"jobId": ')
    [[ "$out" =~ $job_id ]]
}

teardown() {
    run pfb -D $job_id
}
