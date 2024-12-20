import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Загрузка таблицы
file_path = "songs.xlsx"  # Укажите путь к вашему файлу
data = pd.read_excel(file_path)  # Загрузка таблицы

# Убедитесь, что нужные столбцы существуют
if 'Текст' not in data.columns or 'Название' not in data.columns:
    raise ValueError("Таблица должна содержать столбцы 'Текст' и 'Название'")

# Step 2: Преобразование текстов песен в векторное представление
vectorizer = CountVectorizer(stop_words='english')  # Используем английские стоп-слова
song_vectors = vectorizer.fit_transform(data['Текст'].fillna(''))  # Пропуски заменяем на пустую строку

# Step 3: Расчет косинусного сходства между текстами песен
similarity_matrix = cosine_similarity(song_vectors)  # Матрица сходства

# Step 4: Создание графа
threshold = 0.8 # Порог сходства для добавления связи
G = nx.Graph()

# Добавляем узлы (названия песен)
for i, title in enumerate(data['Название']):
    G.add_node(i, label=title)

# Добавляем связи между узлами (если сходство выше порога)
for i in range(similarity_matrix.shape[0]):
    for j in range(i + 1, similarity_matrix.shape[1]):  # Чтобы не дублировать связи
        if similarity_matrix[i, j] > threshold:
            G.add_edge(i, j, weight=similarity_matrix[i, j])

# Step 5: Визуализация графа
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.5)  # Алгоритм для размещения узлов (spring layout)
nx.draw(
    G,
    pos,
    with_labels=False,  # Отключаем автоматические подписи узлов
    node_size=50,
    node_color="red",
    edge_color="gray"
)
# Подписываем узлы (названия песен)
nx.draw_networkx_labels(G, pos, {i: title for i, title in enumerate(data['Название'])}, font_size=8)
plt.title('Карта связей песен (на основе текстов)', fontsize=16)
plt.show()