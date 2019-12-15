def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    word_to_count = dict()
    if type(text) is not str:
        return word_to_count
    text = ''.join([i for i in text if i.isalpha() or i == ' '])
    text = text.lower()
    words = text.split()

    for word in words:
        word_to_count[word] = word_to_count.get(word, 0) + 1
    return word_to_count


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from the given frequencies dictionary
    """
    if stop_words is None or frequencies is None:
        return {}
    for key in stop_words:
        if key in frequencies:
            frequencies.pop(key)

    result_dict = {}
    for key, value in frequencies.items():
        if type(key) is str:
            result_dict[key] = value

    return result_dict


def get_top_n(result_dict: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    if len(result_dict) == 0 or top_n <= 0:
        list_of_top_n = ()
        return list_of_top_n
    list_of_top_n = tuple(sorted(result_dict, key=result_dict.get, reverse=True))
    return list_of_top_n[:top_n]
