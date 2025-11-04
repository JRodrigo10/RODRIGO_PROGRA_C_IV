import flet as ft
from conexion import ConexionDB

class UsuariosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        # Título principal
        self.titulo = ft.Text("👤 Gestión de Usuarios", size=22, weight="bold")

        # Tabla de datos
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Persona ID")),
                ft.DataColumn(ft.Text("Nombre de Usuario")),
                ft.DataColumn(ft.Text("Correo Electrónico")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Activo")),
            ],
            rows=[]
        )

        # Botones de acción
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_usuarios())

        # Estructura de la vista
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50),
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # Cargar datos al iniciar
        self.cargar_usuarios()

    # ──────────────────────────────────────────────
    # FUNCIÓN PARA CARGAR LOS USUARIOS
    # ──────────────────────────────────────────────
    def cargar_usuarios(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("""
                    SELECT usuario_id, persona_id, nombre_usuario, email, rol, activo 
                    FROM usuarios
                """)
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    usuario_id, persona_id, nombre_usuario, email, rol, activo = fila
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(usuario_id))),
                                ft.DataCell(ft.Text(str(persona_id))),
                                ft.DataCell(ft.Text(nombre_usuario)),
                                ft.DataCell(ft.Text(email)),
                                ft.DataCell(ft.Text(str(rol))),
                                ft.DataCell(ft.Text("Sí" if activo == 1 else "No")),
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar usuarios: {e}")
            finally:
                cursor.close()
                self.conexion.cerrar(conexion)
