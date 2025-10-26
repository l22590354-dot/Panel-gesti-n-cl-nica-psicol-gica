import reflex as rx
from app.components.sidebar import base_layout
from app.states.base_state import State, Cita


def calendar_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Gestión de Citas", class_name="text-3xl font-bold text-gray-800"),
            rx.el.div(
                rx.el.button(
                    rx.icon("chevron-left"),
                    on_click=State.prev_week,
                    class_name="p-2 rounded-md hover:bg-gray-100",
                ),
                rx.el.button(
                    rx.icon("chevron-right"),
                    on_click=State.next_week,
                    class_name="p-2 rounded-md hover:bg-gray-100",
                ),
                rx.el.span(
                    State.current_week_display,
                    class_name="text-lg font-semibold text-gray-700",
                ),
                class_name="flex items-center space-x-4",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        appointment_modal(),
    )


def appointment_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                "Crear Cita",
                rx.icon("plus", class_name="ml-2"),
                on_click=lambda: State.toggle_appointment_modal(None),
                class_name="bg-violet-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-violet-700 transition",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Añadir/Editar Cita"),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Paciente"),
                    rx.el.select(
                        rx.el.option("Seleccionar Paciente", value=""),
                        rx.foreach(
                            State.patients,
                            lambda p: rx.el.option(p["nombre"], value=p["CURP"]),
                        ),
                        name="paciente_CURP",
                        default_value=rx.cond(
                            State.editing_appointment,
                            State.editing_appointment["paciente_CURP"],
                            "",
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.label("Psicólogo"),
                    rx.el.select(
                        rx.el.option("Seleccionar Psicólogo", value=""),
                        rx.foreach(
                            State.psychologists,
                            lambda p: rx.el.option(p["nombre"], value=p["RFC"]),
                        ),
                        name="psicologo_RFC",
                        default_value=rx.cond(
                            State.editing_appointment,
                            State.editing_appointment["psicologo_RFC"],
                            "",
                        ),
                        class_name="border rounded p-2 w-full",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("Fecha"),
                            rx.el.input(
                                name="fecha",
                                type="date",
                                default_value=rx.cond(
                                    State.editing_appointment,
                                    State.editing_appointment["fecha"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        rx.el.div(
                            rx.el.label("Hora"),
                            rx.el.input(
                                name="hora",
                                type="time",
                                default_value=rx.cond(
                                    State.editing_appointment,
                                    State.editing_appointment["hora"],
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
                            rx.el.label("Consultorio"),
                            rx.el.input(
                                name="consultorio",
                                default_value=rx.cond(
                                    State.editing_appointment,
                                    State.editing_appointment["consultorio"],
                                    "",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        rx.el.div(
                            rx.el.label("Modalidad"),
                            rx.el.select(
                                rx.el.option("Presencial", value="Presencial"),
                                rx.el.option("En línea", value="En línea"),
                                name="modalidad",
                                default_value=rx.cond(
                                    State.editing_appointment,
                                    State.editing_appointment["modalidad"],
                                    "Presencial",
                                ),
                                class_name="border rounded p-2 w-full",
                            ),
                            class_name="w-1/2",
                        ),
                        class_name="flex space-x-4",
                    ),
                    class_name="flex flex-col space-y-4",
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
                            on_click=lambda: State.toggle_appointment_modal(None),
                            variant="soft",
                        )
                    ),
                    class_name="mt-4 flex justify-end space-x-2",
                ),
                on_submit=State.save_appointment,
            ),
            open=State.show_appointment_modal,
        ),
    )


def time_slot(hour: str, day_date: str) -> rx.Component:
    return rx.el.div(
        class_name="h-16 border-t border-gray-200",
        on_click=lambda: State.create_appointment_at_slot(day_date, f"{hour}:00"),
    )


def day_column(day_info: list[str | int]) -> rx.Component:
    date_str = day_info[3].to(str)
    return rx.el.div(
        rx.el.div(
            rx.el.span(day_info[0], class_name="text-sm font-medium"),
            rx.el.span(
                day_info[1],
                class_name=rx.cond(
                    day_info[2],
                    "flex items-center justify-center h-8 w-8 rounded-full bg-violet-600 text-white font-bold",
                    "flex items-center justify-center h-8 w-8 rounded-full font-bold",
                ),
            ),
            class_name="flex flex-col items-center p-2 sticky top-0 bg-white z-10 border-b",
        ),
        rx.el.div(
            rx.foreach(State.hours, lambda hour: time_slot(hour, date_str)),
            rx.foreach(
                State.appointments,
                lambda appt: rx.cond(
                    appt["fecha"] == date_str, appointment_card(appt), rx.fragment()
                ),
            ),
            class_name="relative",
        ),
        class_name="flex-1 min-w-[14%]",
        style={"min_height": "1500px"},
    )


def appointment_card(appt: Cita) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                State.get_patient_name.get(appt["paciente_CURP"]),
                class_name="font-semibold text-xs",
            ),
            rx.el.p(appt["hora"], class_name="text-xs"),
            class_name="p-1",
        ),
        on_click=lambda: State.toggle_appointment_modal(appt),
        class_name="absolute w-full text-white rounded-lg overflow-hidden cursor-pointer",
        style={
            "top": State.get_appointment_top.get(appt["id"].to_string()),
            "height": "4rem",
            "background_color": State.get_psychologist_color.get(appt["psicologo_RFC"]),
        },
    )


def calendar_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="w-16 sticky left-0 bg-white z-20"),
            rx.el.div(
                rx.foreach(State.week_days, day_column), class_name="flex flex-1"
            ),
            class_name="flex",
        ),
        class_name="flex-1 overflow-auto bg-white border rounded-lg shadow-sm",
        style={"height": "calc(100vh - 200px)"},
    )


def time_labels() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            State.hours,
            lambda hour: rx.el.div(
                rx.el.span(
                    f"{hour}:00",
                    class_name="text-xs text-right text-gray-500 pr-2 -translate-y-2",
                ),
                class_name="h-16",
            ),
        ),
        class_name="w-16 pt-16",
    )


def appointments() -> rx.Component:
    return base_layout(
        rx.el.div(
            calendar_header(),
            rx.el.div(time_labels(), calendar_view(), class_name="flex"),
            rx.cond(
                State.is_loading,
                rx.el.div(
                    rx.spinner(class_name="text-violet-500"),
                    class_name="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center z-30",
                ),
                None,
            ),
        )
    )