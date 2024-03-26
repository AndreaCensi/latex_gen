all:
	@echo


template:
	zuper-cli template

bump:
	zuper-cli bump

upload:
	zuper-cli upload

black:
	black -l 110 --target-version py311 src

install-deps:
	pip3 install --user shyaml
	shyaml get-values install_requires < project.pp1.yaml > .requirements.txt
	pip3 install --user --upgrade -r .requirements.txt
	rm .requirements.txt

install-testing-deps:
	pip3 install --user shyaml
	shyaml get-values tests_require < project.pp1.yaml > .requirements_tests.txt
	pip3 install --user --upgrade -r .requirements_tests.txt
	rm .requirements_tests.txt

	pip install \
		pipdeptree\
		bumpversion\
		nose\
		nose2\
		nose2-html-report\
		nose-parallel\
		nose_xunitmp\
		pre-commit\
		rednose\
		coverage\
		codecov\
		sphinx\
		sphinx-rtd-theme
cover_packages=latex_gen,latex_gen_tests,latex_gen_tests.demos,latex_gen_tests.demos.demo1,latex_gen_tests.demos.escaping,latex_gen_tests.demos.latex_gen_demos,latex_gen_tests.demos.tables,latex_gen_tests.test1,latex_gen_tests.test_escaping,latex_gen_tests.test_idions,latex_gen_tests.test_tables,latex_gen_tests.utils

# PROJECT_ROOT ?= /project
# REGISTRY ?= docker.io
# PIP_INDEX_URL ?= https://pypi.org/simple
# BASE_IMAGE ?= python:3.7

CIRCLE_NODE_INDEX ?= 0
CIRCLE_NODE_TOTAL ?= 1

out=out
coverage_dir=$(out)/coverage
tr=$(out)/test-results
xunit_output=$(tr)/nose-$(CIRCLE_NODE_INDEX)-xunit.xml

parallel=--processes=8 --process-timeout=1000 --process-restartworker
coverage=--cover-html --cover-html-dir=$(coverage_dir) --cover-tests \
            --with-coverage --cover-package=$(cover_packages)

xunit=--with-xunit --xunit-file=$(xunit_output)
xunitmp=--with-xunitmp --xunitmp-file=$(xunit_output)
extra=--rednose --immediate

clean:
	coverage erase
	rm -rf $(out) $(coverage_dir) $(tr)

test:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage)  latex_gen_tests  -v --nologcapture $(xunit)


test-parallel:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage) latex_gen_tests -v --nologcapture $(parallel) $(xunitmp)


test-parallel-circle:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 \
	NODE_TOTAL=$(CIRCLE_NODE_TOTAL) \
	NODE_INDEX=$(CIRCLE_NODE_INDEX) \
	nosetests $(coverage) $(xunitmp) latex_gen_tests  -v  $(parallel)


coverage-combine:
	coverage combine

docs:
	sphinx-build src $(out)/docs

-include extra.mk

# sigil 96e2b55d292d2f3925c360a80a8ea998
