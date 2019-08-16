ENV_VARS := \
	NODE_ENV=test \
	API_HEALTH_KEY=xxx

test: lint
	@ $(ENV_VARS) ./node_modules/.bin/mocha -A --recursive $(MOCHA_OPTS)

lint:
	@ find . -name "*.js" \
		-not -path "./node_modules/*" \
		-not -path "./test/*" \
		-not -path "./coverage/*" -print0 | \
		xargs -0 ./node_modules/jshint/bin/jshint

test-cov:
	@ $(ENV_VARS) node \
		node_modules/.bin/istanbul cover \
		./node_modules/.bin/_mocha -A --recursive $(MOCHA_OPTS)

open-cov: test-cov
	open coverage/lcov-report/index.html

test-travis: lint test-cov
	@NODE_ENV=test node node_modules/.bin/istanbul check-coverage

.PHONY: test test-cov open-cov
