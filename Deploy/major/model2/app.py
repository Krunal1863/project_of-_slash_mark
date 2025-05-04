from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

# Load the preprocessed data and similarity matrix
df = pickle.load(open('D:\Github_slash_mark_project\slash_mark_project\Deploy\major\model2\model\df.pkl', 'rb'))
similarity = pickle.load(open('D:\Github_slash_mark_project\slash_mark_project\Deploy\major\model2\model\similarity.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Recommendation function
def recommendation(song_name):
    try:
        idx = df[df['song'] == song_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
        
        songs = []
        for m_id in distances[1:21]:
            songs.append(df.iloc[m_id[0]].song)
        
        return songs
    except IndexError:
        return ["Song not found in the dataset."]

# Define the API route
@app.route('/recommend', methods=['GET'])
def recommend():
    song_name = request.args.get('song')
    if not song_name:
        return jsonify({'error': 'Please provide a song name.'}), 400
    
    recommendations = recommendation(song_name)
    return jsonify({'recommendations': recommendations})

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5012)