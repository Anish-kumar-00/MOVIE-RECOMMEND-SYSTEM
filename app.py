import streamlit as st
import pickle
import requests
import gzip

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]