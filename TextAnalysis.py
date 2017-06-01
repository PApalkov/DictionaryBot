import os
import pandas as pd

MAX_FREQUENCY = 0.99

def read_texts():
    """Making dictionary: key - filename, value - text"""

    files_list = os.listdir(path="./texts")

    texts = dict()

    for file in files_list:
        f_object = open("./texts/" + file, "r")
        texts[file] = f_object.read()
        f_object.close()

    return texts


def parse_texts(texts):
    """Counts the number of each word in text"""

    dictionary = dict()

    for key in texts.keys():
        new_key = key.replace(".txt", "")

        words = list(delete_punctuation(texts[key].lower()).split())

        count_words = dict()
        for word in words:
            if word in count_words.keys():
                count_words[word] += 1
            else:
                count_words[word] = 1

        dictionary[new_key] = count_words


    return dictionary


def delete_punctuation(s):
    #todo optimize
    """Deleting punctuation and other stuff"""
    s = s.replace('.', '')
    s = s.replace(',', '')
    s = s.replace('!', '')
    s = s.replace('?', '')
    s = s.replace('-', '')
    s = s.replace(':', '')
    s = s.replace(';', '')
    s = s.replace('\"', '')
    s = s.replace('\'', '')
    s = s.replace('/', ' ')
    s = s.replace('(', ' ')
    s = s.replace(')', ' ')

    return s


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

    return theme_dict


def all_words_from_texts(texts):
    all_words = dict()

    for text in texts.keys():
        for word in texts[text]:
            if word in all_words:
                all_words[word] += texts[text][word]
            else:
                all_words[word] = texts[text][word]

    return all_words


def get_info():
    texts = read_texts()
    texts = parse_texts(texts)

    special_words = divide_to_theme(texts)
    all_words = all_words_from_texts(texts)

    return all_words, special_words



#todo delete short words
if __name__ == "__main__":
    all_words, special_words = get_info()

    for key, value in all_words.items():
        print(key, value)


    print()
    print()

    for key, value in special_words.items():
        print(key, value)
        print(key, len(value))
        print()
