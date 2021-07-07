# translate_article

Helper python tool for translate web page from english to russian in educatinal purposes

## Installation

1. Install python
2. Install libraries:
* nltk
* beautifulsoup4

## Usage

1. Save desired web-page from browser to disk (html only)
2. Run `python preprocess.py`
3. Enter path to the saved web-page when prompted
4. Enter CSS-selector for page main content. You can use developer tools from browser for it
5. Mark words from page as known (`y`) or unknown (`n`). Type `stop` for interrupt
6. When Google Translate web-page opened copy translation to clipboard
7. Paste translation to prompt
8. Prepared page will be saved near the original page
