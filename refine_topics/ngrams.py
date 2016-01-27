import re


def __read_ngrams__(dir_file):
    ngrams = {}
    with open(dir_file) as f:
        for l in f:
            l_parts = re.split(' |\t', l.strip('\n'))
            parts_length = len(l_parts)
            if parts_length == 3 and l_parts[2].isdigit():
                word_one = l_parts[0]
                word_two = l_parts[1]
                ngram_count = int(l_parts[2])
                ngrams[word_one + " " + word_two] = ngram_count
            elif parts_length == 2 and l_parts[1].isdigit():
                word_one = l_parts[0]
                ngram_count = l_parts[1]
                ngrams[word_one] = int(ngram_count)
            else:
                with open('/Users/junk_ngrams.txt', 'a') as junk_file:
                    junk_file.write(l)
        f.close()
    return ngrams


