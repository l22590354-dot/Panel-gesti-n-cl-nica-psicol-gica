import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State


def detail_item(label: str, value: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="font-semibold text-gray-500"),
        rx.el.p(value, class_name="text-gray-800"),
        class_name="py-2 border-b",
    )


def patient_details() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.cond(
                State.selected_patient,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/initials/svg?seed={State.selected_patient['nombre']}",
                                class_name="h-24 w-24 rounded-full border-4 border-violet-100",
                            ),
                            rx.el.div(
                                rx.el.h1(
                                    State.selected_patient["nombre"],
                                    class_name="text-3xl font-bold text-gray-800",
                                ),
                                rx.el.p(
                                    State.selected_patient["CURP"],
                                    class_name="text-md text-gray-500",
                                ),
                                class_name="ml-6",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.button(
                            "Editar Paciente",
                            rx.icon("copy", class_name="ml-2"),
                            on_click=lambda: State.toggle_patient_modal(
                                State.selected_patient
                            ),
                            class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
                        ),
                        class_name="flex justify-between items-center mb-8 p-4 bg-white rounded-lg shadow-sm border",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Información Personal",
                            class_name="text-xl font-semibold text-gray-700 mb-4",
                        ),
                        detail_item(
                            "Fecha de Nacimiento",
                            State.selected_patient["fecha_nacimiento"],
                        ),
                        detail_item("Profesión", State.selected_patient["profesion"]),
                        detail_item("Teléfono", State.selected_patient["telefono"]),
                        detail_item(
                            "Correo Electrónico", State.selected_patient["correo"]
                        ),
                        detail_item("Domicilio", State.selected_patient["domicilio"]),
                        class_name="bg-white p-6 rounded-lg shadow-sm border mb-8",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Información Médica",
                            class_name="text-xl font-semibold text-gray-700 mb-4",
                        ),
                        detail_item(
                            "Motivo de Consulta", State.selected_patient["motivo"]
                        ),
                        detail_item("Alergias", State.selected_patient["alergias"]),
                        detail_item(
                            "Medicamento Actual", State.selected_patient["medicamento"]
                        ),
                        class_name="bg-white p-6 rounded-lg shadow-sm border",
                    ),
                ),
                rx.el.div(
                    rx.spinner(),
                    rx.el.p("Cargando detalles del paciente..."),
                    class_name="flex flex-col items-center justify-center h-full",
                ),
            )
        )
    )