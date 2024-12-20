import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize

# Step 1: Загрузка данных из Excel
file_path = "songs.xlsx"  # Замените на путь к вашему файлу
data = pd.read_excel(file_path)  # Загрузка таблицы

# Step 2: Преобразование даты в год
if 'Дата выхода' not in data.columns:
    raise ValueError("В таблице отсутствует колонка 'Дата выхода'")

data['Год'] = pd.to_datetime(data['Дата выхода'], errors='coerce').dt.year

# Step 3: Проверка корректности преобразования
if data['Год'].isnull().any():
    print("Некоторые строки содержат некорректные даты и были пропущены.")

# Step 4: Подсчёт количества песен по годам
year_counts = data['Год'].value_counts().sort_index()

# Преобразование индексов годов в целые числа
year_counts.index = year_counts.index.astype(int)

# Step 5: Построение графика с черным фоном и цветовым градиентом
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor("black")  # Черный фон для всей фигуры
ax.set_facecolor("black")  # Черный фон для области осей

# Создаем градиент цветов от белого к красному и темному
norm = Normalize(vmin=min(year_counts.values), vmax=max(year_counts.values))  # Нормализация значений
colors = [cm.Reds(norm(value)) for value in year_counts.values]

# Рисуем график
bars = ax.bar(year_counts.index, year_counts.values, color=colors, edgecolor="none")

# Добавляем подписи над столбцами
for bar, count in zip(bars, year_counts.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(count),
        ha="center",
        va="bottom",
        fontsize=12,  # Размер текста над столбцами
        color="white"
    )

# Настройка осей и заголовков
ax.set_xticks(year_counts.index)
ax.set_xticklabels(year_counts.index, rotation=45, color='white', fontsize=12)  # Увеличение шрифта меток оси X
ax.tick_params(axis='y', colors='white', labelsize=12)  # Увеличение шрифта меток оси Y
ax.grid(axis='y', linestyle='--', alpha=0.5, color='gray')

# Убираем лишнее пространство
plt.tight_layout()

# Отображаем график
plt.show()