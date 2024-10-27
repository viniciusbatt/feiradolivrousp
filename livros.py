import streamlit as st
import numpy as np
import pandas as pd


conn = st.connection('livros_usp_2024', type='sql')

st.title('Catálogo de livros da Feira do Livro da USP 2024')

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

editoras_sem_livros_no_catalogo = editoras.loc[~editoras['name'].isin(livros['publisher'].unique(),), ['name', 'price_list', 'site']]


cols_metrics = st.columns(3)

with cols_metrics[0]:
    st.metric('Livros cadastrados', value=str(len(livros)))
    # st.metric('Livros únicos', value=str(livros['isbn'].nunique()))
with cols_metrics[1]:
    st.metric('Editoras', value=str(livros['publisher'].nunique()))
    st.metric('Autores', value=str(livros['authors'].nunique()))
with cols_metrics[2]:
    st.metric('Preço de capa', value='R$ ' + str("{:,.0f}".format(livros['price'].sum())).replace(',', '.'))
    st.metric('Preço com desconto', value='R$ ' + str("{:,.0f}".format(livros['price_discount'].sum())).replace(',', '.') + ' (' + str("{:.0f}".format(livros['price_discount'].sum() / livros['price'].sum() * 100)) +  ' %)')

st.subheader('Filtros')

cols_filtros1 = st.columns(2)

filtro_aplicado = False

# Assunto
with cols_filtros1[0]:
    lista_assuntos = conn.query('SELECT DISTINCT subject FROM livros_usp ORDER BY subject ASC')
    lista_assuntos = lista_assuntos['subject'].to_list()
    lista_assuntos.append('Todos')

    filtros_assuntos = st.selectbox('Assunto', options=lista_assuntos, index=len(lista_assuntos)-1)

    if filtros_assuntos != 'Todos':
        livros = livros.loc[livros['subject'] == filtros_assuntos,].copy()
        filtro_aplicado = True
# Editora
with cols_filtros1[1]:
    lista_editora = conn.query('SELECT DISTINCT publisher FROM livros_usp ORDER BY publisher ASC')

    lista_editora = lista_editora['publisher'].to_list()
    lista_editora.append('Todas')

    filtros_editora = st.selectbox('Editora', options=lista_editora, index=len(lista_editora)-1)



    if filtros_editora != 'Todas':
        filtro_aplicado = True
        livros = livros.loc[livros['publisher'] == filtros_editora,].copy()

cols_filtros2 = st.columns(3)
with cols_filtros2[0]:
    # Autor
    filtro_autor = st.text_input('Autor(es)')

    if filtro_autor:
        filtro_aplicado = True
        livros = livros.loc[livros['authors'].str.contains(filtro_autor, case=False)]
with cols_filtros2[1]:
    # Nome
    filtro_titulo = st.text_input('📗 Título')

    if filtro_titulo:
        filtro_aplicado = True
        livros = livros.loc[livros['name'].str.contains(filtro_titulo, case=False)]
with cols_filtros2[2]:
    # ISBN
    filtro_isbn = st.text_input('ISBN')

    if filtro_isbn:
        filtro_aplicado = True
        livros = livros.loc[livros['isbn'].str.startswith(filtro_isbn)]

# Preços
cols_filtro_precos = st.columns(2)

with cols_filtro_precos[0]:
    preco_minimo = st.number_input('Preço com desconto mínimo', value=livros['price_discount'].min())
with cols_filtro_precos[1]:
    preco_maximo = st.number_input('Preço com desconto máximo', value=livros['price_discount'].max())

if preco_minimo > livros['price_discount'].min():
    filtro_aplicado = True
    livros = livros.loc[livros['price_discount'] >= preco_minimo].copy()

if preco_maximo < livros['price_discount'].max():
    filtro_aplicado = True
    livros = livros.loc[livros['price_discount'] <= preco_maximo].copy()



if filtro_aplicado:
    cols_metrics_filtros = st.columns(3)

    with cols_metrics_filtros[0]:
        st.metric('Livros encontrados', value=str(len(livros)))
        # st.metric('Livros únicos', value=str(livros['isbn'].nunique()))
    with cols_metrics_filtros[1]:
        st.metric('Editoras', value=str(livros['publisher'].nunique()))
        st.metric('Autores', value=str(livros['authors'].nunique()))
    with cols_metrics_filtros[2]:
        st.metric('Preço de capa', value='R$ ' + str("{:,.0f}".format(livros['price'].sum())).replace(',', '.'))
        st.metric('Preço com desconto', value='R$ ' + str("{:,.0f}".format(livros['price_discount'].sum())).replace(',', '.') + ' (' + str("{:.0f}".format(livros['price_discount'].sum() / livros['price'].sum() * 100)) +  ' %)')

livros['link_pesquisa_google'] = 'https://www.google.com.br/search?q=isbn%3A+' + livros['isbn']

st.dataframe(livros.loc[:,['isbn', 'authors', 'name', 'price', 'price_discount', 'publisher', 'subject', 'link', 'link_pesquisa_google']], use_container_width=True, hide_index=True, column_config={
    'isbn': 'ISBN',
    'authors':  'Autores',
    'name': 'Título',
    'publisher': 'Editora',
    'subject': 'Assunto',
    'price': st.column_config.NumberColumn(
        label='Preço',
        format="R$ %.2f"
    ),
    'price_discount': st.column_config.NumberColumn(
        label='Preço com desconto',
        format="R$ %.2f"
    ),
    'link': st.column_config.LinkColumn(
        label='Link',
        width='small',
        display_text='🔗'
    ),
    'link_pesquisa_google': st.column_config.LinkColumn(
        label='Pesquisa Google',
        width='small',
        display_text='🔗'
    )
})

with st.expander('Editoras sem livros cadastrados no catálogo'):
    st.dataframe(editoras_sem_livros_no_catalogo, hide_index=True, column_config={
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
