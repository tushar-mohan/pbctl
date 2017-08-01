#!/usr/bin/env bats


@test "can we login?" {
    run pb login --batch
    [ $status -eq 0 ]
}
