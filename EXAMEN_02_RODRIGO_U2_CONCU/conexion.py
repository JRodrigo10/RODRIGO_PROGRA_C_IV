# conexion.py
import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "empleados_db"

    # 🔹 Conectar a la base de datos
    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            print(f"❌ Error al conectar con MySQL: {e}")
            return None

    # 🔹 Cerrar conexión
    def cerrar(self, conexion):
        if conexion and conexion.is_connected():
            conexion.close()

    # 🔹 Crear tabla empleados si no existe
    def crear_tabla_empleados(self):
        conexion = self.conectar()
        if not conexion:
            print("⚠️ No se pudo conectar para crear la tabla.")
            return
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100),
                    apellido VARCHAR(100),
                    dni VARCHAR(8),
                    fecha_nacimiento DATE,
                    cargo VARCHAR(100),
                    departamento VARCHAR(100),
                    salario DECIMAL(10,2),
                    fecha_contratacion DATE,
                    telefono VARCHAR(9)
                )
            """)
            conexion.commit()
            print("✅ Tabla 'empleados' verificada o creada correctamente.")
        except Error as e:
            print(f"❌ Error al crear tabla: {e}")
        finally:
            cursor.close()
            self.cerrar(conexion)

    # 🔹 Agregar empleado
    def agregar_empleado(self, nombre, apellido, dni, cargo, departamento, salario, telefono):
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            query = """
                INSERT INTO empleados (nombre, apellido, dni, cargo, departamento, salario, telefono)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, dni, cargo, departamento, salario, telefono))
            conexion.commit()
            print("✅ Empleado agregado correctamente")
        except Error as e:
            print(f"❌ Error al agregar empleado: {e}")
        finally:
            cursor.close()
            self.cerrar(conexion)

    # 🔹 Obtener todos los empleados
    def obtener_empleados(self):
        conexion = self.conectar()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM empleados")
            return cursor.fetchall()
        except Error as e:
            print(f"❌ Error al obtener empleados: {e}")
            return []
        finally:
            cursor.close()
            self.cerrar(conexion)

    # 🔹 Actualizar empleado
    def actualizar_empleado(self, id_empleado, nombre, apellido, dni, cargo, departamento, salario, telefono):
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            query = """
                UPDATE empleados
                SET nombre=%s, apellido=%s, dni=%s, cargo=%s, departamento=%s, salario=%s, telefono=%s
                WHERE id_empleado=%s
            """
            cursor.execute(query, (nombre, apellido, dni, cargo, departamento, salario, telefono, id_empleado))
            conexion.commit()
            print("✅ Empleado actualizado correctamente")
        except Error as e:
            print(f"❌ Error al actualizar empleado: {e}")
        finally:
            cursor.close()
            self.cerrar(conexion)

    # 🔹 Eliminar empleado
    def eliminar_empleado(self, id_empleado):
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM empleados WHERE id_empleado=%s", (id_empleado,))
            conexion.commit()
            print("✅ Empleado eliminado correctamente")
        except Error as e:
            print(f"❌ Error al eliminar empleado: {e}")
        finally:
            cursor.close()
            self.cerrar(conexion)
    
    