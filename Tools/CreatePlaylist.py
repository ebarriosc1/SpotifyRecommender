
username = None
import pandas as pd


def create_playlist(json_response, sp, username=username, playlistName='Default1'):
    """To be used in the Recommend_songs function"""
    all_songs = []

    for track in json_response:
        try:
            song_dict= {}
            song_dict['name'] =track['tracks'][0]['name']
            song_dict['artist'] = track['tracks'][0]['artists'][0]['name']
            song_dict['uri'] = track['tracks'][0]['uri']
            all_songs.append(song_dict)
        except: 
            continue
    song = pd.DataFrame(all_songs)
    
    #Make the new playlist with the new songs that were recommended
    #Making a new playlist with songs classified in the cluster 
    for i in range(1):
        result = sp.user_playlist_create(username, playlistName , public=True, collaborative=False, description='')
        playlist_id = result['id']
        songs = song['uri'].tolist()
        if len(songs) > 100:
            sp.playlist_add_items(playlist_id, songs[:100])
            sp.playlist_add_items(playlist_id, songs[100:])
        else:
            sp.playlist_add_items(playlist_id, songs)
            
    return print('Completed')