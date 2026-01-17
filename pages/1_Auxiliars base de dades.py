import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="Auxiliars")
st.sidebar.title("Auxiliars")

def crear_taules(DB_FILE):

    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()

    sql_txt = """
    CREATE TABLE IF NOT EXISTS Stock (
        CodiStock INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiXapa INTEGER,
        Longitud INTEGER NOT NULL,
        Amplada INTEGER NOT NULL,
        Quantitat INTEGER NOT NULL,
        Estat TEXT,
        Anotacio TEXT,
        Data DATE,
        FOREIGN KEY (CodiXapa) REFERENCES Xapes(CodiXapa)
        
    );
    
    CREATE TABLE IF NOT EXISTS Xapes (
        CodiXapa INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiMaterial INTEGER,
        CodiQualitat INTEGER,
        CodiAcabat INTEGER NULL,
        Espesor REAL NOT NULL,
        PreuKg REAL NOT NULL,
        Data DATE,
        FOREIGN KEY (CodiMaterial) REFERENCES Materials(CodiMaterial),
        FOREIGN KEY (CodiQualitat) REFERENCES Qualitats(CodiQualitat),
        FOREIGN KEY (CodiAcabat) REFERENCES Acabats(CodiAcabat),
        UNIQUE (CodiMaterial, CodiQualitat, CodiAcabat, Espesor)
    );

    CREATE TABLE IF NOT EXISTS Materials (
        CodiMaterial INTEGER PRIMARY KEY AUTOINCREMENT,
        Material TEXT UNIQUE NOT NULL,
        Densitat REAL NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS Qualitats (
        CodiQualitat INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiMaterial INTEGER,
        Qualitat TEXT NOT NULL,
        FOREIGN KEY (CodiMaterial) REFERENCES Materials(CodiMaterial),
        UNIQUE (CodiMaterial, Qualitat)
    );

    CREATE TABLE IF NOT EXISTS Acabats (
        CodiAcabat INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiMaterial INTEGER,
        Acabat TEXT NOT NULL,
        FOREIGN KEY (CodiMaterial) REFERENCES Materials(CodiMaterial),
        UNIQUE (CodiMaterial, Acabat)
    );
    
    CREATE TABLE IF NOT EXISTS Proveidors (
        CodiProveidor INTEGER PRIMARY KEY AUTOINCREMENT,
        Proveidor TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS RegistresPreus (
        CodiPreu INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiXapa INTEGER,
        CodiProveidor INTEGER,
        Data DATE,
        PreuKg REAL NOT NULL,
        FOREIGN KEY (CodiXapa) REFERENCES Xapes(CodiXapa),
        FOREIGN KEY (CodiProveidor) REFERENCES Proveidors(CodiProveidor)
    );
    
    CREATE TABLE IF NOT EXISTS RegistresStock (
        CodiRegistre INTEGER PRIMARY KEY AUTOINCREMENT,
        CodiXapa INTEGER,
        Longitud INTEGER NOT NULL,
        Amplada INTEGER NOT NULL,
        Quantitat INTEGER NOT NULL,
        Estat TEXT,
        Anotacio TEXT,
        Data DATETIME,
        FOREIGN KEY (CodiXapa) REFERENCES Xapes(CodiXapa)
    );
    """
    cursor.executescript(sql_txt)
    conexio.commit()
    conexio.close()



# ---- PANTALLES OPCIONS ----

def pantalla_iniciar_valors(DB_FILE, opcio):
    st.title(f"{opcio}")
    col1, col2, col3 = st.columns(3)
    with col1:    
        if st.button("Iniciar Materials"):
            iniciar_materials(DB_FILE)

    with col2:
        if st.button("Iniciar Qualitats"):
            iniciar_qualitats(DB_FILE)

    with col3:
        if st.button("Iniciar Acabats"):
            iniciar_acabats(DB_FILE)

def pantalla_auxiliars_materials (DB_FILE, opcio):
    st.title(f"Introduir {opcio}")
    st.info("En aquesta pàgina pots introduir materials a la base de dades amb les seves densitats")
    col1, col2 = st.columns(2)
    with col1:
        with st.form(f"Auxiliar {opcio}", clear_on_submit=False, enter_to_submit=False):
            material = st.text_input("Introdueix el material")
            densitat = st.number_input("Introdueix la densitat (g/cm^3)",
                                           value=None,
                                           format = "%0.1f",
                                           placeholder = "Densitat...")
            submitted = st.form_submit_button(f"Introduir {opcio}")
        
        if submitted:
            auxiliar_material(DB_FILE, material, densitat)
    with col2:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        cursor.execute("SELECT * FROM Materials")
        materials = cursor.fetchall()
        df = pd.DataFrame(materials)
        if not df.empty:
            df.columns = ["Codi", "Material", "Densitat (g/cm^3)"]
        else:
            st.error("No s'ha trobat cap material a la base de dades")
            return
        col1, col2, col3 = st.columns([1,8,1]) # Proporcions de les columnes
        with col2:
            st.write("Materials introduïts a la base de dades")
        st.dataframe(df, hide_index=True)

def pantalla_auxiliars_qualitats (DB_FILE, opcio):
    st.title(f"Introduir {opcio}")
    st.info("En aquesta pàgina pots introduir qualitats de cada material introduït a la base de dades")
    col1, col2 = st.columns(2)
    with col1:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        materials = {fila[0]:fila[1] for fila in cursor.execute("SELECT Material, CodiMaterial FROM Materials").fetchall()}
        material = st.selectbox("Selecciona el material",
                                list(materials.keys()),
                                index=None,
                                placeholder="Material...")
        conexio.close()
        if material:
            codi_material = materials[material]
        else:
            codi_material = None
        
        with st.form(f"Auxiliar {opcio}", clear_on_submit=False, enter_to_submit=False):
            qualitat = st.text_input(f"Introdueix la qualitat del {material}")
            submitted = st.form_submit_button(f"Introduir {opcio}")
        
        if submitted:
            auxiliar_qualitat(DB_FILE, material, codi_material, qualitat)
    with col2:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        cursor.execute("SELECT * FROM Qualitats as q JOIN Materials as m ON q.CodiMaterial = m.CodiMaterial")
        qualitats = cursor.fetchall()
        df = pd.DataFrame(qualitats)
        if not df.empty:
            df.columns = ["Codi", "Codi mat1", "Qualitat", "Codi Mat2", "Material", "Densitat"]
            columnes_visibles = ["Codi", "Qualitat", "Material"]
            df_filtrat = df[columnes_visibles]
        else:
            st.error("No s'ha trobat cap qualitat a la base de dades")
            return
        col1, col2, col3 = st.columns([1,9,1])
        with col2:
            st.write("Qualitats introduides a la base de dades")
        st.dataframe(df_filtrat, hide_index=True)


def pantalla_auxiliars_acabats(DB_FILE, opcio):
    st.title(f"Introduir {opcio}")
    st.info("En aquesta pàgina pots introduir acabats de cada material introduït a la base de dades")
    col1, col2 = st.columns(2)
    with col1:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        materials = {fila[0]:fila[1] for fila in cursor.execute("SELECT Material, CodiMaterial FROM Materials").fetchall()}
        material = st.selectbox("Selecciona el material",
                                list(materials.keys()),
                                index=None,
                                placeholder="Material...")
        conexio.close()
        if material:
            codi_material = materials[material]
        else:
            codi_material = None
        with st.form(f"Auxiliar {opcio}", clear_on_submit=False, enter_to_submit=False):
            acabat = st.text_input(f"Introdueix l'acabat del {material}")
            submitted = st.form_submit_button(f"Inicialitzar {opcio}")
        
        if submitted:
            auxiliar_acabats(DB_FILE, material, codi_material, acabat)
    with col2:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        cursor.execute("SELECT * FROM Acabats as a JOIN Materials as m ON a.CodiMaterial = m.CodiMaterial")
        qualitats = cursor.fetchall()
        df = pd.DataFrame(qualitats)
        if not df.empty:
            df.columns = ["Codi", "Codi mat1", "Acabat", "Codi Mat2", "Material", "Densitat"]
            columnes_visibles = ["Codi", "Acabat", "Material"]
            df_filtrat = df[columnes_visibles]
        else:
            st.error("No s'ha trobat cap acabat a la base de dades")
            return
        col1, col2, col3 = st.columns([1,8,1])
        with col2:
            st.write("Acabats introduïts a la base de dades")
        st.dataframe(df_filtrat, hide_index=True)

def pantalla_auxiliars_proveidors (DB_FILE, opcio):
    st.title(f"Introduir {opcio}")
    st.info("En aquesta pàgina pots introduir proveïdors de xapa a la base de dades")
    col1, col2 = st.columns(2)
    with col1:
        with st.form(f"Auxiliar {opcio}", clear_on_submit=False, enter_to_submit=False):
            proveidor = st.text_input("Introdueix el proveidor")
            submitted = st.form_submit_button(f"Introduir {opcio}")
        
        if submitted:
            auxiliar_proveidor(DB_FILE, proveidor)
    with col2:
        conexio = sqlite3.connect(DB_FILE)
        cursor = conexio.cursor()
        cursor.execute("SELECT * FROM Proveidors")
        proveidors = cursor.fetchall()
        df = pd.DataFrame(proveidors)
        if not df.empty:
            df.columns = ["Codi", "Proveïdor"]
        else:
            st.error("No s'ha trobat cap proveïdor a la base de dades")
            return
        col1, col2, col3 = st.columns([1,8,1]) # Proporcions de les columnes
        with col2:
            st.write("Proveïdors introduïts a la base de dades")
        st.dataframe(df, hide_index=True)
    
#----- FUNCIONS DEL PROGRAMA-----

def iniciar_materials(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    sql_txt = """INSERT INTO Materials (Material, Densitat)
                VALUES
                ("Acer", 8),
                ("Inoxidable", 8),
                ("Alumini", 2.7);
                """
    try:
        cursor.execute(sql_txt)
        st.success("El material s'ha inicialitzat correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error("El material ja està inicialitzat")
        time.sleep(5)
        st.rerun()
        return
    finally:
        conexio.close()

def iniciar_qualitats(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    sql_txt = """INSERT INTO Qualitats (CodiMaterial, Qualitat)
                VALUES
                (1, "S235"),
                (1, "S355"),
                (2, "AISI 304"),
                (2, "AISI 316"),
                (2, "AISI 430"),
                (3, "5754"),
                (3, "5083"),
                (3, "6082");
                """
    try:
        cursor.execute(sql_txt)
        st.success("La qualitat s'ha inicialitzat correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error("La qualitat ja està inicialitzada")
        time.sleep(5)
        st.rerun()
        return
    finally:
        conexio.close()

def iniciar_acabats (DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    sql_txt = """INSERT INTO Acabats (CodiMaterial, Acabat)
                VALUES
                (1, "Pulida"),
                (1, "Decapada"),
                (1, "Negra"),
                (2, "2B"),
                (2, "Satinada"),
                (2, "BA"),
                (2, "LC"),
                (3, "Brut"),
                (3, "Damero");
                """
    try:
        cursor.execute(sql_txt)
        st.success("L'acabat s'ha inicialitzat correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error("L'acabat ja està inicialitzat")
        time.sleep(5)
        st.rerun()
        return
    finally:
        conexio.close()

def auxiliar_material(DB_FILE, material, densitat):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    
    if not material:
        st.error("Has d'introduir un material")
        return
    if densitat is None or densitat <= 0:
        st.error("Has d'introduir una densitat positiva")
        return
    try:
        cursor.execute("""INSERT INTO Materials (Material, Densitat)
                       VALUES (?, ?)""", (material, densitat)
                       )
        st.success(f"El material {material} s'ha afegit correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error(f"El material {material} ja està creat")
        return
    finally:
        conexio.close()
        
def auxiliar_qualitat(DB_FILE, material, codi_material, qualitat):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    
    if not material or not qualitat:
        st.error("Has d'introduir un material i la seva qualitat")
        return

    try:
        cursor.execute("""INSERT INTO Qualitats (CodiMaterial, Qualitat)
                       VALUES (?, ?)""", (codi_material, qualitat)
                       )
        st.success(f"La qualitat {qualitat} del material {material} s'ha afegit correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error(f"La qualitat {qualitat} del material {material} ja està creada")
        return
    finally:
        conexio.close()

def auxiliar_acabats(DB_FILE, material, codi_material, acabat):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    
    if not material or not acabat:
        st.error("Has d'introduir un material i el seu acabat")
        return

    try:
        cursor.execute("""INSERT INTO Acabats (CodiMaterial, Acabat)
                       VALUES (?, ?)""", (codi_material, acabat)
                       )
        st.success(f"L'acabat {acabat} del material {material} s'ha afegit correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error(f"L'acabat {acabat} del material {material} ja està creat")
        return
    finally:
        conexio.close()

def auxiliar_proveidor(DB_FILE, proveidor):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    
    if not proveidor:
        st.error("Has d'introduir un proveïdor")
        return
    try:
        cursor.execute("""INSERT INTO Proveidors (Proveidor)
                       VALUES (?)""", (proveidor,)
                       )
        st.success(f"El proveïdor {proveidor} s'ha afegit correctament")
        conexio.commit()
        time.sleep(2)
        st.rerun()
    except sqlite3.IntegrityError:
        st.error(f"El proveïdor {proveidor} ja està creat")
        return
    finally:
        conexio.close()

# ---- FLUX PRINCIPAL DEL PROGRAMA ----

def main():

# ---- INICIALITZACIÓ TAULES BASES DE DADES ----

    DB_FILE = "./dat/stock_xapa.db"
    crear_taules(DB_FILE)

#---- INTERFÍCIE STREAMLIT ----
# ---- BARRA LATERAL ----
    
    opcions_menu = ["Iniciar valors", "Materials", "Qualitats", "Acabats", "Proveïdors"]

    with st.sidebar:
        st.header("Menú principal")
        opcio = st.selectbox("Selecciona una opció d'inicialització",
                             opcions_menu,
                             index = None,
                             placeholder = "Selecciona una opció...")

# ---- PANTALLES MENÚ ----

    pantalles = {
        "Iniciar valors": pantalla_iniciar_valors,
        "Materials": pantalla_auxiliars_materials,
        "Qualitats": pantalla_auxiliars_qualitats,
        "Acabats": pantalla_auxiliars_acabats,
        "Proveïdors": pantalla_auxiliars_proveidors
    }
    if opcio in pantalles:
        pantalles[opcio](DB_FILE, opcio)
    
    

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()
