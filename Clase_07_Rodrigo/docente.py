import flet as ft
import login

def mostrar_docente(page: ft.Page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("👨‍🏫 Bienvenido Docente", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Tienes acceso completo como profesor."),
                ft.ElevatedButton("Cerrar sesión", on_click=lambda e: login.main(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
