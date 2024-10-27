import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title='Buscar livros da Feira do Livro da USP 2024', layout='wide', page_icon=':books:')

estatisticas_page = st.Page('estatisticas.py', title='Estatísticas', icon='📊')
livros_page = st.Page('livros.py', title='Busca de Livros', icon='📚')
sobre_page = st.Page('sobre.py', title='Sobre')

pg = st.navigation([livros_page, estatisticas_page, sobre_page])

pg.run()
