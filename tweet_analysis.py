import string_analysis_utils as utils
import operator


def primary_tweet_analysis(tweet: str):
    return tweet


def frequency_analysis(data: str):
    word_to_frequency = utils.calculate_frequences(data)
    filtered_words = {k: v for k, v in word_to_frequency.items() if not k.startswith('http') and v > 5}
    sorted_word_to_frequency = sorted(filtered_words.items(), key=operator.itemgetter(1), reverse=True)


    return sorted_word_to_frequency


class TwitterAnalyzer:
    def __init__(self):
        #self.stop_words = open("stop_words_file.txt", "r").read().split()
        self.stop_if_contains = ["http"]
        data_file = open("data.txt", "r")
        self.data = data_file.read()

    def do(self):
        word_to_frequency = frequency_analysis(self.data)


def main():
    TwitterAnalyzer().do()
    print("End of story")


if __name__ == '__main__':
    main()
