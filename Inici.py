from datetime import date
import streamlit as st
import sqlite3


st.set_page_config(
    page_title="Gestió del stock de xapes",
)

st.write("# Gestió del stock de xapes")
tab1, tab2 = st.tabs(['Descripció', 'Instruccions'])
with tab1:
    st.write("Aquest programa crea i gestiona una base de dades de xapes metàl·liques, podent afegir, modificar i eliminar xapes del stock.")
    st.space('small')
    st.write("""Aquesta és la interfície principal, on es mostraran i s'introduïran les dades. A la barra lateral es pot seleccionar la secció on es vol treballar:
                \n - Auxiliars: Apartat on es poden iniciar les dades per defecte i afegir nous materials, qualitats, acabats i proveïdors.
                \n - Manteniment xapes: Apartat on s'afegeixen les xapes i on es poden modificar els preus.
                \n - Manteniment stock: Apartat on s'afegeixen, es modifiquen i s'eliminen les xapes existents al stock del magatzem.
                \n - Consultes: Apartat on es poden consultar diferents dades sobre el stock disponible i els preus de les xapes.""")
with tab2:
    st.write("**Instruccions d'us del programa**")
    st.markdown("""
    1. Iniciar els diferents valors de la base de dades  
        - Iniciar materials per defecte  
        - Iniciar qualitats per defecte  
        - Iniciar acabats per defecte  
        - Introduir els diferents proveïdors  

    2. Introduir les xapes amb l'espessor i el preu/Kg  

    3. Introduir les xapes al stock  

    4. Modificar o eliminar les xapes utilitzades amb el codi identificatiu de cada xapa del stock  
        - Xapa al stock amb més d'una unitat
            - Si s'ha utilitzat tot el material en stock  
                - Eliminar la xapa del stock corresponent amb el codi d'aquesta  
            - Si **no** s'ha utilitzat tot el material
                - Introduir quantitat utilitzada i afegir el nou retal sobrant (si n'ha quedat)
        - Xapa al stock amb una unitat
            - Introduir les noves dimensions i, si calen, anotacions
            - Si surten altres retals, afegir-los
    """)

