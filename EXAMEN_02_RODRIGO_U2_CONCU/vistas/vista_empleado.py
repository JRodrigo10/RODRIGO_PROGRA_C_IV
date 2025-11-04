import flet as ft
from conexion import ConexionDB
from vistas.agregar_empleado import AgregarEmpleadoView


class VistaEmpleado(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.db = ConexionDB()

        # 🔹 Encabezado
        titulo = ft.Text("👨‍💼 Gestión de Empleados (MySQL)", size=22, weight=ft.FontWeight.BOLD)
        boton_volver = ft.ElevatedButton("⬅ Volver al Dashboard", on_click=lambda e: self.volver())
        boton_agregar = ft.ElevatedButton("➕ Agregar Empleado", on_click=lambda e: self.abrir_formulario())

        # 🔹 Tabla
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # Cargar datos iniciales
        self.cargar_datos()

        # Layout
        self.content = ft.Column(
            [
                titulo,
                ft.Row([boton_agregar, boton_volver], alignment="start"),
                ft.Divider(),
                self.tabla
            ],
            scroll="auto"
        )

    # 🔹 Cargar datos de empleados desde MySQL
    def cargar_datos(self):
        empleados = self.db.obtener_empleados()
        self.tabla.rows.clear()

        for emp in empleados:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(emp["id_empleado"]))),
                        ft.DataCell(ft.Text(emp["nombre"])),
                        ft.DataCell(ft.Text(emp["apellido"])),
                        ft.DataCell(ft.Text(emp["dni"])),
                        ft.DataCell(ft.Text(emp["telefono"])),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,  # ✅ usar ft.Icons, no ft.icons
                                        icon_color="blue",
                                        tooltip="Editar empleado",
                                        on_click=lambda e, emp=emp: self.editar_empleado(emp),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color="red",
                                        tooltip="Eliminar empleado",
                                        on_click=lambda e, emp=emp: self.eliminar_empleado(emp["id_empleado"]),
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
        self.update()

    # 🔹 Abrir formulario para agregar empleado
    def abrir_formulario(self):
        self.cambiar_vista(AgregarEmpleadoView(self.page, self.cambiar_vista))

    # 🔹 Editar empleado (abre vista de agregar con datos cargados)
    def editar_empleado(self, empleado):
        self.cambiar_vista(AgregarEmpleadoView(self.page, self.cambiar_vista, empleado=empleado))

    # 🔹 Eliminar empleado
    def eliminar_empleado(self, id_empleado):
        try:
            self.db.eliminar_empleado(id_empleado)
            self.mostrar_alerta("🗑 Empleado eliminado correctamente")
            self.cargar_datos()
        except Exception as e:
            self.mostrar_alerta(f"⚠ Error al eliminar: {e}")

    # 🔹 Mostrar mensaje tipo SnackBar
    def mostrar_alerta(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    # 🔹 Volver al Dashboard
    def volver(self):
        from dashboard_view import DashboardView
        self.cambiar_vista(DashboardView(self.page, self.cambiar_vista))
