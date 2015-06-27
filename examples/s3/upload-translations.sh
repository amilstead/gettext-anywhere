#!/bin/bash

# pass in a bucket name as an argument to this script

aws s3 sync locale s3://$1/locale
