#!/bin/sh

sudo apt-get install -y git-core
git config --global user.name "Hongxia Zhong"
git config --global user.email hongxia.zhong@gmail.com

echo -e "\n" | ssh-keygen -t rsa -N "" -C "hongxia.zhong@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub