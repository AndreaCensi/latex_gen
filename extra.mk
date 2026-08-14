.PHONY: clean

clean:
	coverage erase
	rm -rf $(out) $(out)/coverage $(out)/test-results

pre-circle-tests:
	apt-get update
	apt-get install -y texlive
