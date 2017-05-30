import os
import pandas as pd


def read_texts():
    """Making dictionary: key - filename, value - text"""

    files_list = os.listdir(path="./texts")
    print(files_list)

    texts = {}
    for file in files_list:
        f_object = open("./texts/" + file, "r")
        texts[file] = f_object.read()
        f_object.close()

    return texts


def parse_texts(texts):
    """Counts the number of each word in text"""
    dictionary = {}
    for key in texts.keys():
        new_key = key.replace(".txt", "")
        words = list(delete_punctuation(texts[key].lower()).split())

        count_words = {}
        for word in words:
            if word in count_words.keys():
                count_words[word] += 1
            else:
                count_words[word] = 1


        dictionary[new_key] = count_words

    return dictionary


def delete_punctuation(s):
    s = s.replace('.', '')
    s = s.replace(',', '')
    s = s.replace('!', '')
    s = s.replace('?', '')
    s = s.replace('-', '')
    s = s.replace(':', '')
    s = s.replace(';', '')
    s = s.replace('\"', '')
    s = s.replace('\'', '')
    return s

def make_matrix(texts):
    df = pd.DataFrame.from_dict(texts)
    print(df)





def divide_to_theme(texts):

    for text in texts:
        pass


def main():
    texts = read_texts()
    texts = parse_texts(texts)
    make_matrix(texts)
    print(texts)



if __name__ == "__main__":
    main()
