import flet as ft
from dashboard_view import DashboardView

def main(page: ft.Page):
    page.title = "Sistema de Empleados - Dashboard"
    page.window_width = 1200
    page.window_height = 900
    page.theme_mode = "light"
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def cambiar_vista(vista):
        page.clean()
        page.add(vista)
        page.update()

    dashboard = DashboardView(page, cambiar_vista)
    cambiar_vista(dashboard)

ft.app(target=main)
