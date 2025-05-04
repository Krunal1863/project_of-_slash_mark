# from flask import Flask, request, jsonify
# import pickle
# import pandas as pd

# # Initialize Flask app
# app = Flask(__name__)

# # Load the trained models
# with open('popularity_model.pkl', 'rb') as file:
#     popularity_model = pickle.load(file)

# with open('item_similarity_model.pkl', 'rb') as file:
#     similarity_model = pickle.load(file)

# # Load the dataset (if needed for recommendations)
# song_df = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\triplets_file\triplets_file.csv')
# song_df_2 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\song_data\song_data.csv')
# song_df = pd.merge(song_df, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')
# song_df['song'] = song_df['title'] + ' - ' + song_df['artist_name']

# # Define routes
# @app.route('/')
# def home():
#     return "Welcome to the Recommendation System API!"

# @app.route('/recommend/popularity', methods=['GET'])
# def recommend_popularity():
#     """Recommend songs based on popularity."""
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({"error": "Please provide a user_id"}), 400

#     recommendations = popularity_model.recommend(user_id)
#     return jsonify(recommendations)

# @app.route('/recommend/similarity', methods=['GET'])
# def recommend_similarity():
#     """Recommend songs based on item similarity."""
#     user_id = request.args.get('user_id')
#     if not user_id:
#         return jsonify({"error": "Please provide a user_id"}), 400

#     recommendations = similarity_model.recommend(user_id)
#     return jsonify(recommendations)

# @app.route('/recommend/similar_items', methods=['POST'])
# def recommend_similar_items():
#     """Recommend similar songs based on input songs."""
#     data = request.json
#     if not data or 'songs' not in data:
#         return jsonify({"error": "Please provide a list of songs in the request body"}), 400

#     similar_items = similarity_model.get_similar_items(data['songs'])
#     return jsonify(similar_items)

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the dataset directly from CSV files
song_df_1 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\triplets_file\triplets_file.csv')
song_df_2 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\song_data\song_data.csv')
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')
song_df['song'] = song_df['title'] + ' - ' + song_df['artist_name']

# Load the trained models
popularity_model = pickle.load(open('popularity_model.pkl', 'rb'))
item_similarity_model = pickle.load(open('item_similarity_model.pkl', 'rb'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get the user input
        user_id = request.form.get("user_id")
        model_type = request.form.get("model_type")

        # Generate recommendations based on the selected model
        if model_type == "popularity":
            recommendations = popularity_model.recommend(user_id)
            recommendations = [
                {
                    "song": rec,
                    "count": song_df[song_df['song'] == rec]['listen_count'].sum()
                }
                for rec in recommendations
            ]
        elif model_type == "similarity":
            recommendations = item_similarity_model.recommend(user_id)
            recommendations = [{"song": rec} for rec in recommendations]
        else:
            return render_template("error.html", message="Invalid model type selected.")

        return render_template("recommendations.html", user_id=user_id, recommendations=recommendations, model_type=model_type)
    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/lyrics/<song_name>")
def lyrics(song_name):
    try:
        # Find the song in the dataset
        song_row = song_df[song_df['song'] == song_name]
        if song_row.empty:
            return render_template("error.html", message="Lyrics not found for the selected song.")

        # Extract the song details
        song_details = {
            "song": song_row.iloc[0]["song"],
            "artist": song_row.iloc[0]["artist_name"],
            "lyrics": "Lyrics not available in this dataset."  # Placeholder for lyrics
        }

        return render_template("lyrics.html", song=song_details)
    except Exception as e:
        return render_template("error.html", message=str(e))

if __name__ == "__main__":
    app.run(debug=True, port=5000)