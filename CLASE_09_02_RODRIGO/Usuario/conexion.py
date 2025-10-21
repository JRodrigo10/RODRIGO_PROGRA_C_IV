import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "Horarios_Marello"

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

    # 🔹 NUEVO: Obtener lista de usuarios
    def obtener_usuarios(self):
        conexion = self.conectar()
        if not conexion:
            print("⚠️ No se pudo conectar a la base de datos.")
            return []

        try:
            cursor = conexion.cursor()
            query = """
                SELECT 
                    usuario_id,
                    persona_id,
                    nombre_usuario,
                    email,
                    rol,
                    activo
                FROM usuarios
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            print(f"✅ Usuarios obtenidos: {len(resultados)} registros.")
            return resultados

        except Error as e:
            print(f"❌ Error al obtener usuarios: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)
