#!/bin/sh

. .deploy-now/env.sh

GIT_REF=$(git rev-parse --abbrev-ref HEAD)-$(git rev-parse --short HEAD)
IMAGE=ondrejsika/demo-cloud:$GIT_REF-$(date +%s)

docker build -t $IMAGE .
docker push $IMAGE

ORIGINAL_KUBERNETES_CONTEXT=$(kubectl config current-context)
kubectl config use-context $KUBERNETES_CONTEXT
helm upgrade --install demo-cloud-${1:-prod} helm/demo-cloud/ --values .deploy-now/${1:-prod}.yml --set image=$IMAGE --set changeCause=$GIT_REF
kubectl config use-context $ORIGINAL_KUBERNETES_CONTEXT
