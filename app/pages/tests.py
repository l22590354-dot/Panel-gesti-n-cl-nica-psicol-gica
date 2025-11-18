import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State, Prueba


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
                on_click=lambda: State.toggle_test_modal(None),
                class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
            )
        ),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(State.editing_test, "Editar Prueba", "Añadir Nueva Prueba"),
                    class_name="text-2xl font-bold pb-2 mb-4 border-b-2 border-violet-200 text-gray-800 font-['Lora']",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.h3(
                            "📋 Información de la Prueba",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Paciente",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.select(
                                    rx.el.option("Seleccionar Paciente", value=""),
                                    rx.foreach(
                                        State.patients,
                                        lambda p: rx.el.option(
                                            p["nombre"], value=p["CURP"]
                                        ),
                                    ),
                                    name="paciente_CURP",
                                    default_value=rx.cond(
                                        State.editing_test,
                                        State.editing_test["paciente_CURP"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Psicólogo",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.select(
                                    rx.el.option("Seleccionar Psicólogo", value=""),
                                    rx.foreach(
                                        State.psychologists,
                                        lambda p: rx.el.option(
                                            p["nombre"], value=p["RFC"]
                                        ),
                                    ),
                                    name="psicologo_RFC",
                                    default_value=rx.cond(
                                        State.editing_test,
                                        State.editing_test["psicologo_RFC"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Tipo de Prueba",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.input(
                                name="tipo_prueba",
                                placeholder="Ej. Inventario de Ansiedad de Beck",
                                default_value=rx.cond(
                                    State.editing_test,
                                    State.editing_test["tipo_prueba"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.hr(class_name="my-6"),
                        rx.el.h3(
                            "📊 Resultados",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Puntaje",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="puntaje",
                                    type="number",
                                    placeholder="0",
                                    default_value=rx.cond(
                                        State.editing_test,
                                        State.editing_test["puntaje"].to_string(),
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nivel",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.select(
                                    rx.el.option("Seleccionar Nivel", value=""),
                                    rx.foreach(
                                        ["Bajo", "Moderado", "Alto", "Severo"],
                                        lambda opt: rx.el.option(opt, value=opt),
                                    ),
                                    name="nivel",
                                    default_value=rx.cond(
                                        State.editing_test,
                                        State.editing_test["nivel"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Resultado",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.textarea(
                                name="resultados",
                                placeholder="Descripción de los resultados obtenidos...",
                                default_value=rx.cond(
                                    State.editing_test,
                                    State.editing_test["resultados"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                rows="2",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.hr(class_name="my-6"),
                        rx.el.h3(
                            "📎 Archivo Adjunto",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        upload_component(),
                        rx.el.hr(class_name="my-6"),
                        rx.el.h3(
                            "📝 Notas Adicionales",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.textarea(
                            name="notas",
                            placeholder="Notas o comentarios adicionales...",
                            default_value="",
                            class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                            rows="2",
                        ),
                        class_name="max-h-[60vh] overflow-y-auto p-1 pr-4",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancelar",
                                type="button",
                                on_click=lambda: State.toggle_test_modal(None),
                                class_name="px-6 py-2 rounded-lg bg-gray-200 text-gray-700 font-semibold hover:bg-gray-300 transition",
                            )
                        ),
                        rx.el.button(
                            rx.icon("save", class_name="mr-2"),
                            "Guardar Cambios",
                            type="submit",
                            class_name="px-6 py-2 rounded-lg bg-violet-600 text-white font-semibold hover:bg-violet-700 transition flex items-center",
                        ),
                        class_name="mt-6 flex justify-end space-x-4 border-t pt-4",
                    ),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-8 w-full max-w-2xl z-50",
            ),
        ),
        open=State.show_test_modal,
        on_open_change=lambda open: State.toggle_test_modal(None),
    )


def tests_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Paciente"),
                    rx.el.th("Tipo"),
                    rx.el.th("Puntaje"),
                    rx.el.th("Nivel"),
                    rx.el.th("Acciones"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    State.tests,
                    lambda test: rx.el.tr(
                        rx.el.td(State.get_patient_name.get(test["paciente_CURP"])),
                        rx.el.td(test["tipo_prueba"]),
                        rx.el.td(test["puntaje"]),
                        rx.el.td(test["nivel"]),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("copy"),
                                on_click=lambda: State.toggle_test_modal(test),
                                class_name="text-blue-500",
                            ),
                            rx.el.button(
                                rx.icon("trash-2"),
                                on_click=lambda: State.delete_test(test["id"]),
                                class_name="text-red-500 ml-2",
                            ),
                            rx.el.button(
                                rx.icon("download"), class_name="text-green-500 ml-2"
                            ),
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