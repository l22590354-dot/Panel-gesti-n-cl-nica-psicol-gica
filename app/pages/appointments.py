import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State


def appointments() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.h1(
                "Gestión de Citas", class_name="text-3xl font-bold text-gray-800 mb-6"
            ),
            rx.el.p("Vista de calendario de citas (próximamente)."),
            rx.el.div(
                class_name="bg-white p-4 rounded-xl shadow-sm border h-96 flex items-center justify-center text-gray-400"
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