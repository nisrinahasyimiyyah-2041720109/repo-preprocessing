from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Buat instance StopWordRemoverFactory
stopword_factory = StopWordRemoverFactory()

# Ambil daftar stopword dari Sastrawi menggunakan factory
stopwords = stopword_factory.get_stop_words()

# Tentukan lokasi file untuk menyimpan daftar stopword
file_path = 'stopwords_indonesian.txt'

# Tulis daftar stopword ke dalam file teks
with open(file_path, 'w', encoding='utf-8') as file:
    for word in stopwords:
        file.write(word + '\n')

print("Daftar stopword telah disimpan dalam file:", file_path)
