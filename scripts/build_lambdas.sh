#!/bin/bash 

temp_path=lambda/.temp/

# Make a temp dir to build in 
mkdir $temp_path

# Copy code to the temp path
cp lambda/cats/* $temp_path

# Install requirements to temp path
cd $temp_path
pip install -r requirements.txt -t .

# Make a build directory and zip up the build package
mkdir -p ../../builds
zip -r ../../builds/cats.zip ./*

# Remove the temparary build dir
cd ../../
rm -r $temp_path
