from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

class CustomStopWordRemover:
    def __init__(self, stop_words):
        self.stop_words = stop_words

    def remove(self, text):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)

# Tentukan lokasi file stopword Bahasa Indonesia
stopword_file = 'stopwords_indonesian.txt'

# Baca isi file stopword
with open(stopword_file, 'r', encoding='utf-8') as file:
    stopwords = file.read().splitlines()

# Kata-kata yang ingin dikecualikan
exceptions = ["belum", "tidak", "tanpa"]

# Buat daftar stopword baru tanpa kata-kata pengecualian
custom_stopwords = [word.lower() for word in stopwords if word.lower() not in exceptions]

# Buat instance custom stopword remover
custom_stopword_remover = CustomStopWordRemover(custom_stopwords)

# Contoh penggunaan
text = "Saya tidak suka belajar bahasa pemrograman. Mereka itu adalah teman-teman saya."
filtered_text = custom_stopword_remover.remove(text)

print("Teks asli:", text)
print("Teks setelah penghapusan stopword:", filtered_text)



# from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# class CustomStopWordRemoverFactory(StopWordRemoverFactory):
#     def create_stop_word_remover(self):
#         # Buat instance StopWordRemover dengan objek dictionary kosong
#         stop_word_remover = StopWordRemover({})

#         # Ambil daftar stopword default dari Sastrawi
#         default_stop_words = stop_word_remover.get_stop_words()

#         # Modifikasi daftar stopword sesuai kebutuhan Anda
#         modified_stop_words = self.modify_stop_words(default_stop_words)

#         # Buat instance baru dari StopWordRemover dengan daftar stopword yang telah dimodifikasi
#         custom_stop_word_remover = StopWordRemover(modified_stop_words)

#         return custom_stop_word_remover

#     def modify_stop_words(self, default_stop_words):
#         # Modifikasi daftar stopword sesuai kebutuhan Anda
#         # Misalnya, hapus beberapa kata stopword tertentu
#         # atau tambahkan kata-kata baru yang ingin dianggap sebagai stopword

#         # Contoh: hapus kata "mereka" dan "tidak" dari daftar stopword
#         modified_stop_words = [word for word in default_stop_words if word not in ["mereka", "tidak", "namun"]]
#         return modified_stop_words



# # Buat instance dari CustomStopWordRemoverFactory
# customFactory = CustomStopWordRemoverFactory()

# # Buat StopWordRemover yang sudah dimodifikasi
# customStopWordRemover = customFactory.create_stop_word_remover()

# # Teks yang akan diproses
# teks = "Saya suka belajar bahasa pemrograman. Mereka adalah teman-teman saya."

# # Hapus stopword dari teks
# hasil = customStopWordRemover.remove(teks)

# # Tampilkan hasil
# print("Teks asli:", teks)
# print("Teks setelah penghapusan stopword:", hasil)

# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
# from Sastrawi.StopWordRemover.StopWordRemover import STOP_WORDS as stopwords

# # Kata-kata yang ingin dikecualikan
# exceptions = ["mereka", "tidak", "namun"]

# # Buat daftar stopword baru tanpa kata-kata pengecualian
# custom_stopwords = [word for word in stopwords if word not in exceptions]

# # Buat instance StopWordRemoverFactory
# stopword_factory = StopWordRemoverFactory()

# # Buat instance StopWordRemover dengan daftar stopword yang telah dimodifikasi
# custom_stopword_remover = stopword_factory.create_stop_word_remover(custom_stopwords)

# # Contoh penggunaan
# text = "Saya suka belajar bahasa pemrograman. Mereka tidak teman-teman saya."
# filtered_text = custom_stopword_remover.remove(text)

# print("Teks asli:", text)
# print("Teks setelah penghapusan stopword:", filtered_text)


