import pandas as pd
import random

def load_song_data(file_path):
    """
    Load the song data from a CSV file.
    """
    try:
        df = pd.read_csv("D:\Github_slash_mark_project\slash_mark_project\Deploy\major\model1\data\songdata.csv")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def get_random_recommendations(df, num_recommendations):
    """
    Get random song recommendations from the dataset.
    """
    if df is None or df.empty:
        print("Error: The dataset is empty or not loaded.")
        return []

    # Randomly sample songs from the dataset
    recommendations = df.sample(n=min(num_recommendations, len(df)))
    return recommendations

if __name__ == "__main__":
    # Path to the song data CSV file
    file_path = "d:\\Github_slash_mark_project\\slash_mark_project\\major-project\\model-1\\data\\songdata.csv"

    # Load the song data
    song_data = load_song_data(file_path)

    # Number of random recommendations to generate
    num_recommendations = 5

    # Get random recommendations
    recommendations = get_random_recommendations(song_data, num_recommendations)

    # Display the recommendations
    if not recommendations.empty:
        print("Random Song Recommendations:")
        for index, row in recommendations.iterrows():
            print(f"Song: {row['song']}, Artist: {row['artist']}")