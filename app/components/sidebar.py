import reflex as rx
from app.states.base_state import State


def sidebar_link(text: str, url: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, size=20),
            rx.el.span(text),
            class_name="flex items-center space-x-3 text-gray-700 hover:text-violet-700 hover:bg-violet-50 rounded-lg px-3 py-2 transition-all duration-150",
        ),
        href=url,
        class_name=rx.cond(
            State.router.page.path == url.lower(),
            "bg-violet-100 text-violet-800 rounded-lg",
            "",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("git-branch-plus", size=32, class_name="text-violet-600"),
                rx.el.h1(
                    "Clínica Psicológica",
                    class_name="text-xl font-bold text-gray-800 font-['Lora']",
                ),
                class_name="flex items-center space-x-2 p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                sidebar_link("Dashboard", "/", "layout-dashboard"),
                sidebar_link("Pacientes", "/patients", "users"),
                sidebar_link("Psicólogos", "/psychologists", "user-plus"),
                sidebar_link("Citas", "/appointments", "calendar"),
                sidebar_link("Pruebas", "/tests", "file-text"),
                class_name="flex flex-col space-y-2 p-4",
            ),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon("log-out", size=20),
                    rx.el.span("Cerrar Sesión"),
                    class_name="flex items-center space-x-3 text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg px-3 py-2 transition-all duration-150",
                ),
                on_click=State.logout,
                href="#",
                class_name="w-full",
            ),
            class_name="p-4 border-t border-gray-200",
        ),
        class_name="flex flex-col h-full bg-white text-gray-800 border-r border-gray-200 transform transition-all duration-300 ease-in-out",
        width=rx.cond(State.sidebar_open, "256px", "0px"),
        opacity=rx.cond(State.sidebar_open, 1, 0),
        padding_x=rx.cond(State.sidebar_open, "0rem", "0rem"),
    )


def main_content(child: rx.Component) -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(State.sidebar_open, "panel-left-close", "panel-left-open")
                ),
                on_click=State.toggle_sidebar,
                class_name="p-2 rounded-md hover:bg-gray-100 text-gray-600",
            ),
            class_name="p-4 bg-white border-b border-gray-200 sticky top-0 z-10",
        ),
        rx.el.div(child, class_name="p-4 md:p-8"),
        class_name="flex-1 bg-gray-50 overflow-y-auto",
        style={"font_family": "Lora, serif"},
    )


def base_layout(child: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        main_content(child),
        class_name="flex h-screen bg-gray-50 font-['Lora']",
    )