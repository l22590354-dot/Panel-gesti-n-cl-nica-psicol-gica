import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State


def stat_card(title: str, value: rx.Var[str], icon: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=24, class_name=f"text-{color}-500"),
            class_name=f"p-3 bg-{color}-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-3xl font-bold text-gray-800"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-lg transition-shadow",
    )


def index() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.h1(
                "Dashboard",
                class_name="text-3xl font-bold text-gray-800 mb-6 font-['Lora']",
            ),
            rx.el.div(
                stat_card(
                    "Total Pacientes",
                    State.patients.length().to_string(),
                    "users",
                    "violet",
                ),
                stat_card(
                    "Total Psicólogos",
                    State.psychologists.length().to_string(),
                    "user-plus",
                    "blue",
                ),
                stat_card(
                    "Citas Pendientes",
                    State.appointments.length().to_string(),
                    "calendar-clock",
                    "orange",
                ),
                stat_card(
                    "Pruebas Realizadas",
                    State.tests.length().to_string(),
                    "file-check",
                    "green",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Próximas Citas",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            State.appointments,
                            lambda appt: rx.el.div(
                                rx.el.p(
                                    f"Paciente: {appt['paciente_CURP']}",
                                    class_name="font-semibold",
                                ),
                                rx.el.p(f"Fecha: {appt['fecha']} Hora: {appt['hora']}"),
                                class_name="p-4 border-b border-gray-100",
                            ),
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Pacientes Recientes",
                        class_name="text-xl font-semibold text-gray-700 mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            State.patients,
                            lambda patient: rx.el.div(
                                rx.el.div(
                                    rx.image(
                                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={patient['nombre']}",
                                        class_name="h-10 w-10 rounded-full",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            patient["nombre"],
                                            class_name="font-semibold",
                                        ),
                                        rx.el.p(
                                            patient["CURP"],
                                            class_name="text-sm text-gray-500",
                                        ),
                                    ),
                                ),
                                class_name="flex items-center space-x-4 p-4 border-b border-gray-100",
                            ),
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    class_name="w-full lg:w-1/2",
                ),
                class_name="flex flex-col lg:flex-row gap-8",
            ),
            rx.cond(
                State.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-20",
                ),
            ),
        )
    )