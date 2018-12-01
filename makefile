PACKAGE = BluesBot

DOCKER_IMAGE = $(PACKAGE)-env
DOCKER_HOST_USER_PERMS = -v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro
DOCKER_VOLUMES = -v $(PWD):/tmp/build $(DOCKER_HOST_USER_PERMS)
DOCKER_USER = -u $(shell id -u):$(shell id -g)
DOCKER_RUN_FLAGS = --rm $(DOCKER_VOLUMES) $(DOCKER_USER) -w /tmp/build
DOCKER_COMMAND_BASE = docker run --rm $(DOCKER_RUN_FLAGS) $(DOCKER_IMAGE)

ENVIRONMENTS = analysis py3-test
DOCKER_ENVIRONMENTS = $(patsubst %,%-docker,$(ENVIRONMENTS))
ENVIRONMENT = $(patsubst %-docker, %, $@)
ENVIRONMENT_METAS = py3-test
DOCKER_ENVIRONMENT_METAS = py3-test-docker


usage:
	@echo "***********************************************************************************"
	@echo "all - Runs all default tox environments"
	@echo "$(ENVIRONMENTS) - run tox -e <environment>"
	@echo "target-docker - run target in docker environment (e.g all-docker)"
	@echo "clean - clean up generated files"
	@echo "***********************************************************************************"


all: $(ENVIRONMENT_METAS)
	tox

.SECONDEXPANSION:

.PHONY: $(ENVIRONMENTS)
$(ENVIRONMENTS): .python_scaffold_meta_venv
	tox -e $(ENVIRONMENT)

.PHONY: all-docker
all-docker: build-docker $(DOCKER_ENVIRONMENT_METAS)
	$(DOCKER_COMMAND_BASE) tox

.PHONY: $(DOCKER_ENVIRONMENTS)
$(DOCKER_ENVIRONMENTS): build-docker .python_scaffold_meta_venv_docker
	$(DOCKER_COMMAND_BASE) tox -e $(ENVIRONMENT)

.PHONY: build-docker
build-docker: .python_scaffold_meta_docker_build

clean:
	@rm -rf $(PACKAGE).egg-info .tox .python_scaffold_meta* dist/ build/

# Special targets to force venv regeneration
# on requirement file changes
.python_scaffold_meta_docker_build: Dockerfile
	docker build --tag $(DOCKER_IMAGE) .
	@touch $@

.python_scaffold_meta_venv: requirements.txt test-requirements.txt
	@echo "(Re-)creating virtualenv for py3-test"
	tox --notest -r -e py3-test
	@touch $@

.python_scaffold_meta_venv_docker: requirements.txt test-requirements.txt .python_scaffold_meta_docker_build
	@echo "(Re-)creating virtualenv for py3-test (Docker)"
	$(DOCKER_COMMAND_BASE) tox --notest -r -e py3-test
	@touch $@
