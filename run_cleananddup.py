import pandas as pd
import re
import string

def casefolding(text):
    if isinstance(text, str):  # Pastikan input adalah string tunggal
        return text.lower().strip()
    elif isinstance(text, pd.Series):  # Jika input adalah Series, gunakan apply untuk menerapkan fungsi ke setiap elemen
        return text.apply(lambda x: x.lower().strip())
    elif isinstance(text, pd.DataFrame):  # Jika input adalah DataFrame, gunakan applymap untuk menerapkan fungsi ke setiap sel
        return text.applymap(lambda x: x.lower().strip())
    else:
        raise TypeError("Input harus berupa string tunggal, Series, atau DataFrame.")

def cleaning(text):
    if isinstance(text, str):  # Pastikan input adalah string tunggal
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
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"") #remove tab, new line, ans back slice
        text = text.translate(str.maketrans('','',string.punctuation)).lower() #Menghapus Punctuation
        return text
    elif isinstance(text, pd.Series):
        # Jika input adalah Series, gunakan apply untuk menerapkan fungsi ke setiap elemen
        return text.apply(cleaning)
    elif isinstance(text, pd.DataFrame):
        # Jika input adalah DataFrame, gunakan applymap untuk menerapkan fungsi ke setiap sel
        return text.applymap(cleaning)
    else:
        raise TypeError("Input harus berupa string tunggal, Series, atau DataFrame.")

# Definisikan metode remove_duplicate di dalam kelas
def remove_duplicate(text):
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


# Baca file CSV
df = pd.read_csv('datasettoko.csv')

# Terapkan case folding pada kolom 'Review'
df['Review'] = casefolding(df['Review'])

# Terapkan pembersihan pada kolom 'Review'
df['Review'] = cleaning(df['Review'])

# Hapus duplikat pada kolom 'Review'
df_unique = remove_duplicate(df['Review'])

# Cetak hasil
print(df_unique)
df_unique.to_csv('df_unique.csv', index=False)

# # Buat DataFrame contoh
# data = pd.DataFrame({'Review': ["Teks @username yang ingin dinormalisasi.", "ini adalah #tes123", "Teks yang memiliki non-ASCII karakter é"]})

# # Normalisasi
# data['Review'] = casefolding(data['Review'])

# # Pembersihan
# data['Review'] = cleaning(data['Review'])

# # Penghapusan Duplikat
# unique_data = remove_duplicate(data['Review'])

# # Cetak hasil
# print(unique_data)