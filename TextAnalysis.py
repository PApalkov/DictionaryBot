import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words


MAX_FREQUENCY = 0.8


def read_texts(language):
    """Making dictionary: key - filename, value - text"""

    texts_path = "./texts/" + language + "/"
    files_list = os.listdir(path=texts_path)

    texts = list()
    stop_w = get_stop_words(language)
    vectorizer = CountVectorizer(stop_words=stop_w)

    for file in files_list:
        f_object = open(texts_path + file, "r")
        texts.append( delete_digits(f_object.read()) )
        f_object.close()

    vectorizer.fit_transform(texts)
    analyzer = vectorizer.build_analyzer()

    dictionary = dict()
    for i, file in enumerate(files_list):
        dictionary[file.replace(".txt", "")] = analyzer(texts[i])

    return dictionary


def delete_digits(text):
    for i in range(0, 10):
        text = text.replace(str(i), "")

    return text


def parse_texts(texts):
    """Counts the number of each word in text"""

    dictionary = dict()

    for theme in texts.keys():
        words = texts[theme]
        count_words = dict()
        for word in words:
            if word in count_words.keys():
                count_words[word] += 1
            else:
                count_words[word] = 1

        dictionary[theme] = count_words

    return dictionary


def divide_to_theme(texts):
    """Making dictionary with words of different themes"""

    df = pd.DataFrame.from_dict(texts, 'index').fillna(0)

    theme_dict = dict()
    for item in df.index:
        theme_dict[item] = dict()

    for word in df:

        word_frequency = df[word].sum()

        for i, num_of_word_in_text in enumerate(df[word]):
            if df[word][i] / word_frequency > MAX_FREQUENCY:
                if not(word in theme_dict[df.index[i]]):
                    theme_dict[df.index[i]][word] = word_frequency
                    break
        else:
            if not (word in theme_dict[df.index[i]]):
                theme_dict["COMMON"][word] = word_frequency

    return theme_dict


def get_info(language):
    texts = read_texts(language)
    print("Texts uploaded")
    texts = parse_texts(texts)
    print("words are counted")
    words = divide_to_theme(texts)
    print("Words are divided")

    return words


if __name__ == "__main__":
    all_words = get_info('english')
    for key, value in all_words.items():
        print(key, value)
        print(key, len(value))
        print()
