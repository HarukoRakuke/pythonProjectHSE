from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Загрузка данных
file_path = "songs.xlsx"  # Укажите путь к вашему файлу
data = pd.read_excel(file_path)

# Step 2: Инициализация предобученной модели анализа эмоций
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

# Step 3: Анализ эмоций
def analyze_emotions(text):
    try:
        result = emotion_analyzer(str(text))[0]
        return result['label']  # Возвращаем определённую моделью эмоцию
    except Exception as e:
        return "Не определено"

data['Эмоция'] = data['Текст'].apply(analyze_emotions)

# Step 4: Подсчёт эмоций
emotion_counts = data['Эмоция'].value_counts()

# Step 5: Построение круговой диаграммы
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

# Новые цвета для категорий эмоций
colors = ['#370815', '#906F61', '#940B13', '#FB694A', '#D9D9D9', '#FE0000']  # Цвета в HEX-формате

ax.pie(
    emotion_counts,
    labels=emotion_counts.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    textprops={'color': "white", 'fontsize': 12}
)

# Заголовок
ax.set_title("Распределение песен по эмоциям", fontsize=14, color="white")

# Убираем лишнее пространство
plt.tight_layout()

# Отображение графика
plt.show()