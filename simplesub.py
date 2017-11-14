from pycipher import SimpleSubstitution as SimpleSub
from math import log10
import random
import re
import sys

class heristic(object):
    def __init__(self, grams):
        self.map = {}
        fp = open(grams, 'r', encoding='utf-8')
        for line in fp:
            line = line.strip()
            if line == '': continue
            key, count = line.split()
            self.map[key] = int(count)
        fp.close()
        self.key_length = len(key)
        total = sum(self.map.values())
        for key in self.map.keys():
            self.map[key] = log10(float(self.map[key] / total))
        self.min_score = log10(0.01 / total)

    def score(self, text):
        score = 0
        getitem = self.map.__getitem__
        for i in range(len(text) - self.key_length + 1):
            obj = text[i:i + self.key_length]
            if obj in self.map: score += getitem(obj)
            else: score += self.min_score
        return score

def encipher_with_format(text, key):
    sub_list = {}
    for i in range(len(key)):
        sub_list[chr(i + ord('A'))] = key[i]
        sub_list[chr(i + ord('a'))] = key[i].lower()

    text_list = list(text)
    for i in range(len(text_list)):
        if text_list[i] in sub_list:
            text_list[i] = sub_list[text_list[i]]

    return ''.join(text_list)

def decipher_with_format(text, key):
    sub_list = {}
    for i in range(len(key)):
        sub_list[key[i]] = chr(i + ord('A'))
        sub_list[key[i].lower()] = chr(i + ord('a'))

    text_list = list(text)
    for i in range(len(text_list)):
        if text_list[i] in sub_list:
            text_list[i] = sub_list[text_list[i]]

    return ''.join(text_list)

def generate_key(text):
    en = re.sub('^[A-Z]', '', s.upper())
    test = heristic('english_quadgrams.txt')
    max_score = -1e10
    max_key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    parent_score, parent_key = max_score, max_key[:]

    try:
        count = 0
        while(True):
            count += 1
            random.shuffle(parent_key)
            de = SimpleSub(parent_key).decipher(en)
            parent_score = test.score(de)
            i = 0
            while i < 1000:
                a = random.randint(0, 25)
                b = random.randint(0, 25)
                child_key = parent_key[:]
                child_key[a], child_key[b] = child_key[b], child_key[a]
                de = SimpleSub(child_key).decipher(en)
                child_score = test.score(de)
                if child_score > parent_score:
                    parent_score, parent_key = child_score, child_key[:]
                    i = 0
                i += 1

            if parent_score > max_score:
                max_score, max_key = parent_score, parent_key[:]
                print('current score', max_score, 'on iteration', count)
                print('key:', ''.join(max_key))
                print('text:', decipher_with_format(s, max_key))

    except KeyboardInterrupt:
        return max_key

    except:
        print('error.')
        sys.exit()

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('arg error.')
        sys.exit()
    filename = sys.argv[1];
    fp = open(filename, 'r', encoding='utf-8')
    s = fp.read()
    fp.close()

    print('try to decode text in', filename)
    print('press ctrl+c to finish process when correct text is displayed.')
    key = generate_key(s)

    print('best key:', ''.join(key))
    print('decoded text has been saved in de_%s' % filename)
    s = decipher_with_format(s, key)
    fp = open('de_' + filename, 'w', encoding='utf-8')
    fp.write(s)
    fp.close()
