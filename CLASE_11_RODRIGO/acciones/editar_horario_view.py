# editar_horario_view.py
import flet as ft
from conexion import ConexionDB


class EditarHorarioView(ft.Container):
    def __init__(self, page, horario_id, volver_atras=None):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.horario_id = horario_id
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"🕒 Editar Horario ID: {horario_id}", size=22, weight="bold")

        # Campos del formulario según tu tabla de horarios
        self.txt_dia = ft.TextField(label="Día", width=300)
        self.txt_hora_inicio = ft.TextField(label="Hora Inicio", width=300)
        self.txt_hora_fin = ft.TextField(label="Hora Fin", width=300)
        self.txt_id_docente = ft.TextField(label="ID Docente", width=300)
        self.txt_id_curso = ft.TextField(label="ID Curso", width=300)

        # Botones
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.ir_atras_seguro())
        self.btn_guardar = ft.ElevatedButton("💾 Guardar Cambios", on_click=lambda e: self.guardar_cambios())

        # Layout
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row([self.txt_dia, self.txt_hora_inicio, self.txt_hora_fin]),
                ft.Row([self.txt_id_docente, self.txt_id_curso]),
                ft.Row([self.btn_volver, self.btn_guardar]),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
        )

        self.controls = [self.content]

        # Cargar datos actuales del horario
        self.cargar_datos()

    # =============================
    #   CARGAR DATOS EXISTENTES
    # =============================
    def cargar_datos(self):
        conexion = self.conexion.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT dia, hora_inicio, hora_fin, id_docente, id_curso FROM horarios WHERE id_horario = %s",
                    (self.horario_id,),
                )
                horario = cursor.fetchone()
                if horario:
                    self.txt_dia.value = horario[0]
                    self.txt_hora_inicio.value = str(horario[1])
                    self.txt_hora_fin.value = str(horario[2])
                    self.txt_id_docente.value = str(horario[3])
                    self.txt_id_curso.value = str(horario[4])
                    self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar datos del horario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   GUARDAR CAMBIOS
    # =============================
    def guardar_cambios(self):
        conexion = self.conexion.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    UPDATE horarios
                    SET dia = %s, hora_inicio = %s, hora_fin = %s, id_docente = %s, id_curso = %s
                    WHERE id_horario = %s
                    """,
                    (
                        self.txt_dia.value,
                        self.txt_hora_inicio.value,
                        self.txt_hora_fin.value,
                        self.txt_id_docente.value,
                        self.txt_id_curso.value,
                        self.horario_id,
                    ),
                )
                conexion.commit()
                print("✅ Horario actualizado correctamente")

                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("✅ Horario actualizado correctamente", color="white"),
                    bgcolor="green",
                    open=True,
                    duration=1500,
                )
                self.page.update()

                self.ir_atras_seguro()
            except Exception as e:
                print(f"❌ Error al actualizar horario: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   VOLVER ATRÁS SEGURO
    # =============================
    def ir_atras_seguro(self):
        """Regresa a la lista de horarios o a la vista anterior."""
        if callable(self.volver_atras):
            self.volver_atras()
        else:
            print("↩️ Regresando a la lista de horarios (vista anterior)")
            from Horario.horarios_view import HorariosView  # ✅ carpeta correcta

            self.page.clean()
            nueva_vista = HorariosView(self.page, volver_atras=lambda: print("Volver desde horarios view por defecto"))
            self.page.add(nueva_vista)
            self.page.update()
