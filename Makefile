
install_builddeps:  ## install python packages unsafe to handle with pip-tools
	./install_builddeps.sh

update_reqs:  ## reflect changes in requirements.in without upgrading package versions by default
	make install_builddeps
	pip-compile requirements/requirements.in -o requirements/requirements.txt

update_reqs_dev:  ## reflect changes in requirements-dev.in without upgrading package versions by default
	make install_builddeps
	pip-compile requirements/requirements-dev.in -o requirements/requirements_dev.txt

update_reqs_all: ## reflect changes in the input files in the output files for runtime and dev dependencies
	make update_reqs
	make update_reqs_dev

upgrade_reqs:  ## upgrade versions of runtime dependencies
	make install_builddeps
	pip-compile --upgrade requirements/requirements-dev.in -o requirements/requirements_dev.txt

upgrade_reqs_dev:  ## upgrade versions of development dependencies
	make install_builddeps
	pip-compile --upgrade requirements/requirements-dev.in -o requirements/requirements_dev.txt

upgrade_reqs_all:  ## upgrade both dev and runtime versions of dependencies
	make upgrade_reqs
	make upgrade_reqs_dev

install_main:
	pip-sync ./requirements/requirements.txt

install_dev:
	pip-sync ./requirements/requirements_dev.txt
