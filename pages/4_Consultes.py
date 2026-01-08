from datetime import date
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Consultes")
st.sidebar.title("Consultes")

# ---- FUNCIONS AUXILIARS ----

def obtenir_materials(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    materials = {fila[0]:fila[1] for fila in cursor.execute("SELECT Material, CodiMaterial FROM Materials").fetchall()}
    conexio.close()
    return materials

def obtenir_qualitats(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    qualitats = {fila[0]:fila[1] for fila in cursor.execute("SELECT Qualitat, CodiQualitat FROM Qualitats").fetchall()}
    conexio.close()
    return qualitats

def obtenir_acabats(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    acabats = {fila[0]:fila[1] for fila in cursor.execute("SELECT Acabat, CodiAcabat FROM Acabats").fetchall()}
    conexio.close()
    return acabats

def obtenir_espesors(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    espesors = [fila[0] for fila in cursor.execute("SELECT DISTINCT Espesor FROM Xapes").fetchall()]
    espesors.sort()
    conexio.close()
    return espesors


# ---- FUNCIONS PANTALLES PROGRAMA ----

def pantalla_consulta_stock(DB_FILE, opcio):
    st.title(opcio)
    col1, col2 = st.columns(2)
    with col1:
        materials = obtenir_materials(DB_FILE)
        material = st.selectbox("Filtra per **material**",
                                list(materials.keys()),
                                index=None,
                                placeholder="Material...")

        acabats = obtenir_acabats(DB_FILE)
        acabat = st.selectbox("Filtra per **acabat**",
                              list(acabats.keys()),
                              index=None,
                              placeholder="Acabat...")     

    with col2:
        qualitats = obtenir_qualitats(DB_FILE)
        qualitat = st.selectbox("Filtra per **qualitat**",
                                list(qualitats.keys()),
                                index=None,
                                placeholder="Qualitat...")

        espesors = obtenir_espesors(DB_FILE)
        espesor = st.selectbox("Filtra per **espesor**",
                               espesors,
                               index=None,
                               placeholder="Espesor...")
    sql_txt = """
        SELECT s.CodiStock, m.Material, q.Qualitat, a.Acabat, x.Espesor, s.Longitud, s.Amplada, s.Quantitat
        FROM Stock as S
        JOIN Xapes as x ON x.CodiXapa = s.CodiXapa
        JOIN Materials as m ON m.CodiMaterial = x.CodiMaterial
        JOIN Qualitats as q ON q.CodiQualitat = x.CodiQualitat
        JOIN Acabats as a ON a.CodiAcabat = x.CodiAcabat
        WHERE s.Estat = "Activa"
        """
    parametres = []
    if material:
        sql_txt += " AND m.Material = ?"
        parametres.append(material)
    if qualitat:
        sql_txt += " AND q.Qualitat = ?"
        parametres.append(qualitat)
    if acabat:
        sql_txt += " AND a.Acabat = ?"
        parametres.append(acabat)
    if espesor:
        sql_txt += " AND x.Espesor = ?"
        parametres.append(espesor)

    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute(sql_txt, parametres)
    consultes = cursor.fetchall()
    df = pd.DataFrame(consultes)
    if not df.empty:
        df.columns = ["Codi", "Material", "Qualitat", "Acabat", "Espesor", "Longitud", "Amplada", "Quantitat"]
    else:
        st.error("No s'ha trobat cap resultat amb aquests filtres")
    st.dataframe(df, hide_index=True)

    
def pantalla_consulta_valor_stock(DB_FILE, opcio):
    st.title(opcio)
    st.info(""""Aquí s'haurà d'introduir un material, una qualitat, un acabat i un espesor
            i ens mostrarà el preu d'aquesta xapa""")
    pass

# ---- FUNCIONS DEL PROGRAMA ----



# ---- FLUX PRINCIPAL DEL PROGRAMA ----

def main():
    DB_FILE = "./dat/stock_xapa.db"
    opcions_menu = ["Consulta stock", "Consulta valor stock"]
    
    with st.sidebar:
        st.header("Menú principal")
        opcio = st.selectbox("Selecciona una opció",
                             opcions_menu,
                             index = None,
                             placeholder = "Selecciona una opció...")
        
    # ---- PANTALLES MENÚ ----
    pantalles = {
            "Consulta stock": pantalla_consulta_stock,
            "Consulta valor stock": pantalla_consulta_valor_stock,
        }
    if opcio in pantalles:
        pantalles[opcio](DB_FILE, opcio)

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()

