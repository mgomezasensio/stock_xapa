from datetime import date
import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="Manteniment Xapes")
st.sidebar.title("Manteniment Xapes")

# ---- FUNCIONS AUXILIARS ----

def obtenir_dada(cursor):
    fila = cursor.fetchone()
    if fila:
        return fila[0]
    else:
        return None

def obtenir_dades(cursor):
    fila = cursor.fetchone()
    if fila:
        return fila
    else:
        return None

def obtenir_materials(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    materials = {fila[0]:fila[1] for fila in cursor.execute("SELECT Material, CodiMaterial FROM Materials").fetchall()}
    conexio.close()
    return materials

def obtenir_qualitats(DB_FILE, codi_material):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    qualitats = {fila[0]:fila[1] for fila in cursor.execute("""SELECT Qualitat, CodiQualitat FROM Qualitats
                                                                WHERE CodiMaterial = ?""", (codi_material,)).fetchall()}
    conexio.close()
    return qualitats

def obtenir_acabats(DB_FILE, codi_material):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    acabats = {fila[0]:fila[1] for fila in cursor.execute("""SELECT Acabat, CodiAcabat FROM Acabats
                                                            WHERE CodiMaterial = ?""", (codi_material,)).fetchall()}
    conexio.close()
    return acabats

def obtenir_espesors(DB_FILE, codi_material, codi_qualitat, codi_acabat):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    espesors = [fila[0] for fila in cursor.execute("""SELECT DISTINCT Espesor FROM Xapes
                                                        WHERE CodiMaterial = ? AND CodiQualitat = ? AND CodiAcabat = ?""",
                                                       (codi_material, codi_qualitat, codi_acabat)).fetchall()]
    conexio.close()
    return espesors

def obtenir_proveidors(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    proveidors = {fila[0]:fila[1] for fila in cursor.execute("SELECT Proveidor, CodiProveidor FROM Proveidors").fetchall()}
    conexio.close()
    return proveidors

# ---- FUNCIONS PANTALLES PROGRAMA ----

def pantalla_afegir_xapa(DB_FILE, opcio):
    st.title(f"{opcio} Xapa")
    with st.popover("Explicació"):    
        st.info("""En aquesta pàgina pots introduïr les xapes amb les que es treballa, seleccionant material,
                qualitat i acabat i afegint l'espesor, el proveïdor i el preu""")
    materials = obtenir_materials(DB_FILE)
    material = st.selectbox("Selecciona el material",
                            list(materials.keys()),
                            index=None,
                            placeholder="Material...",
                            key=f"{opcio}_xapa_material")
    sql_txt = ""
    parametres = []
    if material:
        codi_material = materials[material]
        sql_txt = """SELECT x.CodiXapa, m.Material, q.Qualitat, a.Acabat, x.Espesor
                    FROM Xapes AS x
                    JOIN Materials AS m
                    ON m.CodiMaterial = x.CodiMaterial
                    JOIN Qualitats AS q
                    ON q.CodiQualitat = x.CodiQualitat
                    JOIN Acabats AS a
                    ON a.CodiAcabat = x.CodiAcabat
                    WHERE m.Material = ?
                    """
        parametres.append(material)
    else:
        codi_material = None
    
    qualitats = obtenir_qualitats(DB_FILE, codi_material)
    qualitat = st.selectbox("Selecciona la qualitat",
                            list(qualitats.keys()),
                            index=None,
                            placeholder="Qualitat...",
                            key=f"{opcio}_xapa_qualitat")
    if qualitat:
        codi_qualitat = qualitats[qualitat]
        sql_txt += " AND q.Qualitat = ?"
        parametres.append(qualitat)
    else:
        codi_qualitat = None        
    
    acabats = obtenir_acabats(DB_FILE, codi_material)
    acabat = st.selectbox("Selecciona l'acabat",
                          list(acabats.keys()),
                          index=None,
                          placeholder="Acabat...",
                          key=f"{opcio}_xapa_acabat")
    if acabat:
        codi_acabat = acabats[acabat]
        sql_txt += " AND a.Acabat = ?"
        parametres.append(acabat)
    else:
        codi_acabat = None

    with st.form(f"{opcio} Xapa", clear_on_submit=False, enter_to_submit=False):
        espesor = st.number_input("Introdueix l'espesor",
                                  value=None,
                                  format = "%0.1f",
                                  placeholder = "Espesor...")
        proveidors = obtenir_proveidors(DB_FILE)
        proveidor = st.selectbox("Selecciona el proveïdor",
                            list(proveidors.keys()),
                            index=None,
                            placeholder="Proveïdor...",
                            key=f"{opcio}_xapa_proveidor")
        if proveidor:
            codi_proveidor = proveidors[proveidor]
        else:
            codi_proveidor = None
        preu_kg = st.number_input("Introdueix el preu per Kg",
                                  value=None,
                                  format = "%0.2f",
                                  placeholder = "Preu per Kg...")
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button(f"{opcio} Xapa")
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute(sql_txt, parametres)
    consultes = cursor.fetchall()
    conexio.close()
    df = pd.DataFrame(consultes)
    
    if not df.empty:
        df.columns = ["Codi", "Material", "Qualitat", "Acabat", "Espesor"]
        st.dataframe(df, hide_index=True)
    else:
        st.error("No s'ha trobat cap resultat amb aquests filtres")
    
    if submitted:
        if not (codi_material and codi_qualitat and codi_acabat):
            st.error("Has de seleccionar el material, la qualitat i l'acabat")
        elif not codi_proveidor:
            st.error("Has de seleccionar el proveïdor")
        elif not(espesor and preu_kg):
            st.error("Has d'introduir l'espesor i el preu per Kg")
        else:
            afegir_xapa(DB_FILE, codi_material, codi_qualitat, codi_acabat, codi_proveidor, espesor, preu_kg) 

def pantalla_modificar_xapa(DB_FILE, opcio):
    st.title(f"{opcio} Xapa")
    with st.popover("Explicació"):
        st.info("En aquesta pàgina pots modificar el preu de les xapes seleccionant material, qualitat, acabat i espesor i afegir el proveïdor i el nou preu")
    materials = obtenir_materials(DB_FILE)
    material = st.selectbox("Selecciona el material",
                            list(materials.keys()),
                            index=None,
                            placeholder="Material...",
                            key=f"{opcio}_xapa_material")
    if material:
        codi_material = materials[material]
    else:
        codi_material = None
    qualitats = obtenir_qualitats(DB_FILE, codi_material)
    qualitat = st.selectbox("Selecciona la qualitat",
                            list(qualitats.keys()),
                            index=None,
                            placeholder="Qualitat...",
                            key=f"{opcio}_xapa_qualitat")
    if qualitat:
        codi_qualitat = qualitats[qualitat]
    else:
        codi_qualitat = None
    acabats = obtenir_acabats(DB_FILE, codi_material)
    acabat = st.selectbox("Selecciona l'acabat",
                          list(acabats.keys()),
                          index=None,
                          placeholder="Acabat...",
                          key=f"{opcio}_xapa_acabat")
    if acabat:
        codi_acabat = acabats[acabat]
    else:
        codi_acabat = None
    espesors = obtenir_espesors(DB_FILE, codi_material, codi_qualitat, codi_acabat)
    espesor = st.selectbox("Selecciona l'espesor",
                           espesors,
                           index=None,
                           placeholder="Espesor...",
                           key=f"{opcio}_xapa_espesor")
    if not espesor:
        espesor = None

    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute("""SELECT CodiXapa, PreuKg FROM Xapes
                    WHERE CodiMaterial = ? AND CodiQualitat = ? AND
                    CodiAcabat = ? AND Espesor = ?""",
                   (codi_material, codi_qualitat, codi_acabat, espesor)
                   )
    fila = obtenir_dades(cursor)
    if fila:
        codi_xapa, preu_kg = fila
    else:
        codi_xapa, preu_kg = None, None 
    conexio.close()
    st.info(f"Preu anterior = **{preu_kg} €/Kg**")
    with st.form(f"{opcio} Xapa", clear_on_submit=False, enter_to_submit=False):
        proveidors = obtenir_proveidors(DB_FILE)
        proveidor = st.selectbox("Selecciona el proveïdor",
                            list(proveidors.keys()),
                            index=None,
                            placeholder="Proveïdor...",
                            key=f"{opcio}_xapa_proveidor")
        if proveidor:
            codi_proveidor = proveidors[proveidor]
        else:
            codi_proveidor = None
        nou_preu_kg = st.number_input("Introdueix el nou preu per Kg",
                                      value=None,
                                      format = "%0.2f",
                                      placeholder = "Preu per Kg...")
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button(f"{opcio} Xapa")

    if submitted:
        if not(codi_material and codi_qualitat and codi_acabat and espesor):
            st.error("Has de seleccionar el material, la qualitat, l'acabat i l'espesor")
        elif not nou_preu_kg:
            st.error("Has d'introduir el nou preu per Kg")
        else:
            modificar_xapa(DB_FILE, codi_xapa, codi_proveidor, nou_preu_kg)

# ---- FUNCIONS DEL PROGRAMA ----

def afegir_xapa(DB_FILE, codi_material, codi_qualitat, codi_acabat, codi_proveidor, espesor, preu_kg):
    if espesor <= 0 or preu_kg <= 0:
        st.error("Espesor i preu han de ser positius")
        return
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    data = date.today().strftime("%Y-%m-%d")
    try:
        cursor.execute("""INSERT INTO Xapes (CodiMaterial, CodiQualitat, CodiAcabat, Espesor, PreuKg, Data)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                            (codi_material, codi_qualitat, codi_acabat, espesor, preu_kg, data)
                        )
        conexio.commit()
        codi_xapa = cursor.lastrowid
        cursor.execute("""INSERT INTO RegistresPreus (CodiXapa, CodiProveidor, Data, PreuKg)
                            VALUES (?, ?, ?, ?)""",
                           (codi_xapa, codi_proveidor, data, preu_kg)
                       )
        st.success("Xapa afegida correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error("La xapa ja existeix a la base de dades")

    conexio.close()

def modificar_xapa(DB_FILE, codi_xapa, codi_proveidor, nou_preu_kg):
    if nou_preu_kg <= 0:
        st.error("Preu per Kg ha de ser positiu")
        return
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    nova_data = date.today().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Xapes SET PreuKg = ?, Data = ? WHERE CodiXapa = ?",
                       (nou_preu_kg, nova_data, codi_xapa))
    cursor.execute("""INSERT INTO RegistresPreus (CodiXapa, CodiProveidor, Data, PreuKg)
                            VALUES (?, ?, ?, ?)""",
                           (codi_xapa, codi_proveidor, nova_data, nou_preu_kg)
                   )
    conexio.commit()
    st.success("El preu de la xapa ha estat actualitzat correctament")
    time.sleep(2)
    st.rerun()
    conexio.close()

# ---- FLUX PRINCIPAL DEL PROGRAMA ----

def main():

    DB_FILE = "./dat/stock_xapa.db"

#---- INTERFÍCIE STREAMLIT ----
# ---- BARRA LATERAL ----
    
    opcions_menu = ["Afegir", "Modificar"]

    with st.sidebar:
        st.header("Menú principal")
        opcio = st.selectbox("Selecciona una opció",
                             opcions_menu,
                             index = None,
                             placeholder = "Selecciona una opció...")

    # ---- PANTALLES MENÚ ----

    if opcio == "Afegir":
        pantalla_afegir_xapa(DB_FILE, opcio)
    elif opcio == "Modificar":
        pantalla_modificar_xapa(DB_FILE, opcio)
    else:
        st.title("Manteniment de les xapes")
        st.space("medium")
        st.write("""En aquest apartat pots seleccionar a la barra lateral una de les opcions.
                    \n - Afegir una nova xapa
                    \n - Modificar el preu d'una xapa creada""") 
    

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()
