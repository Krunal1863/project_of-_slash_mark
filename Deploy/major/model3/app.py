from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the dataset and models
song_df = pickle.load(open('song_df.pkl', 'rb'))
popularity_model = pickle.load(open('popularity_model.pkl', 'rb'))
item_similarity_model = pickle.load(open('item_similarity_model.pkl', 'rb'))

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     try:
#         # Get the user input
#         user_id = request.form.get("user_id")
#         model_type = request.form.get("model_type")

#         # Generate recommendations based on the selected model
#         if model_type == "popularity":
#             recommendations = popularity_model.recommend(user_id)
#         elif model_type == "similarity":
#             recommendations = item_similarity_model.recommend(user_id)
#         else:
#             return render_template("error.html", message="Invalid model type selected.")

#         return render_template("recommendations.html", user_id=user_id, recommendations=recommendations)
#     except Exception as e:
#         return render_template("error.html", message=str(e))

# @app.route("/lyrics/<song_name>")
# def lyrics(song_name):
#     try:
#         # Find the song in the dataset
#         song_row = song_df[song_df['song'] == song_name]
#         if song_row.empty:
#             return render_template("error.html", message="Lyrics not found for the selected song.")

#         # Extract the song details
#         song_details = {
#             "song": song_row.iloc[0]["song"],
#             "artist": song_row.iloc[0]["artist_name"],
#             "lyrics": "Lyrics not available in this dataset."  # Placeholder for lyrics
#         }

#         return render_template("lyrics.html", song=song_details)
#     except Exception as e:
#         return render_template("error.html", message=str(e))

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)


from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the dataset and models
song_df = pickle.load(open('song_df.pkl', 'rb'))
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
            print("Popularity Recommendations:", recommendations)  # Debug print
            # Add listen_count to the recommendations
            recommendations = [
                {
                    "song": rec,
                    "count": song_df[song_df['song'] == rec]['listen_count'].sum()
                }
                for rec in recommendations
            ]
        elif model_type == "similarity":
            recommendations = item_similarity_model.recommend(user_id)
            print("Similarity Recommendations:", recommendations)  # Debug print
            # Format recommendations for similarity-based model
            recommendations = [{"song": rec} for rec in recommendations]
        else:
            return render_template("error.html", message="Invalid model type selected.")

        print("Final Recommendations:", recommendations)  # Debug print
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
    app.run(debug=True, port=5013)