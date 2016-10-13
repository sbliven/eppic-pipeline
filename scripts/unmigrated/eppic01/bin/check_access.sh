#!/bin/sh
file="$1"
grep -v "^129.129." $file | grep -v  "^137.110.134" | grep "\.1\.75x75.png"
