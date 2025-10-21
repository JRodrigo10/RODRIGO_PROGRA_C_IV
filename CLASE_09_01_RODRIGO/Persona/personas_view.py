# personas_view.py
import flet as ft
from conexion import ConexionDB

class PersonasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("👥 Gestión de Personas", size=22, weight="bold")

        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_personas())

        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar]),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.controls = [self.content]
        self.cargar_personas()

    # ✅ Carga de datos desde MySQL
    def cargar_personas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT persona_id, nombres, apellidos, numero_documento, telefono FROM personas")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()

                for fila in resultados:
                    persona_id, nombres, apellidos, dni, telefono = fila

                    # 👇 importante: usar función interna para capturar fila correctamente
                    def crear_boton_editar(fila_capturada):
                        return ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.BLUE,
                            tooltip="Editar persona",
                            on_click=lambda e: self.abrir_dialogo_editar(fila_capturada)
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(persona_id))),
                                ft.DataCell(ft.Text(nombres)),
                                ft.DataCell(ft.Text(apellidos)),
                                ft.DataCell(ft.Text(dni)),
                                ft.DataCell(ft.Text(telefono)),
                                ft.DataCell(crear_boton_editar(fila)),
                            ]
                        )
                    )

                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar personas: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # ✅ Diálogo para editar persona
    def abrir_dialogo_editar(self, fila):
        try:
            persona_id, nombres, apellidos, dni, telefono = fila
        except Exception as e:
            print(f"⚠️ Error al abrir diálogo: {e}")
            return

        txt_nombres = ft.TextField(label="Nombres", value=nombres)
        txt_apellidos = ft.TextField(label="Apellidos", value=apellidos)
        txt_dni = ft.TextField(label="DNI", value=dni)
        txt_telefono = ft.TextField(label="Teléfono", value=telefono)

        def guardar_cambios(e):
            nuevos_nombres = txt_nombres.value
            nuevos_apellidos = txt_apellidos.value
            nuevo_dni = txt_dni.value
            nuevo_telefono = txt_telefono.value

            resultado = self.conexion.actualizar_persona(
                persona_id, nuevos_nombres, nuevos_apellidos, nuevo_dni, nuevo_telefono
            )

            if resultado["status"]:
                self.page.snack_bar = ft.SnackBar(ft.Text("✅ Datos actualizados correctamente"))
                dlg.open = False
                self.cargar_personas()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("❌ Error al actualizar los datos"))

            self.page.snack_bar.open = True
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("✏️ Editar Persona"),
            content=ft.Column(
                [txt_nombres, txt_apellidos, txt_dni, txt_telefono],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.ElevatedButton("💾 Guardar", on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()
