all:
	flask --app Gomoku run

debug:
	flask --app Gomoku --debug run

clean:
	rm -rf **/__pycache__

.PHONY: all debug clean
