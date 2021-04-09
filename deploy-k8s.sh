#!/usr/bin/env bash
set -e 
# Define variables so these can be modified for future use
CLUSTER_NAME="argo"
SEALED_SECRETS_URL="https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.15.0/controller.yaml"

# Check for Docker install
if [[ `which docker` == "" ]]; then
  echo "Docker not found. Please install docker before moving on."
  exit 1
fi

# Check for kubectl install
if [[ `which kubectl` == "" ]]; then
  echo "Kubectl not found. Please install kubectl before moving on."
  echo "https://kubernetes.io/docs/tasks/tools/install-kubectl/"
  exit 1
fi

# If kind is not installed then exit
if [[ `which kind` == "" ]]; then
  echo "Kind not found. Please install kind before moving on."
  echo "https://kind.sigs.k8s.io/docs/user/quick-start"
  exit 1
fi

# If kustomize is not installed then exit
if [[ `which kustomize` == "" ]]; then
  echo "Kustomize not found. Please install kustomize before moving on."
  exit 1
fi

# If kubeseal is not installed then exit
if [[ `which kubeseal` == "" ]]; then
  echo "Kubeseal not found. Please install kubeseal before moving on."
  exit 1
fi

# Check for existing kind cluster with same name
if [[ `kind get clusters | grep ${CLUSTER_NAME}` == "" ]]; then
  echo "Creating K8s locally with kind..."
  kind create cluster --config argo/kind.yaml --name ${CLUSTER_NAME}
else
  echo "kind cluster with cluster name ${CLUSTER_NAME} already exists..."
  echo "Please delete it before moving on or utilize the existing cluster..."
  exit 1
fi

# Apply the context to kubectl
kubectl cluster-info --context kind-${CLUSTER_NAME} 2> /dev/null

# Wait for K8s services to start
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=etcd --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-scheduler --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-apiserver --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-controller-manager --timeout=130s

# Deploy Sealed Secrets
echo "Deploying Sealed Secrets..."
kubectl apply --filename sealed-secrets/controller.yaml
sleep 3
kubectl wait --namespace kube-system --for=condition=ready pod --selector=name=sealed-secrets-controller --timeout=90s

# Deploy Argo CD
echo "Deploying Argo CD..."
kustomize build argo-cd/overlays/kind/ | kubectl apply -f -
kubectl wait --namespace argocd --for=condition=ready pod --selector=app.kubernetes.io/name=argocd-server --timeout=90s

# Deploy the Prereqs which will hand deploying All the things: NGINX, ArgoWF, metrics-server, pipeline configs and the
# initial Production app
echo "Deploying All other things which can be found in Argo CD UI..."
kustomize build mlops/prereqs/ | kubectl apply -f -

# Deploy and create SealedSecret for Docker
echo "Creating Sealed Secret for Docker Creds..."
kubectl create secret -n argo docker-registry docker-config --docker-server=${DOCKER_SERVER} \
  --docker-username=${DOCKER_USERNAME} --docker-password=${DOCKER_PASSWORD} \
  --docker-email=${DOCKER_EMAIL} -output json \
  --dry-run=client \
  | kubeseal --format yaml \
  | tee pipelines/overlays/kind/secrets.yaml

kubectl apply --filename pipelines/overlays/kind/secrets.yaml

# Update /etc/hosts
echo "###########################################################"
echo "Please be sure to update your /etc/hosts file with..."
echo "127.0.0.1 argo"
echo "127.0.0.1 argocd"
echo "127.0.0.1 tests"
ehco ""
echo "Once you update /etc/hosts you can access the following:"
echo "Argo Workflows UI: http://argo/argo-wf"
echo "ArgoCD UI: http://argocd/argo-cd"
echo ""
echo "You will be able to access the apps at:"
echo "Tests: http://tests/ml/audit"
echo "Prod (Existing): http://localhost/ml/audit"


