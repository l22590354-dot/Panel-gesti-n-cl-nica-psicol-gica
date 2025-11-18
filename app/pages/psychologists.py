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
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    rx.cond(
                        State.editing_psychologist,
                        "Editar Psicólogo",
                        "Añadir Nuevo Psicólogo",
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
                                    "RFC*",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="RFC",
                                    placeholder="XXXXXXXXXXXXX",
                                    default_value=rx.cond(
                                        State.editing_psychologist,
                                        State.editing_psychologist["RFC"],
                                        "",
                                    ),
                                    read_only=State.editing_psychologist.is_not_none(),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                    background_color=rx.cond(
                                        State.editing_psychologist, "#f3f4f6", "white"
                                    ),
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Nombre Completo*",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="nombre",
                                    placeholder="Ej. Mónica García Robles",
                                    default_value=rx.cond(
                                        State.editing_psychologist,
                                        State.editing_psychologist["nombre"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.hr(class_name="my-6 border-gray-200"),
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
                                        State.editing_psychologist,
                                        State.editing_psychologist["telefono"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
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
                                        State.editing_psychologist,
                                        State.editing_psychologist["correo"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        rx.el.hr(class_name="my-6 border-gray-200"),
                        rx.el.h3(
                            "🎓 Información Profesional",
                            class_name="text-lg font-semibold text-violet-700 mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Especialidad",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="especialidad",
                                    placeholder="Ej. Terapia Cognitivo-Conductual",
                                    default_value=rx.cond(
                                        State.editing_psychologist,
                                        State.editing_psychologist["especialidad"],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Cédula Profesional",
                                    class_name="text-sm font-medium text-gray-600",
                                ),
                                rx.el.input(
                                    name="cedula_profesional",
                                    placeholder="Ej. 12345678",
                                    default_value=rx.cond(
                                        State.editing_psychologist,
                                        State.editing_psychologist[
                                            "cedula_profesional"
                                        ],
                                        "",
                                    ),
                                    class_name="w-full px-3 py-2 rounded-lg border-2 border-gray-300 focus:border-violet-500 focus:ring-1 focus:ring-violet-500 transition-shadow",
                                ),
                                class_name="w-full",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        class_name="max-h-[60vh] overflow-y-auto p-1 pr-4",
                    ),
                    rx.el.div(
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Cancelar",
                                type="button",
                                on_click=lambda: State.toggle_psychologist_modal(None),
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
                    on_submit=State.save_psychologist,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-8 w-full max-w-2xl z-50",
            ),
        ),
        open=State.show_psychologist_modal,
        on_open_change=lambda open: State.toggle_psychologist_modal(None),
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
                            rx.el.button(
                                rx.icon("trash-2"),
                                on_click=lambda: State.delete_psychologist(
                                    psych["RFC"]
                                ),
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