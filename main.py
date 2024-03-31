# main.py

from data_extractor import Extractor
from analysis import Analyser
from helpers.create_file import create_output_csv_file

def main():
    """
    The main script orchestrating the data extraction and text analysis process.

    Steps:
    1. Initialize Extractor to retrieve positive/negative words, stopwords, and URLs.
    2. Initialize Analyser with extracted word lists and stopwords.
    3. Create an output CSV file.
    4. For each URL, extract text and save to a text file, then perform text analysis and save the results.

    Usage:
    Run this script to execute data extraction and text analysis.

    Note:
    Ensure the required dependencies are installed before running the script.

    """

    with Extractor() as extractor:
        positive_words, negative_words = extractor.extract_positive_n_negative()
        stopwords = extractor.extract_stopwords()
        analyser = Analyser(positive_words, negative_words, stopwords)

        list_of_urls = extractor.extract_urls()

        create_output_csv_file()
        for (url_id, url) in list_of_urls:
            extractor.extract_text_and_save(url_id, url)
            analyser.analyse(url_id, url)

if __name__ == '__main__':
    main()



