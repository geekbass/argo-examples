# Argo Workflow and ArgoCD Example
The following is an example of using Argo Workflows and Argo CD for both CI and CD for an ML Application running on Kubernetes. 
This will be broken up into several phases over time as more research is done and may be outdated from time to time. Complete pipeline vision currently includes the following tools:
 [MLFlow](https://mlflow.org/) (for experimentation, model building, model registry), [Argo Workflows](https://argoproj.github.io/argo-workflows/) for pipelines for building and testing ML apps, and [Argo CD](https://argoproj.github.io/argo-cd/)
 for a GitOps approach for managing our Apps running on Kubernetes. 

**You may use this repo as a template and for testing locally on your own and is adjusted to be used for such. Please do not use this in production.**

The current setup assumes that you have a Production environment setup and running managed by Argo CD. This will get updated automatically by staying in sync with main branch. A test environment will be built and deployed with Argo Workflow.  

Phases:
1) [x] Get an example build/deploy pipeline setup

2) [ ] Add tests to the pipeline

3) [ ] Add MLfow to the mix 

## Prereqs
 - Kind

 - Docker

 - DockerHub access Token

 - Kubectl

## Overview of Current Process Flow
1) Pull the repo and create a new branch.

2) Make changes to you code (`app.py`), modify the image version in both test (`tests/deployment.yaml`) and prod (`prod/deployment.yaml`) deployment.

3) Commit your changes and create a PR against the main branch.

4) Submit a workflow template (`argo/workflow-template-mlpipeline-template.yaml`). Be sure to change the image and the branch arguments. The image should be the same image version you placed in the deployment files. The branch is the current branch you are developing on.

Step 4 runs a [DAG](https://argoproj.github.io/argo-workflows/examples/#dag) with 3 steps (more to come): 1) Clone, 2) Build a new image of your new code and 3) Deploy a "test" version of the Production environment.

5) Once all tests Pass from the Pipeline, destroy the test application in Argo CD.

6) Merge the PR into main.

Step 6 will deploy the changes to your Production Application in Argo CD. You may either kick off the sync immediately or wait a couple of minutes as auto-sync is currently enabled.

## Getting Started
