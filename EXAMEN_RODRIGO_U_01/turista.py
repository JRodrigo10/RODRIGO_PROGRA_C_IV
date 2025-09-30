import flet as ft
import os
import sys
import subprocess
import asyncio

def main(page: ft.Page):
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True
    page.window.center()
    page.title = "Sistema - Online de Reservaciones o venta de Cupos para Viajes Turísticos"

    # Variables dinámicas
    mensaje = ft.Text("", size=16, color="orange", weight=ft.FontWeight.BOLD)
    contador = ft.Text("Cupos reservados: 0", size=16, color="green", weight=ft.FontWeight.BOLD)
    cupos_reservados = {"cantidad": 0}  # usamos dict para que sea mutable dentro de funciones

    def volver_inicio(e):
        page.window.close()
        ruta_main = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta_main])

    # Función asíncrona para simular reserva
    async def reservar_cupo_async():
        mensaje.value = "⏳ Reservando cupo..."
        page.update()
        await asyncio.sleep(2)  # simula tiempo de proceso
        cupos_reservados["cantidad"] += 1  # aumenta contador
        mensaje.value = "✅ Cupo reservado con éxito"
        contador.value = f"Cupos reservados: {cupos_reservados['cantidad']}"
        page.update()

    def reservar_cupo(e):
        page.run_task(reservar_cupo_async)

    # Layout del dashboard
    page.add(
        ft.Column(
            [
                ft.Text("🪐 RESERVACIONES Y VENTAS EN MODO TURÍSTA DE CUPOS PARA VIAJES TURÍSTICOS POR TODO EL MUNDO 🌻",
                        size=26, weight=ft.FontWeight.BOLD, color="#DA0A0A"),
                ft.Divider(height=20),
                ft.Text("Bienvenido al sistema de gestión de ventas online Turístico", size=18),
                ft.Divider(height=30),
                ft.Row(
                    [
                        ft.ElevatedButton("Ver Reportes"),
                        ft.ElevatedButton("Reservar Cupo", on_click=reservar_cupo),
                        ft.ElevatedButton("Modo Turista"),
                    ],
                    spacing=20
                ),
                mensaje,
                contador,  # mostramos el contador debajo
                ft.Divider(height=30),
                ft.ElevatedButton("Volver al Inicio y cerrar sesión", on_click=volver_inicio)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
