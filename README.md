# Habbo Flooder - Proof of Concept

This project is a proof of concept (POC) for a script that allows users to automate text input in the Habbo Hotel game. The script uses Python, `pyautogui` for automation, `customtkinter` for the graphical user interface (GUI), and SQLite for persistent storage of text inputs.

## Features

- Multiple tabs, each associated with a function key (F1-F11), to store different text inputs.
- Persistent storage of text inputs between restarts using SQLite.
- A stopping keybind (F12) to stop the automated text input.
- A clean and user-friendly GUI.

## Prerequisites

- Python 3.x
- `pyautogui` library
- `customtkinter` library
- `sqlite3` (standard library, no need for installation)

## Installation

1. Clone the repository or download the script.

    ```bash
    git clone https://github.com/kWAYTV/habbo-origins-flooder.git
    cd habbo-origins-flooder
    ```

2. Install the required libraries.

    ```bash
    python -m pip install -r requirements.txt
    ```

## Usage

1. Run the script.

    ```bash
    python habbo_flooder.py
    ```

2. The GUI will open with multiple tabs for each function key (F1-F11). Enter the text you want to flood in the respective tabs.

3. Press the corresponding function key (e.g., F1) to start the flooding with the text from that tab.

4. Press F12 to stop the flooding.

## Script Explanation

- `focus_and_type(phrase)`: This function finds the Habbo Hotel window and sends the text phrase to it, split into multiple messages if it exceeds 60 characters.
- `on_keybind(key)`: This function starts the flooding process by creating a new thread for the `focus_and_type` function with the text from the corresponding tab.
- `stop_flood()`: This function sets a flag to stop the flooding process.
- `save_texts()`: This function saves the text inputs to an SQLite database.
- `load_texts()`: This function loads the text inputs from the SQLite database.

## Disclaimer

This project is a proof of concept (POC) and should be used responsibly. Automating interactions in online games can violate the terms of service of the game and result in penalties, including bans. Use this script at your own risk.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
