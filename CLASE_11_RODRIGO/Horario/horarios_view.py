import flet as ft
from conexion import ConexionDB
from acciones.editar_horario_view import EditarHorarioView

class HorariosView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("🕒 Gestión de Horarios", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Día Semana")),
                ft.DataColumn(ft.Text("Hora Inicio")),
                ft.DataColumn(ft.Text("Hora Fin")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_horarios())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        # --- Contenedor principal ---
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
                ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        # Cargar datos iniciales
        self.cargar_horarios()

    # =============================
    #   CARGAR HORARIOS
    # =============================
    def cargar_horarios(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT horario_id, dia_semana, hora_inicio, hora_fin, descripcion FROM horarios")
                resultados = cursor.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    horario_id = fila[0]
                    def crear_botones(hid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _hid=hid: self.mostrar_id_capturado(_hid, "editar")
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _hid=hid: self.mostrar_id_capturado(_hid, "eliminar")
                                )
                            ]
                        )
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(str(fila[1]))),
                                ft.DataCell(ft.Text(str(fila[2]))),
                                ft.DataCell(ft.Text(str(fila[3]))),
                                ft.DataCell(ft.Text(fila[4] or "")),
                                ft.DataCell(crear_botones(horario_id))
                            ]
                        )
                    )
                self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar horarios: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   MOSTRAR ID CAPTURADO
    # =============================
    def mostrar_id_capturado(self, horario_id, accion):
        print(f"✅ mostrar_id_capturado -> accion={accion}, id={horario_id}")

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"ID capturado para {accion.upper()}: {horario_id}", color="white"),
            bgcolor="green",
            open=True,
            duration=1500
        )
        self.page.update()

        if accion == "editar":
            self.mostrar_formulario_editar(horario_id)
        elif accion == "eliminar":
            self.eliminar_horario(horario_id)

    # =============================
    #   NUEVO HORARIO
    # =============================
    def mostrar_formulario_nuevo(self):
        txt_dia = ft.TextField(label="Día Semana (0=Lunes, 6=Domingo)")
        txt_inicio = ft.TextField(label="Hora Inicio (HH:MM:SS)")
        txt_fin = ft.TextField(label="Hora Fin (HH:MM:SS)")
        txt_descripcion = ft.TextField(label="Descripción")

        def guardar_nuevo(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO horarios (dia_semana, hora_inicio, hora_fin, descripcion)
                        VALUES (%s, %s, %s, %s)
                    """, (txt_dia.value, txt_inicio.value, txt_fin.value, txt_descripcion.value))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_horarios()
                except Exception as ex:
                    print(f"❌ Error al insertar horario: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nuevo Horario"),
            content=ft.Column([txt_dia, txt_inicio, txt_fin, txt_descripcion], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nuevo),
            ]
        )
        self.page.show_dialog(dlg)

    # =============================
    #   EDITAR HORARIO
    # =============================
    def mostrar_formulario_editar(self, horario_id):
        print(f"🧩 Navegando a vista edición para horario {horario_id}")
        from acciones.editar_horario_view import EditarHorarioView
        editar_vista = EditarHorarioView(self.page, horario_id, volver_atras=lambda: self.recargar_y_mantener_volver())
        self.page.clean()
        self.page.add(editar_vista)
        self.page.update()

    def recargar_y_mantener_volver(self):
        self.page.clean()
        self.page.add(HorariosView(self.page, volver_atras=self.volver_atras))
        self.page.update()

    # =============================
    #   ELIMINAR HORARIO
    # =============================
    def eliminar_horario(self, horario_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este horario?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(horario_id, dlg_confirm)
                )
            ]
        )
        self.page.dialog = dlg_confirm
        self.page.dialog.open = True
        self.page.update()

    def confirmar_eliminar(self, horario_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("DELETE FROM horarios WHERE horario_id = %s", (horario_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_horarios()
            except Exception as e:
                print(f"❌ Error al eliminar horario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   CERRAR DIÁLOGO
    # =============================
    def cerrar_dialogo(self, dlg):
        try:
            dlg.open = False
            self.page.update()
        except Exception as e:
            print("DEBUG: error cerrando dialogo:", e)
