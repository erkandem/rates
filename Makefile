
install_builddeps:  # install python packes unsafe to handle with pip-tools
	bash ./install_builddeps.sh
update_reqs:
	make install_builddeps
	pip-compile requirements/requirements.in -o requirements/requirements.txt

update_reqs_dev:
	make install_builddeps
	pip-compile requirements/requirements-dev.in -o requirements/requirements_dev.txt

install_main:


