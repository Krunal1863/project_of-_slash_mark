import nltk
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Download the required NLTK resource
nltk.download('punkt')

# Load the dataset
df = pd.read_csv("D:\Github_slash_mark_project\slash_mark_project\major-project\model-2\data\spotify_millsongdata.csv")

# Preprocess the dataset
df = df.sample(15000).drop('link', axis=1).reset_index(drop=True)
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex=True)

# Initialize the stemmer
stemmer = PorterStemmer()

# Tokenization and stemming function
def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = [stemmer.stem(w) for w in tokens]
    return " ".join(stemming)

# Apply tokenization to the text column
df['text'] = df['text'].apply(lambda x: tokenization(x))

# Create the TF-IDF matrix and calculate cosine similarity
tfidvector = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfidvector.fit_transform(df['text'])
similarity = cosine_similarity(matrix)

# Recommendation function
def recommendation(song_df):
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    songs = []
    for m_id in distances[1:21]:
        songs.append(df.iloc[m_id[0]].song)
        
    return songs

# Example usage of the recommendation function
recommendation('Crying Over You')

# Save the processed data and similarity matrix
pickle.dump(df, open('df.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))