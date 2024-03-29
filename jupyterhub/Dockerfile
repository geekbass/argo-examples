# Forked from https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
ARG DOCKER_IMAGE=wbassler/pyspark-aws:3.1.2
FROM ${DOCKER_IMAGE}

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# ---- Miniforge installer ----
# Default values can be overridden at build time
# (ARGS are in lower case to distinguish them from ENV)
# Check https://github.com/conda-forge/miniforge/releases
# Conda version
#ARG conda_version="4.10.1"
## Miniforge installer patch version
#ARG miniforge_patch_number="5"
## Miniforge installer architecture
#ARG miniforge_arch="x86_64"
## Package Manager and Python implementation to use (https://github.com/conda-forge/miniforge)
## - conda only: either Miniforge3 to use Python or Miniforge-pypy3 to use PyPy
## - conda + mamba: either Mambaforge to use Python or Mambaforge-pypy3 to use PyPy
#ARG miniforge_python="Mambaforge"
#
## Miniforge archive to install
#ARG miniforge_version="${conda_version}-${miniforge_patch_number}"
## Miniforge installer
#ARG miniforge_installer="${miniforge_python}-${miniforge_version}-Linux-${miniforge_arch}.sh"
## Miniforge checksum
#ARG miniforge_checksum="069e151cae85ed4747721e938e7974aa00889a1ae87cff33ddbdde9530fc4c6d"

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    tini \
    wget \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation && \
    #run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}" \
    CONDA_VERSION="${conda_version}" \
    MINIFORGE_VERSION="${miniforge_version}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${HOME}" && \
    fix-permissions "${CONDA_DIR}"

USER ${NB_UID}
ARG PYTHON_VERSION=default

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Install conda as jovyan and check the sha256 sum provided on the download site
WORKDIR /tmp

# Prerequisites installation: conda, mamba, pip, tini
#RUN wget --quiet "https://github.com/conda-forge/miniforge/releases/download/${miniforge_version}/${miniforge_installer}" && \
#    echo "${miniforge_checksum} *${miniforge_installer}" | sha256sum --check && \
#    /bin/bash "${miniforge_installer}" -f -b -p "${CONDA_DIR}" && \
#    rm "${miniforge_installer}" && \
#    # Conda configuration see https://conda.io/projects/conda/en/latest/configuration.html
#    echo "conda ${CONDA_VERSION}" >> "${CONDA_DIR}/conda-meta/pinned" && \
#    conda config --system --set auto_update_conda false && \
#    conda config --system --set show_channel_urls true && \
#    if [[ "${PYTHON_VERSION}" != "default" ]]; then conda install --yes python="${PYTHON_VERSION}"; fi && \
#    conda list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
#    conda install --quiet --yes \
#    "conda=${CONDA_VERSION}" \
#    'pip' && \
#    conda update --all --quiet --yes && \
#    conda clean --all -f -y && \
#    rm -rf "/home/${NB_USER}/.cache/yarn" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
#RUN conda install --quiet --yes \
#    'notebook=6.4.0' \
#    'jupyterhub=1.4.1' \
#    'jupyterlab=3.0.16' && \
#    conda clean --all -f -y && \
#    npm cache clean --force && \
#    jupyter notebook --generate-config && \
#    jupyter lab clean && \
#    rm -rf "/home/${NB_USER}/.cache/yarn" && \
#    fix-permissions "${CONDA_DIR}" && \
#    fix-permissions "/home/${NB_USER}"
# Fix permissions on /etc/jupyter as root
USER root

#RUN apt-get update &&     \
#    apt install -y python3 python3-pip &&  \
#    pip3 install --upgrade pip setuptools &&  \
#    python3 --version
# Install MLFlow and pyspark python packages
RUN python3 -m pip install --upgrade pip && \
    pip3 install mlflow[extras] && \
    pip3 install psycopg2-binary && \
    pip3 install notebook==6.4 && \
    pip3 install jupyterhub==1.4.1 && \
    pip3 install jupyterlab==3.0.16 && \
    pip3 install pyspark==3.1.2
EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Copy local files as late as possible to avoid cache busting
COPY start.sh start-notebook.sh start-singleuser.sh /usr/local/bin/
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY jupyter_notebook_config.py /etc/jupyter/


# Prepare upgrade to JupyterLab V3.0 #1205
RUN sed -re "s/c.NotebookApp/c.ServerApp/g" \
    /etc/jupyter/jupyter_notebook_config.py > /etc/jupyter/jupyter_server_config.py && \
    fix-permissions /etc/jupyter/

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
