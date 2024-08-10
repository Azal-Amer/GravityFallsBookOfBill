# Gravity Falls Code Checker

This Python script, `gravityFalls.py`, is designed to check for valid Gravity Falls codes on a specified website. It can process a list of keywords, save responses (including images, videos, and HTML content), and avoid rechecking previously checked codes.

## Features

- Checks multiple codes in parallel for faster processing
- Handles various types of responses (images, videos, HTML, text)
- Saves response content locally for further analysis
- Avoids rechecking previously checked codes
- Supports custom timeouts for requests
- Allows input of keywords via command-line arguments or from a file

## Requirements

- Python 3.6+
- Required libraries: requests, beautifulsoup4

## Installation

1. Clone this repository or download the `gravityFalls.py` script.
2. Install the required libraries:
   ```
   pip install requests beautifulsoup4
   ```

## Usage

Run the script from the command line with various options:

1. Using default keywords and timeout:
   ```
   python gravityFalls.py
   ```

2. Specifying a custom timeout:
   ```
   python gravityFalls.py --timeout 45
   ```

3. Checking specific keywords:
   ```
   python gravityFalls.py --keywords dipper mabel stan
   ```

4. Reading keywords from a file:
   ```
   python gravityFalls.py --file keywords.txt
   ```

5. Combining options:
   ```
   python gravityFalls.py --timeout 60 --file keywords.txt
   ```

### Command-line Arguments

- `--timeout`: Set the timeout for each request in seconds (default is 30)
- `--keywords`: Provide a list of keywords to check
- `--file`: Specify a file containing keywords to check (one per line)

## Output

- Results are printed to the console.
- Valid responses are saved in a `codes` folder, organized by code.
- Checked codes are saved in `checked_codes.json` to avoid rechecking.

## Creating a Keywords File

Create a text file (e.g., `keywords.txt`) with one keyword or phrase per line:

```
dipper
mabel
stan
weirdmageddon
618
trust no one
```

## Note

This script is for educational purposes only. Please be respectful of the target website and avoid excessive requests. Ensure you comply with the website's terms of service and robot.txt file.

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.

## License

This project is open source and available under the [MIT License](LICENSE).