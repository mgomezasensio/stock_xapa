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
                        (2,3,4,1.5,2.80,'2024-01-01'),
                        (1, 1, 2, 0.8, 1.10, '2024-01-01'),
                        (1, 2, 1, 3.0, 1.55, '2024-01-01'),
                        (2, 3, 4, 2.0, 2.95, '2024-01-01'),
                        (1, 1, 3, 1.2, 1.25, '2024-01-01'),
                        (1, 2, 2, 2.5, 1.48, '2024-01-01'),
                        (2, 4, 5, 1.0, 3.10, '2024-01-01'),
                        (2, 4, 6, 1.5, 3.45, '2024-01-01'),
                        (3, 6, 8, 2.0, 2.40, '2024-01-01'),
                        (3, 7, 9, 3.0, 2.85, '2024-01-01');

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
                        (3,1,'2024-03-30',2.99),
                        (1,1,'2024-04-05',1.34),
                        (1,3,'2024-04-10',1.36),
                        (1,5,'2024-04-15',1.38),
                        (1,7,'2024-04-20',1.40),
                        (2,2,'2024-04-04',1.58),
                        (2,4,'2024-04-12',1.60),
                        (2,6,'2024-04-18',1.63),
                        (2,8,'2024-04-25',1.65),
                        (3,5,'2024-04-03',2.95),
                        (3,7,'2024-04-11',2.98),
                        (3,9,'2024-04-19',3.02),
                        (3,1,'2024-04-28',3.05),
                        (4,1,'2024-01-10',1.08),
                        (4,3,'2024-02-10',1.12),
                        (4,5,'2024-03-10',1.15),
                        (5,2,'2024-01-12',1.60),
                        (5,4,'2024-02-12',1.63),
                        (5,6,'2024-03-12',1.67),
                        (6,7,'2024-01-15',2.85),
                        (6,8,'2024-02-15',2.90),
                        (6,9,'2024-03-15',2.95),
                        (7,1,'2024-01-10',1.22),
                        (7,3,'2024-02-10',1.24),
                        (7,5,'2024-03-10',1.27),
                        (8,2,'2024-01-12',1.50),
                        (8,4,'2024-02-12',1.53),
                        (8,6,'2024-03-12',1.56),
                        (9,5,'2024-01-15',3.05),
                        (9,7,'2024-02-15',3.12),
                        (9,1,'2024-03-15',3.18),
                        (10,4,'2024-01-18',3.42),
                        (10,6,'2024-02-18',3.48),
                        (10,8,'2024-03-18',3.55),
                        (11,9,'2024-01-20',2.38),
                        (11,3,'2024-02-20',2.42),
                        (11,1,'2024-03-20',2.45),
                        (12,2,'2024-01-22',2.82),
                        (12,4,'2024-02-22',2.87),
                        (12,7,'2024-03-22',2.92),
                        (1,1,'2024-04-05',1.34),
                        (1,3,'2024-05-05',1.36),
                        (1,5,'2024-06-05',1.38),
                        (2,2,'2024-04-08',1.58),
                        (2,4,'2024-05-08',1.61),
                        (2,6,'2024-06-08',1.64),
                        (3,5,'2024-04-10',2.96),
                        (3,7,'2024-05-10',2.99),
                        (3,9,'2024-06-10',3.03),
                        (4,1,'2024-04-12',1.17),
                        (4,3,'2024-05-12',1.19),
                        (4,5,'2024-06-12',1.22),
                        (5,2,'2024-04-14',1.62),
                        (5,4,'2024-05-14',1.65),
                        (5,6,'2024-06-14',1.68),
                        (6,7,'2024-04-16',2.97),
                        (6,8,'2024-05-16',3.00),
                        (6,9,'2024-06-16',3.04),
                        (7,1,'2024-04-10',1.29),
                        (7,3,'2024-05-10',1.31),
                        (7,5,'2024-06-10',1.34),
                        (8,2,'2024-04-12',1.58),
                        (8,4,'2024-05-12',1.61),
                        (8,6,'2024-06-12',1.64),
                        (9,5,'2024-04-15',3.20),
                        (9,7,'2024-05-15',3.25),
                        (9,1,'2024-06-15',3.30),
                        (10,4,'2024-04-18',3.58),
                        (10,6,'2024-05-18',3.63),
                        (10,8,'2024-06-18',3.68),
                        (11,9,'2024-04-20',2.48),
                        (11,3,'2024-05-20',2.52),
                        (11,1,'2024-06-20',2.55),
                        (12,2,'2024-04-22',2.95),
                        (12,4,'2024-05-22',3.00),
                        (12,7,'2024-06-22',3.05);
                        
                INSERT INTO Stock (CodiXapa, Longitud, Amplada, Quantitat, Anotacio, Estat, Data) VALUES
                        (1,2000,1000,5,'Test','Activa','2024-03-01 10:00:00'),
                        (2,3000,1500,1,'Test','Activa','2024-03-01 11:00:00'),
                        (3,2500,1250,4,'Test','Activa','2024-03-01 12:00:00'),
                        (1,2500,1250,7,'Reposició','Activa','2024-04-01 09:00:00'),
                        (2,2000,1000,4,'Entrada','Activa','2024-04-01 10:00:00'),
                        (3,3000,1500,6,'Entrada','Activa','2024-04-01 11:00:00'),
                        (4,2000,1000,10,'Nova xapa','Activa','2024-04-02 08:30:00'),
                        (5,2500,1250,8,'Nova xapa','Activa','2024-04-02 09:15:00'),
                        (6,3000,1500,5,'Nova xapa','Activa','2024-04-02 10:00:00'),
                        (7,2000,1000,1,'Nova entrada','Activa','2024-04-04 08:30:00'),
                        (8,2500,1250,9,'Nova entrada','Activa','2024-04-04 09:00:00'),
                        (9,3000,1500,6,'Nova entrada','Activa','2024-04-04 09:30:00'),
                        (10,2000,1000,1,'Nova entrada','Activa','2024-04-05 08:45:00'),
                        (11,2500,1250,10,'Nova entrada','Activa','2024-04-05 09:15:00'),
                        (12,3000,1500,7,'Nova entrada','Activa','2024-04-05 10:00:00');
    """
    cursor.executescript(sql_txt)
    conexio.commit()
    st.success("El joc de dades s'ha creat correctament")
    time.sleep(2)
    st.rerun()
    conexio.close()

def eliminar_dades (DB_FILE):
    sql_txt = """DELETE FROM Proveidors;
                DELETE FROM sqlite_sequence WHERE name='Proveidors';
                DELETE FROM Xapes;
                DELETE FROM sqlite_sequence WHERE name='Xapes';
                DELETE FROM RegistresPreus;
                DELETE FROM sqlite_sequence WHERE name='RegistresPreus';
                DELETE FROM Stock;
                DELETE FROM sqlite_sequence WHERE name='Stock';
                DELETE FROM RegistresStock;
                DELETE FROM sqlite_sequence WHERE name='RegistresStock';
                """
    conexio = sqlite3.connect(DB_FILE)
    cursor = conexio.cursor()
    cursor.executescript(sql_txt)
    conexio.commit()
    conexio.close()


# ---- PANTALLES OPCIONS ----

def pantalla_iniciar_valors(DB_FILE, opcio):
    st.title(f"{opcio}")
    with st.container():
        st.write('Crea els materials inicials')
        if st.button("Iniciar Materials"):
            iniciar_materials(DB_FILE)
            
        st.space(size="small")
        
        st.write('Crea les qualitats inicials dels materials')
        if st.button("Iniciar Qualitats"):
            iniciar_qualitats(DB_FILE)
        
        st.space(size="small")
        
        st.write('Crea els acabats inicials dels materials')
        if st.button("Iniciar Acabats"):
            iniciar_acabats(DB_FILE)
    st.space(size="large")
    with st.expander('Proves'):
        col1, col2 = st.columns(2)
        with col1:
            st.write('Crea un joc de dades generat amb IA')
            if st.button("Iniciar joc de dades"):
                try:
                    crear_joc_dades(DB_FILE)
                except sqlite3.IntegrityError:
                    st.error("El joc de dades ja està creat")
                    time.sleep(3)
                    st.rerun()
        with col2:
            st.write('Elimina les dades de la base de dades')
            if "confirmar_eliminar" not in st.session_state:
                st.session_state.confirmar_eliminar = False
            if st.button("Eliminar dades"):
                st.session_state.confirmar_eliminar = True
            
            if st.session_state.confirmar_eliminar:
                st.warning("Vols eliminar totes les dades?")
                if st.button('Acceptar'):
                    eliminar_dades(DB_FILE)
                    st.success("Les dades s'han eliminat correctament de la base de dades")
                    time.sleep(2)
                    st.session_state.confirmar_eliminar = False
                    st.rerun()
                if st.button('Cancelar'):
                    st.session_state.confirmar_eliminar = False
                    st.rerun()

def pantalla_auxiliars_materials (DB_FILE, opcio):
    st.title(f"Introduir {opcio}")
    with st.popover("Explicació"):
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
    with st.popover("Explicació"):
        st.info("En aquesta pàgina pots introduir les qualitats de cada material introduït a la base de dades")
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
    with st.popover("Explicació"):
        st.info("En aquesta pàgina pots introduir els acabats de cada material introduït a la base de dades")
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
    with st.popover("Explicació"):
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
    else:
        st.title("Funcions auxiliars del programa")
        st.space("medium")
        st.write("""En aquest apartat pot seleccionar les diferents opcions a la barra lateral.
                    \n - Iniciar valors
                    \n - Afegir materials
                    \n - Afegir qualitats als material
                    \n - Afegir acabats als materials
                    \n - Afegir proveïdors de xapa""")
    

# ---- INICIALITZACIÓ PROGRAMA ----

if __name__ == "__main__":
    main()
