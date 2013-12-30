all: test

filename=redisgpg-`python -c 'import redisgpg.version;print redisgpg.version.version'`.tar.gz

export PYTHONPATH:=  ${PWD}

test: clean unit functional docstests

test-kind:
	@echo "Running unit tests"
	@nosetests --cover-branches --rednose --with-coverage  --cover-erase --cover-package=redisgpg --stop -v -s tests/$(kind)

unit:
	@make test-kind kind=unit

functional:
	@make test-kind kind=functional

unit: clean

docstests: clean
	@steadymark README.md

docs: docstests
	@markment -o . -t redisgpg --sitemap-for="http://falcao.it/redisgpg" spec
	@git co master && \
		(git br -D gh-pages || printf "") && \
		git checkout --orphan gh-pages && \
		markment -o . -t redisgpg --sitemap-for="http://falcao.it/redisgpg" spec && \
		git add . && \
		git commit -am 'documentation' && \
		git push --force origin gh-pages && \
		git checkout master

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore`; do rm -rf $$pattern; find . -name "$$pattern" -exec rm -rf {} \;; done
	@echo "OK!"

release: test
	@./.release
	@make publish

publish:
	@python setup.py sdist register upload

prepare:
	@mkdir -p output
