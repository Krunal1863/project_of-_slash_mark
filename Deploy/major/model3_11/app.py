from flask import Flask, request, jsonify, render_template
import pandas as pd
import Recommenders as Recommenders

app = Flask(__name__)

# Load data
song_df_1 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\triplets_file\triplets_file.csv')
song_df_2 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\song_data\song_data.csv')

# Combine data
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')
song_df['song'] = song_df['title'] + ' - ' + song_df['artist_name']

# Train Popularity-Based Recommender
pr = Recommenders.popularity_recommender_py()
pr.create(song_df, 'user_id', 'song')

@app.route('/')
def home():
    """
    Default route to render the HTML page.
    """
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    """
    API endpoint to get top 10 popular song recommendations.
    """
    user_id = request.args.get('user_id', default=None, type=str)
    if not user_id:
        return jsonify({"error": "Please provide a user_id"}), 400

    # Get recommendations
    recommendations = pr.recommend(user_id)
    return jsonify(recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True,port=5020)