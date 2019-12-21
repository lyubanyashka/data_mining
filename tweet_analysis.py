import string_analysis_utils as utils
import operator
from nltk.stem.snowball import SnowballStemmer


def primary_tweet_analysis(tweet: str):
    return tweet




class TwitterAnalyzer:
    def __init__(self):
        self.stop_words = open("stop_words.txt", "r").read().split()
        self.stop_words = set(self.stop_words)
        self.stop_if_contains = ["http"]
        data_file = open("data.txt", "r")
        self.data = data_file.read()

    def do(self):
        word_to_frequency = self.frequency_analysis(self.data)

    def stemmer_test(self):
        stemmer = SnowballStemmer("russian")
        my_words = ['Василий', 'Геннадий', 'Виталий']
        l = [stemmer.stem(word) for word in my_words]
        print(l)

    def frequency_analysis(self, data: str):
        word_to_frequency = utils.calculate_frequences(data)
        filtered_words = {k: v for k, v in word_to_frequency.items() if
                          not k.startswith('http') and v > 5}
        filtered_words = {k: v for k, v in filtered_words.items() if k not in self.stop_words}

        stemmer = SnowballStemmer("russian")
        stemmed_words = dict()
        for word, freq in filtered_words.items():
            stemmed_key = stemmer.stem(word)
            stemmed_words[stemmed_key] = filtered_words.get(stemmed_key, 0) + freq

        sorted_word_to_frequency = sorted(stemmed_words.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_word_to_frequency


def main():
    TwitterAnalyzer().do()
    print("End of story")


if __name__ == '__main__':
    main()
