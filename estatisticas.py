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

editoras = conn.query('SELECT * FROM editoras_usp ORDER BY url')

editoras = editoras.drop_duplicates(subset=['url'])

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
cols_metrics_editoras = st.columns(2)
with cols_metrics_editoras[0]:
    st.metric('Editoras cadastradas na feira', value=str(len(editoras)))
with cols_metrics_editoras[1]:
    st.metric('Editoras com livros no catálogo', value=str(livros['publisher'].nunique()))

st.dataframe(livros['publisher'].value_counts(), use_container_width=True)

st.subheader('Editoras sem livros cadastrados no catálogo')

st.dataframe(editoras.loc[~editoras['name'].isin(livros['publisher'].unique(),), ['name', 'price_list', 'site']], hide_index=True, column_config={
    'name': 'Editora',
    'price_list': st.column_config.LinkColumn(
        label='Catálogo de preços',
        width='medium',
        display_text='💸'
    ),
    'site': st.column_config.LinkColumn(
        label='Site',
        width='small',
        display_text='🔗'
    ),
})


st.header('Autores')
st.metric('Autores', value=str(livros['authors'].nunique()))

st.dataframe(livros['authors'].value_counts(), use_container_width=True)

