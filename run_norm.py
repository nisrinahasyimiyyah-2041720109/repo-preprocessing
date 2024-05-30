from text_preprocessing import TextPreprocessing
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import re
factory = StemmerFactory()
stemmer = factory.create_stemmer()

PATH = {
    'DATASET' : 'dataset/dataframe/avoskin-df.csv',
    'PREPROCESS' : 'dataset/preprocessing/dataset_preprocess.csv',
    'NORMALFILE' : 'dataset/preprocessing/colloquial-indonesian-lexicon.csv',
    'STOPWORDS' : 'stopwords_id.txt',
    'KAMUS_EMOJI' : 'dataset/preprocessing/emoji.csv',
    'KAMUS_EMOTICON' : 'dataset/preprocessing/emoticon.json',
}

def normalisasi_dataframe(dataframe, slang_dictionary_path):
    slang_dictionary = pd.read_csv(slang_dictionary_path)
    slang_dict = pd.Series(slang_dictionary['formal'].values, index=slang_dictionary['slang']).to_dict()

    # Menerapkan normalisasi pada teks
    def apply_normalization(text, slang_dict):
        for word in text.split():
            if word in slang_dict.keys():
                # menambahkan \b untuk menandakan batas kata di sekitar kata slang
                text = re.sub(r'\b{}\b'.format(re.escape(word)), slang_dict[word], text)
        text = re.sub('@[\w]+', '', text)
        return text

    # Normalisasi setiap teks dalam kolom 'Review'
    dataframe['Review'] = dataframe['Review'].apply(lambda x: apply_normalization(x, slang_dict))

    return dataframe

def tokenize(dataframe):
    dataframe['Review'] = dataframe['Review'].apply(lambda x: word_tokenize(x))
    return dataframe
    
def remove_stopwords(dataframe):
    txt_stopword = pd.read_csv(PATH['STOPWORDS'], names=['stopwords_id'], header=None)
    stopwordTexts = stopwords.words('indonesian')
    stopwordTexts.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 'kalo', 'amp', 'biar', 'bikin', 'bilang', 'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 'jd', 'jgn', 'sdh', 'aja', 'n', 't', 'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt','&amp', 'yah', 'wkwkwkkwwk', 'wkwkwkwkwk', 'wkwkwk','wkkwkw', 'anjirrr'])
    stopwordTexts.extend(txt_stopword["stopwords_id"][0].split(' '))
    stopwordTexts = set(stopwordTexts)
    dataframe['Review'] = dataframe['Review'].apply(lambda x: [word for word in x if word not in stopwordTexts])
    return dataframe

def lemmatization(dataframe):
    dataframe['Review'] = dataframe['Review'].apply(lambda x: [stemmer.stem(word) for word in x])
    return dataframe


# Contoh penggunaan
path_to_normal_file = 'colloquial-indonesian-lexicon.csv'
data = pd.read_csv('df_unique.csv')  # Ganti 'data.csv' dengan nama file CSV yang Anda miliki
data_normalized = normalisasi_dataframe(data, path_to_normal_file)
data_token = tokenize(data_normalized)
data_without_stopwords = remove_stopwords(data_token)
data_lemma = lemmatization(data_without_stopwords)
# Simpan DataFrame yang sudah dinormalisasi ke file CSV
data_lemma.to_csv('data_normalized_lemma.csv', index=False)
# print(data_normalized)

# def normalisasi(text, slang_dictionary_path):
#     slang_dictionary = pd.read_csv(slang_dictionary_path)
#     slang_dict = pd.Series(slang_dictionary['formal'].values, index=slang_dictionary['slang']).to_dict()

#     # Menerapkan normalisasi pada teks
#     def apply_normalization(text, slang_dict):
#         for word in text.split():
#             if word in slang_dict.keys():
#                 # menambahkan \b untuk menandakan batas kata di sekitar kata slang
#                 text = re.sub(r'\b{}\b'.format(re.escape(word)), slang_dict[word], text)
#         text = re.sub('@[\w]+', '', text)
#         return text

#     # Pastikan teks adalah string sebelum menerapkan normalisasi
#     if isinstance(text, str):
#         return apply_normalization(text, slang_dict)
#     else:
#         raise ValueError("Input text should be a string.")

# # Contoh penggunaan
# path_to_normal_file = 'colloquial-indonesian-lexicon.csv'
# text = "yg mana saya sudah beli banyak tapi bagusss"
# normalized_text = normalisasi(text, path_to_normal_file)
# print(normalized_text)

# PATH = {
#     'DATASET' : 'dataset/dataframe/avoskin-df.csv',
#     'PREPROCESS' : 'dataset/preprocessing/dataset_preprocess.csv',
#     'NORMALFILE' : 'colloquial-indonesian-lexicon.csv',
#     'STOPWORDS' : 'dataset/preprocessing/stopwords_id.txt',
#     'KAMUS_EMOJI' : 'dataset/preprocessing/emoji.csv',
#     'KAMUS_EMOTICON' : 'dataset/preprocessing/emoticon.json',
# }

# def preprocess_data():
#     data = pd.read_csv('datasettoko.csv')
#     # reviews = data['Review']  # Memilih hanya kolom 'Review'
#     your_object = TextPreprocessing(PATH)

#     # Pastikan teks yang akan dinormalisasi adalah string
#     text = "yg mana saya sudah beli banyak tapi bagusss"
#     normalized_text = normalisasi(text, PATH)
#     print(normalized_text)
#     # text_preprocess = TextPreprocessing(data, PATH)
#     # data['Review'] = data['Review'].astype(str)
#     # result = text_preprocess.output(export=True)
#     # return result

# preprocess_data()