# Argo Workflow and ArgoCD Example
The following is an example of using [MLFlow](https://mlflow.org/) (for experimentation, model building, model registry), [Argo Workflows](https://argoproj.github.io/argo-workflows/) (for ML pipelines for building and testing ML apps), and [Argo CD](https://argoproj.github.io/argo-cd/)
(for a GitOps approach for managing our Apps) running on Kubernetes. It uses an example ML App in Flask to serve an example ML model and utilizes several tasks in a Dag as examples of specific tasks that you might do in an MLPipeline. 
This will be broken up into several phases over time as more research is done and may be outdated from time to time. 

This creates a Kind cluster locally and deploys the following components using ArgoCD App of Apps: MLFlow (with PGSQL backend and Minio artifacts), ArgoCD, Argo Workflows, Nginx Ingress, Metrics Server, Kubeseal, and Pipeline configuration to Argo Workflow. 

**You may use this repo as a template and for testing locally on your own and is adjusted to be used for such. Please do not use this in production but for local testing and demos.**

The current setup assumes that you have a Production environment setup and running managed by Argo CD. This will get updated automatically by staying in sync with main branch. A test environment will be built and deployed with Argo Workflow.  

Phases:
1) [x] Get an example build/deploy pipeline setup

2) [x] Add tests to the pipeline (Examples not real)

3) [x] Add MLflow 

4) [ ] Add Jupyter Notebooks


## Prereqs
 - Kind

 - Docker

 - DockerHub access Token

 - Kubectl

 - Kubeseal CLI

## Overview of Current Pipeline Flow
The following steps are used when we need to run a new version of the example ML App. It is an example process that kicks off the example ML Pipeline.

1) Pull the repo and create a new branch.

2) Make changes to your code (`app.py`) such as the VERSION and modify the image NewTag in `ml-app/base/kustomization.yaml` file. Note: that if you forked this repo you will modify the image and the tag for the app in order to publish and pull an image from your own Docker registry.

3) Commit your changes and create a PR against the main branch.

4) Run the workflow template created. Modifying the parameters

5) Once all tasks complete as successful in the workflow template, Merge the PR to main branch.


Step 6 will deploy the changes to your Production Application in Argo CD. You may either kick off the sync immediately or wait a couple of minutes as auto-sync is currently enabled.

## Getting Started
