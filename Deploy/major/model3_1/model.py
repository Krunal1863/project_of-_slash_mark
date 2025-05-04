import pandas as pd
import numpy as np
import Recommenders as Recommenders


song_df_1 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\triplets_file\triplets_file.csv')
song_df_1.head()


song_df_2 = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\major-project\model-3\data\song_data\song_data.csv')
song_df_2.head()

# combine both data
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')
song_df.head()





# creating new feature combining title and artist name
song_df['song'] = song_df['title']+' - '+song_df['artist_name']
song_df.head()



# cummulative sum of listen count of the songs
song_grouped = song_df.groupby(['song']).agg({'listen_count':'count'}).reset_index()
song_grouped.head(15)



grouped_sum = song_grouped['listen_count'].sum()
song_grouped['percentage'] = (song_grouped['listen_count'] / grouped_sum ) * 100
song_grouped.sort_values(['listen_count', 'song'], ascending=[0,1])



pr = Recommenders.popularity_recommender_py()
pr.create(song_df, 'user_id', 'song')
# display the top 10 popular songs
pr.recommend(song_df['user_id'][5])





ir = Recommenders.item_similarity_recommender_py()
ir.create(song_df, 'user_id', 'song')
user_items = ir.get_user_items(song_df['user_id'][5])



# display user songs history
for user_item in user_items:
    print(user_item)



# give song recommendation for that user
ir.recommend(song_df['user_id'][5])




# give related songs based on the words
ir.get_similar_items(['Oliver James - Fleet Foxes', 'The End - Pearl Jam'])



