@test "perfbrowser driver" {
  pbctl -h
}

@test "dependencies" {
  which bash
  which curl
  which wc
}
