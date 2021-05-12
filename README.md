# Argo Workflow and ArgoCD Example
The following is an example of using [MLFlow](https://mlflow.org/) (for experimentation, model building, model registry), [Argo Workflows](https://argoproj.github.io/argo-workflows/) (for ML pipelines for building and testing ML apps), and [Argo CD](https://argoproj.github.io/argo-cd/)
(for a GitOps approach for managing our Apps) running on Kubernetes. It uses an example ML App in Flask to serve an example ML model and utilizes several tasks in a Dag as examples of specific tasks that you might do in an MLPipeline. It is also worth noting that we are using Kustomize for initial install of Argo CD and also for Argo CD to manage our apps. A bash script has been provided to make initial setup of the cluster automated.

This creates a Kind cluster locally and deploys the following components using ArgoCD App of Apps (`mlops/overlays/kind`): MLFlow (with PGSQL backend and Minio artifacts), ArgoCD, Argo Workflows, Nginx Ingress, Metrics Server, Kubeseal, and Pipeline configuration to Argo Workflow. Anytime you make changes to any of these components you can simply wait a few minutes or manually sync the `mlops-tools` application in Argo CD.

**You may use this repo as a template and for testing locally on your own and is adjusted to be used for such. Please do not use this in production but for local testing and demos.**

The current setup assumes/creates a "Production" app managed by Argo CD. This will get updated automatically by staying in sync with main branch. A test environment will be built and deployed with Argo Workflow.

All parameters in the Pipeline file should be adjusted accordingly to fit your needs. If you fork this repo you will need to either modify the default parameter values for repo and registry in the workflow template (`pipeline/base/pipeline-workflow-template.yaml`) or simply change them each time you run the workflow template.

Phases:
1) [x] Get an example build/deploy pipeline setup

2) [x] Add tests to the pipeline (Examples not real)

3) [x] Add MLflow 

4) [ ] Add Jupyter Notebooks


## Prereqs
 - [Kind]()

 - [Docker]()

 - [DockerHub access Token]()

 - [Kubectl]()

 - [Kubeseal CLI]()

 - [Kustomize CLI]()

## Overview of Current Pipeline Flow
The following steps are used when we need to run a new version of the example ML App. It is an example process that kicks off the example ML Pipeline.

1) Pull the repo and create a new branch.

2) Make changes to your a) code (`app.py`) such as the VERSION and b) modify the image NewTag in `ml-app/base/kustomization.yaml` file. Note: that if you forked this repo you will modify the image and the tag for the app in order to publish and pull an image from your own Docker registry.

3) Commit your changes and create a PR against the main branch.

4) Run the workflow template created. Modifying the parameters for branch and version. Branch should be set to the new branch you just created and version is the updated version tag you are creating. *NOTE: If you forked this repo you may also need to modify the registry and the repo values if you did not set new defaults*

5) Once all tasks complete as successful in the workflow template, Merge the PR to main branch.


*Step 5 will deploy the changes to your Production Application in Argo CD. You may either kick off the sync immediately or wait a couple of minutes as auto-sync is currently enabled.*

## Getting Started
Ensure that you have all the prereqs listed above. A simple bash script has been provided to assist with complete initial setup.

1) Export variables for `$DOCKER_USERNAME` and `$DOCKER_TOKEN`. This will give permissions to create a registry and new tag with each pipeline run. *NOTE: the script creates the secret with kubseal so that we do not accidentally push a secrets file that can be decoded to a public repo. Although we do not commit this kubeseal file either, you can do this yourself if you so desire. For more information on Kubeseal see their documentation.*
```
export DOCKER_USERNAME=username
export DOCKER_TOKEN=yourtoken1234
```

2) Run the bash script. This will take some time to complete.
```
bash deploy-k8s.sh
```