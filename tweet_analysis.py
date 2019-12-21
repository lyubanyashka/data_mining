import string_analysis_utils as utils
import operator
from nltk.stem.snowball import SnowballStemmer


def primary_tweet_analysis(tweet: str):
    return tweet


def filter(i):
    return i == ' ' or 'а' <= i <= 'я' or i == 'ё' or i == '\n'


estimation_file_name = "estimations.txt"
t_low = -2
t_up = 2
negative_idx = 0
neutral_idx = 1
positive_idx = 2


class TwitterAnalyzer:
    def __init__(self):
        self.total_words_count = 0
        self.stop_words = open("stop_words.txt", "r").read().split()
        self.stop_words = set(self.stop_words)
        self.word_to_count = dict()
        data_file = open("data.txt", "r")
        self.data = data_file.read()
        self.sorted_word_count_pair = []
        self.tweets = []

        self.tweet_to_estimation = dict()
        self.word_to_estimation = dict()

    def get_estimation(self):
        if type(self.word_to_estimation) is dict and len(self.word_to_estimation) != 0:
            return self.word_to_estimation
        f = open(estimation_file_name, "r")
        lines = f.readlines()
        for line in lines:
            res = line.split()
            if len(res) != 2:
                print("Incorrect line: {} in {}".format(line, estimation_file_name))
            self.word_to_estimation[res[0]] = int(res[1])
        f.close()

    def do(self):
        self.frequency_analysis()
        self.save_word_frequency()
        self.save_word_estimation()
        self.general_tweet_estimate()
        rules_res = ""
        rules_res += self.rule1_estimate()
        rules_res += self.rule2_estimate()
        f = open("classifications.txt", "w+")
        f.write(rules_res)
        f.close()

    def rule1_estimate(self):
        rule_res = "Rule1 name\n"

        all_tweets_estimation = [0, 0, 0]
        for _, estimation in self.tweet_to_estimation.items():
            res = neutral_idx
            total_estimation = estimation[positive_idx] - estimation[negative_idx]
            if total_estimation < t_low:
                res = negative_idx
            if total_estimation > t_up:
                res = positive_idx
            all_tweets_estimation[res] += 1
        size = len(self.tweet_to_estimation)
        rule_res += "Good - {} - {}%\n".format(all_tweets_estimation[positive_idx],
                                               100 * all_tweets_estimation[positive_idx] / size)
        rule_res += "Bad - {} - {}%\n".format(all_tweets_estimation[negative_idx],
                                              100 * all_tweets_estimation[negative_idx] / size)
        rule_res += "Neutral - {} - {}%\n".format(all_tweets_estimation[neutral_idx],
                                                  100 * all_tweets_estimation[neutral_idx] / size)
        return rule_res

    def rule2_estimate(self):
        rule_res = "Rule2 name\n"

        all_tweets_estimation = [0, 0, 0]
        for _, estimation in self.tweet_to_estimation.items():
            res = neutral_idx
            if estimation[res] < estimation[positive_idx]:
                res = positive_idx
            if estimation[res] < estimation[negative_idx]:
                res = negative_idx
            all_tweets_estimation[res] += 1
        size = len(self.tweet_to_estimation)
        rule_res += "Good - {} - {}%\n".format(all_tweets_estimation[positive_idx],
                                               100 * all_tweets_estimation[positive_idx] / size)
        rule_res += "Bad - {} - {}%\n".format(all_tweets_estimation[negative_idx],
                                              100 * all_tweets_estimation[negative_idx] / size)
        rule_res += "Neutral - {} - {}%\n".format(all_tweets_estimation[neutral_idx],
                                                  100 * all_tweets_estimation[neutral_idx] / size)
        return rule_res

    def general_tweet_estimate(self):
        self.get_estimation()
        for tweet in self.tweets:
            estimations_counter = [0, 0, 0]
            words = tweet.split()
            for word in words:
                estimation = self.word_to_estimation.get(word, 0) + 1
                estimations_counter[estimation] += 1
            self.tweet_to_estimation[tweet] = estimations_counter

    def save_word_estimation(self):
        f = open(estimation_file_name, "w+")
        for item in self.sorted_word_count_pair:
            word = item[0]
            f.write("{} 0\n".format(word))
        f.close()

    def save_word_frequency(self):
        f = open("frequency.txt", "w+")
        for item in self.sorted_word_count_pair:
            word = item[0]
            count = item[1]
            printed_str = "{} - {} - {:.3}%\n".format(word, count, 100 * count / self.total_words_count)
            f.write(printed_str)
        f.close()

    def save_tweets_length(self, tweets_len_to_count):
        f = open("twits_length.txt", "w+")
        sorted_tweets_len = sorted(tweets_len_to_count.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_tweets_len:
            tweet_len = item[0]
            count = item[1]
            printed_str = "{} - {} - {:.3}%\n".format(tweet_len, count, 100 * count / len(self.tweets))
            f.write(printed_str)
        f.close()

    def frequency_analysis(self):
        word_to_count = dict()
        tweets_len_to_count = dict()
        text = self.data
        if type(text) is not str:
            return word_to_count, tweets_len_to_count

        text = text.lower()
        text = ''.join([i for i in text if filter(i)])
        end_of_tweet = " |ENDOFTWEET| "
        text = text.replace("\n\n", end_of_tweet)
        words = text.split()
        words = [word for word in words if not word.startswith('http')]
        words = [word for word in words if word not in self.stop_words]

        stemmer = SnowballStemmer("russian")
        stemmed_words = []
        for word in words:
            if word == end_of_tweet:
                continue
            stemmed_words.append(stemmer.stem(word))
        words = stemmed_words

        self.tweets = text.split(end_of_tweet)
        for tweet in self.tweets:
            tweet_len = len(tweet.split())
            tweets_len_to_count[tweet_len] = tweets_len_to_count.get(tweet_len, 0) + 1

        words = [word for word in words if word not in end_of_tweet]
        self.total_words_count = len(words)
        for word in words:
            self.word_to_count[word] = self.word_to_count.get(word, 0) + 1
        self.sorted_word_count_pair = sorted(self.word_to_count.items(), key=operator.itemgetter(1), reverse=True)


def main():
    TwitterAnalyzer().do()
    print("End of story")


if __name__ == '__main__':
    main()
