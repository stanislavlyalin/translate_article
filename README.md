# translate_article

Helper python tool for translate web page from english to russian in educatinal purposes

Original page (fragment)

![Original page](images/original.png)

Page after processing (fragment)

![Page after processing](images/preprocessed.png)


## Installation

1. Install python
2. Install libraries:
* nltk
* beautifulsoup4
* eng-to-ipa

## Usage

1. Save desired web-page from browser to disk (html only)
2. Run `python preprocess.py`
3. Enter path to the saved web-page when prompted
4. Enter CSS-selector for page main content. You can use developer tools from browser for it
5. Mark words from page as known (`y`) or unknown (`n`). Type `stop` for interrupt
6. When Google Translate web-page opened copy translation to clipboard
7. Paste translation to prompt
8. Prepared page will be saved near the original page

If you want to get **pdf** from processed page, use **Print to pdf function** in your browser.

## Use as dictionary for learning words

You can open file `unknown.txt` in Excel to use it as dictionary for learning words. See screenshot below:

![Use as dictionary for learning words](images/use_as_dict.png)
