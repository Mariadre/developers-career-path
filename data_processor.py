import streamlit as st
import pandas as pd


@st.cache
def read_csv(path):
    return pd.read_csv(path)
