#!/usr/bin/env bash
set -e 

# Define variables so these can be modified for future use
CLUSTER_NAME="argo"

# Check for environment variables to be set so kubeseal can create the proper secret for DH creds
if [ -z $DOCKER_USERNAME ]; then
  echo "Please be sure to set your environment variable for DOCKER_USERNAME..."
  echo "export DOCKER_USERNAME=username"
  exit 1
fi

if [ -z $DOCKER_TOKEN ]; then
  echo "Please be sure to set your environment variable for DOCKER_TOKEN..."
  echo "export DOCKER_TOKEN=yourtoken1234"
  exit 1
fi

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
  # If data for MLflow exists from previous run delete it first.
  rm -rf mlflow/artifacts
  rm -rf mlflow/backend
  kind create cluster --config kind.yaml --name ${CLUSTER_NAME}
else
  echo "kind cluster with cluster name ${CLUSTER_NAME} already exists..."
  echo "Please delete it before moving on or utilize the existing cluster..."
  echo "kind delete clusters argo"
  exit 1
fi

# Apply the context to kubectl
kubectl cluster-info --context kind-${CLUSTER_NAME} 2> /dev/null

# Sleep for 5 secs. Hack for giving enough time for control plane components to start.
sleep 5

# Wait for K8s services to start
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=etcd --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-scheduler --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-apiserver --timeout=130s
kubectl wait --namespace kube-system --for=condition=ready pod --selector=component=kube-controller-manager --timeout=130s

# Deploy Sealed Secrets. Need this done before everything else.
echo "###########################################################"
echo "Deploying Sealed Secrets..."
kubectl apply --filename sealed-secrets/controller.yaml
sleep 3
kubectl wait --namespace kube-system --for=condition=ready pod --selector=name=sealed-secrets-controller --timeout=90s

# Deploy Argo CD
echo "###########################################################"
echo "Deploying Argo CD..."
kustomize build argo-cd/overlays/kind/ | kubectl apply -f -
kubectl wait --namespace argocd --for=condition=ready pod --selector=app.kubernetes.io/name=argocd-server --timeout=90s

# Deploy the Prereqs which will hand deploying All the things: NGINX, ArgoWF, metrics-server, pipeline configs and the
# initial Production app
echo "###########################################################"
echo "Deploying All other things which can be found in Argo CD UI..."
kustomize build mlops/prereqs/ | kubectl apply -f -

# Deploy and create SealedSecret for Docker
echo "###########################################################"
echo "Creating Sealed Secret for Docker Creds..."
kubectl create secret --namespace argo generic docker-config \
  --from-literal="config.json={\"auths\": {\"https://index.docker.io/v1/\": {\"auth\": \"$(echo -n $DOCKER_USERNAME:$DOCKER_TOKEN|base64)\"}}}" \
  --output json --dry-run=client \
  | kubeseal --format yaml \
  | tee pipeline/overlays/kind/secrets.yaml

kubectl apply --filename pipeline/overlays/kind/secrets.yaml

# Update /etc/hosts
echo "###########################################################"
echo "Please be sure to update your /etc/hosts file with..."
echo "127.0.0.1 argo"
echo "127.0.0.1 argocd"
echo "127.0.0.1 tests"
echo "127.0.0.1 mlfow"
echo "127.0.0.1 minio"
echo ""
echo "Once you update /etc/hosts you can access the following:"
echo "Argo Workflows UI: https://argo/argo"
echo "ArgoCD UI: http://argocd"
echo "MLFlow UI: http://mlfow"
echo "Minio UI: http://minio"
echo ""
echo "Send requests for prediction to:"
echo "Tests: http://tests/predict"
echo "Prod (Existing): http://localhost/predict"


