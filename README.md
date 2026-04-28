### Overview

- Author: Daniel Schuster
- This project implements a portion of a modem to decode text messages encoded as audio with the Bell 103 modem protocol.
- The program reads in a .wav file, processes it, decodes it into a sequence of bits, and generates the corresponding ASCII text.  The decoded message text is written to a file MESSAGE.txt in the current directory.

### Usage

- The program can be run as follows.  It assumes a .wav file named message.wav is located in the current directory.
```
# Optional: create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run program (creates .txt file in current directory)
python code/main.py
```
