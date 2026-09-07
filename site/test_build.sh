#!/usr/bin/env bash
set -e
if test -f site/dist/index.html; then
  echo "PASS: site/dist/index.html exists"
  exit 0
else
  echo "FAIL: site/dist/index.html missing"
  exit 1
fi
