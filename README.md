# Chess_2
# User Guide

## Download the Source Code
**If you already have the source code, please proceed to the next step.**

1. Open your browser, navigate to the GitHub repository below, and download the source code:

https://github.com/BowenZhu790/Chess_2


## Download Python
**If Python is already installed, please proceed to the next step.**

1. This project used Python 3.12.2, but any version higher than that should also work. To download the specific version, visit:

https://www.python.org/downloads/release/python-3122/


## Download the Stockfish Chess Engine
**If the Stockfish Engine is already installed, please proceed to the next step.**

1. This project used Stockfish Chess Engine 16.1, but any version higher than that should work. To download the specific version, visit:

https://stockfishchess.org/download/


## Setting Up and Running the Chess Algorithm
**If the Stockfish Engine is already configured, please proceed to the next step.**

### Create a Virtual Environment (Windows):
1. Navigate to the project directory using the command prompt or terminal:

cd path\to\Chess_2-main

2. Create a virtual environment named `env` by running:

python -m venv env

3. Activate the virtual environment:

env\Scripts\activate


### Installing Dependencies:
1. Install the required packages by running:

pip install -r requirements.txt


### Replace Stockfish Engine's Path (Windows):
1. Find your Stockfish engine's folder. It should look similar to the structure below:

stockfish
├── AUTHORS
├── COPYING
├── README
├── stockfish-windows-x86-64-avx2
└── ...

2. Go to the directory where the executable file is located.
3. Copy the path of the `stockfish-windows-x86-64-avx2` file.
4. Update the `path_to_stockfish` in `chess_algo.py` at line 115 to match the path of your Stockfish executable. For example:

path_to_stockfish = "D:\path\to\stockfish\stockfish-windows-x86-64-avx2"

5. Running tests.

python test_chess_algo.py

6. Running the main.

python chess_algo.py



