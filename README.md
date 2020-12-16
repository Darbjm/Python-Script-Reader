# <img src='readme/eigen-logo.svg' width='400'>
 
 
<h1>Back End Test: Eigen Technologies</h1>
<h2>Problem: It takes a lot of time to read through documents and find interesting words and accompanying data.</h2>
<h2>Solution: Build a program that can find interesting words in .txt files and place them into a table along with the documents and sentences that contain them.</h2>
<br/>
<br/>
<h2>Deployment</h2>
<br/>
I have designed the program to work as simply as possible. To run it all you need is Python 3.<br/>
Use the terminal to enter Eigen_Technologies_Test_James_Darby directory and run the command: python index.py<br/>
Once completed within Eigen_Technologies_Test_James_Darby there will be interesting_words.csv.<br/>
This csv will contain a list of words from the .txt files in the textfiles folder. <br/>
These words are longer than 8 letters, the table will show their total occurrences, documents containing them and sentences containing them, sometimes the sentence will contain the word twice.<br/>
I viewed the table in vscode using Excel viewer, however it can be imported to googles sheets.<br/>
<br/>
<br/>
<h2>Use of libraries</h2>
<br/>
I could use libraries such as NLTK.
 
```
vocab = nltk.FreqDist(textexample)
print(vocab.most_common(20))
```
 
The above will return a list with the 20 most used words. <br/>
However, I would like to show my ability to work in python taking into account memory and efficiency, and will therefore try to avoid using libraries where possible in this program.
<br/>
<br/>
<h2>Interpretation</h2>
<br/>
Being asked to look for 'interesting words', to me meant either a word longer than 8 letters or proper nouns, I decided to go with words longer the 8 letters. <br/>This was because I had no way of separating proper nouns from words that just began the sentence, this would mean my top interesting words would likely not be that interesting.
<br/>
<br/>
<h2>Starting thoughts</h2>
<br/>
- When opening the .txt files I will use a context manager to reduce memory leak.<br/>
- I will use a for loop so it goes through one line at a time rather than loading the whole file. This takes into account memory issues which I spoke to David Hills about.<br/>
- I will have to loop over arrays and create a quadratic loop which is not efficient, therefore I will need to implement recursion.<br/>
<br/>
<br/>
<h2>Edge cases</h2>
<br/>
- Hyphenated words are seen as one word however in doc6 line 44 there is the word 'differences--but' I decided to count this as one word unchanged as I was unsure how to categorise it<br/>
<br/>
<br/>
<h2>Summary</h2>
<br/>
I enjoyed this test, it was challenging to start with, but I kept everything as simple as I could while keeping efficiency and memory in mind.<br/>
My first attempt I created the first loop that filtered out the interesting words and the second loop counted the words and merging their docs and sentences.<br/>
I knew I could do better than this as I thought I could do the whole process in one loop, making the process more efficient.<br/>
<br/>
After I had refactored my work I tested both attempts to see the improvements, I was really happy with the results.<br/>
I tested my work with guppy3, timeit and memory_profiler.<br/>
<br/>
<h3>First attempt</h3>
<br/>
Using timeit I tested it 3 times, in each test the program was run 10 times, the results are in seconds from my first attempt:<br/>
Program run 10 times in: 11.365320683<br/>
Program run 10 times in: 12.248684551<br/>
Program run 10 times in: 12.316931788<br/>
<br/>
average: 11.976979007333<br/>
<br/>
The memory test using guppy3 showed:<br/>
Total size = 8671092 bytes.<br/>
<br/>
<h3>Refactored code</h3>
<br/>
Using timeit I tested it 3 times, in each test the program was run 10 times, the results are in seconds from my refactored code:<br/>
Program run 10 times in: 0.9665343700000001<br/>
Program run 10 times in: 0.9260109780000001<br/>
Program run 10 times in: 0.936999086<br/>
<br/>
average: 0.943181478<br/>
<br/>
The memory test using guppy3 showed:<br/>
Total size = 4774120 bytes.<br/>
<br/>
As you can see the refactoring reduced memory usage by half and time by 11 seconds. I'm really happy with this result.
<br/>
<br/>
<h2>First attempt</h2>
<br/>

```
import re
import csv
from operator import itemgetter
import glob

interesting_words = []
EXACT_OCCURRENCES = 'Total Occurrences'
EXACT_SENTENCES = 'Sentences containing the word'
EXACT_DOCUMENTS = 'Documents'
EXACT_WORD = 'Word'


# find sentences containing the word
def find_sentences(sentence_list, word):
    sentences = set()
    for sentence in sentence_list:
        match = re.search(word, sentence.lower())
        if match:
            sentences.add('• ' + sentence)
    return sentences


# search all txt files in textfiles folder, meaning files can be removed and added
list_of_files = glob.glob('./textfiles/*.txt')
# loop through each file and read it
for file_name in list_of_files:
    # use context manager to reduce memory leaks
    with open(file_name, 'r') as txt_file:
        # go through line by line to keep memory use low
        for line in txt_file:
            # make lowercase and remove full stops, commas and new lines so its easy to match words
            clean_string = re.sub('[^\'a-zA-Z -]+', '', line)
            lowercase = clean_string.lower()
            # split the line by sentence and remove newline
            sentences_split = line.strip().split('.')
            # remove all words less than 9 letters from the line
            clean_array = [w for w in lowercase.split() if len(w) > 8]
            # add each word to the interesting words array with its Document and Sentence
            for word in clean_array:
                sentences_containing_word = find_sentences(
                    sentences_split, word)
                interesting_words.append({
                    EXACT_SENTENCES: sentences_containing_word,
                    EXACT_WORD: word,
                    EXACT_DOCUMENTS: txt_file.name.split('/')[-1],
                })

counted_words = set()
final_words = []

# find matching words
for word_dict in interesting_words:
    count = 0
    sentences = set()
    documents = set()
    # if the word has already been counted do not proceed
    # this creates a more efficient loop
    if word_dict[EXACT_WORD] not in counted_words:
        # otherwise add it to the counted words so it is not counted twice
        counted_words.add(word_dict[EXACT_WORD])
        for word in interesting_words:
            # if the words match, add 1 to count and add the words' documents and sentences into sets to avoid duplicates
            if (word_dict[EXACT_WORD] == word[EXACT_WORD]):
                count += 1
                documents.add(word[EXACT_DOCUMENTS])
                for sentence in word[EXACT_SENTENCES]:
                    sentences.add(sentence)
        # merge the information together and delete repitions
        final_words.append({
            EXACT_WORD: word_dict[EXACT_WORD],
            EXACT_OCCURRENCES: count,
            EXACT_SENTENCES: sentences,
            EXACT_DOCUMENTS: documents
        })
# sort words in order of most occurrences
sorted_words = sorted(final_words, key=itemgetter(
    EXACT_OCCURRENCES), reverse=True)
# create table headings
keys = sorted_words[0].keys()
# export as a csv
with open('tables/interesting_words.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(sorted_words)
```
 

<h2>Full Tests</h2>

<h3>Refactored code</h3>

tested using timeit each test was run 10 times
0.9665343700000001

0.9260109780000001

0.936999086


```

memory test using guppy3
Partition of a set of 37511 objects. Total size = 4774120 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  11011  29   973641  20    973641  20 str
     1   9333  25   758344  16   1731985  36 tuple
     2   2441   7   352912   7   2084897  44 types.CodeType
     3    447   1   343008   7   2427905  51 type
     4   4796  13   339255   7   2767160  58 bytes
     5   2241   6   322704   7   3089864  65 function
     6      2   0   262512   5   3352376  70 _io.BufferedWriter
     7    447   1   248800   5   3601176  75 dict of type
     8     97   0   164216   3   3765392  79 dict of module
     9      1   0   131256   3   3896648  82 _io.BufferedReader


```

```

memory test using memory_profiler
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    21     12.8 MiB     12.8 MiB           1   @profile
    22                                         def test():
    23
    24                                             # find sentences containing the word
    25     14.6 MiB      0.0 MiB        1643       def find_sentences(sentence_list, word):
    26     14.6 MiB      0.1 MiB        1642           sentences = set()
    27     14.6 MiB      0.0 MiB        8657           for sentence in sentence_list:
    28     14.6 MiB      0.6 MiB        7015               match = re.search(word, sentence.lower())
    29     14.6 MiB      0.0 MiB        7015               if match:
    30     14.6 MiB      0.2 MiB        1752                   sentences.add('• ' + sentence)
    31     14.6 MiB      0.0 MiB        1642           return sentences
    32
    33                                             # search all txt files in textfiles folder, meaning files can be removed and added
    34     12.8 MiB      0.0 MiB           1       list_of_files = glob.glob('./textfiles/*.txt')
    35                                             # loop through each file and read it
    36     14.6 MiB      0.0 MiB           7       for file_name in list_of_files:
    37                                                 # use context manager to reduce memory leaks
    38     14.4 MiB      0.0 MiB           6           with open(file_name, 'r') as txt_file:
    39                                                     # go through line by line to keep memory use low
    40     14.6 MiB      0.1 MiB         372               for line in txt_file:
    41                                                         # make lowercase and remove full stops, commas and new lines so its easy to match words
    42     14.6 MiB      0.1 MiB         366                   clean_string = re.sub('[^\'a-zA-Z -]+', '', line)
    43     14.6 MiB      0.0 MiB         366                   lowercase = clean_string.lower()
    44                                                         # split the line by sentence and remove newline
    45     14.6 MiB      0.1 MiB         366                   sentences_split = line.strip().split('.')
    46                                                         # remove all words less than 9 letters from the line
    47     14.6 MiB     -0.1 MiB       20914                   clean_array = [w for w in lowercase.split() if len(w) > 8]
    48                                                         # add each word to the interesting words array with its Document and Sentence
    49     14.6 MiB     -0.0 MiB        2008                   for word in clean_array:
    50     14.6 MiB      0.0 MiB        1642                       sentences_containing_word = find_sentences(
    51     14.6 MiB      0.0 MiB        1642                           sentences_split, word)
    52                                                             # remove none from find_sentences
    53     14.6 MiB      0.0 MiB        1642                       if sentences_containing_word:
    54                                                                 # if the word has already been counted add its data to the data already there
    55     14.6 MiB      0.0 MiB        1637                           if word in word_count:
    56     14.6 MiB      0.0 MiB         790                               word_count[word] += 1
    57     14.6 MiB      0.0 MiB         790                               documents[word].add(
    58     14.6 MiB      0.0 MiB         790                                   '• ' + txt_file.name.split('/')[-1])
    59     14.6 MiB      0.0 MiB        1685                               for sentence in sentences_containing_word:
    60     14.6 MiB      0.0 MiB         895                                   sentences[word].add(sentence)
    61                                                                 # if the word is not in word_count create those entries and add them
    62     14.6 MiB      0.0 MiB        1637                           if word not in word_count:
    63     14.6 MiB      0.0 MiB         847                               word_count[word] = 1
    64                                                                     # use sets to avoid duplicates
    65                                                                     # adding the line directly into the set using .set(sentence_containing_word) caused the line to be split into letters
    66                                                                     # so use set([]) to avoid this
    67     14.6 MiB      0.0 MiB         847                               documents[word] = set(
    68     14.6 MiB      0.1 MiB         847                                   ['• ' + txt_file.name.split('/')[-1]])
    69     14.6 MiB      0.1 MiB         847                               sentences[word] = set()
    70     14.6 MiB      0.0 MiB        1704                               for sentence in sentences_containing_word:
    71     14.6 MiB      0.0 MiB         857                                   sentences[word].add(sentence)
    72
    73                                             # find digits in the text
    74
    75     15.0 MiB     -0.1 MiB        3388       def numbers_in_text(doc):
    76     15.0 MiB     -0.2 MiB        3387           return int(doc) if doc.isdigit() else doc
    77
    78                                             # if the documents' titles have numbers in them it will order them
    79
    80     15.0 MiB     -0.1 MiB        1130       def natural_keys(text):
    81     15.0 MiB     -0.3 MiB        6774           return [numbers_in_text(doc) for doc in re.split(r'(\d+)', text)]
    82
    83     14.6 MiB      0.0 MiB           1       merge_words = []
    84
    85     15.0 MiB     -0.0 MiB         848       for key in word_count.keys():
    86                                                 # format each sentence for easier reading
    87     15.0 MiB     -0.0 MiB         847           sentences_list = list(sentences[key])
    88     15.0 MiB     -0.1 MiB        4166           formatted_sentences = ('\n' + '\n').join(str(sentence)
    89     15.0 MiB      0.0 MiB        4097                                                    for sentence in sentences_list)
    90                                                 # format each document for easier reading
    91     15.0 MiB     -0.0 MiB         847           document_list = list(documents[key])
    92     15.0 MiB     -0.0 MiB         847           document_list.sort(key=natural_keys)
    93     15.0 MiB     -0.1 MiB        3670           formatted_documents = ('\n' + '\n').join(str(doc)
    94     15.0 MiB     -0.0 MiB        3105                                                    for doc in document_list)
    95     15.0 MiB     -0.0 MiB         847           merge_words.append({
    96     15.0 MiB     -0.0 MiB         847               EXACT_WORD: key,
    97     15.0 MiB     -0.0 MiB         847               EXACT_OCCURRENCES: word_count[key],
    98     15.0 MiB     -0.0 MiB         847               EXACT_SENTENCES: formatted_sentences,
    99     15.0 MiB     -0.0 MiB         847               EXACT_DOCUMENTS: formatted_documents
   100                                                 })
   101
   102                                             # sort words in order of most occurrences
   103     15.0 MiB      0.0 MiB           1       sorted_words = sorted(merge_words, key=itemgetter(
   104     15.0 MiB      0.0 MiB           1           EXACT_OCCURRENCES), reverse=True)
   105                                             # create table headings
   106     15.0 MiB      0.0 MiB           1       keys = sorted_words[0].keys()
   107                                             # export as a csv
   108     15.0 MiB      0.0 MiB           1       with open('tables/interesting_words.csv', 'w', newline='') as output_file:
   109     15.0 MiB      0.0 MiB           1           dict_writer = csv.DictWriter(output_file, keys)
   110     15.0 MiB      0.0 MiB           1           dict_writer.writeheader()
   111     15.1 MiB      0.1 MiB           1           dict_writer.writerows(sorted_words)

```

<h3>First attempt</h3>

tested using timeit each test was run 10 times
11.365320683

12.248684551

12.316931788

```

memory test using guppy3
Partition of a set of 70694 objects. Total size = 8671092 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0  20546  29  1917461  22   1917461  22 str
     1  18707  26  1535568  18   3453029  40 tuple
     2   4725   7   682856   8   4135885  48 types.CodeType
     3   9424  13   676270   8   4812155  55 bytes
     4   4618   7   664992   8   5477147  63 function
     5    722   1   610544   7   6087691  70 type
     6    722   1   410616   5   6498307  75 dict of type
     7    181   0   308528   4   6806835  79 dict of module
     8    600   1   286400   3   7093235  82 dict (no owner)
     9      2   0   262512   3   7355747  85 _io.BufferedWriter

```

```

memory test using memory_profiler
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
   156     12.8 MiB     12.8 MiB           1   @profile
   157                                         def test():
   158     14.9 MiB      0.0 MiB        1643       def find_sentences(sentence_list, word):
   159     14.9 MiB      0.2 MiB        1642           sentences = set()
   160     14.9 MiB     -0.2 MiB        8657           for sentence in sentence_list:
   161     14.9 MiB      0.5 MiB        7015               match = re.search(word, sentence.lower())
   162     14.9 MiB     -0.1 MiB        7015               if match:
   163     14.9 MiB      0.3 MiB        1752                   sentences.add('• ' + sentence)
   164     14.9 MiB     -0.0 MiB        1642           return sentences
   165
   166                                             # search all txt files in textfiles folder, meaning files can be removed and added
   167     12.8 MiB      0.0 MiB           1       list_of_files = glob.glob('./textfiles/*.txt')
   168                                             # loop through each file and read it
   169     14.9 MiB      0.0 MiB           7       for file_name in list_of_files:
   170                                                 # use context manager to reduce memory leaks
   171     14.5 MiB      0.0 MiB           6           with open(file_name, 'r') as txt_file:
   172                                                     # go through line by line to keep memory use low
   173     14.9 MiB      0.1 MiB         372               for line in txt_file:
   174                                                         # make lowercase and remove full stops, commas and new lines so its easy to match words
   175     14.9 MiB      0.1 MiB         366                   clean_string = re.sub('[^\'a-zA-Z -]+', '', line)
   176     14.9 MiB      0.1 MiB         366                   lowercase = clean_string.lower()
   177                                                         # split the line by sentence and remove newline
   178     14.9 MiB      0.1 MiB         366                   sentences_split = line.strip().split('.')
   179                                                         # remove all words less than 9 letters from the line
   180     14.9 MiB      0.1 MiB       20914                   clean_array = [w for w in lowercase.split() if len(w) > 8]
   181                                                         # add each word to the interesting words array with its Document and Sentence
   182     14.9 MiB     -0.0 MiB        2008                   for word in clean_array:
   183     14.9 MiB     -0.0 MiB        1642                       sentences_containing_word = find_sentences(
   184     14.9 MiB      0.0 MiB        1642                           sentences_split, word)
   185
   186     14.9 MiB     -0.0 MiB        1642                       interesting_words.append({
   187     14.9 MiB     -0.0 MiB        1642                           EXACT_SENTENCES: sentences_containing_word,
   188     14.9 MiB     -0.0 MiB        1642                           EXACT_WORD: word,
   189     14.9 MiB     -0.0 MiB        1642                           EXACT_DOCUMENTS: txt_file.name.split('/')[-1],
   190                                                             })
   191
   192     14.9 MiB      0.0 MiB           1       counted_words = set()
   193     14.9 MiB      0.0 MiB           1       final_words = []
   194
   195                                             # find matching words
   196     15.6 MiB      0.0 MiB        1643       for word_dict in interesting_words:
   197     15.5 MiB      0.0 MiB        1642           count = 0
   198     15.5 MiB      0.4 MiB        1642           sentences = set()
   199     15.5 MiB      0.0 MiB        1642           documents = set()
   200                                                 # if the word has already been counted do not proceed
   201                                                 # this creates a more efficient loop
   202     15.5 MiB      0.0 MiB        1642           if word_dict[EXACT_WORD] not in counted_words:
   203                                                     # otherwise add it to the counted words so it is not counted twice
   204     15.5 MiB      0.0 MiB         851               counted_words.add(word_dict[EXACT_WORD])
   205     15.5 MiB      0.0 MiB     1398193               for word in interesting_words:
   206                                                         # if the words match, add 1 to count and add the words' documents and sentences into sets to avoid duplicates
   207     15.5 MiB      0.0 MiB     1397342                   if (word_dict[EXACT_WORD] == word[EXACT_WORD]):
   208     15.5 MiB      0.0 MiB        1642                       count += 1
   209     15.5 MiB      0.0 MiB        1642                       documents.add(word[EXACT_DOCUMENTS])
   210     15.5 MiB      0.0 MiB        3394                       for sentence in word[EXACT_SENTENCES]:
   211     15.5 MiB      0.1 MiB        1752                           sentences.add(sentence)
   212                                                     # merge the information together and delete repitions
   213     15.5 MiB      0.0 MiB         851               final_words.append({
   214     15.5 MiB      0.0 MiB         851                   EXACT_WORD: word_dict[EXACT_WORD],
   215     15.5 MiB      0.0 MiB         851                   EXACT_OCCURRENCES: count,
   216     15.5 MiB      0.0 MiB         851                   EXACT_SENTENCES: sentences,
   217     15.6 MiB      0.1 MiB         851                   EXACT_DOCUMENTS: documents
   218                                                     })
   219                                             # sort words in order of most occurrences
   220     15.6 MiB      0.0 MiB           1       sorted_words = sorted(final_words, key=itemgetter(
   221     15.6 MiB      0.0 MiB           1           EXACT_OCCURRENCES), reverse=True)
   222                                             # create table headings
   223     15.6 MiB      0.0 MiB           1       keys = sorted_words[0].keys()
   224                                             # export as a csv
   225     15.6 MiB      0.0 MiB           1       with open('tables/interesting_words.csv', 'w', newline='') as output_file:
   226     15.6 MiB      0.0 MiB           1           dict_writer = csv.DictWriter(output_file, keys)
   227     15.6 MiB      0.0 MiB           1           dict_writer.writeheader()
   228     15.7 MiB      0.1 MiB           1           dict_writer.writerows(sorted_words)

```