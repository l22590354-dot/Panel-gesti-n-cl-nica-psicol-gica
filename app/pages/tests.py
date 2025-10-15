import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State


def upload_component() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", size=48, class_name="text-gray-400"),
                rx.el.p("Arrastra archivos o haz clic para seleccionar."),
                class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg",
            ),
            id="upload_test",
            multiple=True,
            accept={"application/pdf": [".pdf"], "image/*": [".png", ".jpg", ".jpeg"]},
            class_name="w-full cursor-pointer",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("upload_test"),
                lambda file: rx.el.div(
                    file, class_name="text-sm p-2 bg-gray-100 rounded"
                ),
            ),
            class_name="mt-4 space-y-1",
        ),
        rx.el.button(
            "Subir Archivos",
            on_click=State.handle_upload(rx.upload_files("upload_test")),
            class_name="mt-4 bg-violet-600 text-white py-2 px-4 rounded-lg",
        ),
        rx.cond(
            State.is_uploading,
            rx.progress(value=State.upload_progress, class_name="w-full mt-2"),
        ),
    )


def test_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                "Anexar Prueba",
                rx.icon("plus", class_name="ml-2"),
                on_click=State.toggle_test_modal,
                class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Anexar Nueva Prueba"),
            rx.el.form(
                rx.el.div(
                    rx.el.select(
                        rx.el.option(
                            "Seleccionar Paciente...", value="", disabled=True
                        ),
                        rx.foreach(
                            State.patients,
                            lambda patient: rx.el.option(
                                patient["nombre"], value=patient["CURP"]
                            ),
                        ),
                        name="paciente_CURP",
                        default_value="",
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.input(
                        name="tipo_prueba",
                        placeholder="Tipo de prueba",
                        class_name="border rounded p-2 w-full",
                    ),
                    upload_component(),
                    class_name="flex flex-col space-y-2",
                )
            ),
            open=State.show_test_modal,
        ),
    )


def tests_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("ID"),
                    rx.el.th("Paciente"),
                    rx.el.th("Psicólogo"),
                    rx.el.th("Tipo"),
                    rx.el.th("Acciones"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    State.tests,
                    lambda test: rx.el.tr(
                        rx.el.td(test["id"]),
                        rx.el.td(test["paciente_CURP"]),
                        rx.el.td(test["psicologo_RFC"]),
                        rx.el.td(test["tipo_prueba"]),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("download"), class_name="text-green-500"
                            )
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border",
    )


def tests() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Gestión de Pruebas", class_name="text-3xl font-bold text-gray-800"
                ),
                test_modal(),
                class_name="flex justify-between items-center mb-6",
            ),
            tests_table(),
            rx.cond(
                State.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-20",
                ),
            ),
        )
    )