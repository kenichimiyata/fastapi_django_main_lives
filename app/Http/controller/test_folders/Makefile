init:
	clasp create --type standalone --rootDir src

push:
	clasp push

pull:
	clasp pull

deploy:
	clasp deploy --description "Initial deployment"
	make open

open:
	clasp open

test:
	node test/test-runner.js