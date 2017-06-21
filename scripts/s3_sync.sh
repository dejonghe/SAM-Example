#!/bin/bash 

# Set variables
function usage()
{
  echo "ERROR: Incorrect arguments provided."
  echo "Usage: $0 {args}"
  echo "Where valid args are: "
  echo "  -p <profile> (REQUIRED) -- Profile to use for AWS commands"
  echo "  -b <bucket> (REQUIRED) -- bucket name to sync to"
  exit 1
}

# Parse args
if [[ "$#" -lt 2 ]] ; then
  echo 'parse error'
  usage
fi
PROFILE=default
while getopts "p:r:b:" opt; do
  case $opt in
    p)
      PROFILE=$OPTARG
    ;;
    b)
      BUCKET=$OPTARG
    ;;
    \?)
      echo "Invalid option: -$OPTARG"
      usage
    ;;
  esac
done

REGION=$(aws configure list --profile ${PROFILE} | grep region | awk '{print $2}')
ACCOUNT_ID=$(aws ec2 describe-security-groups --query 'SecurityGroups[0].OwnerId' --output text)
CWD=$(echo $PWD | rev | cut -d'/' -f1 | rev)
if [ $CWD != "SAM-Example" ]
then
  echo "These tools are expecting to be ran from the base of the SAM-Example repo."
  exit 1
fi
sed -i "s/<region>/${REGION}/g" docs/awscats.yml
sed -i "s/<account_id>/${ACCOUNT_ID}/g" docs/awscats.yml
aws s3 sync ./builds/ s3://${BUCKET}/builds/ --profile ${PROFILE} --exclude *.git/* --exclude *.swp
aws s3 sync ./docs/ s3://${BUCKET}/docs/ --profile ${PROFILE} --exclude *.git/* --exclude *.swp 
