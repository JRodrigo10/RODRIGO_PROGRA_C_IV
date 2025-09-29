import flet as ft
import login

def mostrar_user(page: ft.Page):
    page.controls.clear()
    page.add(
        ft.Column(
            [
                ft.Text("👤 Bienvenido Usuario", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Eres solo usuario, no tienes privilegios de administrador."),
                ft.ElevatedButton("Cerrar sesión", on_click=lambda e: login.main(page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()
