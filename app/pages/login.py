import reflex as rx
from app.states.base_state import State


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("git-branch-plus", size=40, class_name="text-violet-600"),
                rx.el.h1(
                    "Clínica Psicológica",
                    class_name="text-2xl font-bold text-gray-800 font-['Lora']",
                ),
                class_name="flex items-center justify-center space-x-3 mb-8",
            ),
            rx.el.h2(
                "Iniciar Sesión",
                class_name="text-2xl font-semibold text-gray-700 text-center mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Usuario", class_name="text-sm font-medium text-gray-600 mb-1"
                    ),
                    rx.el.input(
                        name="username",
                        placeholder="Admin",
                        class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-violet-500 focus:ring-2 focus:ring-violet-200 transition",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Contraseña",
                        class_name="text-sm font-medium text-gray-600 mb-1",
                    ),
                    rx.el.input(
                        name="password",
                        type="password",
                        placeholder="•••••••••",
                        class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-violet-500 focus:ring-2 focus:ring-violet-200 transition",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    State.auth_error != "",
                    rx.el.div(
                        rx.icon(
                            "flag_triangle_right",
                            class_name="h-5 w-5 text-red-500 mr-2",
                        ),
                        rx.el.p(State.auth_error, class_name="text-red-600 text-sm"),
                        class_name="flex items-center bg-red-50 p-3 rounded-lg mb-4",
                    ),
                    None,
                ),
                rx.el.button(
                    "Entrar",
                    type="submit",
                    class_name="w-full bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
                ),
                on_submit=State.login,
                reset_on_submit=True,
            ),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border border-gray-100",
        ),
        class_name="flex min-h-screen w-full items-center justify-center bg-gray-50 font-['Lora']",
    )