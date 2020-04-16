# This makefile has been created to help developers perform common actions.
# It assumes it is operating in a virtual environment.


# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: prometheus_metrics_proto Makefile help
# help:


# help: help                           - display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'


# help: clean                          - clean all files using .gitignore rules
.PHONY: clean
clean:
	@git clean -X -f -d


# help: clean-scrub                    - clean all files, even untracked files
.PHONY: clean-scrub
clean.scrub:
	git clean -x -f -d


# help: style                          - apply code formatter
.PHONY: style
style:
	@# Avoid formatting automatically generated code by excluding it
	@black src/prometheus_metrics_proto tests examples setup.py --exclude .*_pb2\.py


# help: check-style                    - check code formatting
.PHONY: check-style
check-style:
	@# Avoid checking format of automatically generated code by excluding it
	@black --check src/prometheus_metrics_proto tests examples --exclude .*_pb2\.py


# help: coverage                       - perform test coverage checks
.PHONY: coverage
coverage:
	@coverage erase
	@PYTHONPATH=src coverage run -m unittest discover -s tests -v
	@coverage html
	@coverage report

# help: test                           - run tests
.PHONY: test
test:
	@python -m unittest discover -s tests


# help: test-verbose                   - run tests [verbosely]
.PHONY: test-verbose
test-verbose:
	@python -m unittest discover -s tests -v


# help: dist                           - create a distribution package
.PHONY: dist
dist:
	@rm -rf dist
	@python setup.py bdist_wheel


# help: dist-test                      - test a distribution package
.PHONY: dist-test
dist-test: dist
	@cd dist && ../tests/test-dist.bash ./prometheus_metrics_proto-*-py3-none-any.whl


# help: dist-upload                    - upload a distribution package
.PHONY: dist-upload
dist-upload:
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
