PYTHON=python3
VENV_PYTHON=./src/venv/bin/python
SRC_DIR=src
COMP_DIR=compiled

.PHONY: all clean install build copy all_clean

all_clean: install build copy clean

all: install build copy

# install python dependencies
install:
	$(PYTHON) -m venv ./src/venv
	$(VENV_PYTHON) -m pip install -r $(SRC_DIR)/requirements.txt

# build with pyinstaller
build:
	cd $(SRC_DIR) && ./venv/bin/pyinstaller --clean --noupx FastFITStoJPG.py

# copy compiled binary to folder
copy:
	mkdir -p $(COMP_DIR)
	cp -r $(SRC_DIR)/dist/FastFITStoJPG/* $(COMP_DIR)/

# optionally clean after building
clean:
	rm -rf $(SRC_DIR)/build $(SRC_DIR)/dist $(SRC_DIR)/venv $(SRC_DIR)/FastFITStoJPG.spec
