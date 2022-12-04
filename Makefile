gen/build:
	cd cmd/generator && go build -o ../../gen

gen: gen/build
	./gen
