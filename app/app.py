import reflex as rx
from app.pages.index import index
from app.pages.patients import patients
from app.pages.psychologists import psychologists
from app.pages.appointments import appointments
from app.pages.tests import tests
from app.pages.patient_details import patient_details
from app.pages.login import login_page
from app.states.base_state import State

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="violet"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/login")
app.add_page(index, route="/", on_load=[State.require_login, State.on_load])
app.add_page(patients, route="/patients", on_load=[State.require_login, State.on_load])
app.add_page(
    patient_details,
    route="/patients/[CURP]",
    on_load=[State.require_login, State.get_patient_by_curp],
)
app.add_page(
    psychologists, route="/psychologists", on_load=[State.require_login, State.on_load]
)
app.add_page(
    appointments, route="/appointments", on_load=[State.require_login, State.on_load]
)
app.add_page(tests, route="/tests", on_load=[State.require_login, State.on_load])