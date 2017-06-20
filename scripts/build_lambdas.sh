#!/bin/bash 

#build attach hosted zone
cd lambda/cats/
pip install -r requirements.txt -t .
mkdir -p ../../builds
zip -r ../../builds/cats.zip ./*
