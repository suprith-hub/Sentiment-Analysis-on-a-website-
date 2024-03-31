# Import necessary libraries and modules
import os
import re
import nltk
import pandas as pd
from constants import EXTRACTED_DATA_FOLDER, PERSONAL_PRONOUNS
from helpers.syllables_count import sylco


class Analyser:
    """
    The Analyser class performs text analysis on the content extracted from URLs.

    Attributes:
    - positive_words (set): Set of positive words.
    - negative_words (set): Set of negative words.
    - stopwords (set): Set of stopwords.
    - personal_pronouns (int): Count of personal pronouns.
    - number_of_words (int): Count of words in the text.
    - number_of_sentences (int): Count of sentences in the text.
    - complex_words_count (int): Count of complex words.

    Methods:
    - positive_score: Calculates the positive score for a given set of words.
    - negative_score: Calculates the negative score for a given set of words.
    - polarity_score: Calculates the polarity score using positive and negative scores.
    - subjectivity_score: Calculates the subjectivity score using positive, negative scores, and the number of words.
    - average_sentence_length: Calculates the average sentence length.
    - complex_words: Identifies and counts complex words in a set of words.
    - average_word_length: Calculates the average word length.
    - syllable_count: Calculates the syllable count for a given word.
    - clean: Cleans and filters a set of words.
    - clean_stop_words: Removes stopwords from a set of words.
    - analyse: Performs text analysis and writes the results to an output CSV file.

    """

    def __init__(self, positive_words, negative_words, stopwords):
        """
        Initializes the Analyser with sets of positive words, negative words, and stopwords.

        """
        self.positive_words = set(positive_words)
        self.negative_words = set(negative_words)
        self.stopwords = set(stopwords)
        self.personal_pronouns = 0
        self.number_of_words = 0
        self.number_of_sentences = 0
        self.complex_words_count = 0

    def positive_score(self, words):
        """
        Calculates the positive score for a given set of words.

        Parameters:
        - words (list): List of words.

        Returns:
        - int: Positive score.

        """
        return len(self.positive_words.intersection(words))

    def negative_score(self, words):
        """
        Calculates the negative score for a given set of words.

        Parameters:
        - words (list): List of words.

        Returns:
        - int: Negative score.

        """
        return len(self.negative_words.intersection(words))

    def polarity_score(self, positive_score, negative_score):
        """
        Calculates the polarity score using positive and negative scores.

        Parameters:
        - positive_score (int): Positive score.
        - negative_score (int): Negative score.

        Returns:
        - float: Polarity score.

        """
        return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    def subjectivity_score(self, positive_score, negative_score, num_words):
        """
        Calculates the subjectivity score using positive, negative scores, and the number of words.

        Parameters:
        - positive_score (int): Positive score.
        - negative_score (int): Negative score.
        - num_words (int): Number of words.

        Returns:
        - float: Subjectivity score.

        """
        return (positive_score + negative_score) / (num_words + 0.000001)

    def average_sentence_length(self, words, sentences):
        """
        Calculates the average sentence length.

        Parameters:
        - words (list): List of words.
        - sentences (list): List of sentences.

        Returns:
        - float: Average sentence length.

        """
        return len(words) / len(sentences)

    def complex_words(self, words):
        """
        Identifies and counts complex words in a set of words.

        Parameters:
        - words (list): List of words.

        Returns:
        - list: List of complex words.

        """
        complex_words = [word for word in words if self.syllable_count(word) > 2]
        self.complex_words_count = len(complex_words)
        return complex_words

    def average_word_length(self, words):
        """
        Calculates the average word length.

        Parameters:
        - words (list): List of words.

        Returns:
        - float: Average word length.

        """
        return sum(len(word) for word in words) / len(words) if words else 0.0

    def syllable_count(self, word):
        """
        Calculates the syllable count for a given word.

        Parameters:
        - word (str): A word.

        Returns:
        - int: Syllable count.

        """
        return sylco(word) if word else 0.0

    def clean(self, words):
        """
        Cleans and filters a set of words.

        Parameters:
        - words (list): List of words.

        Returns:
        - list: List of cleaned and filtered words.

        """

        def clean_and_filter(text):
            # Use regular expression to remove non-alphabetic characters
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text).strip()
            if cleaned_text in PERSONAL_PRONOUNS:
                self.personal_pronouns += 1
            return cleaned_text.lower()

        words = [clean_and_filter(word) for word in words]
        words = [word for word in words if word]
        return words

    def clean_stop_words(self, words):
        """
        Removes stopwords from a set of words.

        Parameters:
        - words (list): List of words.

        Returns:
        - list: List of words after removing stopwords.

        """
        words = [word for word in words if word not in self.stopwords]
        return words

    def analyse(self, url_id, url):
        """
        Performs text analysis and writes the results to an output CSV file.

        Parameters:
        - url_id (str): Identifier for the URL.
        - url (str): URL of the article.

        """
        text = open(os.path.join(EXTRACTED_DATA_FOLDER, url_id + ".txt"), encoding='utf-8').read()

        if not text:
            # write all these into output.csv file for unique url_id
            # Create a DataFrame with the extracted values
            data = {
                'URL_ID': [url_id],
                'URL': [url],
                'POSITIVE SCORE': ['NaN'],
                'NEGATIVE SCORE': ['NaN'],
                'SUBJECTIVITY SCORE': ['NaN'],
                'POLARITY SCORE': ['NaN'],
                'AVG SENTENCE LENGTH': ['NaN'],
                'PERCENTAGE OF COMPLEX WORDS': ['NaN'],
                'FOG INDEX': ['NaN'],
                'AVG NUMBER OF WORDS PER SENTENCE': ['NaN'],
                'COMPLEX WORD COUNT': ['NaN'],
                'WORD COUNT': ['NaN'],
                'SYLLABLE PER WORD': ['NaN'],
                'PERSONAL PRONOUNS': ['NaN'],
                'AVG WORD LENGTH': ['NaN']
            }

            df = pd.DataFrame(data)

            # Specify the path to the CSV file
            output_csv_path = 'output.csv'

            # Write the DataFrame to a CSV file
            df.to_csv(output_csv_path, index=False, mode='a',
                      header=not os.path.exists(output_csv_path))  # 'a' for append
            return

        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)

        words = self.clean(words)

        # considered removal of punctuation marks before going on except stopwords
        # which will be removed from step 5
        self.number_of_words = len(words)
        self.number_of_sentences = len(sentences)

        # task 1.3
        positive_score = self.positive_score(words)
        negative_score = self.negative_score(words)
        polarity_score = self.polarity_score(positive_score, negative_score)
        subjectivity_score = self.subjectivity_score(positive_score, negative_score, len(words))

        # task 2: analyse readability
        average_sentence_length = self.average_sentence_length(words, sentences)
        complex_words = self.complex_words(words)
        percentage_of_complex_words = self.complex_words_count / self.number_of_words
        fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words)

        # task 3:
        average_number_of_words_per_sentence = self.number_of_words / self.number_of_sentences

        # task 4:
        complex_word_count = self.complex_words_count

        # task 5: from here I have considered all steps exclude stopwords
        words = self.clean_stop_words(words)
        word_count = len(words)

        # task 6:
        syllable_per_word = sum(self.syllable_count(word) for word in words) / len(words) if words else 0.0

        #  task 7:
        personal_pronouns = self.personal_pronouns

        # task 8:
        average_word_length = self.average_word_length(words)

        # write all these into output.csv file for unique url_id
        # Create a DataFrame with the extracted values
        data = {
            'URL_ID': [url_id],
            'URL': [url],
            'POSITIVE SCORE': [positive_score],
            'NEGATIVE SCORE': [negative_score],
            'SUBJECTIVITY SCORE': [subjectivity_score],
            'POLARITY SCORE': [polarity_score],
            'AVG SENTENCE LENGTH': [average_sentence_length],
            'PERCENTAGE OF COMPLEX WORDS': [percentage_of_complex_words],
            'FOG INDEX': [fog_index],
            'AVG NUMBER OF WORDS PER SENTENCE': [average_number_of_words_per_sentence],
            'COMPLEX WORD COUNT': [complex_word_count],
            'WORD COUNT': [word_count],
            'SYLLABLE PER WORD': [syllable_per_word],
            'PERSONAL PRONOUNS': [personal_pronouns],
            'AVG WORD LENGTH': [average_word_length]
        }

        df = pd.DataFrame(data)

        # Specify the path to the CSV file
        output_csv_path = 'output.csv'

        # Write the DataFrame to a CSV file
        df.to_csv(output_csv_path, index=False, mode='a', header=not os.path.exists(output_csv_path))  # 'a' for append
