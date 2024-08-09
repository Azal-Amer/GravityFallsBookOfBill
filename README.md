# Gravity Falls Code Checker

This script checks for valid Gravity Falls codes on a specified website and saves the results.

## Features

- Checks multiple codes in parallel
- Saves images, HTML, and text responses
- Avoids rechecking previously checked codes
- Uses threading for improved performance

## Requirements

- Python 3.6+
- Required libraries: requests, beautifulsoup4

## Installation

1. Clone this repository or download the script.
2. Install required libraries:
   ```
   pip install requests beautifulsoup4
   ```

## Usage

1. Edit the `codes_to_check` list in the script to include the codes you want to check.
2. Run the script:
   ```
   python gravityFalls.py
   ```

## Output

- Results are printed to the console.
- Valid responses are saved in a `codes` folder, organized by code.
- Checked codes are saved in `checked_codes.json` to avoid rechecking.

## Note

This script is for educational purposes only. Please be respectful of the target website and avoid excessive requests.
