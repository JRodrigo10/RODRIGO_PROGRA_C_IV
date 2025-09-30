import flet as ft
import os
import sys
import subprocess

# Usuario/contraseña de ejemplo (puedes cambiarlo o conectarlo a BD)
USUARIO = "jrodrigo"
PASSWORD = "200619"

def main(page: ft.Page):
    if not page.web:
        page.window.width = 400
        page.window.height = 300
        page.window.center()
        page.window.resizable = False

    page.title = "Login - Sistema de Viajes"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Campos de entrada
    user_input = ft.TextField(label="Usuario", width=250)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    mensaje = ft.Text("", color="red")

    # Función para abrir dashboard
    def abrir_dashboard():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "dashboard.py")
        subprocess.Popen([sys.executable, ruta_dashboard])
    def abrir_visitas():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "visitas.py")
        subprocess.Popen([sys.executable, ruta_dashboard])
    def abrir_turista():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "turista.py")
        subprocess.Popen([sys.executable, ruta_dashboard])
    def abrir_administrador():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "administrador.py")
        subprocess.Popen([sys.executable, ruta_dashboard])


    # Función para validar login
    def validar_login(e):
        if user_input.value == "USUARIO.COM" and pass_input.value == "123":
            mensaje.value = "✅ Acceso correcto"
            page.update()
            abrir_dashboard()
        if user_input.value == "VISITANTE.COM" and pass_input.value == "123":
            mensaje.value = "✅ Acceso correcto"
            page.clean()
            abrir_visitas()
        if user_input.value == "TURISTA.COM" and pass_input.value == "123":
            mensaje.value = "✅ Acceso correcto"
            page.clean()
            abrir_turista()
        if user_input.value == "ADMINISTRADOR.COM" and pass_input.value == "123":
            mensaje.value = "✅ Acceso correcto"
            page.clean()
            abrir_administrador()
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    # Botón de login
    btn_login = ft.ElevatedButton(
        text="Ingresar",
        bgcolor="#05EF91",
        color="white",
        width=250,
        on_click=validar_login
    )

    # Layout del login
    page.add(
        ft.Column(
            [
                ft.Text("     🔑SISTEMAS DE INICIO DE  SESIÓN DE VIAJES TURISTICOS🐋", size=22, weight=ft.FontWeight.BOLD, color="#2196F3"),
                user_input,
                pass_input,
                btn_login,
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
