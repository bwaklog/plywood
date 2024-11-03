#!/bin/bash

echo "Hello World"

# if [ 10 -eq 10 ]; then echo "hi"; fi 
# if [ 5 -eq 10 ]; then echo "hi"; else echo "bye"; fi 
if [ 5 -eq 10 ] && [ 10 -ne 10 ]; then echo "hi"; fi
if [ 5 -eq 10 ] || [ 10 -ne 10 ]; then echo "hi"; fi
if [ 5 -eq 10 ]; then echo "hi"; fi
if [ 5 -eq 10 ]; then echo "hi"; elif [ 5 -eq 10 ]; then echo "okay"; fi
if [ 5 -eq 10 ]; then echo "hi"; elif [ 5 -eq 10 ]; then echo "okay"; fi
if [ 5 -eq 10 ]; then echo "hi"; elif [ 5 -eq 10 ]; then echo "okay"; else echo "what"; fi