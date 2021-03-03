import re
import csv
from operator import itemgetter
import glob

interesting_words = []
word_count = {}
sentences = {}
documents = {}
EXACT_OCCURRENCES = 'Total occurrences'
EXACT_SENTENCES = 'Sentences containing the word'
EXACT_DOCUMENTS = 'Documents'
EXACT_WORD = 'Word'

def main():
    # search all txt files in textfiles folder, meaning files can be removed and added
    list_of_files = glob.glob('./textfiles/*.txt')
    # loop through each file and read it
    for file_name in list_of_files:
        # use context manager to reduce memory leaks
        with open(file_name, 'r') as txt_file:
            # go through line by line to keep memory use low
            for line in txt_file:
                # make lower case and remove full stops, commas and new lines so its easy to match words
                clean_string = re.sub('[^\'a-zA-Z -]+', '', line)
                lower_case = clean_string.lower()
                # split the line by sentence and remove newline
                sentences_split = line.strip().split('.')
                # remove all words less than 9 letters from the line
                clean_array = [w for w in lower_case.split() if len(w) > 8]
                # add each word to the interesting words array with its Document and Sentence
                for word in clean_array:
                    sentences_containing_word = find_sentences(
                        sentences_split, word)
                    # remove none from find_sentences function
                    if sentences_containing_word:
                        # if the word has already been counted add its data to the data already there
                        if word in word_count:
                            word_count[word] += 1
                            documents[word].add(
                                '• ' + txt_file.name.split('/')[-1])
                            for sentence in sentences_containing_word:
                                sentences[word].add(sentence)
                        # if the word is not in word_count create those entries and add them
                        if word not in word_count:
                            word_count[word] = 1
                            # use sets to avoid duplicates
                            # adding the line directly into the set using .set(sentence_containing_word) caused the line to be split into letters
                            # so use set([]) to avoid this
                            documents[word] = set(
                                ['• ' + txt_file.name.split('/')[-1]])
                            sentences[word] = set()
                            for sentence in sentences_containing_word:
                                sentences[word].add(sentence)
    place_words_in_csv()

# find sentences containing the word
def find_sentences(sentence_list, word):
    sentences = set()
    for sentence in sentence_list:
        match = re.search(word, sentence.lower())
        if match:
            sentences.add('• ' + sentence)
    return sentences


# find digits in the text
def numbers_in_text(doc):
    return int(doc) if doc.isdigit() else doc


# if the documents' titles have numbers in them it will order them
def natural_keys(text):
    return [numbers_in_text(doc) for doc in re.split(r'(\d+)', text)]


merge_words = []

def place_words_in_csv():
    for key in word_count.keys():
        # format each sentence for easier reading
        sentences_list = list(sentences[key])
        formatted_sentences = ('\n' + '\n').join(str(sentence)
                                                for sentence in sentences_list)
        # format each document for easier reading
        document_list = list(documents[key])
        document_list.sort(key=natural_keys)
        formatted_documents = ('\n' + '\n').join(str(doc)
                                                for doc in document_list)
        merge_words.append({
            EXACT_WORD: key,
            EXACT_OCCURRENCES: word_count[key],
            EXACT_SENTENCES: formatted_sentences,
            EXACT_DOCUMENTS: formatted_documents
        })
    # sort words in order of most occurrences
    sorted_words = sorted(merge_words, key=itemgetter(
        EXACT_OCCURRENCES), reverse=True)
    # create table headings
    keys = sorted_words[0].keys()
    # export as a csv
    with open('interesting_words.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(sorted_words)

if __name__ == "__main__":
    main()