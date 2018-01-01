# This makefile has been created to help developers perform common actions.
# It assumes it is operating in an environment, such as a virtual env,
# where the python command links to Python3.6 executable.

STYLE_EXCLUDE_LIST:=git status --porcelain --ignored | grep "!!" | grep ".py$$" | cut -d " " -f2 | tr "\n" ","
STYLE_MAX_LINE_LENGTH:=160
STYLE_CMD:=pycodestyle --exclude=.git,docs,$(shell $(STYLE_EXCLUDE_LIST)),src/prometheus_metrics_proto/prometheus_metrics_pb2.py --ignore=E309,E402 --max-line-length=$(STYLE_MAX_LINE_LENGTH) src/prometheus_metrics_proto tests examples
VENVS_DIR := $(HOME)/.venvs
VENV_DIR := $(VENVS_DIR)/pmp

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: prometheus_metrics_proto Makefile help
# help:


# help: help                           - display this makefile's help information
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'


# help: venv                           - create a virtual environment for development
venv:
	@test -d "$(VENVS_DIR)" || mkdir -p "$(VENVS_DIR)"
	@rm -Rf "$(VENV_DIR)"
	@python3 -m venv "$(VENV_DIR)"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && pip install pip --upgrade && pip install -r requirements.dev.txt"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && make generate && pip install -e ."
	@echo "Enter virtual environment using:\n\n\t$ source $(VENV_DIR)/bin/activate\n"

# help: clean                          - clean all files using .gitignore rules
clean:
	@git clean -X -f -d


# help: clean.scrub                    - clean all files, even untracked files
clean.scrub:
	git clean -x -f -d


# help: style                          - perform pep8 check
style:
	@$(STYLE_CMD)


# help: style.fix                      - perform check with autopep8 fixes
style.fix:
	@# If there are no files to fix then autopep8 typically returns an error
	@# because it did not get passed any files to work on. Use xargs -r to
	@# avoid this problem.
	@$(STYLE_CMD) -q  | xargs -r autopep8 -i --max-line-length=$(STYLE_MAX_LINE_LENGTH)


# help: coverage                       - perform test coverage checks
coverage:
	@coverage run -m unittest discover -s tests
	@# produce html coverage report on modules
	@coverage html -d htmlcov --include="src/prometheus_metrics_proto/*"


# help: test                           - run tests
test:
	@python -m unittest discover -s tests


# help: test.verbose                   - run tests [verbosely]
test.verbose:
	@python -m unittest discover -s tests -v


# help: dist                           - create a distribution package
dist: clean
	@python setup.py bdist_wheel


# help: dist.test                      - test a distribution package
dist.test: dist
	@cd dist && ../tests/test-dist.bash ./prometheus_metrics_proto-*-py3-none-any.whl


# help: dist.upload                    - upload a distribution package
dist.upload:
	@twine upload dist/prometheus_metrics_proto-*-py3-none-any.whl


# help: generate                       - generate protobuf code stubs if needed
generate: src/prometheus_metrics_proto/prometheus_metrics_pb2.py

src/prometheus_metrics_proto/prometheus_metrics_pb2.py:
	@cd proto; python -m grpc_tools.protoc -I . --python_out=../src/prometheus_metrics_proto prometheus_metrics.proto


# help: regenerate                     - force generate protobuf code stubs
regenerate:
	@rm -f rm -f src/prometheus_metrics_proto/prometheus_metrics_pb2.py
	@cd proto; python -m grpc_tools.protoc -I . --python_out=../src/prometheus_metrics_proto prometheus_metrics.proto


# Keep these lines at the end of the file to retain nice help
# output formatting.
# help:

.PHONY: \
	clean clean.scrub dist dist.test dist.upload generate help test test.verbose venv
