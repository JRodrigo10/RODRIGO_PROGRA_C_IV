import flet as ft
import usuario
import administrador

users = {
    "admin": {"password": "1234", "role": "admin"},
    "jrodrigo": {"password": "2006", "role": "user"}
}

def main(page: ft.Page):
    page.title = "Login"
    page.window.width = 400
    page.window.height = 300
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username = ft.TextField(label="Usuario", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text()

    def login_click(e):
        user = username.value
        pwd = password.value

        if user in users and users[user]["password"] == pwd:
            role = users[user]["role"]
            if role == "admin":
                administrador.mostrar_admin(page)  # manda a admin.py
            else:
                usuario.mostrar_user(page)        # manda a usuario.py
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("🔐 Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD),
                username,
                password,
                ft.ElevatedButton("Iniciar sesión", on_click=login_click),
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
