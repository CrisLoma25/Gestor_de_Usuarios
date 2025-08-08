import flet as ft
from pyairtable.formulas import match
from nube import Usuario  # Modelo Airtable
import principal as pr        # Módulo pantalla principal

def main(page: ft.Page):
    def validar_usuario(e: ft.ControlEvent):
        usuario = txt_usuario.value
        contra = txt_contra.value
        snackbar = ft.SnackBar(content=None, bgcolor="blue", show_close_icon=True)

        if usuario == "":
            snackbar.content = ft.Text("Introduce tu usuario")
            page.open(snackbar)
            return

        if contra == "":
            snackbar.content = ft.Text("Introduce tu contraseña")
            page.open(snackbar)
            return

        try:
            formula = match({"clave": usuario, "contra": contra})
            registro = Usuario.first(formula=formula)

            if registro:
                nombre = registro.nombre
                es_admin = registro.admin
                mensaje = f"Bienvenido, {nombre} - Admin: {'Sí' if es_admin else 'No'}"
                snackbar.content = ft.Text(mensaje)
                page.open(snackbar)

                page.clean()
                pr.main(page)
            else:
                snackbar.content = ft.Text(f"Usuario '{usuario}' no encontrado.")
                page.open(snackbar)

        except Exception as e:
            snackbar.content = ft.Text(f"Error de Airtable: {e}")
            page.open(snackbar)

    page.theme_mode = "light"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Inicio de sesión"
    page.window_maximized = True

    logo = ft.Icon(name="ACCOUNT_CIRCLE", size=80, color="pink")
    txt_bienvenido = ft.Text(
        "Bienvenido", 
        size=24,
        weight="bold",
        font_family="Segoe UI",
        color="black"
    )

    txt_usuario = ft.TextField(
        label="Username/correo",
        width=250,
        prefix_icon=ft.Icons.PERSON,
        on_submit=validar_usuario
    )

    txt_contra = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=250,
        prefix_icon=ft.Icons.LOCK,
        on_submit=validar_usuario
    )

    btn_login = ft.FilledButton(
        text="Iniciar sesión",
        icon=ft.Icons.LOGIN,
        width=250,
        color="white",
        bgcolor="pink",
        on_click=validar_usuario
    )

    contenido = ft.Column(
        controls=[logo, txt_bienvenido, txt_usuario, txt_contra, btn_login],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    card_login = ft.Container(
        content=contenido,
        padding=25,
        border_radius=15,
        bgcolor="#FAF9EE",                 # Fondo blanco
        border=ft.border.all(1, "black"),  # Borde negro delgado
        alignment=ft.alignment.center,
        width=350                        # Ancho controlado
    )

    page.add(
        ft.Container(
            content=card_login,
            alignment=ft.alignment.center
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main,view=ft.AppView.WEB_BROWSER)
