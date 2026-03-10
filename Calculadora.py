import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Inicio",
    page_icon="👋",
)

st.write("# Bem-vindo ao Conversos LUAR Telecoom 👋")


st.sidebar.success("Selecione um teste acima")

# --- User Inputs ---
col1, col2 = st.columns(2) # Organize inputs into two columns

with col1:
    num1 = st.number_input("Enter first number", value=0.0, format="%f") # Use number_input for numeric values
with col2:
    num2 = st.number_input("Enter second number", value=0.0, format="%f")

