#!/usr/bin/env bats


@test "can we login?" {
    pb login --verify
}
