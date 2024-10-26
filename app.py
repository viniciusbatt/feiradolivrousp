import streamlit as st
import numpy as np
import pandas as pd



estatisticas_page = st.Page('estatisticas.py', title='Estatísticas')
livros_page = st.Page('livros.py', title='Busca de Livros')

pg = st.navigation([livros_page, estatisticas_page])

st.set_page_config(page_title='Feira do Livro da USP 2024')


pg.run()
