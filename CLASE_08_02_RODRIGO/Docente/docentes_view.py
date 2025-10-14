# docentes_view.py
import flet as ft
from conexion import ConexionDB

class DocentesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        # 🔹 Título principal
        self.titulo = ft.Text("👨‍🏫 Gestión de Docentes", size=22, weight="bold")

        # 🔹 Tabla para mostrar los docentes
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Persona ID")),
                ft.DataColumn(ft.Text("Código Docente")),
                ft.DataColumn(ft.Text("Activo")),
                ft.DataColumn(ft.Text("Especialidad ID")),
            ],
            rows=[]
        )

        # 🔹 Botones de acción
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_docentes())

        # 🔹 Estructura de la vista
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # Cargar los datos iniciales
        self.cargar_docentes()

    # 🔹 Método para cargar docentes desde la base de datos
    def cargar_docentes(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                # Consulta directa a la tabla docentes
                cursor.execute("""
                    SELECT docente_id, persona_id, codigo_docente, activo, especialidad_id
                    FROM docentes
                """)
                resultados = cursor.fetchall()

                # Limpiamos las filas anteriores
                self.tabla.rows.clear()

                # Agregamos nuevas filas
                for fila in resultados:
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(str(fila[1]))),
                                ft.DataCell(ft.Text(fila[2])),
                                ft.DataCell(ft.Text(str(fila[3]))),
                                ft.DataCell(ft.Text(str(fila[4]))),
                            ]
                        )
                    )
                self.page.update()
                print("✅ Datos de docentes cargados correctamente")

            except Exception as e:
                print(f"❌ Error al cargar docentes: {e}")
            finally:
                self.conexion.cerrar(conexion)
