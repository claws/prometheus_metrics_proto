# This makefile has been created to help developers perform common actions.
# It assumes it is operating in an environment, such as a virtual env,
# where the python command links to Python3.6 executable.

.PHONY: clean clean.scrub dist help sdist test test.verbose

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: prometheus_metrics_proto Makefile help
# help:


# help: help                           - display this makefile's help information
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'


# help: clean                          - clean all files using .gitignore rules
clean:
	@git clean -X -f -d


# help: clean.scrub                    - clean all files, even untracked files
clean.scrub:
	git clean -x -f -d


# help: test                           - run tests
test:
	@python -m unittest discover -s tests


# help: test.verbose                   - run tests [verbosely]
test.verbose:
	@python -m unittest discover -s tests -v


# help: dist                           - create a source distribution package
dist: clean
	@python setup.py sdist


# help: dist.test                      - test a source distribution package
dist.test: dist
	@cd tools && ./test.bash


# help: dist.upload                     - upload a source distribution package
dist.upload: clean
	@python setup.py sdist upload


# Keep these lines at the end of the file to retain nice help
# output formatting.
# help:
