# from flask import Flask, request, render_template
# import pickle

# app = Flask(__name__)

# # Load the similarity matrix and dataset
# similarity = pickle.load(open('similarity.pkl', 'rb'))
# df = pickle.load(open('df.pkl', 'rb'))

# def recommend_songs(song_name, num_recommendations=10):
#     """
#     Recommend songs based on the input song name.
#     """
#     try:
#         idx = df[df['song'] == song_name].index[0]
#         distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
#         recommended_songs = [df.iloc[m_id[0]].song for m_id in distances[1:num_recommendations+1]]
#         return recommended_songs
#     except IndexError:
#         return None

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/recommend", methods=["POST"])
# def recommend():
#     try:
#         # Get the song name and number of recommendations from the form
#         song_name = request.form.get("song_name")
#         num_recommendations = int(request.form.get("num_recommendations", 10))

#         # Get recommendations
#         recommendations = recommend_songs(song_name, num_recommendations)

#         if recommendations is None:
#             return render_template("error.html", message="Song not found in the dataset.")

#         return render_template("recommendations.html", song_name=song_name, recommendations=recommendations)
#     except Exception as e:
#         return render_template("error.html", message=str(e))

# if __name__ == "__main__":
#     app.run(debug=True, port=5011)



# version --2


from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the similarity matrix and dataset with links
similarity = pickle.load(open('similarity.pkl', 'rb'))
df = pickle.load(open('df_with_links.pkl', 'rb'))

def recommend_songs(song_name, num_recommendations=10):
    """
    Recommend songs based on the input song name.
    """
    try:
        idx = df[df['song'] == song_name].index[0]
        distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
        recommended_songs = [
            {
                "song": df.iloc[m_id[0]].song,
                "artist": df.iloc[m_id[0]].artist,
                "link": df.iloc[m_id[0]].link,
                "photo": df.iloc[m_id[0]].photo,
                "lyrics": df.iloc[m_id[0]].text
            }
            for m_id in distances[1:num_recommendations+1]
        ]
        return recommended_songs
    except IndexError:
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get the song name and number of recommendations from the form
        song_name = request.form.get("song_name")
        num_recommendations = int(request.form.get("num_recommendations", 10))

        # Get recommendations
        recommendations = recommend_songs(song_name, num_recommendations)

        if recommendations is None:
            return render_template("error.html", message="Song not found in the dataset.")

        return render_template("recommendations.html", song_name=song_name, recommendations=recommendations)
    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/lyrics/<song_name>")
def lyrics(song_name):
    try:
        # Find the song in the dataset
        song_row = df[df['song'] == song_name]
        if song_row.empty:
            return render_template("error.html", message="Lyrics not found for the selected song.")

        # Extract the song details
        song_details = {
            "song": song_row.iloc[0]["song"],
            "artist": song_row.iloc[0]["artist"],
            "lyrics": song_row.iloc[0]["text"]
        }

        return render_template("lyrics.html", song=song_details)
    except Exception as e:
        return render_template("error.html", message=str(e))

if __name__ == "__main__":
    app.run(debug=True, port=5011)