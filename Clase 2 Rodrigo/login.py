import flet as ft
def main(page: ft.Page):

    page.window.width = 500
    page.window.height = 200
    page.window.resizable = False
    page.window.maximizable = False
    page.window.fullscreen = False
    page.window.center()
    page.title = "Segunda clase - Programación Concurrente"

    btn_compra = ft.ElevatedButton(
        text="Realizar compra 🛒",
        width=200,
        height=100,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor="#4CAF50",
            color="white"
        )
    )
    
    btn_login = ft.ElevatedButton(
        text="iniciar sesión 🔑",
        width=200,
        height=100,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor="#2196F3",
            color="white"
        )    
    )

    fila_botones =ft.Row(
        controls= [btn_compra, btn_login],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
    
    page.add(
        ft.Divider(height=6, color="transparent"),
        fila_botones
    )

    page.update()

ft.app(target=main)