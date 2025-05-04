from flask import Flask, request, render_template
import pandas as pd
import random

app = Flask(__name__, static_folder="static")

# Load the song data
file_path = "d:\\Github_slash_mark_project\\slash_mark_project\\major-project\\model-1\\data\\songdata.csv"
try:
    song_data = pd.read_csv(file_path)
except FileNotFoundError:
    song_data = None
    print(f"Error: File not found at {file_path}")

def get_random_recommendations(df, num_recommendations):
    """
    Get random song recommendations from the dataset.
    """
    if df is None or df.empty:
        return []

    # Randomly sample songs from the dataset
    recommendations = df.sample(n=min(num_recommendations, len(df)))
    return recommendations

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get the number of recommendations from the form
        num_recommendations = int(request.form.get("num_recommendations", 5))

        # Generate random recommendations
        recommendations = get_random_recommendations(song_data, num_recommendations)

        # Format the recommendations for display
        formatted_recommendations = [
            {"song": row["song"], "artist": row["artist"]}
            for _, row in recommendations.iterrows()
        ]

        return render_template("recommendations.html", recommendations=formatted_recommendations)
    except Exception as e:
        return render_template("error.html", message=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)

