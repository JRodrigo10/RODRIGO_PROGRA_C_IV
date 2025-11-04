import flet as ft
import alumno_vista as alumno  
import docente

usuarios = {
    "docente.com": {"password": "1234", "rol": "docente"},
    "alumno.com": {"password": "2006", "rol": "alumno"}
}

def main(page: ft.Page):
    page.title = "Login con Correo"
    page.window.width = 400
    page.window.height = 300
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    correo = ft.TextField(label="Correo", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text()

    def login_click(e):
        email = correo.value
        pwd = password.value

        if email in usuarios and usuarios[email]["password"] == pwd:
            rol = usuarios[email]["rol"]
            if rol == "docente":
                docente.mostrar_docente(page)
            else:
                alumno.mostrar_alumno(page)
        else:
            mensaje.value = "❌ Correo o contraseña incorrectos"
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("📧 Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD),
                correo,
                password,
                ft.ElevatedButton("Iniciar sesión", on_click=login_click),
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)