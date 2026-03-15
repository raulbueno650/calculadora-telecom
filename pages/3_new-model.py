import streamlit as st
# import numpy as np
import math
import pandas as pd

# Configuração da página
st.set_page_config(page_title="RFID Item 13.1 - ATO 14448", page_icon="🔢")
st.sidebar.header("new-modelo-side")

st.markdown('<span style="color:gold; font-size: 48px">📚</span> <span style="font-size: 48px; font-weight: bold">RFID Item 13.1 - ATO 14448</span>', unsafe_allow_html=True)
st.write(
    """ 13.1. Sistemas de Identificação por Radiofrequências (RFID),
    operando nas faixas 119 - 135 kHz, 13,11 - 13,36 MHz,
    13,41 - 14,01 MHz, 433,5 - 434,5 MHz, 860 - 869 MHz, 894 - 898,5 MHz,
    902 - 907,5 MHz, 915 - 928 MHz, 2.400 -  2.483,5 MHz e
    5.725 - 5.850 MHz devem atender aos limites definidos na Tabela V."""
)
st.markdown('---')

#Resumo da intensidade de campo
st.subheader('Calculo da conversão de intensidade de campo')
st.markdown("**Equação:** $E_{\mu V/m} = 10^{\\frac{E_{dB\\mu V/m}}{20}}$")
st.write("""     
    Onde:
    - E[dBμV/m] = Intensidade de campo em dBμV/m
    - E[μV/m] = Intensidade de campo em μV/m
    """)

st.markdown('---')

#Resumo do calculo para extrapolação de distância
st.subheader('Calculo da extrapolação de distância')
st.write(""" 
    O ATO 237 permite que os ensaios sejam realizados a uma distância diferente especificada nos regulamentos específicos,
    desde que não sejam realizadas na região de campo próximo.
    Ao realizar as medições a uma distância diferente da especificada,
    os resultados devem ser extrapolados para a distância especificada, usando um fator de extrapolação de:
     """) 
st.write("""
    - $F_{extrapolação} = 20 dB/década$ para frequencias <= 30 MHz
    - $F_{extrapolação} = 40 dB/década$ para frequencias > 30 MHz
    """)
st.write("""  
    Para realizarmos o cálculo do valor de extrapolação de distância, utilizamos a seguinte Equação: 
    $E_{extrapolação} = F_{extrapolação} * log_{10}(\\frac{d1}{d2})$
    """)
st.write("""     
    Onde:
    - $E_{extrapolação}$ = Valor da extrapolação da distância em dB
    - $F_{extrapolação}$ = Fator de extrapolação em dB/década (20 ou 40 dB/década)
    - $d1$ = Distância especificada na norma (m)
    - $d2$ = Distância do ensaio (m)
    """)

st.markdown('---')
st.subheader('Calculadora 🔢')
# --- User Inputs ---
col1, col2, col3 = st.columns(3) # Organize inputs em 03 colunas

with col1:
    faixas = {
    "119 – 135 kHz": {"E": "2400/F(kHz)", "dist": 300},
    "13.11 – 13.36 MHz": {"E": 106, "dist": 30},
    "13.41 – 13.553 MHz": {"E": 334, "dist": 30},
    "13.553 – 13.567 MHz": {"E": 15848, "dist": 30},
    "13.567 – 13.710 MHz": {"E": 334, "dist": 30},
    "13.710 – 14.01 MHz": {"E": 106, "dist": 30},
    "433.5 – 434.5 MHz": {"E": 70359, "dist": 3},
    "860 – 869 MHz": {"E": 70359, "dist": 3},
    "894 – 898.5 MHz": {"E": 70359, "dist": 3},
    "902 – 907.5 MHz": {"E": 70359, "dist": 3},
    "915 – 928 MHz": {"E": 70359, "dist": 3},
    "2400 – 2483.5 MHz": {"E": 50000, "dist": 3},
    "5725 – 5850 MHz": {"E": 50000, "dist": 3},
    }

    faixa = st.selectbox(
    "Selecione a faixa de frequência",
    list(faixas.keys())
    )

# Tratamento especial da primeira faixa caso o usuário selecione a faixa de 119-135 kHz, onde o limite é dado por uma fórmula e não por um valor fixo:
if faixa == "119 – 135 kHz":
    kHz_value = st.number_input("Digite a frequência em kHz (entre 119 e 135):", min_value=119.0, max_value=135.0, value=119.0, format="%f")
    faixas[faixa]["E"] = 2400/kHz_value

with col2:
    distancia_ensaio = st.select_slider(
    "Distância do Ensaio (m):",
    options=[1, 3, 10]
    )

with col3:
    E_medido = st.number_input("Valor medido pelo Lab. em [dBμV/m]", min_value=1.0, value=1.0, format="%f")


#Cálculos --------------------------------------------------------------
# --- Descobrindo o fator por década ---
if faixa in  ("119 – 135 kHz", "13.11 – 13.36 MHz", "13.41 – 13.553 MHz", "13.553 – 13.567 MHz", "13.567 – 13.710 MHz", "13.710 – 14.01 MHz"):
    decada = 40
    st.write (f"O fator de extrapolação para este caso é de: {decada} [dB/década]")
else:
     decada = 20
     st.write (f"O fator de extrapolação para este caso é de: {decada} [dB/década]")
 
# --- Descobrindo valor da extrapolação ---

d1d2 = faixas[faixa]["dist"]/distancia_ensaio
extrapolacao = decada*(math.log10(d1d2))
st.write (f"O valor da extrapolação da distância neste caso é de: {round(extrapolacao, 2)} [dB]")

# --- Calculado os valores do limites tanto em linear quanto em dB ---
# Limite da norma na distancia da norma:
    #Limite liner é o próptio E da lista de faixas da entrada do usuário, que já está em μV/m;
#Limite em dB é o limite linear convertido para dB usando a fórmula: E[dBμV/m] = 20*log10(E[μV/m])
E_norma_db = 20*math.log10(faixas[faixa]["E"])

# Limite do RELATORIO em Logaritmico e Linear extrapolado para distancia do ensaio:
limite_rel_db = E_norma_db + extrapolacao
limite_rel_linear = math.pow(10, limite_rel_db/20)


#Calculando o valor da conversão do valor medido pelo laboratório para norma tanto em dB quanto em linear:
E_medido_extrapolado = E_medido - extrapolacao #Já na distância da norma
E_medido_extrapoaldo_linear = math.pow(10, E_medido_extrapolado/20) #Já na distância da norma

#Calculos feitos, agora vamos organizar a apresentação dos resultados para o usuário:

tab1, tab2, tab3 = st.tabs(["Cálculo do Limite do Relatório", "Cálculo Resumido", "Cálculo Passo a Passo"])

with tab1:
    st.subheader("Cálculo do Limite do Relatório")
    st.write("Para a Faixa selecionada de:", faixa)
    st.write("O Limite de campo elétrico da norma é de:", faixas[faixa]["E"], "µV/m")
    st.write("A Distância de medição da norma é de:", faixas[faixa]["dist"], "m")
    st.write("Logo, segue a tabela:")

    # Criando a tabela com os dados:
    #Linha 1 distancia da norma: Limite da norma em Linear e Logaritmico
    #Linha 2 distancia do ensaio: Limite da norma extrapolado para a distância do ensaio em Linear e Logaritmico
    
    dados = pd.DataFrame(
    [
        [faixas[faixa]["dist"], faixas[faixa]["E"], E_norma_db],
        [distancia_ensaio, limite_rel_linear, limite_rel_db]
    ],
    columns=[
        "Distância (m)",
        "Limite Linear (µV/m)",
        "Limite (dBµV/m)"
    ],
    index=[
        "Limites da Norma",
        "Limites do Relatório"
    ]
    )

    st.table(
    dados.style.format({
        "Distância (m)": "{:.1f}",
        "Limite Linear (µV/m)": "{:.1f}",
        "Limite (dBµV/m)": "{:.2f}"
        })
    )   


with tab2:
    st.subheader("Cálculo Resumido")
    #Cálculo da IC extrapolada para distancia da norma em [dBμV/m]
    E_medido_extrapolado = E_medido - extrapolacao
    #Cálculo da IC extrapolada para distancia da norma convertida em linear [μV/m]
    E_medido_extrapolado_linear = math.pow (10,(E_medido_extrapolado/20))

    st.write(f"""     
    A Intensidade de Campo medida convertida para a distância da norma é de:
    - {E_medido_extrapolado}, **[dBμV/m]**
    - {E_medido_extrapoaldo_linear}, **[μV/m]**
    """)




with tab3:
     st.subheader("Cálculo Passo a Passo")