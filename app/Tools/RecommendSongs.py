from Tools.getSong_genres import get_song_genres
from Tools.Spotify_genres import avail_genres
from Tools.Query import spotify_recommend
import pandas as pd
from itertools import cycle, islice

def recommend_songs(num_songs,uri,token, df):
    """Recommend songs based on the genres, audio_features,
    and can adjust the number of songs that we want recommended
    BUT YOU CAN DECIDE WHAT GENRE YOU WANT TO HEAR"""
    
    df_genres = get_song_genres(uri, token)
    ranked_Genres = df_genres.Genres.value_counts()[df_genres.Genres.unique()].index.tolist()
    
    df_filtered= df
    #df_filtered = df_filtered.drop(['Cluster'], axis=1)
    df_filtered_info =df_filtered[['name', 'artist', 'track_URI', 'playlist']]
    df_filtered= df_filtered.drop(['name', 'artist', 'track_URI', 'playlist'], axis=1)


    dfSTD = pd.DataFrame(df_filtered.std(), columns=['STD'])
    dfSTD = dfSTD.sort_values(by=['STD'])
    target_columns = dfSTD.iloc[:3].index.tolist()
    target_columns.append('tempo')
    df_target = pd.DataFrame(df_filtered[target_columns].mean(), columns=['AVG'])
    target_dfSTD = dfSTD.loc[target_columns]
    #Want to attribute the data such that the recommended songs  
    #sound similar to the top songs in the playlist 
    for i in range(len(df_target)):
        df_target.iloc[i] = df_target.iloc[i].values + 2*(target_dfSTD.iloc[i].values)
        
        
    #Use spotipy to recommed songs based on the similar features 
    #described in the features analysis 
    #Filtering genres so that we only have genres that are existing in spotify API 
    #Cleaning data 
    Cleaned_data = ranked_Genres
    for i in range(len(Cleaned_data)):
        Cleaned_data[i]= Cleaned_data[i].replace(' ', '-')
        
    filtered_genres=[]
    for i in range(len(Cleaned_data)):
        if Cleaned_data[i] in avail_genres():
            filtered_genres.append(Cleaned_data[i])
        else:
            continue
            
     
    #Filters 
    market='US'
    batch = [i for i in range(1, (num_songs)) if (num_songs)%i == 0]
    for x in batch:
        if x < 10.0:
            batch_size = x
            
    songs = []        
    for i in range(0, num_songs,batch_size):
        genres = list(islice(cycle(filtered_genres), i+1, i+1+batch_size))
        for j in range(batch_size):
            seed_genres = genres[j]
            target_1 = df_target.iloc[1].tolist()[0]
            target_1Name = df_target.index[0]

            target_2 = df_target.iloc[0].tolist()[0]
            target_2Name = df_target.index[1]

            target_3 = df_target.iloc[2].tolist()[0]
            target_3Name = df_target.index[2]

            target_4 = df_target.iloc[3].tolist()[0]
            target_4Name = df_target.index[3]

            songs.append(spotify_recommend(token, target_1, target_2, target_3, target_4, target_1Name,
                                     target_2Name, target_3Name, target_4Name, seed_genres))
        
    return songs