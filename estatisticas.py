import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


st.title('Estatísticas')



conn = st.connection('livros_usp_2024', type='sql')

livros = conn.query('SELECT * FROM livros_usp ORDER BY publisher, authors, name')

livros = livros.drop_duplicates(subset=['name', 'subject', 'isbn', 'authors', 'publisher'])

livros['price'] = livros['price'].str.strip('R$ ').str.replace(',', '.')
livros.loc[livros['price'] == '', ['price']] = np.nan
livros['price'] = livros['price'].astype('float')


livros['price_discount'] = livros['price_discount'].str.strip('R$ ').str.replace(',', '.')
livros.loc[livros['price_discount'] == '', ['price_discount']] = np.nan
livros['price_discount'] = livros['price_discount'].astype('float')

st.header('Preços')
cols_metrics_precos = st.columns(3)
with cols_metrics_precos[0]:
    st.metric('Preço médio', value='R$ ' + str("{:,.2f}".format(livros['price_discount'].mean())))
with cols_metrics_precos[1]:
    st.metric('Preço Máximo', value='R$ ' + str("{:,.2f}".format(livros['price_discount'].max())))
with cols_metrics_precos[2]:
    st.metric('Preço Mínimo', value='R$ ' + str("{:,.2f}".format(livros['price_discount'].min())))

fig_precos = px.histogram(livros.loc[:,['price_discount']], title='Histograma de preços', text_auto=True ) #color='publisher'

st.plotly_chart(fig_precos)


st.header('Editoras')
st.metric('Editoras', value=str(livros['publisher'].nunique()))

st.dataframe(livros['publisher'].value_counts(), use_container_width=True)


st.header('Autores')
st.metric('Autores', value=str(livros['authors'].nunique()))

st.dataframe(livros['authors'].value_counts(), use_container_width=True)

