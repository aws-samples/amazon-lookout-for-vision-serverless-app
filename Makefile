SHELL := /bin/bash

.PHONY: package
package: 
	zip -r packaged.zip \
		functions/ \
		cfn-publish.config \
		template.yml \
		-x '**/__pycache*' @

.PHONY: test
test:
	cfn-lint template.yml --ignore-checks E2531
	cfn_nag template.yml

.PHONY: setup
setup:
	# build dependencies
	pip3 install -r requirements.txt
	pre-commit install

	# node.js lambdas
	cd ./functions/ApiGwCustomAuthorizer && npm install
	cd ./functions/S3UploaderFunction && npm install

	# python lambdas
	cd ./functions/CreateManifestFileInS3 && pip3 install -r requirements.txt -t .
	cd ./functions/CreateS3BucketNotification && pip3 install -r requirements.txt -t .
	cd ./functions/DetectAnomaliesFunction && pip3 install -r requirements.txt -t .
	cd ./functions/DynamoDbToFirehose && pip3 install -r requirements.txt -t .

.PHONY: version
version:
	@echo $(shell cfn-flip template.yml | python -c 'import sys, json; print(json.load(sys.stdin)["Globals"]["Function"]["Environment"]["Variables"]["VERSION"])')
