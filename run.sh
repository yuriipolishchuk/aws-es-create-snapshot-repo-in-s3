#!/usr/bin/env bash

AWS_PROFILE=test

HOST=my-domain-yhaej3lsbrkq6d4tl25so2ey6e.us-east-1.es.amazonaws.com
REGION=us-east-1
BUCKET=es-snapshots
REPO=s3-snapshots
ROLE=arn:aws:iam::012345678910:role/es-snapshot-role


###############################################################
## for ES in private subnets
## First, you need to proxy the port over ssh bastion
# SSH_BASTION_IP=52.54.111.28
# sudo ssh -v -L 443:${HOST}:443 ${SSH_BASTION_IP}

## docker.for.mac.localhost
# LOCAL_IP=192.168.65.2

# docker run \
#   --add-host ${HOST}:${LOCAL_IP} \
#   -v ${HOME}/.aws/:/root/.aws/ \
#   -e "AWS_PROFILE=${AWS_PROFILE}" \
#   polishchuk/aws-es-create-snapshot-repo-in-s3:latest \
#   --region ${REGION} \
#   --host ${HOST} \
#   --bucket ${BUCKET} \
#   --repo ${REPO} \
#   --role ${ROLE}

# for AWS ES in public subnets (direct access, no proxying)
docker run \
  -v ${HOME}/.aws/:/root/.aws/ \
  -e "AWS_PROFILE=${AWS_PROFILE}" \
  polishchuk/aws-es-create-snapshot-repo-in-s3:latest \
  --region ${REGION} \
  --host ${HOST} \
  --bucket ${BUCKET} \
  --repo ${REPO} \
  --role ${ROLE}
