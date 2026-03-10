import streamlit as st
# import numpy as np
import math

st.set_page_config(page_title="RFID Item 13.1 - ATO 14448", page_icon="📈")

st.markdown("# RFID Item 13.1 - ATO 14448")
st.sidebar.header("RFID Item 13.1")
st.write(
    """ 13.1. Sistemas de Identificação por Radiofrequências (RFID),
    operando nas faixas 119 - 135 kHz, 13,11 - 13,36 MHz,
    13,41 - 14,01 MHz, 433,5 - 434,5 MHz, 860 - 869 MHz, 894 - 898,5 MHz,
    902 - 907,5 MHz, 915 - 928 MHz, 2.400 -  2.483,5 MHz e
    5.725 - 5.850 MHz devem atender aos limites definidos na Tabela V."""
)

st.image("13.1_rfid.PNG", caption="Print do ATO 14448")

# --- User Inputs ---
col1, col2, col3 = st.columns(3) # Organize inputs into two columns

with col1:
    freq_op = st.number_input("Entre com a frequencia em MHz:", min_value=0.0, value=0.0, format="%f")
with col2:
    distancia_ensaio = st.number_input("Entre com a distancia do ensaio em Metros", min_value=0.5, value=1.0, format="%f")
with col3:
    ICmedido = st.number_input("Entre com o valor medido pelo Lab. em [dBμV/m]", min_value=0.0, value=0.0, format="%f")


if st.button ("Calcular"):

# --- Descobrindo o fator por década ---
    if freq_op >= 30:
        st.image("decada_sup_30MHz.PNG", caption="Print do ATO 237")
        decada = 20
        st.write (f"O valor do fator de extrapolação para este caso é de: {decada} [dB/década]")
    else:
        st.image("decada_inf_30MHz.PNG", caption="Print do ATO 237")
        decada = 40
        st.write (f"O valor do fator de extrapolação para este caso é de: {decada} [dB/década]")
    
    

# --- Cálculos d limite extrapolado para a distância da medida---
    # fazer aqui e apresentar os cálculos do limite para conferir com os limites do relatório !!


# --- Cálculos do valor medido pelo lab extrapolado para a distância da medida---
    if freq_op >= 13.553 and freq_op <= 13.567:
        d1d2 = 30/distancia_ensaio
        extrapolacao = decada*(math.log10(d1d2))
        st.write (f"O fator de extrapolação da distância é igual a {decada}*log d1/d2, que neste caso é: {extrapolacao} [dB]")

        #Cálculo da IC extrapolada para distancia da norma em [dBμV/m]
        ICextrapolada = ICmedido - extrapolacao
        #Cálculo da IC extrapolada para distancia da norma convertida em linear [μV/m]
        ICextrapolada_linear = math.pow (10,(ICextrapolada/20))
        
        st.write ("RESULTADOS:")
        st.write (f"A intensidade de campo extrapolada para a distância da norma (30m) em [dBμV/m], é de: {ICextrapolada} [dBμV/m]")
        st.write (f"A intensidade de campo extrapolada para a distância da norma (30m) em [μV/m], é de: {ICextrapolada_linear} [μV/m]")
        