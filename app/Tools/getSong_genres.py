import requests
import pandas as pd

def get_song_genres(uri, token):
    """Getting the genres for a list of songs or just one song."""
    genres = []
    
    for i in range(len(uri)):

        query1 = f'https://api.spotify.com/v1/tracks/{uri[i]}?market=US'
    

        response1 = requests.get(query1, 
                           headers={'Content-Type': "application/json", 
                                   "Authorization": 'Bearer ' +token})
        ID2 = response1.json()
        ID2 = ID2['album']['artists'][0]['uri'].split(':')[2]
        
        query2 = f'https://api.spotify.com/v1/artists/{ID2}'
        response2 = requests.get(query2, 
                           headers={'Content-Type': "application/json", 
                                   "Authorization": 'Bearer ' +token})
        genres.append(response2.json())
        
    gen = [tmp['genres'] for tmp in genres]
    genres_cat =[]
    for i in range(len(gen)):
        for j in range(len(gen[-2])):
            try: 
                genres_cat.append(gen[i][j])
            except:
                break

    genres_df = pd.DataFrame(genres_cat, columns=['Genres'])
    return genres_df