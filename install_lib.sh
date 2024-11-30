#!/bin/bash


echo "Installing jieba..."
pip3 install jieba -i https://mirrors.aliyun.com/pypi/simple/
if [ $? -ne 0 ]; then
    echo "Failed to install jieba, exiting."
    exit 1
fi

echo "Installing pypinyin..."
pip3 install pypinyin -i https://mirrors.aliyun.com/pypi/simple/
if [ $? -ne 0 ]; then
    echo "Failed to install pypinyin, exiting."
    exit 1
fi



echo "Installing fuzzywuzzy..."
pip3 install fuzzywuzzy -i https://mirrors.cloud.tencent.com/pypi/simple
if [ $? -ne 0 ]; then
    echo "Failed to install fuzzywuzzy, exiting."
    exit 1
fi


echo "Installing python-Levenshtein..."
pip3 install python-Levenshtein -i https://mirrors.cloud.tencent.com/pypi/simple
if [ $? -ne 0 ]; then
    echo "Failed to install python-Levenshtein, exiting."
    exit 1
fi


echo "Installing qq-botpy..."
pip3 install qq-botpy -i https://mirrors.cloud.tencent.com/pypi/simple
if [ $? -ne 0 ]; then
    echo "Failed to install qq-botpy, exiting."
    exit 1
fi

echo "Installing ordered-set..."
pip3 install ordered-set -i https://mirrors.cloud.tencent.com/pypi/simple
if [ $? -ne 0 ]; then
    echo "Failed to install ordered-set, exiting."
    exit 1
fi

echo "ordered-set installed successfully."

echo "All packages installed successfully!"