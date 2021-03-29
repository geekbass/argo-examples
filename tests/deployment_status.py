from kubernetes import client, config
import os
import time
import sys
import logging

# Constants to be used as ENV Vars
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
NAMESPACE_NAME = os.getenv("NAMESPACE_NAME")
FAIL_COUNT = os.getenv("FAIL_COUNT", "5")
CHECK_INTERVAL = os.getenv("CHECK_INTERVAL", "15")

# Set Logging
log_format = "%(asctime)s - %(levelname)s - %(process)d/%(threadName)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)


def get_deployment_status_type(name, namespace):
    config.load_kube_config()
    v1 = client.AppsV1Api()
    get_status = v1.read_namespaced_deployment_status(name=name, namespace=namespace, pretty="true")

    conditions = get_status.status.conditions

    # Initiate condition list as types will return as a list
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1DeploymentCondition.md
    condition_list = []
    for condition in conditions:
        status = condition.type
        condition_list.append(status)

    # Return the current list of condition Types
    return condition_list


def check_status(conditions):
    # We only care if current status is 'Available'
    # Great reference: https://maelvls.dev/deployment-available-condition/
    if 'Available' not in conditions:
        status = "ready"
    else:
        status = "not_ready"

    logging.info("Deployment is {}".format(status))
    # Return if app is ready or not
    return status


def main():
    # Initiate fail counter
    failure_counter = []

    while len(failure_counter) < int(FAIL_COUNT):
        # Get the current status list
        conditions = get_deployment_status_type(DEPLOYMENT_NAME, NAMESPACE_NAME)
        # Get current status
        status = check_status(conditions)

        if status == "not_ready":
            # Append to fail counter
            failure_counter.append(status)
            logging.info("Checking again in {} secs.".format(CHECK_INTERVAL))
        else:
            sys.exit("Exiting -- Deployment is {}".format(status))

        # If deployment is slow, give some time to start
        time.sleep(int(CHECK_INTERVAL))


if __name__ == '__main__':
    main()




