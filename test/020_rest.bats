#!/usr/bin/env bats


setup() {
    datafile="${PB_TEST_DIR}/data/sample.papiex.csv"
    [ -f "$datafile" ]
    run pb import "$datafile"
    [ $status -eq 0 ]
    job_id=$(echo ${output} | grep JobId | awk '{print $NF}')
}

@test "jobs listing" {
    out=$(pb rest -l | grep '"id": ')
    [[ "$out" =~ $job_id ]]
}

@test "job detail" {
    out=$(pb rest -s $job_id | grep '"jobId": ')
    [[ "$out" =~ $job_id ]]
}

teardown() {
    run pb rest -d $job_id
}
