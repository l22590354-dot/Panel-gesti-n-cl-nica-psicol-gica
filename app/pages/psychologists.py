import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State, Psicologo


def psychologist_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                "Añadir Psicólogo",
                rx.icon("plus", class_name="ml-2"),
                on_click=lambda: State.toggle_psychologist_modal(None),
                class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Añadir/Editar Psicólogo"),
            rx.el.form(
                rx.el.div(
                    rx.el.label("RFC"),
                    rx.el.input(
                        name="RFC",
                        default_value=rx.cond(
                            State.editing_psychologist,
                            State.editing_psychologist["RFC"],
                            "",
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.label("Nombre"),
                    rx.el.input(
                        name="nombre",
                        default_value=rx.cond(
                            State.editing_psychologist,
                            State.editing_psychologist["nombre"],
                            "",
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    class_name="flex flex-col space-y-2",
                ),
                rx.el.div(
                    rx.el.button(
                        "Guardar",
                        type="submit",
                        class_name="bg-violet-600 text-white py-2 px-4 rounded",
                    ),
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=lambda: State.toggle_psychologist_modal(None),
                            variant="soft",
                        )
                    ),
                    class_name="mt-4 flex justify-end space-x-2",
                ),
            ),
            open=State.show_psychologist_modal,
        ),
    )


def psychologist_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("RFC"),
                    rx.el.th("Nombre"),
                    rx.el.th("Especialidad"),
                    rx.el.th("Cédula"),
                    rx.el.th("Acciones"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    State.psychologists,
                    lambda psych: rx.el.tr(
                        rx.el.td(psych["RFC"]),
                        rx.el.td(psych["nombre"]),
                        rx.el.td(psych["especialidad"]),
                        rx.el.td(psych["cedula_profesional"]),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("copy"),
                                on_click=lambda: State.toggle_psychologist_modal(psych),
                                class_name="text-blue-500",
                            ),
                            rx.el.button(rx.icon("trash-2"), class_name="text-red-500"),
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border",
    )


def psychologists() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Gestión de Psicólogos",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                psychologist_modal(),
                class_name="flex justify-between items-center mb-6",
            ),
            psychologist_table(),
            rx.cond(
                State.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-20",
                ),
            ),
        )
    )