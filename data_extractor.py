import os
import sys

from selenium.common import NoSuchElementException

from constants import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd



class Extractor:
    """
    The Extractor class is responsible for extracting various types of data including stopwords,
    positive and negative words, URLs, and article text from the given URLs.

    Attributes:
    - driver (webdriver.Chrome): Selenium WebDriver for interacting with web pages.

    Methods:
    - __init__: Initializes the Extractor by setting up the Selenium WebDriver.
    - __enter__: Handles entering the 'with' block, returning an instance of the Extractor.
    - __exit__: Handles exiting the 'with' block, providing an opportunity for cleanup.
    - extract_stopwords: Extracts stopwords from files in a specified directory.
    - extract_positive_n_negative: Extracts positive and negative words from files in a specified directory.
    - extract_urls: Reads URLs from an Excel file and returns them as a list of tuples.
    - extract_text_and_save: Extracts article text from a given URL and saves it to a text file.

    """

    def __init__(self):
        """
        Initializes the Extractor by setting up the Selenium WebDriver.

        """
        # Initialize selenium web driver
        opts = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=opts)
        os.environ['PATH'] += DRIVER_FOLDER_PATH
        # Add options for the chrome driver if needed
        # self.driver.implicitly_wait(3)
        # self.wait = WebDriverWait(self.driver, 10)

    def __enter__(self):
        """
        Handles entering the 'with' block, returning an instance of the Extractor.

        Returns:
        - Extractor: An instance of the Extractor class.

        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Handles exiting the 'with' block, providing an opportunity for cleanup.

        """
        self.driver.quit()
        pass

    def extract_stopwords(self, directory=STOP_W_DIR):
        """
        Extracts stopwords from files in a specified directory.

        Parameters:
        - directory (str): Path to the directory containing stopwords files.

        Returns:
        - list: A list of stopwords.

        """
        stopwords = []
        for file in os.listdir(directory):
            with open(os.path.join(directory, file), 'r') as f:
                for line in f.read().split('\n'):
                    words = line.split() if line else []
                    if words:
                        stopwords.append(words[0].lower())
        return stopwords

    def extract_positive_n_negative(self, directory=POS_N_DIR):
        """
        Extracts positive and negative words from files in a specified directory.

        Parameters:
        - directory (str): Path to the directory containing positive and negative words files.

        Returns:
        - tuple: A tuple containing lists of positive and negative words.

        """
        file1, file2 = os.listdir(directory)
        positive = []
        negative = []
        with open(os.path.join(directory, file1), 'r') as f:
            positive += f.read().split('\n')
        with open(os.path.join(directory, file2), 'r') as f:
            negative += f.read().split('\n')
        return positive, negative

    def extract_urls(self):
        """
        Reads URLs from an Excel file and returns them as a list of tuples.

        Returns:
        - list: A list of tuples containing URL_ID and URL.

        """
        # Specify the path to your Excel file (xlsx)
        excel_file_path = INPUT_FILE_NAME

        # Read Excel file and store tuples in a list
        df = pd.read_excel(excel_file_path)

        # Convert DataFrame to a list of tuples and return
        return list(df.itertuples(index=False, name=None))

    def extract_text_and_save(self, url_id, url):
        """
        Extracts article text from a given URL and saves it to a text file.

        Parameters:
        - url_id (str): Identifier for the URL.
        - url (str): URL of the article.

        """
        self.driver.get(url)
        text = ''
        try:
            # Try the first XPath
            text += self.driver.find_element(By.XPATH,
                                             "/html/body/div[6]/div[2]/div/div/article/div/div/div[2]/div/div[1]/div/div[4]/div/h1").text
        except NoSuchElementException:
            try:
                # Try the second XPath
                text += self.driver.find_element(By.XPATH,
                                                 '/html/body/div[6]/article/div[1]/div[1]/div[2]/div[2]/header/h1').text
            except NoSuchElementException:
                # Handle the case when both XPaths fail
                print("Both XPaths failed to locate the text element")

        try:
            # Try the first XPath
            tags = self.driver.find_element(By.XPATH,
                                            '/html/body/div[6]/div[2]/div/div/article/div/div/div[2]/div/div[1]/div/div[11]/div')
        except NoSuchElementException:
            try:
                # Try the second XPath
                tags = self.driver.find_element(By.XPATH,
                                                '/html/body/div[6]/article/div[2]/div/div[1]/div/div[2]')
            except NoSuchElementException:
                # Handle the case when both XPaths fail
                print("Both XPaths failed to locate the tags element")
                tags = None

        if text and tags:
            for tag in tags.find_elements(By.TAG_NAME, 'p'):
                text += " " + tag.text

            for tag in tags.find_elements(By.TAG_NAME, 'ol'):
                for li in tag.find_elements(By.TAG_NAME, 'li'):
                    text += " " + li.text

            for tag in tags.find_elements(By.TAG_NAME, 'ul'):
                for li in tag.find_elements(By.TAG_NAME, 'li'):
                    text += " " + li.text

            for tag in tags.find_elements(By.TAG_NAME, 'h2'):
                text += " " + tag.text

        if not os.path.exists('extracted_text_files'):
            os.makedirs('extracted_text_files')
        with open(f'extracted_text_files/{url_id}.txt', 'w', encoding='utf-8', errors='replace') as f:
            f.write(text)
        return


