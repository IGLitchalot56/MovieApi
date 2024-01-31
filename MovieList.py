import streamlit as st
import pandas as pd
import requests

csv_path = r"movie.csv"
data = pd.read_csv(csv_path)

# st.write(data)

with st.sidebar:
    search_query_title = st.sidebar.text_input('Search for movie titles: ', '')

    released_year_min = st.sidebar.text_input('Released year (Min): ', '')
    released_year_max = st.sidebar.text_input('Released year (Max): ', '')
    vote_averages_min = st.sidebar.text_input('Vote averages (Min): ', '')
    vote_averages_max = st.sidebar.text_input('Vote averages (Max): ', '')
    reset_button = st.sidebar.button("Reset")

filter = st.empty()

if reset_button:
    search_query_title = ''
    released_year_min = ''
    released_year_max = ''
    vote_averages_min = ''
    vote_averages_max = ''

filter = st.empty()

if (
    search_query_title or released_year_min or released_year_max or
    vote_averages_min or vote_averages_max
):
    
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    data['vote_average'] = data['vote_average'].astype(float)

    vote_averages_min = float(vote_averages_min) if vote_averages_min else None
    vote_averages_max = float(vote_averages_max) if vote_averages_max else None

    filtered_data = data[
        (data.apply(lambda row: search_query_title.lower() in str(row['title']).lower(), axis=1)) &
        (data['release_date'].between(released_year_min, released_year_max,) if released_year_min and released_year_max else True) &
        (data['vote_average'].between(vote_averages_min, vote_averages_max,) if vote_averages_min and vote_averages_max else True)
    ]

    filter.write(filtered_data)

else:
    st.info("Enter a movie title, released year, or vote averages in the search bar.")
    filter.empty()
