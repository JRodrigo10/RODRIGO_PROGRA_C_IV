import flet as ft
from conexion import ConexionDB

class AgregarEmpleadoView(ft.Container):
    def __init__(self, page, cambiar_vista, empleado=None):
        super().__init__(expand=True)
        self.page = page
        self.cambiar_vista = cambiar_vista
        self.db = ConexionDB()
        self.empleado = empleado  # Recibe empleado si viene desde Editar

        # Si hay empleado, estamos editando
        self.editando = empleado is not None

        # Título dinámico
        titulo_texto = "✏️ Editar Empleado" if self.editando else "➕ Agregar Empleado"
        titulo = ft.Text(titulo_texto, size=22, weight=ft.FontWeight.BOLD)

        # Campos del formulario
        self.nombre = ft.TextField(label="Nombre", value=empleado["nombre"] if self.editando else "")
        self.apellido = ft.TextField(label="Apellido", value=empleado["apellido"] if self.editando else "")
        self.dni = ft.TextField(label="DNI", value=empleado["dni"] if self.editando else "")
        self.cargo = ft.TextField(label="Cargo", value=empleado["cargo"] if self.editando else "")
        self.departamento = ft.TextField(label="Departamento", value=empleado["departamento"] if self.editando else "")
        self.salario = ft.TextField(label="Salario", value=str(empleado["salario"]) if self.editando else "")
        self.telefono = ft.TextField(label="Teléfono", value=empleado["telefono"] if self.editando else "")

        # Botones
        boton_guardar = ft.ElevatedButton("💾 Guardar Cambios", on_click=self.guardar)
        boton_cancelar = ft.OutlinedButton("⬅ Volver", on_click=lambda e: self.volver())

        self.content = ft.Column(
            [
                titulo,
                ft.Divider(),
                self.nombre,
                self.apellido,
                self.dni,
                self.cargo,
                self.departamento,
                self.salario,
                self.telefono,
                ft.Row([boton_guardar, boton_cancelar])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400,
        )

    # 🔹 Guardar cambios o agregar nuevo empleado
    def guardar(self, e):
        nombre = self.nombre.value.strip()
        apellido = self.apellido.value.strip()
        dni = self.dni.value.strip()
        cargo = self.cargo.value.strip()
        departamento = self.departamento.value.strip()
        salario = self.salario.value.strip()
        telefono = self.telefono.value.strip()

        # Validaciones básicas
        if nombre == "" or apellido == "":
            self.mostrar_alerta("⚠️ Nombre y Apellido no pueden estar vacíos")
            return

        try:
            salario = float(salario) if salario else 0.0
        except ValueError:
            self.mostrar_alerta("⚠️ El salario debe ser numérico")
            return

        if self.editando:
            # Actualizar empleado existente
            id_emp = self.empleado.get("id_empleado")
            self.db.actualizar_empleado(id_emp, nombre, apellido, dni, cargo, departamento, salario, telefono)
            self.mostrar_alerta("✅ Empleado actualizado correctamente")
        else:
            # Agregar nuevo empleado
            self.db.agregar_empleado(nombre, apellido, dni, cargo, departamento, salario, telefono)
            self.mostrar_alerta("✅ Empleado agregado correctamente")

        self.volver()

    # 🔹 Mostrar alerta en pantalla
    def mostrar_alerta(self, mensaje):
        self.page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        self.page.snack_bar.open = True
        self.page.update()

    # 🔹 Volver al listado de empleados
    def volver(self):
        from vistas.vista_empleado import VistaEmpleado
        self.cambiar_vista(VistaEmpleado(self.page, self.cambiar_vista))
