import flet as ft
from conexion import ConexionDB

class EspecialidadesView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        if not callable(volver_atras):
            raise ValueError('El argumento volver_atras debe ser una función (callable), pero se recibió: {}'.format(type(volver_atras)))
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()
        self.titulo = ft.Text("👨‍🔬 Gestión de Especialidades", size=22, weight="bold")
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_especialidades())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())
        self.content = ft.Column([
            self.titulo,
            ft.Row([self.btn_volver, self.btn_actualizar, self.btn_agregar], alignment=ft.MainAxisAlignment.START),
            ft.Container(self.tabla, expand=True, border_radius=10, padding=10, bgcolor=ft.Colors.BLUE_50)
        ], spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)
        self.controls = [self.content]
        self.cargar_especialidades()

    def cargar_especialidades(self):
        conexion = self.conexion.conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                cursor.execute("SELECT especialidad_id, nombre, descripcion FROM especialidades")
                resultados = cursor.fetchall()
                self.tabla.rows.clear()
                for fila in resultados:
                    especialidad_id = fila[0]
                    def crear_botones(eid):
                        return ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, _eid=eid: self.mostrar_formulario_editar(_eid)),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Eliminar", icon_color="red", on_click=lambda e, _eid=eid: self.confirmar_eliminar_especialidad(_eid)),
                        ])
                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(crear_botones(especialidad_id))
                            ]
                        )
                    )
                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar especialidades: {e}")
            finally:
                cursor.close()
                self.conexion.cerrar(conexion)

    def mostrar_formulario_nuevo(self):
        txt_nombre = ft.TextField(label="Nombre de especialidad")
        txt_descripcion = ft.TextField(label="Descripción")

        def guardar_nueva(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute(
                        "INSERT INTO especialidades (nombre, descripcion) VALUES (%s, %s)",
                        (txt_nombre.value, txt_descripcion.value)
                    )
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_especialidades()
                except Exception as ex:
                    print(f"❌ Error al insertar especialidad: {ex}")
                finally:
                    cur.close()
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Especialidad"),
            content=ft.Column([txt_nombre, txt_descripcion], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nueva),
            ]
        )
        self.page.show_dialog(dlg)

    def mostrar_formulario_editar(self, especialidad_id):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("SELECT nombre, descripcion FROM especialidades WHERE especialidad_id=%s", (especialidad_id,))
                datos = cur.fetchone()
                if not datos:
                    print("Especialidad no encontrada")
                    return
                txt_nombre = ft.TextField(label="Nombre de especialidad", value=datos[0])
                txt_descripcion = ft.TextField(label="Descripción", value=datos[1])

                def guardar_editada(e):
                    conexion2 = self.conexion.conectar()
                    if conexion2:
                        cur2 = conexion2.cursor()
                        try:
                            cur2.execute("UPDATE especialidades SET nombre=%s, descripcion=%s WHERE especialidad_id=%s", (txt_nombre.value, txt_descripcion.value, especialidad_id))
                            conexion2.commit()
                            self.cerrar_dialogo(dlg)
                            self.cargar_especialidades()
                        except Exception as ex:
                            print(f"❌ Error editando especialidad: {ex}")
                        finally:
                            cur2.close()
                            self.conexion.cerrar(conexion2)

                dlg = ft.AlertDialog(
                    title=ft.Text("✏️ Editar Especialidad"),
                    content=ft.Column([txt_nombre, txt_descripcion], spacing=10),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                        ft.TextButton("Guardar", on_click=guardar_editada),
                    ]
                )
                self.page.show_dialog(dlg)
            finally:
                cur.close()
                self.conexion.cerrar(conexion)

    def confirmar_eliminar_especialidad(self, especialidad_id):
        dlg = ft.AlertDialog(
            title=ft.Text("Eliminar Especialidad"),
            content=ft.Text("¿Está seguro que desea eliminar esta especialidad?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Eliminar", on_click=lambda e: self.eliminar_especialidad(especialidad_id, dlg)),
            ]
        )
        self.page.show_dialog(dlg)

    def eliminar_especialidad(self, especialidad_id, dlg):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("DELETE FROM especialidades WHERE especialidad_id=%s", (especialidad_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg)
                self.cargar_especialidades()
            except Exception as ex:
                print(f"❌ Error al eliminar especialidad: {ex}")
            finally:
                cur.close()
                self.conexion.cerrar(conexion)

    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()



