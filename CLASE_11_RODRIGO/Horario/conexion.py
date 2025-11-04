import mysql.connector
from mysql.connector import Error


class ConexionDB:
    """
    Clase para manejar la conexión con la base de datos Horarios_Marello.
    """

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "Horarios_Marello"

    # =============================
    #   CONECTAR A LA BASE DE DATOS
    # =============================
    def conectar(self):
        """Abre una conexión a la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos Horarios_Marello")
                return conexion
        except Error as e:
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    # =============================
    #   CERRAR CONEXIÓN
    # =============================
    def cerrar(self, conexion):
        """Cierra la conexión si está abierta."""
        try:
            if conexion and conexion.is_connected():
                conexion.close()
                print("🔒 Conexión cerrada correctamente")
        except Error as e:
            print(f"⚠️ Error al cerrar la conexión: {e}")

    # =============================
    #   LOGIN DE USUARIO (OPCIONAL)
    # =============================
    def login_usuario(self, nombre_usuario, clave):
        """Valida el inicio de sesión de un usuario."""
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}

        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT * FROM usuarios 
                WHERE nombre_usuario = %s AND hashed_pass = %s
            """
            cursor.execute(query, (nombre_usuario, clave))
            usuario = cursor.fetchone()

            if usuario:
                print(f"👤 Usuario autenticado: {usuario['nombre_usuario']}")
                return {"status": True, "mensaje": "Login exitoso", "data": usuario}
            else:
                return {"status": False, "mensaje": "Usuario o contraseña incorrectos"}
        except Error as e:
            return {"status": False, "mensaje": f"Error en la consulta: {e}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    # =============================
    #   EJECUTAR CONSULTAS GENERALES
    # =============================
    def ejecutar_consulta(self, query, valores=None, fetch=False):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE o SELECT).
        Si `fetch=True`, devuelve los resultados de un SELECT.
        """
        conexion = self.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(query, valores or ())

            if fetch:
                resultados = cursor.fetchall()
                return resultados
            else:
                conexion.commit()
                print("💾 Consulta ejecutada correctamente")
                return True
        except Error as e:
            print(f"❌ Error al ejecutar consulta: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)


# --- 🔹 Prueba directa (debug manual) ---
if __name__ == "__main__":
    db = ConexionDB()
    conexion = db.conectar()
    if conexion:
        print("🎯 Base de datos lista para usarse")
        db.cerrar(conexion)
