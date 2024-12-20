import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import string
import nltk

# Download English stop words
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Add custom stop words
custom_stop_words = {'verse', 'intro', 'vocals', 'instrumental', 'chorus', 'lyrics', 'не указано', 'mrkitty'}

# Combine stop words
all_stop_words = stop_words.union(custom_stop_words)

# Step 1: Load the file
file_path = "songs.xlsx"  # Replace with the path to your file
data = pd.read_excel(file_path)

data['Дата выхода'] = pd.to_datetime(data['Дата выхода'], errors='coerce')  # Convert to datetime
data['Год'] = data['Дата выхода'].dt.year  # Extract the year

# Step 2: Split data into time periods
time_periods = {
    "2006-2011": data[(data['Год'] >= 2006) & (data['Год'] <= 2011)],
    "2012-2018": data[(data['Год'] >= 2012) & (data['Год'] <= 2018)],
    "2019-2024": data[(data['Год'] >= 2019) & (data['Год'] <= 2024)],
}

# Step 3: Process text and generate word clouds
masks = {
    "2006-2011": "scull.png",  # Replace with the path to your mask file for this period
    "2012-2018": "cross.png",
    "2019-2024": "heart.png",
}

font_path = "TimesNewRomaNCondensed.otf"  # Replace with your font file path

def preprocess_text(text):
    # Remove punctuation and convert text to lowercase
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    # Split text into words, remove short words and all stop words
    words = [word for word in cleaned_text.split() if len(word) > 3 and word not in all_stop_words]
    return words

fig, axes = plt.subplots(1, 3, figsize=(30, 10), facecolor='black')  # Create a single figure with 3 subplots

for i, (period, df) in enumerate(time_periods.items()):
    if df.empty:
        continue
    # Combine all lyrics for the time period
    all_lyrics = ' '.join(df['Текст'].dropna())
    words = preprocess_text(all_lyrics)
    word_freq = Counter(words)

    # Load mask
    mask_image = Image.open(masks[period]).convert("L")  # Convert to grayscale
    mask_array = np.array(mask_image)
    transformed_mask = np.where(mask_array > 128, 255, 0).astype(np.uint8)  # Binary mask


    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        if font_size > 40:  # Самые крупные слова
            return "white"
        elif font_size > 30:  # Чуть менее крупные
            return "#D6D6D6"
        elif font_size > 10:  # Средние
            return "#FE0000"
        else:  # Мелкие
            return "#572631"

    # Generate word cloud
    wordcloud = WordCloud(
        width=4000,
        height=3000,
        background_color='black',
        mask=transformed_mask,
        color_func=color_func,  # Replace with your custom function if needed
        font_path=font_path,
        max_words=500,
    ).generate_from_frequencies(word_freq)

    # Plot in the corresponding subplot
    axes[i].imshow(wordcloud, interpolation='bilinear'),
    axes[i].set_facecolor('black'),
    axes[i].set_title(f"Word Cloud for {period}", fontsize=20, color='white')
    axes[i].axis('off')

plt.tight_layout()
plt.show()