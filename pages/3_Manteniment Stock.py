from datetime import date
import time
import streamlit as st
import sqlite3

st.set_page_config(page_title="Manteniment Stock")
st.sidebar.title("Manteniment Stock")

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


# ---- FUNCIONS PANTALLES PROGRAMA ----

def pantalla_afegir_stock(DB_FILE, opcio):
    st.title(f"{opcio} al Stock")
    materials = obtenir_materials(DB_FILE)
    material = st.selectbox("Selecciona el material",
                            list(materials.keys()),
                            index=None,
                            placeholder="Material...",
                            key=f"{opcio}_stock_material")
    if material:
        codi_material = materials[material]
    else:
        codi_material = None
    qualitats = obtenir_qualitats(DB_FILE, codi_material)
    qualitat = st.selectbox("Selecciona la qualitat",
                            list(qualitats.keys()),
                            index=None,
                            placeholder="Qualitat...",
                            key=f"{opcio}_stock_qualitat")
    if qualitat:
        codi_qualitat = qualitats[qualitat]
    else:
        codi_qualitat = None
    acabats = obtenir_acabats(DB_FILE, codi_material)
    acabat = st.selectbox("Selecciona l'acabat",
                          list(acabats.keys()),
                          index=None,
                          placeholder="Acabat...",
                          key=f"{opcio}_stock_acabat")
    if acabat:
        codi_acabat = acabats[acabat]
    else:
        codi_acabat = None
    espesors = obtenir_espesors(DB_FILE, codi_material, codi_qualitat, codi_acabat)
    espesor = st.selectbox("Selecciona l'espesor",
                           espesors,
                           index=None,
                           placeholder="Espesor...",
                           key=f"{opcio}_stock_espesor")

    with st.form(f"{opcio} Stock", clear_on_submit=False, enter_to_submit=False): 
        longitud = st.number_input("Introdueix la longitud (mm)",
                                   step=1,
                                   value=None,
                                   placeholder="Longitud...")
        amplada = st.number_input("Introdueix l'amplada (mm)",
                                   step=1,
                                   value=None,
                                   placeholder="Amplada...")
        quantitat = st.number_input("Introdueix la quantitat",
                                    step=1,
                                    value=None,
                                    placeholder="Quantitat...")
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button(f"{opcio} al Stock")
    if submitted:
        if not(codi_material and codi_qualitat and codi_acabat and espesor):
            st.error("Has de seleccionar el material, la qualitat, l'acabat i l'espesor")
        elif not(longitud and amplada and quantitat):
            st.error("Has d'introduir la longitud, l'amplada i la quantitat")
        else:
            afegir_stock(DB_FILE, codi_material, codi_qualitat, codi_acabat, espesor, longitud, amplada, quantitat)

def pantalla_modificar_stock(DB_FILE, opcio):
    st.title(f"{opcio} al Stock")
    codi_stock = st.number_input("Codi de la xapa en stock",
                                value=None,
                                step=1,
                                placeholder = "Codi de la xapa en stock...")
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute("""SELECT s.CodiStock, m.Material, q.Qualitat, a.Acabat,
                            x.Espesor, s.Longitud, s.Amplada, s.Quantitat
                    FROM Stock as s
                    JOIN Xapes as x ON x.CodiXapa = s.CodiXapa
                    JOIN Materials as m ON m.CodiMaterial = x.CodiMaterial
                    JOIN Qualitats as q ON q.CodiQualitat = x.CodiQualitat
                    JOIN Acabats as a ON a.CodiAcabat = x.CodiAcabat
                    WHERE CodiStock = ?""", (codi_stock,))
    fila_stock = obtenir_dades(cursor)
    try:
        codi_stock, material, qualitat, acabat, espesor, longitud, amplada, quantitat = fila_stock
        st.info(f"""La xapa del stock a modificar es **{material} {qualitat} {acabat} de {espesor} mm** d'espesor.
                \nLes dimensions de la xapa són **{longitud} x {amplada} mm**.\nHi ha **{quantitat} unitats**""")
    except TypeError:
        st.error("Has d'indicar un codi de stock vàlid")
        return
    except sqlite3.Error as e:
        st.error(e)
        return
    
    if quantitat > 1:
        with st.form(f"{opcio} quantitat Stock", clear_on_submit=False, enter_to_submit=False):
            quantitat_utilitzada = st.number_input("Quantitat de xapes utilitzades:",
                                                    value=None,
                                                    step=1,
                                                    placeholder = "Quantitat utilitzada...")
            col1, col2, col3 = st.columns(3)
            with col2:
                submitted = st.form_submit_button(f"{opcio} quantitat al Stock")
        if submitted:
            if not quantitat_utilitzada:
                st.error("Has d'introduir la quantitat utilitzada")
            else:
                modificar_quantitat(DB_FILE, codi_stock, quantitat, quantitat_utilitzada)
    else:
        with st.form(f"{opcio} Stock", clear_on_submit=False, enter_to_submit=False):
            nova_longitud = st.number_input("Introdueix la nova longitud",
                                      value=None,
                                      step=1,
                                      placeholder = "Nova longitud...")
            nova_amplada = st.number_input("Introdueix la nova amplada",
                                      value=None,
                                      step=1,
                                      placeholder = "Nova amplada...")
            col1, col2, col3 = st.columns(3)
            with col2:
                submitted2 = st.form_submit_button(f"{opcio} al Stock")
        
            if submitted2:
                if not (nova_longitud and nova_amplada):
                    st.error("Has d'introduir les noves longitud i amplada")
                else:
                    modificar_stock(DB_FILE, codi_stock, nova_longitud, nova_amplada)

def pantalla_eliminar_stock(DB_FILE, opcio):
    st.title(f"{opcio} del Stock")            
    
    codi_stock = st.number_input("Codi de la xapa en stock",
                                value=None,
                                step=1,
                                placeholder = "Codi de la xapa...")
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute("""SELECT s.CodiStock, m.Material, q.Qualitat, a.Acabat,
                            x.Espesor, s.Longitud, s.Amplada
                    FROM Stock as s
                    JOIN Xapes as x ON x.CodiXapa = s.CodiXapa
                    JOIN Materials as m ON m.CodiMaterial = x.CodiMaterial
                    JOIN Qualitats as q ON q.CodiQualitat = x.CodiQualitat
                    JOIN Acabats as a ON a.CodiAcabat = x.CodiAcabat
                    WHERE CodiStock = ?""", (codi_stock,))
    fila_stock = obtenir_dades(cursor)
    try:
        codi_stock, material, qualitat, acabat, espesor, longitud, amplada = fila_stock        
        st.info(f"""La xapa del stock a eliminar es **{material} {qualitat} {acabat} de {espesor}mm** d'espesor.
                \nLes dimensions de la xapa són **{longitud}x{amplada}**""")
    
    except TypeError:
        st.error("Has d'indicar un codi de stock vàlid")
    except sqlite3.Error as e:
        st.error(e)
    with st.form(f"{opcio} Stock", clear_on_submit=False, enter_to_submit=False):
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button(f"{opcio} del Stock")
    
        if submitted:
            if not codi_stock:
                st.error("Has d'introduir el codi de la xapa en stock a eliminar")
            else:
                eliminar_stock(DB_FILE, codi_stock)

# ---- FUNCIONS DEL PROGRAMA ----

def afegir_stock(DB_FILE, codi_material, codi_qualitat, codi_acabat, espesor, longitud, amplada, quantitat):
    if longitud <= 0 or amplada <= 0 or quantitat <= 0:
        st.error("Longitud, amplada i quantitat han de ser positius")
        return
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.execute("""SELECT * FROM Xapes
                    WHERE CodiMaterial = ? AND CodiQualitat = ? AND
                    CodiAcabat = ? AND Espesor = ?""",
                   (codi_material, codi_qualitat, codi_acabat, espesor)
                   )
    codi_xapa = obtenir_dada(cursor)
    if codi_xapa is None:
        return
    data = date.today().strftime("%Y-%m-%d")
    cursor.execute("""INSERT INTO Stock (CodiXapa, Longitud, Amplada, Quantitat, Estat, Data)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        (codi_xapa, longitud, amplada, quantitat, "Activa", data)
                    )
    conexio.commit()
    st.success("Xapa afegida correctament al stock")
    time.sleep(2)
    st.rerun()
    conexio.close()

def modificar_stock(DB_FILE, codi_stock, nova_longitud, nova_amplada):
    if nova_longitud <= 0 or nova_amplada <= 0:
        st.error("La longitud i l'amplada han de ser positives")
        return
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    nova_data = date.today().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Stock SET Longitud = ?, Amplada = ?, Data = ? WHERE CodiStock = ?", (nova_longitud, nova_amplada, nova_data, codi_stock))
    conexio.commit()
    st.success("Les dimensions de la xapa en stock s'han modificat correctament")
    time.sleep(2)
    st.rerun()
    conexio.close()

def modificar_quantitat(DB_FILE, codi_stock, quantitat, quantitat_utilitzada):
    if quantitat_utilitzada <= 0:
        st.error("La quantitat ha de ser positiva")
        return
    restant = quantitat - quantitat_utilitzada
    st.write(restant)
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    nova_data = date.today().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Stock SET Quantitat=?, Data = ? WHERE CodiStock = ?", (restant, nova_data, codi_stock))
    conexio.commit()
    st.success("Les dimensions de la xapa en stock s'han modificat correctament")
    time.sleep(2)
    st.rerun()
    conexio.close()

def eliminar_stock(DB_FILE, codi_stock):
    if codi_stock <= 0:
        st.error("Has d'introduir un codi de stock vàlid")
        return
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    nova_data = date.today().strftime("%Y-%m-%d")
    cursor.execute("UPDATE Stock SET Estat = ?, Data = ? WHERE CodiStock = ?", ("Inactiva", nova_data, codi_stock))
    conexio.commit()
    st.success("La xapa en stock s'ha eliminat correctament")
    time.sleep(2)
    st.rerun()
    conexio.close()

# ---- FLUX PRINCIPAL DEL PROGRAMA ----

def main():

    DB_FILE = "./dat/stock_xapa.db"

#---- INTERFÍCIE STREAMLIT ----
# ---- BARRA LATERAL ----
    
    opcions_menu = ["Afegir", "Modificar", "Eliminar"]

    with st.sidebar:
        st.header("Menú principal")
        opcio = st.selectbox("Selecciona una opció",
                             opcions_menu,
                             index = None,
                             placeholder = "Selecciona una opció...")

    # ---- PANTALLES MENÚ ----

    if opcio == "Afegir":
        pantalla_afegir_stock(DB_FILE, opcio)
    elif opcio == "Modificar":
        pantalla_modificar_stock(DB_FILE, opcio)
    elif opcio == "Eliminar":
        pantalla_eliminar_stock(DB_FILE, opcio)
    

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()
