import flet as ft
import nube as at
import main as login_main

def alta_usuario(page: ft.Page):
    def guardar_usuario(e: ft.ControlEvent):
        clave = txt_clave.value.strip()
        contra = txt_contra.value.strip()
        contra2 = txt_contra2.value.strip()
        nombre = txt_nombre.value.strip()
        snackbar = ft.SnackBar(content=None, bgcolor="blue", show_close_icon=True)

        if not clave:
            snackbar.content = ft.Text("Introduce tu clave usuario", color="white")
            page.open(snackbar)
            return
        if not contra:
            snackbar.content = ft.Text("Introduce la contraseña", color="white")
            page.open(snackbar)
            return
        if not contra2:
            snackbar.content = ft.Text("Confirma la contraseña", color="white")
            page.open(snackbar)
            return
        if not nombre:
            snackbar.content = ft.Text("Introduce tu nombre", color="white")
            page.open(snackbar)
            return
        if contra != contra2:
            snackbar.content = ft.Text("Las contraseñas no coinciden", color="white")
            page.open(snackbar)
            return

        nuevo = at.Usuario(
            clave=clave,
            contra=contra,
            nombre=nombre,
            admin=chk_admin.value
        )
        try:
            nuevo.save()
            snackbar.content = ft.Text("Usuario registrado", color="white")
            page.open(snackbar)
            txt_clave.value = ""
            txt_contra.value = ""
            txt_contra2.value = ""
            txt_nombre.value = ""
            chk_admin.value = False
            page.update()
        except Exception as error:
            snackbar.content = ft.Text(f"Error: {error}", color="white")
            page.open(snackbar)

    def cancelar(e: ft.ControlEvent):
        page.controls.clear()
        main(page)

    page.title = "Alta de usuario"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = "white"
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text(
            "Agregar nuevo usuario",
            size=20,
            weight="bold",
            font_family="Segoe UI",  
            color="white"),
        center_title=True,
        leading=ft.Icon(ft.Icons.PERSON_ADD),
        bgcolor="purple",
        color="white"
    )

    txt_clave = ft.TextField(label="Clave de usuario", color="black")
    txt_contra = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, color="black")
    txt_contra2 = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, color="black")
    txt_nombre = ft.TextField(label="Nombre completo", color="black")
    chk_admin = ft.Checkbox(label="¿Es administrador?", value=False)

    btn_guardar = ft.FilledButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar_usuario, bgcolor="green", color="white")
    btn_cancelar = ft.FilledButton("Cancelar", icon=ft.Icons.CANCEL, on_click=cancelar, bgcolor="red", color="white")
    fila_botones = ft.Row(controls=[btn_guardar, btn_cancelar], spacing=10)

    formulario = ft.Column(
        controls=[txt_clave, txt_contra, txt_contra2, txt_nombre, chk_admin, fila_botones],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        ft.Container(
            content=formulario,
            alignment=ft.alignment.center,
            expand=True
        )
    )
    page.update()

def consulta_usuarios(page: ft.Page):
    mostrar_contrasenas = False
    acceso_autorizado = False

    txt_clave_admin = ft.TextField(
        label="Palabra clave para ver contraseñas",
        label_style=ft.TextStyle(size=12),
        password=True,
        visible=False,
        color="black",
        can_reveal_password=True,
    )

    snackbar = ft.SnackBar(content=None, bgcolor="red", show_close_icon=True)

    def regresar_menu(e: ft.ControlEvent):
        page.controls.clear()
        main(page)

    def verificar_clave(e: ft.ControlEvent):
        nonlocal mostrar_contrasenas, acceso_autorizado
        clave_ingresada = txt_clave_admin.value.strip()
        if clave_ingresada == "admin123":
            mostrar_contrasenas = True
            acceso_autorizado = True
            txt_clave_admin.value = ""
            txt_clave_admin.visible = False
            cargar_tabla()
        else:
            snackbar.content = ft.Text("⚠️ Clave incorrecta. No puedes ver las contraseñas.", color="white")
            page.open(snackbar)
            txt_clave_admin.value = ""
            page.update()

    def toggle_contrasenas(e: ft.ControlEvent):
        nonlocal mostrar_contrasenas, acceso_autorizado
        if not acceso_autorizado:
            txt_clave_admin.visible = True
            btn_validar_clave.visible = True
            cargar_tabla()
        else:
            mostrar_contrasenas = False
            acceso_autorizado = False
            txt_clave_admin.visible = False
            btn_validar_clave.visible = False
            cargar_tabla()

    btn_validar_clave = ft.ElevatedButton(
        text="Aceptar",
        on_click=verificar_clave,
        visible=False,
        bgcolor="purple",
        color="white"
    )

    def cargar_tabla():
        page.controls.clear()
        page.bgcolor = "white"
        page.appbar = appbar

        encabezado = [
            ft.DataColumn(ft.Text("Clave", color="black")),
            ft.DataColumn(ft.Text("Contraseña", color="black")),
            ft.DataColumn(ft.Text("Nombre completo", color="black")),
            ft.DataColumn(ft.Text("Administrador", color="black")),
        ]

        filas = []
        try:
            datos = at.Usuario.all()
        except Exception as e:
            page.add(ft.Text(f"Error al cargar datos: {e}", color="red"))
            page.update()
            return

        if not datos:
            page.add(ft.Text("No hay usuarios registrados.", color="black"))
            btn_volver = ft.ElevatedButton("Volver al menú", on_click=regresar_menu)
            page.add(btn_volver)
            page.update()
            return

        for d in datos:
            celda1 = ft.DataCell(ft.Text(d.clave, color="black"))
            celda2 = ft.DataCell(ft.Text(d.contra if mostrar_contrasenas else "●●●●●●●", color="black"))
            celda3 = ft.DataCell(ft.Text(d.nombre, color="black"))
            celda4 = ft.DataCell(
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green") if d.admin else ft.Icon(ft.Icons.CANCEL, color="red")
            )
            fila = ft.DataRow([celda1, celda2, celda3, celda4])
            filas.append(fila)

        tabla = ft.DataTable(
            columns=encabezado,
            rows=filas,
            column_spacing=20,
            heading_row_color=ft.Colors.AMBER_100
        )

        btn_toggle = ft.TextButton(
            text="👁️ Mostrar contraseñas" if not mostrar_contrasenas else "🔒 Ocultar contraseñas",
            on_click=toggle_contrasenas
        )

        fila_clave = ft.Row(
            controls=[
                ft.Container(txt_clave_admin, width=300),
                btn_validar_clave
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=txt_clave_admin.visible,
            spacing=10
        )

        btn_volver = ft.ElevatedButton(
            "Volver al menú",
            on_click=regresar_menu,
            bgcolor="blue",
            color="white"
        )

        contenido = ft.Column(
            controls=[
                btn_toggle,
                fila_clave,
                tabla,
                ft.Container(height=20),
                btn_volver
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.add(
            ft.Container(
                content=contenido,
                alignment=ft.alignment.center,
                expand=True
            )
        )
        page.update()

    page.title = "Consulta de usuarios"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = "white"

    appbar = ft.AppBar(
        title=ft.Text(
            "Consulta de usuarios en la nube",
            size=20,
            weight="bold",
            font_family="Segoe UI",
            color="white"
        ),
        center_title=True,
        leading=ft.Icon(ft.Icons.CLOUD),
        bgcolor="green",
        color="white"
    )

    cargar_tabla()

def main(page: ft.Page):
    def abrir_alta_usuario(e: ft.ControlEvent):
        page.controls.clear()
        alta_usuario(page)

    def abrir_consulta_usuarios(e: ft.ControlEvent):
        page.controls.clear()
        consulta_usuarios(page)

    def abrir_login(e: ft.ControlEvent):
        page.controls.clear()
        page.appbar = None
        login_main.main(page)

    page.title = "Gestión de Usuarios"
    page.window_width = 800
    page.window_height = 600
    page.bgcolor = "white"
    page.controls.clear()

    page.appbar = ft.AppBar(
        title=ft.Text(
            "Gestión de Usuarios",
            size=20,
            weight="bold",
            font_family="Segoe UI",  
            color="white"),
        leading=ft.Icon(ft.Icons.GROUP),
        center_title=True,
        bgcolor="blue",
        color="white"
    )

    btn_agregar = ft.FilledButton(
        "Agregar nuevo usuario",
        icon=ft.Icons.PERSON_ADD,
        on_click=abrir_alta_usuario,
        width=200,
        bgcolor="purple",
        color="white"
    )

    btn_consultar = ft.FilledButton(
        "Consultar usuarios",
        icon=ft.Icons.SEARCH,
        on_click=abrir_consulta_usuarios,
        width=200,
        bgcolor="green",
        color="white"
    )

    btn_login = ft.FilledButton(
        "Cerrar sesión",
        icon=ft.Icons.ACCOUNT_CIRCLE,
        on_click=abrir_login,
        width=200,
        bgcolor="orange",
        color="white"
    )

    columna = ft.Column(
        controls=[btn_agregar, btn_consultar, btn_login],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    contenedor = ft.Container(
        content=columna,
        alignment=ft.alignment.center,
        expand=True
    )

    page.add(contenedor)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
