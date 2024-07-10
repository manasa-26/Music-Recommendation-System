import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to fetch album cover URL for a given song and artist
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image if no results found

# Function to recommend songs based on similarity
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    
    for i in distances[1:6]:  # Recommend top 5 similar songs
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit web app
st.header('Music Recommender System')

# Load data (assumes 'df.pkl' and 'similarity.pkl' are pickled data files)
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Dropdown to select a song
music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

# Button to trigger recommendation
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    # Display recommendations in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])

    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])

    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])

    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])

    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
