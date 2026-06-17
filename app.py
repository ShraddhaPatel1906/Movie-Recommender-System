import pickle
import streamlit as st
import requests
 
# ------------------------------------------------------------
# FUNCTION 1: Fetch movie poster from TMDB API
# ------------------------------------------------------------
def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        response = requests.get(url, timeout=5)  # wait max 5 seconds
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return None  # no poster found
    except Exception:
        return None  # network error or timeout
 
# ------------------------------------------------------------
# FUNCTION 2: Find top 5 similar movies using cosine similarity
# ------------------------------------------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
 
    recommended_names   = []
    recommended_posters = []
 
    for i in distances[1:6]:  # skip index 0 — that's the movie itself
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
 
    return recommended_names, recommended_posters
 
# ------------------------------------------------------------
# HELPER: Show poster or fallback emoji card
# ------------------------------------------------------------
def show_movie_card(col, name, poster_url):
    with col:
        if poster_url:
            st.image(poster_url, width=200)
        else:
            # Show a nice emoji card when poster is not available
            st.markdown(f"""
            <div style="
                width: 200px;
                height: 280px;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 2px solid #e50914;
                border-radius: 12px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 10px;
                box-sizing: border-box;
            ">
                <div style="font-size: 60px;">🎬</div>
                <div style="color: #aaaaaa; font-size: 12px; margin-top: 10px;">Poster not available</div>
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"🎥 {name}")
 
# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
 
st.title("🎬 Movie Recommender System")
st.markdown("Select your favorite movie and we will suggest 5 similar movies!")
st.markdown("---")
 
# ------------------------------------------------------------
# LOAD SAVED MODEL FILES
# ------------------------------------------------------------
try:
    movies     = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("⚠️ Model files not found! Please run Movie_Recommender.ipynb first.")
    st.info("After running the notebook, 'movie_list.pkl' and 'similarity.pkl' will be saved in the 'model' folder.")
    st.stop()
 
# ------------------------------------------------------------
# MOVIE SELECTION AND DISPLAY RECOMMENDATIONS
# ------------------------------------------------------------
movie_list     = movies['title'].values
selected_movie = st.selectbox("🔍 Search or select a movie:", movie_list)
 
if st.button('🎯 Show Recommendations'):
 
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie)
 
    st.markdown("### 🍿 Top 5 Recommendations For You:")
    st.markdown("---")
 
    col1, col2, col3, col4, col5 = st.columns(5)
 
    show_movie_card(col1, names[0], posters[0])
    show_movie_card(col2, names[1], posters[1])
    show_movie_card(col3, names[2], posters[2])
    show_movie_card(col4, names[3], posters[3])
    show_movie_card(col5, names[4], posters[4])