#!/bin/bash
# the intention is to run the commands of make makefile to catch simple errors like typos
# Of course, a full test would need to check the state before and after a command and compare it to
# the outcome after the command has been run to a desired state.
set -e

DEVELOPMENT_VIRTUAL_ENV_PATH=$VIRTUAL_ENV
TESTING_VIRTUAL_ENV_PATH="$(mktemp -d)"
function setup_virtualenv() {
  required_python_version=$(grep Python ./requirements/runtime.txt)
  required_python_version="${required_python_version// /}"
  required_python_version="${required_python_version,,}"
  virtualenv "$TESTING_VIRTUAL_ENV_PATH" -p "$required_python_version"
  source "$TESTING_VIRTUAL_ENV_PATH/bin/activate"
}

setup_virtualenv
which python
make install_builddeps
make update_reqs
make update_reqs_dev
make update_reqs_all
make upgrade_reqs
make upgrade_reqs_dev
make upgrade_reqs_all
make install_main
make install_dev

deactivate
source "$DEVELOPMENT_VIRTUAL_ENV_PATH/bin/activate"
which python
