import nltk
import string
import re
import glob
import pandas as pd
import emoji
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nlp_id.lemmatizer import Lemmatizer
import json
from sklearn.model_selection import train_test_split

factory = StemmerFactory()
stemmer = factory.create_stemmer()

class TextPreprocessing():
    def __init__(self, text, config):
        self.path = config
        self.text = text

    # def translate_emoticon(self, text):
    #     load_emoji = None
    #     with open(self.path['KAMUS_EMOTICON']) as f:
    #         load_emoji = json.load(f)
    #     for index, keys in enumerate(load_emoji.keys()):
    #         text = text.replace(keys, load_emoji[keys])
    #     return text
    
    # def convert_emoji(self, text):
    #     text = re.sub('@[^\s]+','', text)
    #     text = re.sub('#[^\s]+','', text)
    #     text = emoji.demojize(text)
    #     text = text.replace(':', ' ')
    #     text = ' '.join(text.split())
    #     return text
    
    # def translate_emoji(self, text):
    #     df_emoji = pd.read_csv(self.path['KAMUS_EMOJI'])
    #     for index, row in df_emoji.iterrows():
    #         text = text.replace(row[1].replace(' ', '_'), row[5])
    #     return text

    def casefolding(self, text):
        if isinstance(text, str):  # Pastikan input adalah string tunggal
            return text.lower().strip()
        elif isinstance(text, pd.Series):  # Jika input adalah Series, gunakan apply untuk menerapkan fungsi ke setiap elemen
            return text.apply(lambda x: x.lower().strip())
        elif isinstance(text, pd.DataFrame):  # Jika input adalah DataFrame, gunakan applymap untuk menerapkan fungsi ke setiap sel
            return text.applymap(lambda x: x.lower().strip())
        else:
            raise TypeError("Input harus berupa string tunggal, Series, atau DataFrame.")

    
    def cleaning(self, text):
        # remove tab, new line, and back slice
        text = text.replace('\\t'," ").replace('\\n', " ").replace('\\u', " ").replace('\\',"")
        # remove non ASCII (emoticon, chinese word, etc)
        text = text.encode('ascii', 'replace').decode('ascii')
        # remove mention, link, hashtag
        text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
        # remove incomplete URL
        text = text.replace("http://", " ").replace("https://", " ")
        # remove number
        text = re.sub(r"\d+", "", text)
        # remove punctuation and replace with space
        text = re.sub(r'[.,]', ' ', text)
        # remove punctuation
        # Menghapus simbol-simbol tidak standar dan menggantinya dengan spasi
        cleaned_text = re.sub(r'[^\w\s]', ' ', text)
        # Menghapus multiple whitespace
        text = re.sub('\s+', ' ', cleaned_text).strip()
        # Menentukan ambang batas panjang string acak
        threshold_length = 20
        # menghapus string acak berdasarkan panjangnya
        text = ' '.join(word for word in text.split() if len(word) <= threshold_length)
        #remove whitespace leading & trailing
        text = text.strip()
        #remove multiple whitespace into single whitespace
        text = re.sub('\s+',' ',text)
        # remove single char
        text = re.sub(r"\b[a-zA-Z]\b", "", text)
        # remove laughter pattern
        laughter_patterns = r'\b((ha)+h*|(he)+h*|(hi)+h*|(wk)+w*k*|(eh)+e*|(ah)+a*|(ih)+i*|(kw)+k*w*|(hem)+m*)\b'
        text = re.sub(laughter_patterns, '', text, flags=re.IGNORECASE)
        text = re.sub('@[^\s]+','',text) #Menghapus Username
        text = ' '.join(re.sub("(rt )"," ", text).split()) #Menghapus kata 'rt'
        text = re.sub('((www\S+)|(http\S+))', ' ', text) #Menghapus URL
        text = text.encode('ascii', 'replace').decode('ascii') #remove non ASCII (emoticon, chinese word, .etc)
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"") #remove tab, new line, ans back slice
        text = text.translate(str.maketrans('','',string.punctuation)).lower() #Menghapus Punctuation
        return text
    
    # def remove_duplicate(self, data):
    #     # REMOVE DUPLICATE
    #     data = data.drop_duplicates()
    #     data = data.reset_index(drop=True)
    #     # Menghapus baris yang kosong
    #     data = data.dropna(subset=['Review'])
    #     # Menghapus baris yang hanya berisi spasi atau whitespace
    #     data = data[data['Review'].str.strip() != '']
    #     return data
    # Definisikan metode remove_duplicate di dalam kelas
    def remove_duplicate(self, text):
        unique_reviews = set()  # Set untuk menyimpan teks ulasan yang sudah unik
        unique_data = []  # Daftar untuk menyimpan data unik
        for review in text:
            cleaned_review = review.strip()  # Membersihkan teks ulasan dan menghapus spasi tambahan
            if cleaned_review not in unique_reviews:
                unique_reviews.add(cleaned_review)  # Menambahkan teks ulasan ke dalam set unik
                unique_data.append(cleaned_review)  # Menambahkan teks ulasan yang unik ke dalam daftar
        
        # Buat DataFrame baru dari data unik
        unique_df = pd.DataFrame({'Review': unique_data})
        
        # Konversi kolom 'Review' ke tipe data string
        unique_df['Review'] = unique_df['Review'].astype(str)
        
        # Reset index dan hapus baris yang kosong atau hanya terdiri dari spasi
        unique_df = unique_df.dropna(subset=['Review'])
        unique_df = unique_df[unique_df['Review'].str.strip() != '']

        return unique_df

    # def load_dataset_normalization(self):
    #     load_word = pd.read_csv(self.path['NORMALFILE'])
    #     normal_word_dict = {}
    #     for index, row in load_word.iterrows():
    #         if row[0] not in normal_word_dict:
    #             normal_word_dict[row[0]] = row[1]
    #     return normal_word_dict
    
    def normalisasi(self, text):
        slang_dictionary = pd.read_csv(self.path['NORMALFILE'])
        slang_dict = pd.Series(slang_dictionary['formal'].values,index=slang_dictionary['slang']).to_dict()

        # Menerapkan normalisasi pada teks
        def apply_normalization(text, slang_dict):
            for word in text.split():
                if word in slang_dict.keys():
                    # menambahkan \b untuk menandakan batas kata di sekitar kata slang
                    text = re.sub(r'\b{}\b'.format(re.escape(word)), slang_dict[word], text)
            text = re.sub('@[\w]+', '', text)
            return text

        # Memastikan text adalah string sebelum menerapkan normalisasi
        if isinstance(text, str):
            return apply_normalization(text, slang_dict)
        else:
            raise ValueError("Input text should be a string.")

        # word_dict = self.load_dataset_normalization()
        # return [word_dict[term] if term in word_dict else term for term in data]
    
    def tokenize(self, text):
        return word_tokenize(text)
    
    def remove_stopwords(self, data):
        totalIndex = len(data)
        base = [[] for i in range(totalIndex)]
        count = 0
        txt_stopword = pd.read_csv(self.path['STOPWORDS'], names=['stopwords_id'], header=None)
        stopwordTexts = stopwords.words('indonesian')
        stopwordTexts.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 'kalo', 'amp', 'biar', 'bikin', 'bilang', 'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 'jd', 'jgn', 'sdh', 'aja', 'n', 't', 'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt','&amp', 'yah', 'wkwkwkkwwk', 'wkwkwkwkwk', 'wkwkwk','wkkwkw', 'anjirrr'])
        stopwordTexts.extend(txt_stopword["stopwords_id"][0].split(' '))
        stopwordTexts = set(stopwordTexts)
        for x in data:
            for text in x:
                if text not in stopwordTexts:
                    base[count].append(text)
            count = count + 1
        return base
    
    def lemmatization(self, data):
        lengthData = len(data)
        base = [[] for i in range(0, lengthData)]
        count = 0
        for list_text in data:
            for text in list_text:
                base[count].append(stemmer.stem(text))
            count = count + 1
        return base
    
    def output(self, export):
        self.dataframe = pd.DataFrame()
        # self.dataframe['emoticon'] = self.text.apply(self.translate_emoticon)
        # self.dataframe['convert_emoji'] = self.dataframe['emoticon'].apply(self.convert_emoji)
        # self.dataframe['translate_emoji'] = self.dataframe['convert_emoji'].apply(self.translate_emoji)
        self.dataframe['case_folding'] = self.text.apply(self.casefolding)
        self.dataframe['cleaned'] = self.dataframe['case_folding'].apply(self.cleaning)
        self.dataframe['remove_duplicate'] = self.dataframe['cleaned'].apply(self.remove_duplicate)
        self.dataframe['normalization'] = self.dataframe['remove_duplicate'].apply(self.normalisasi)
        self.dataframe['tokenize'] = self.dataframe['normalization'].apply(self.tokenize)
        self.dataframe['remove_stopwords'] = self.remove_stopwords(self.dataframe['tokenize'])
        self.dataframe['lemmatization'] = self.lemmatization(self.dataframe['remove_stopwords'])
        self.dataframe['text_string_lemma'] = self.dataframe['lemmatization'].apply(lambda x: ' '.join(x))
        if export == True:
            # self.dataframe['label'] = self.label
            self.dataframe = self.dataframe.dropna()
            self.dataframe = self.dataframe.reset_index(drop=True)
            self.dataframe.to_csv('app/dataset/preprocessing/dataset_preprocess.csv', index=False)
            return self.dataframe
        elif export == False:
            self.dataframe = self.dataframe.dropna()
            self.dataframe = self.dataframe.reset_index(drop=True)
            return self.dataframe
        else:
            print('Error')

