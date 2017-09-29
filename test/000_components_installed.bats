@test "perfbrowser driver" {
  pfb -h
}

@test "dependencies" {
  which bash
  which curl
  which wc
  which col
}
