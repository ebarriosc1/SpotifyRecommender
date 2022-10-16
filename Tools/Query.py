import requests


def spotify_recommend(token, target_1, target_2, target_3, target_4, target_1Name, target_2Name, target_3Name, target_4Name, seed_genres):
    """to be used in the Recommend_songs function"""
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    market = 'US'
    limit = 1
    query = f'{endpoint_url}limit={limit}\
    &market={market}&seed_genres={seed_genres}\
    &target_${target_1Name}={target_1}\
    &target_${target_2Name}={target_2}\
    &target_${target_3Name}={target_3}\
    &target_${target_4Name}={target_4}'
    
    query2 =  f'{endpoint_url}limit={limit}\
    &market={market}&seed_genres={seed_genres}\
    &target_${target_1Name}={target_1}\
    &target_${target_2Name}={target_2}\
    &target_${target_3Name}={target_3}'


    query = query.replace('    ', '')

    response = requests.get(query, 
                           headers={'Content-Type': "application/json", 
                                   "Authorization": 'Bearer ' + token})
    return response.json()