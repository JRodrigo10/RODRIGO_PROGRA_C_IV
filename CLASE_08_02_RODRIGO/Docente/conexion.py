import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "Horarios_Marello"

    # ──────────────────────────────
    # CONECTAR Y CERRAR BASE DE DATOS
    # ──────────────────────────────
    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos")
                return conexion
        except Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def cerrar(self, conexion):
        if conexion and conexion.is_connected():
            conexion.close()
            print("🔒 Conexión cerrada correctamente")

    # ──────────────────────────────
    # OBTENER LISTA DE DOCENTES
    # ──────────────────────────────
    def obtener_docentes(self):
        conexion = self.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
            SELECT 
                d.docente_id,
                d.persona_id,
                d.codigo_docente,
                CASE 
                    WHEN d.activo = 1 THEN 'Sí'
                    WHEN d.activo = 0 THEN 'No'
                    ELSE d.activo
                END AS activo,
                e.nombre AS especialidad
            FROM docentes d
            LEFT JOIN especialidades e ON d.especialidad_id = e.especialidad_id
            ORDER BY d.docente_id ASC
            """
            cursor.execute(query)
            docentes = cursor.fetchall()
            return docentes

        except Error as e:
            print(f"❌ Error al obtener docentes: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    # ──────────────────────────────
    # AGREGAR NUEVO DOCENTE (opcional)
    # ──────────────────────────────
    def agregar_docente(self, persona_id, codigo_docente, activo, especialidad_id):
        conexion = self.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO docentes (persona_id, codigo_docente, activo, especialidad_id, creado_en)
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query, (persona_id, codigo_docente, activo, especialidad_id))
            conexion.commit()
            print("✅ Docente agregado correctamente")
            return True
        except Error as e:
            print(f"❌ Error al agregar docente: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)
