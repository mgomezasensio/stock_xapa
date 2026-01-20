from datetime import date
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def obtenir_df(DB_FILE):
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
        SELECT s.CodiStock, m.Material, q.Qualitat, a.Acabat, x.Espesor, s.Longitud, s.Amplada,
                s.Quantitat, m.Densitat, x.PreuKg, s.Anotacio
        FROM Stock as s
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
    conexio.close()
    df = pd.DataFrame(consultes)
    return df

def obtenir_df_preus (DB_FILE):
    sql_txt = """
        SELECT rp.CodiPreu, m.Material, q.Qualitat, a.Acabat, x.Espesor, rp.PreuKg, p.Proveidor, rp.Data
        FROM RegistresPreus as rp
        JOIN Xapes as x ON x.CodiXapa = rp.CodiXapa
        JOIN Materials as m ON m.CodiMaterial = x.CodiMaterial
        JOIN Qualitats as q ON q.CodiQualitat = x.CodiQualitat
        JOIN Acabats as a ON a.CodiAcabat = x.CodiAcabat
        JOIN Proveidors as p ON p.CodiProveidor = rp.CodiProveidor
        ORDER BY rp.Data
        """
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute(sql_txt)
    consultes = cursor.fetchall()
    conexio.close()
    df = pd.DataFrame(consultes)
    return df

# ---- FUNCIONS PANTALLES PROGRAMA ----

def pantalla_consulta_stock(DB_FILE, opcio):
    st.title(opcio)
    df = obtenir_df(DB_FILE)
    if not df.empty:
        df.columns = ["Codi", "Material", "Qualitat", "Acabat", "Espesor", "Longitud",
                      "Amplada", "Quantitat", "Densitat", "PreuKg", "Anotacio"]
        df = df[["Codi", "Material", "Qualitat", "Acabat", "Espesor",
                 "Longitud", "Amplada", "Quantitat", "Anotacio"]]
        st.dataframe(df, hide_index=True)
    else:
        st.error("No s'ha trobat cap resultat amb aquests filtres")

def pantalla_consulta_valor_stock(DB_FILE, opcio):
    st.title(opcio)
    df = obtenir_df(DB_FILE)
    if not df.empty:
        df.columns = ["Codi", "Material", "Qualitat", "Acabat", "Espesor", "Longitud",
                      "Amplada", "Quantitat", "Densitat", "PreuKg", "Anotacio"]
        df['Pes'] = round((df.Longitud/1000) * (df.Amplada/1000) * df.Espesor * df.Densitat * df.Quantitat, 2)
        df['Valor'] = round(df.Pes * df.PreuKg, 2)
    else:
        st.error("No s'ha trobat cap resultat amb aquests filtres")
        return
    
    st.metric("Valor (€)", f"{round(df.Valor.sum(), 2)} €")
    
    col1, col2 = st.columns(2)
    fig = px.histogram(df, x='Material', y='Valor', color="Qualitat", barmode="group")
    fig2 = px.bar(df, x='Material', y='Valor', color="Qualitat", text="Acabat")
    fig3 = px.pie(df, values="Quantitat", names="Material")
    fig4 = px.pie(df, values="Pes", names="Material")
    with col1:
        st.plotly_chart(fig, width='stretch')
        st.plotly_chart(fig3, width='stretch')
    with col2:
        st.plotly_chart(fig2, width='stretch')
        st.plotly_chart(fig4, width='stretch')
    
def pantalla_evolucio_preus(DB_FILE, opcio):
    st.title(opcio)
    df = obtenir_df_preus(DB_FILE)
    if not df.empty:
        df.columns = ["Codi registre", "Material", "Qualitat", "Acabat", "Espesor",
                      "PreuKg", "Proveidor", "Data"]
    else:
        st.error("No s'ha trobat cap resultat amb aquests filtres")
        return
    proveidors = ['Tots'] + sorted(df['Proveidor'].unique())
    proveidor = st.selectbox("Filtre per proveidor", proveidors)
    
    if proveidor != 'Tots':
        df = df[df['Proveidor'] == proveidor]
        
    df["Xapa"] = (
        df["Material"] + " " +
        df["Qualitat"] + " " +
        df["Acabat"] + " " +
        df["Espesor"].astype(str) + " mm" )
    
    if proveidor != 'Tots':
        xapes = ['Totes'] + sorted(df.Xapa[df.Proveidor == proveidor].unique())
        xapa = st.selectbox("Filtre per xapa", xapes)
    else:
        xapes = ['Totes'] + sorted(df.Xapa.unique())
        xapa = st.selectbox("Filtre per xapa", xapes)
    
    if xapa != 'Totes':
        df = df[df.Xapa == xapa]
    
    df = df[['Xapa', 'Proveidor', 'PreuKg', 'Data']]
    st.dataframe(df, hide_index=True)
    fig = px.line(df, x="Data", y="PreuKg", title='Evolució del preu de les xapes',
                  color="Xapa", markers=True)
    st.plotly_chart(fig, width='stretch')

# ---- FUNCIONS DEL PROGRAMA ----




# ---- FLUX PRINCIPAL DEL PROGRAMA ----

def main():
    DB_FILE = "./dat/stock_xapa.db"
    opcions_menu = ["Consulta stock", "Consulta valor stock", "Evolució preus"]
    
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
            "Evolució preus": pantalla_evolucio_preus
        }
    if opcio in pantalles:
        pantalles[opcio](DB_FILE, opcio)

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()

