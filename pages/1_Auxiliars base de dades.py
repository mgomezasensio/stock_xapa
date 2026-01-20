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

def crear_joc_dades(DB_FILE):
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    sql_txt = """INSERT INTO Proveidors (Proveidor) VALUES
                        ('Ferros Brugués'),
                        ('Ferrovallès'),
                        ('Ferros Puig'),
                        ('Gutmetal'),
                        ('Inoxcenter'),
                        ('Hastinik'),
                        ('Inoxidables Lapuente'),
                        ('Montal'),
                        ('Alu-stock');
                INSERT INTO Xapes (CodiMaterial, CodiQualitat, CodiAcabat, Espesor, PreuKg, Data) VALUES
                        (1,1,1,1.0,1.20,'2024-01-01'),
                        (1,2,2,2.0,1.40,'2024-01-01'),
                        (2,3,4,1.5,2.80,'2024-01-01');

                INSERT INTO RegistresPreus (CodiXapa, CodiProveidor, Data, PreuKg) VALUES
                        (1,1,'2024-01-05',1.18),
                        (1,1,'2024-01-12',1.20),
                        (1,1,'2024-01-20',1.22),
                        (1,1,'2024-02-01',1.25),
                        (1,1,'2024-02-10',1.27),

                        (1,3,'2024-01-08',1.19),
                        (1,3,'2024-01-18',1.21),
                        (1,3,'2024-01-28',1.23),
                        (1,3,'2024-02-05',1.26),
                        (1,3,'2024-02-15',1.28),

                        (1,5,'2024-02-20',1.30),
                        (1,7,'2024-02-25',1.32),

                        (2,2,'2024-01-06',1.38),
                        (2,2,'2024-01-14',1.40),
                        (2,2,'2024-01-22',1.42),
                        (2,2,'2024-02-02',1.45),
                        (2,2,'2024-02-12',1.48),

                        (2,4,'2024-01-10',1.39),
                        (2,4,'2024-01-19',1.41),
                        (2,4,'2024-01-30',1.44),
                        (2,4,'2024-02-08',1.47),
                        (2,4,'2024-02-18',1.50),

                        (2,6,'2024-02-22',1.52),
                        (2,8,'2024-02-28',1.55),

                        (3,5,'2024-01-07',2.75),
                        (3,5,'2024-01-15',2.78),
                        (3,5,'2024-01-25',2.80),
                        (3,5,'2024-02-03',2.82),
                        (3,5,'2024-02-14',2.85),

                        (3,7,'2024-01-09',2.76),
                        (3,7,'2024-01-18',2.79),
                        (3,7,'2024-01-29',2.81),
                        (3,7,'2024-02-06',2.84),
                        (3,7,'2024-02-16',2.87),

                        (3,9,'2024-02-22',2.90),
                        (3,1,'2024-02-28',2.92),
                        
                        (1,1,'2024-03-01',1.29),
                        (1,1,'2024-03-10',1.31),
                        (1,1,'2024-03-20',1.33),

                        (1,3,'2024-03-03',1.30),
                        (1,3,'2024-03-12',1.32),
                        (1,3,'2024-03-22',1.34),

                        (1,5,'2024-03-15',1.35),
                        (1,7,'2024-03-25',1.37),

                        (2,2,'2024-03-02',1.50),
                        (2,2,'2024-03-11',1.53),
                        (2,2,'2024-03-21',1.56),

                        (2,4,'2024-03-05',1.49),
                        (2,4,'2024-03-14',1.52),
                        (2,4,'2024-03-24',1.55),

                        (2,6,'2024-03-18',1.58),
                        (2,8,'2024-03-28',1.60),

                        (3,5,'2024-03-04',2.88),
                        (3,5,'2024-03-13',2.90),
                        (3,5,'2024-03-23',2.93),

                        (3,7,'2024-03-06',2.89),
                        (3,7,'2024-03-16',2.92),
                        (3,7,'2024-03-26',2.95),

                        (3,9,'2024-03-20',2.97),
                        (3,1,'2024-03-30',2.99);

                        
                INSERT INTO Stock (CodiXapa, Longitud, Amplada, Quantitat, Anotacio, Estat, Data) VALUES
                        (1,2000,1000,5,'Test','Activa','2024-03-01 10:00:00'),
                        (2,3000,1500,3,'Test','Activa','2024-03-01 11:00:00'),
                        (3,2500,1250,4,'Test','Activa','2024-03-01 12:00:00');
    """
    cursor.executescript(sql_txt)
    conexio.commit()
    st.success("El joc de dades s'ha creat correctament")
    time.sleep(2)
    st.rerun()
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
    if st.button("Iniciar joc de dades"):
        crear_joc_dades(DB_FILE)

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
