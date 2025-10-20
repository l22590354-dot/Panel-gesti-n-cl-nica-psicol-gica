import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State, Usuario


def patient_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                "Añadir Paciente",
                rx.icon("plus", class_name="ml-2"),
                on_click=lambda: State.toggle_patient_modal(None),
                class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Añadir/Editar Paciente"),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("CURP"),
                            rx.el.input(
                                name="CURP",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["CURP"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        rx.el.div(
                            rx.el.label("Nombre"),
                            rx.el.input(
                                name="nombre",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["nombre"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        class_name="flex space-x-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("Fecha de Nacimiento"),
                            rx.el.input(
                                name="fecha_nacimiento",
                                placeholder="YYYY-MM-DD",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["fecha_nacimiento"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        rx.el.div(
                            rx.el.label("Profesión"),
                            rx.el.input(
                                name="profesion",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["profesion"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        class_name="flex space-x-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("Teléfono"),
                            rx.el.input(
                                name="telefono",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["telefono"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        rx.el.div(
                            rx.el.label("Correo Electrónico"),
                            rx.el.input(
                                name="correo",
                                type="email",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["correo"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        class_name="flex space-x-4",
                    ),
                    rx.el.label("Domicilio"),
                    rx.el.input(
                        name="domicilio",
                        default_value=rx.cond(
                            State.editing_patient,
                            State.editing_patient["domicilio"],
                            "",
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.label("Motivo de Consulta"),
                    rx.el.textarea(
                        name="motivo",
                        default_value=rx.cond(
                            State.editing_patient, State.editing_patient["motivo"], ""
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.label("Alergias"),
                    rx.el.input(
                        name="alergias",
                        default_value=rx.cond(
                            State.editing_patient, State.editing_patient["alergias"], ""
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.label("Medicamento Actual"),
                    rx.el.input(
                        name="medicamento",
                        default_value=rx.cond(
                            State.editing_patient,
                            State.editing_patient["medicamento"],
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
                            on_click=lambda: State.toggle_patient_modal(None),
                            variant="soft",
                        )
                    ),
                    class_name="mt-4 flex justify-end space-x-2",
                ),
                on_submit=State.save_patient,
            ),
            open=State.show_patient_modal,
        ),
    )


def patient_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("CURP"),
                    rx.el.th("Nombre"),
                    rx.el.th("Fecha Nac."),
                    rx.el.th("Teléfono"),
                    rx.el.th("Correo"),
                    rx.el.th("Acciones"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    State.patients,
                    lambda patient: rx.el.tr(
                        rx.el.td(patient["CURP"]),
                        rx.el.td(patient["nombre"]),
                        rx.el.td(patient["fecha_nacimiento"]),
                        rx.el.td(patient["telefono"]),
                        rx.el.td(patient["correo"]),
                        rx.el.td(
                            rx.el.button(
                                rx.icon("copy"),
                                on_click=lambda: State.toggle_patient_modal(patient),
                                class_name="text-blue-500",
                            ),
                            rx.el.button(
                                rx.icon("trash-2"),
                                on_click=lambda: State.delete_patient(patient["CURP"]),
                                class_name="text-red-500 ml-2",
                            ),
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="bg-white p-4 rounded-xl shadow-sm border overflow-x-auto",
    )


def patients() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Gestión de Pacientes",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                patient_modal(),
                class_name="flex justify-between items-center mb-6",
            ),
            patient_table(),
            rx.cond(
                State.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-20",
                ),
            ),
        )
    )