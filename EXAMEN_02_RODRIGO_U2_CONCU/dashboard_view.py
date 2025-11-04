
import flet as ft
from conexion import ConexionDB
from vistas.vista_empleado import VistaEmpleado  # Nuestra vista de empleados

class DashboardView(ft.Container):
    def __init__(self, page, cambiar_vista):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista

        self.db = ConexionDB()
        # Aquí podrías crear la tabla empleados si no existe
        # self.db.crear_tabla_empleados()  # Opcional si quieres asegurarte que exista

        titulo = ft.Text(
            "📊 Panel Principal – Sistema de Empleados (MySQL)",
            size=24,
            weight=ft.FontWeight.BOLD
        )

        # Card única para Empleados
        card_empleados = self.crear_card(
            "👨‍💼 Empleados",
            "Gestionar registros de empleados (CRUD conectado a MySQL)",
            lambda e: self.abrir_empleados()
        )

        grid = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=card_empleados,
                    col={"xs": 12, "sm": 6, "md": 3},
                    padding=10
                )
            ]
        )

        self.content = ft.Column(
            [
                titulo,
                ft.Divider(),
                grid
            ],
            expand=True,
            scroll="auto"
        )

    def crear_card(self, titulo, descripcion, evento):
        return ft.Card(
            content=ft.Container(
                bgcolor=ft.Colors.BLUE_100,
                border_radius=15,
                padding=15,
                content=ft.Column(
                    [
                        ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(descripcion, size=13, color=ft.Colors.GREY_700)
                    ]
                ),
                on_click=evento
            )
        )

    def abrir_empleados(self):
        self.cambiar_vista(VistaEmpleado(self.page, self.cambiar_vista))
