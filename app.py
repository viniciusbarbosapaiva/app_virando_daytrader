import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit import bootstrap
import warnings
warnings.filterwarnings('ignore')
from itertools import product

# Funções
def gerenciamento(gain_valor,loss_valor, repeticao):
    gain = gain_valor
    loss = loss_valor
    n = repeticao
    
    # multiplos de 2
    multiplos_2= [n for n in range(1, 2*n) if n % 2 == 0]
    multiplos_2.insert(0,1)
    multiplos_2 = np.array(multiplos_2)
    
    # Verificando quantas combinações são possíveis
    caracteres = [0, 1]
    combinacao = list(product(caracteres, repeat=n))
    
    print('realizando {} por dia, há a possibilidade de {} combinações'.format(n, len(combinacao)))
    
    # Transformando de tupla para lista
    combinacao = [list(i) for i in combinacao]
    
    # Criando index
    index = [i for i in np.arange(0, len(combinacao))]
    
    # Zipando o index com combinação
    combinacao_pontos = list(zip(index,combinacao))
    
    # Criando dicionário
    combinacao_dict = {k:v for (k,v) in combinacao_pontos}
    
    # Transformando dicionário em DataFrame
    combinacao_df = pd.DataFrame({'item':combinacao_dict.values()})
    combinacao_df.head()
    
    # Criando a coluna VAlores
    combinacao_df['valores'] = combinacao_df['item']
    
    # Transformando a coluna valores com a primeira regra de gerenciamento 2 para 1
    lista = []
    for i in np.arange(0,len(combinacao_df)):
        lista = [gain if price == 1 else loss for price in combinacao_df['item'][i]]
        combinacao_df['valores'][i] = lista 
    combinacao_df.head()
    
    # Verificando os valores monetários de cada combinação
    # soma sem Soros
    combinacao_df['soma_s_soros'] = combinacao_df['valores'].apply(lambda x: np.sum(x))
    combinacao_df.head()
    
    # Transformando a coluna valores com a segunda regra de gerenciamento, aplicando soros 
    combinacao_df['valores_c_soros'] = combinacao_df['item']
    combinacao_df['valores_c_soros'] = combinacao_df['valores_c_soros'].apply(lambda x: np.array(x))
    combinacao_df.head()
    
    lista_02 = []
    for i in np.arange(0,len(combinacao_df)):
        lista_02 = [gain if price == 1 else loss for price in combinacao_df['valores_c_soros'][i]][0]
        combinacao_df['valores_c_soros'][i][0] = lista_02
    
    a = 0
    a_1 =1
    length = n
    while a_1 != length:
        for i in np.arange(0,len(combinacao_df)):
    
            if combinacao_df['valores_c_soros'][i][a] <= 0 and combinacao_df['item'][i][a_1] <= 0:
                combinacao_df['valores_c_soros'][i][a_1] = loss
            elif combinacao_df['valores_c_soros'][i][a] <= 0 and combinacao_df['item'][i][a_1] >= 1:
                combinacao_df['valores_c_soros'][i][a_1] = gain
            elif combinacao_df['valores_c_soros'][i][a] >= 1  and combinacao_df['item'][i][a_1] >= 1:
                combinacao_df['valores_c_soros'][i][a_1] = combinacao_df['valores_c_soros'][i][a]+gain
            elif combinacao_df['valores_c_soros'][i][a] >= 1  and combinacao_df['item'][i][a_1] <= 0:
                combinacao_df['valores_c_soros'][i][a_1] = -combinacao_df['valores_c_soros'][i][a]
        a += 1
        a_1 +=1 
    combinacao_df.head()
    
    # Verificando os valores monetários de cada combinação
    # soma com Soros
    combinacao_df['soma_c_soros'] = combinacao_df['valores_c_soros'].apply(lambda x: np.sum(x))
    combinacao_df.head()
    
    # Transformando a coluna valores com a terceira regra de gerenciamento, aplicando martingale
    combinacao_df['valores_c_martingale'] = combinacao_df['item']

    combinacao_df['valores_c_martingale'] = combinacao_df['valores_c_martingale'].apply(lambda x: np.array(x))

    lista_02 = []
    for i in np.arange(0,len(combinacao_df)):
        lista_02 = [gain if price == 1 else loss for price in combinacao_df['valores_c_martingale'][i]][0]
        combinacao_df['valores_c_martingale'][i][0] = lista_02
        
    a = 0
    a_1 =1
    length = len(combinacao_df['valores_c_martingale'][0])
    while a_1 != length:
        for i in np.arange(0,len(combinacao_df)):
    
            if combinacao_df['valores_c_martingale'][i][a] <= 0 and combinacao_df['item'][i][a_1] <= 0:
                combinacao_df['valores_c_martingale'][i][a_1] =  loss + combinacao_df['valores_c_martingale'][i][a] 
            elif combinacao_df['valores_c_martingale'][i][a] <= 0 and combinacao_df['item'][i][a_1] >= 1:
                combinacao_df['valores_c_martingale'][i][a_1] = (combinacao_df['valores_c_martingale'][i][a] + np.abs(combinacao_df['valores_c_martingale'][i][a])) + gain*a_1
            elif combinacao_df['valores_c_martingale'][i][a] >= 1  and combinacao_df['item'][i][a_1] >= 1:
                combinacao_df['valores_c_martingale'][i][a_1] = combinacao_df['valores_c_martingale'][i][a] + gain
            elif combinacao_df['valores_c_martingale'][i][a] >= 1  and combinacao_df['item'][i][a_1] <= 0:
                combinacao_df['valores_c_martingale'][i][a_1] = loss * a_1
        a += 1
        a_1 +=1
        
    # Verificando os valores monetários de cada combinação
    # soma com Martingale
    combinacao_df['soma_c_martingale'] = combinacao_df['valores_c_martingale'].apply(lambda x: np.sum(x))
    combinacao_df.head()
    
    # Transformando a coluna valores com a terceira regra de gerenciamento, aplicando segundo martingale
    # Criando colnas com aplicação do martingale 01
    combinacao_df['valores_c_martingale_01'] = combinacao_df['valores']

    combinacao_df['valores_c_martingale_01'] = combinacao_df['valores_c_martingale_01'].apply(lambda x: np.array(x))

    lista_02 = []
    for i in np.arange(0,len(combinacao_df)):
        lista_02 = [gain if price == 1 else loss for price in combinacao_df['valores_c_martingale_01'][i]][0]
        combinacao_df['valores_c_martingale_01'][i][0] = lista_02
    
    combinacao_df['valores_c_martingale_01'] = combinacao_df['valores_c_martingale_01'].apply(lambda x: x*multiplos_2)
    
    # Verificando os valores monetários de cada combinação
    # soma com Martingale_01
    combinacao_df['soma_c_martingale_01'] = combinacao_df['valores_c_martingale_01'].apply(lambda x: np.sum(x))
    
    return combinacao_df
    
def print_gerenciamento(value_gain, value_loss, repetion):
    c1,c2,c3 = st.beta_columns((0.5,1,0.5))

    analise = gerenciamento(value_gain, value_loss, repetion)    

    return analise

def resumo():    
   
    c1,c2,c3 = st.beta_columns((0.5,1,0.5))
    analise = print_gerenciamento(gain, loss, operacoes)
    
    positivo_s_soros = analise[analise['soma_s_soros'] >0]   
    c2.text('Quantidades de vezes que a configuração sem aplicação do soros \nfoi positivo= {}%'.format((len(positivo_s_soros)/len(analise))*100))
    c2.text('Únicos valores de prejuizo e ganhos da configuração sem soros = {}'.format(sorted(analise['soma_s_soros'].unique()))) 
    
    c2.text(100*'-')
    
    positivo_c_soros = analise[analise['soma_c_soros'] >0] 
    c2.text('Quantidades de vezes que a configuração com aplicação do soros \nfoi positivo= {}%'.format((len(positivo_c_soros)/len(analise))*100))
    c2.text('Únicos valores de prejuizo e ganhos da configuração com soros = {}'.format(sorted(analise['soma_c_soros'].unique())))
    
    c2.text(100*'-')
    
    positivo_c_martingale = analise[analise['soma_c_martingale'] >0]
    c2.text('Quantidades de vezes que a configuração com aplicação do martingale \nfoi positivo= {}%'.format((len(positivo_c_martingale)/len(analise))*100))
    c2.text('Únicos valores de prejuizo e ganhos da configuração com martingale = {}'.format(sorted(analise['soma_c_martingale'].unique())))
    
    c2.text(100*'-')
    
    positivo_c_martingale_01 = analise[analise['soma_c_martingale_01'] >0]
    c2.text('Quantidades de vezes que a configuração com aplicação do segundo martingale \nfoi positivo= {}%'.format((len(positivo_c_martingale_01)/len(analise))*100))
    c2.text('Únicos valores de prejuizo e ganhos da configuração com martingale = {}'.format(sorted(analise['soma_c_martingale_01'].unique())))
    
    c2.text(100*'-')
    
    c2.subheader('Download do Documento')
    operacao = c2.selectbox('Deseja realizar download das combinações?',('Sim','Não'), index=1)
    
    
    if operacao == 'Sim':
        c4,c5,c6 = st.beta_columns((1,1,1))
        download = c5.download_button('Download CSV', positivo_s_soros.to_csv().encode('utf-8'),"file.csv","text/csv",key='download-csv')
        if download:
            c7,c8,c9 = st.beta_columns((1,1,1))
            c8.write('Obrigado pelo download!')
        
    elif operacao == 'Não':
        c7,c8,c9 = st.beta_columns((1,1,1))
        c8.write('Caso queira baixar as combinações, selecione "Sim".')
    

# Definindo layout da página
logo_aba = Image.open(r'virando_daytrader_logo.png')
logo_aba = logo_aba.resize((16, 16), Image.ANTIALIAS)
st.set_page_config(
    layout="wide",
    page_title='App Virando Daytrader',
    page_icon=logo_aba
)

# Define o título do Dashboard
image = Image.open(r'virando_daytrader_logo.png')
image = image.resize((200, 200), Image.ANTIALIAS)
st.markdown('---')
c1,c2,c3 = st.beta_columns((1,1,1))
c1.image(image)
c2.title("App Virando Daytrader")
c3.subheader("Autor: Vinícius B. Paiva ([LinkedIn](https://www.linkedin.com/in/vinicius-barbosa-paiva/)) ([GitHub](https://github.com/viniciusbarbosapaiva))")
st.markdown('---')


# Definindo os Botões para as respostas
c4,c5,c6 = st.beta_columns((1,1,1))
c4.subheader('Qual será o valor do gain (em valor monetário R$)?')
gain = c4.number_input('Pontos para Take Profit', value=int(80))
c5.subheader('Qual será o valor do loss (em valor monetário R$)?')
loss = c5.number_input('Pontos para Stop Loss', value=int(-40))
c6.subheader('Quantas operações serão realizadas?')
operacoes = c6.slider('Selecione Quantidade',2,15)
st.markdown('---')

# Botão para gerar combinações
c7,c8,c9 = st.beta_columns((1,1,1))
c8.subheader("Gerar Combinações?")
resumo_botao = c8.selectbox('Deseja gerar combinações?', ['Sim', 'Não'], index=1)

# Ir para aba Resumo do trabalho
if resumo_botao == 'Sim':
    resumo()


#real_script = 'app.py'
#bootstrap.run(real_script, f'run.py {real_script}', [], {})
