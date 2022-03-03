#!/bin/bash

PRIVATE_KEY_PATH=$(find ~/Documents/**/data_intensive_and_cloud_computing -name 'private_key.pem' -print -quit)
echo 'Enter public IPv4 DNS:' && read ADDR && ssh -i $PRIVATE_KEY_PATH ec2-user@$ADDR
