#! /usr/bin/env bash

function test_abcli_host() {
    abcli_assert \
        $(abcli_host get name) \
        - non-empty
}
