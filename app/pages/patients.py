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
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        State.editing_patient,
                        "Editar Paciente",
                        "Añadir Nuevo Paciente",
                    ),
                    class_name="text-2xl font-bold pb-2 mb-4 border-b-2 border-violet-200 text-gray-800 font-['Lora']",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.h3(
                            "📋 Información Personal",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "CURP",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="CURP",
                                    placeholder="XXXXXXXXXXXXXXXXXX",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["CURP"],
                                        "",
                                    ),
                                    read_only=State.editing_patient.is_not_none(),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                    background_color=rx.cond(
                                        State.editing_patient, "#f3f4f6", "white"
                                    ),
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nombre Completo",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="nombre",
                                    placeholder="Ej. Juan Pérez García",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["nombre"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Fecha de Nacimiento",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="fecha_nacimiento",
                                    type="date",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["fecha_nacimiento"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Profesión",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="profesion",
                                    placeholder="Ej. Ingeniero, Estudiante",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["profesion"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.hr(class_name="my-6"),
                        rx.el.h3(
                            "📞 Información de Contacto",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Teléfono",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="telefono",
                                    type="tel",
                                    placeholder="Ej. 4421234567",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["telefono"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Correo Electrónico",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="correo",
                                    type="email",
                                    placeholder="ejemplo@correo.com",
                                    default_value=rx.cond(
                                        State.editing_patient,
                                        State.editing_patient["correo"],
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
                                "Domicilio",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.input(
                                name="domicilio",
                                placeholder="Ej. Av. Siempre Viva 123, Col. Centro",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["domicilio"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.hr(class_name="my-6"),
                        rx.el.h3(
                            "⚕️ Información Médica",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Motivo de Consulta",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.textarea(
                                name="motivo",
                                placeholder="Describe brevemente el motivo de la consulta...",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["motivo"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                rows="2",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Alergias",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.textarea(
                                name="alergias",
                                placeholder="Ej. Penicilina, polen, etc. o 'Ninguna'",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["alergias"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                rows="2",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Medicamentos Actuales",
                                class_name="text-sm font-medium text-gray-600",
                            ),
                            rx.el.textarea(
                                name="medicamento",
                                placeholder="Ej. Paracetamol 500mg, Sertralina 50mg, etc. o 'Ninguno'",
                                default_value=rx.cond(
                                    State.editing_patient,
                                    State.editing_patient["medicamento"],
                                    "",
                                ),
                                class_name="w-full px-3 py-2 rounded-md border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                rows="2",
                            ),
                            class_name="mb-4",
                        ),
                        class_name="max-h-[60vh] overflow-y-auto p-1 pr-4",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancelar",
                                type="button",
                                on_click=lambda: State.toggle_patient_modal(None),
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
                    on_submit=State.save_patient,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-8 w-full max-w-2xl z-50",
            ),
        ),
        open=State.show_patient_modal,
        on_open_change=lambda open: State.toggle_patient_modal(None),
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
                                rx.icon("file_input"),
                                on_click=lambda: rx.redirect(
                                    f"/patients/{patient['CURP']}"
                                ),
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