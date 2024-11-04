#!/bin/bash

# echo "Hello World"

# if [ 10 -eq 10 ]; then echo "hi"; fi
# if [ 5 -eq 10 ]; then echo "hi"; else echo "bye"; fi
# if [ 5 -eq 10 ] && [ 10 -ne 10 ]; then echo "hi"; fi
# if [ 5 -eq 10 ] || [ 10 -ne 10 ]; then echo "hi"; fi
# if [ 5 -eq 10 ]; then echo "hi"; fi
# if [ 5 -eq 10 ]; then echo "hi"; elif [ 5 -eq 10 ]; then echo "okay"; fi
# if [ 5 -eq 10 ]; then echo "hi"; elif [ 5 -eq 10 ]; then echo "okay"; fi
# if [5 -eq 10]; then echo "should not parse"; fi
# if [ 5 -eq 10 ]; then echo "should parse"; fi
# foo=8
# bar = 10
# echo "foo"
# echo bar
# [ 5 -eq 10 ]
# if [ 5 -ne 10 ]; then echo "baz"; fi
# if [ 5 -eq 10 ]; then echo "foo"; elif [ 5 -ne 10 ]; then echo "baz"; fi
# if [ 5 -eq 10 ]; then echo "foo"; else echo "baz"; fi
# if [ 5 -eq 10 ]; then echo "foo"; elif [ 5 -eq 2 ]; then echo "bar"; else echo "baz"; fi
# [[ 10 -eq 10 ]] && [ 5 -eq 5 ]
# echo "hi" && echo "hey"
foo=8
bar=10
if [[ 10 -eq 10 ]]; then echo "foo" && echo "bar" || echo "baz"; fi
if [ 5 -eq 10 ]; then echo "foo"; else echo "bar"; fi
if [ 5 -eq 10 ]; then echo "foo"; elif [ 5 -eq 10 ]; then echo "bar"; else echo "baz"; fi
while [ 10 -eq 10 ] && [ 5 -ne 10 ]; do echo "foo"; done
b=$((5+3))
echo $b
echo $bar
echo $foo
echofoo
