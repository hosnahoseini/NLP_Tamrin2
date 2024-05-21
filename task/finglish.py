import re
from re import sub
import itertools
import re
import itertools

class TextProcessor:
    def __init__(self, special_words, numbers, two_char, one_char, multiple_char):
        self.special_words = special_words
        self.numbers = numbers
        self.kha_pattern = {
            'kha':['@'],
        }
        self.two_char = two_char
        self.one_char = one_char
        self.multiple_char = multiple_char


        self.dic = self.load_dictionary("task/normalize.txt")
        self.frequencies = self.load_frequency_file("task/persian-wikipedia.txt")

    def preprocess_text(self, text):
        # حذف فضای اضافه از ابتدا و انتهای متن
        text = text.strip()
        # تبدیل فاصله‌های متعدد به یک فاصله
        text = re.sub(r'\s+', ' ', text)
        # تبدیل متن به حروف کوچک
        return text.lower()

    # درست کردن نیم فاصله ها
    def space_correction(self, text):
        a00 = r'^(بی|می|نمی)( )'
        b00 = r'\1‌'
        c00 = re.sub(a00, b00, text)
        a0 = r'( )(می|نمی|بی)( )'
        b0 = r'\1\2‌'
        c0 = re.sub(a0, b0, c00)
        a1 = r'( )(هایی|ها|های|ایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ات|ان|ین' \
             r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست)( )'
        b1 = r'‌\2\3'
        c1 = re.sub(a1, b1, c0)
        a2 = r'( )(شده|نشده)( )'
        b2 = r'‌\2‌'
        c2 = re.sub(a2, b2, c1)
        a3 = r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
             r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
             r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        b3 = r'‌\2\3'
        c3 = re.sub(a3, b3, c2)
        return c3

    def space_correction_2(self, text):
        out_sentences = ''
        for wrd in text.split(' '):
            try:
                out_sentences = out_sentences + ' ' + self.dic[wrd]
            except KeyError:
                out_sentences = out_sentences + ' ' + wrd
        return out_sentences

    @staticmethod
    def load_frequency_file(filename):
        frequencies = {}
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line[0] != "#":
                    word, frequency = line.strip().split('\t')
                    frequencies[word] = int(frequency)
        return frequencies

    def choose_highest_frequency_combination(self, combinations):
        max_frequency = 0
        best_combination = None
        for combination in combinations:
            frequency = self.frequencies.get(combination, 0)
            if frequency > max_frequency:
                max_frequency = frequency
                best_combination = combination
        return best_combination


    @staticmethod
    def load_dictionary(file_path):
        dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            g = f.readlines()
            for Wrds in g:
                wrd = Wrds.split(' ')
                dict[wrd[0].strip()] = sub('\n', '', wrd[1].strip())
        return dict

    @staticmethod
    def split_finglish_persian(word):
        # Regular expression to match sequences of Latin or Persian characters
        latin_pattern = re.compile(r'[a-zA-Z]+')
        persian_pattern = re.compile(r'[\u0600-\u06FF]+')
        # Find all matches of Latin and Persian sequences
        parts = []
        while word:
            latin_match = latin_pattern.match(word)
            persian_match = persian_pattern.match(word)

            if latin_match:
                parts.append(latin_match.group(0))
                word = word[latin_match.end():]
            elif persian_match:
                parts.append(persian_match.group(0))
                word = word[persian_match.end():]

            else:
                # In case of any non-matching characters (optional handling)
                parts.append(word[0])
                word = word[1:]

        return parts

    def convert_finglish_to_persian_word(self, word):
        for key in self.special_words.keys():
            word = re.sub(key, [key][0], word)
        if word in self.numbers:
            return self.numbers[word]

        for key in self.kha_pattern.keys():
            word = re.sub(key, self.kha_pattern[key][0], word)
        for key in self.two_char.keys():
            word = re.sub(key, self.two_char[key][0], word)

        for key in self.one_char.keys():
            word = re.sub(key, self.one_char[key][0], word)

        ########## handeling multiple forms
        parts = self.split_finglish_persian(word)
        latin_pattern = re.compile(r'[a-zA-Z@]+')

        all_comb = []
        vars = {}
        for part in parts:
            latin_match = latin_pattern.match(part)
            if latin_match:
                for key in self.multiple_char.keys():
                    if key in part:
                        vars[key] = self.multiple_char[key]

                pattern = "|".join(re.escape(key) for key in vars.keys())
                regex = re.compile(pattern)
                found_keys = regex.findall(part)
                for key in found_keys:
                    all_comb.append(self.multiple_char[key])
            else:
                all_comb.append([part])
        alternatives = [''.join(comb) for comb in itertools.product(*all_comb)]
        choosed_persian_word = self.choose_highest_frequency_combination(alternatives)
        return choosed_persian_word

    def run(self, text):
        text = self.preprocess_text(text).split(" ")
        res = ""
        for word in text:
            word = self.convert_finglish_to_persian_word(word)
            res += word + " "
        return res.strip()
