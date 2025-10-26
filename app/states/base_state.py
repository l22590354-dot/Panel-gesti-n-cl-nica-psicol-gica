import reflex as rx
from typing import TypedDict, Optional
import asyncio
import datetime
import logging


class Usuario(TypedDict):
    CURP: str
    nombre: str
    fecha_nacimiento: str
    profesion: str
    telefono: str
    correo: str
    domicilio: str
    motivo: str
    alergias: str
    medicamento: str


class Psicologo(TypedDict):
    RFC: str
    nombre: str
    especialidad: str
    cedula_profesional: str


class Cita(TypedDict):
    id: int
    paciente_CURP: str
    psicologo_RFC: str
    fecha: str
    hora: str
    consultorio: str
    modalidad: str


class Prueba(TypedDict):
    id: int
    paciente_CURP: str
    psicologo_RFC: str
    tipo_prueba: str
    fecha_aplicacion: str
    resultados: str
    archivo_url: str


class State(rx.State):
    sidebar_open: bool = True
    is_loading: bool = False
    is_uploading: bool = False
    upload_progress: int = 0
    patients: list[Usuario] = []
    psychologists: list[Psicologo] = []
    appointments: list[Cita] = []
    tests: list[Prueba] = []
    show_patient_modal: bool = False
    editing_patient: Usuario | None = None
    show_psychologist_modal: bool = False
    editing_psychologist: Psicologo | None = None
    show_appointment_modal: bool = False
    editing_appointment: Cita | None = None
    show_test_modal: bool = False
    current_date: str = datetime.date.today().isoformat()
    hours: list[str] = [f"{h:02d}" for h in range(8, 22)]

    @rx.var
    def current_week_start(self) -> datetime.date:
        today = datetime.date.fromisoformat(self.current_date)
        return today - datetime.timedelta(days=today.weekday())

    @rx.var
    def current_week_display(self) -> str:
        start = self.current_week_start
        end = start + datetime.timedelta(days=6)
        return f"{start.strftime('%B %d')} - {end.strftime('%d, %Y')}"

    @rx.var
    def week_days(self) -> list[list[str | int | bool]]:
        start_of_week = self.current_week_start
        days = []
        today = datetime.date.today()
        day_names = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
        for i in range(7):
            current_day = start_of_week + datetime.timedelta(days=i)
            days.append(
                [
                    day_names[i],
                    current_day.day,
                    current_day == today,
                    current_day.isoformat(),
                ]
            )
        return days

    @rx.var
    def appointments_for_day(self) -> dict[str, list[Cita]]:
        appointments_by_day = {}
        for appt in self.appointments:
            date_str = appt["fecha"]
            if date_str not in appointments_by_day:
                appointments_by_day[date_str] = []
            appointments_by_day[date_str].append(appt)
        return appointments_by_day

    @rx.var
    def get_appointment_top(self) -> dict[str, str]:
        tops = {}
        for appt in self.appointments:
            time_str = appt["hora"]
            hour = int(time_str.split(":")[0])
            minute = int(time_str.split(":")[1])
            top_pixels = (hour - 8) * 64 + minute / 60 * 64
            tops[str(appt["id"])] = f"{top_pixels}px"
        return tops

    @rx.var
    def get_patient_name(self) -> dict[str, str]:
        return {p["CURP"]: p["nombre"] for p in self.patients}

    @rx.var
    def get_psychologist_color(self) -> dict[str, str]:
        colors = ["#3b82f6", "#ef4444", "#10b981", "#f97316", "#8b5cf6"]
        psych_colors = {}
        for i, psych in enumerate(self.psychologists):
            psych_colors[psych["RFC"]] = colors[i % len(colors)]
        return psych_colors

    @rx.event
    async def on_load(self):
        self.is_loading = True
        await asyncio.sleep(1)
        self.patients = [
            {
                "CURP": "ABC123456",
                "nombre": "Juan Perez",
                "fecha_nacimiento": "1990-01-01",
                "profesion": "Ingeniero",
                "telefono": "5512345678",
                "correo": "juan.perez@email.com",
                "domicilio": "Calle Falsa 123",
                "motivo": "Ansiedad",
                "alergias": "Ninguna",
                "medicamento": "Ninguno",
            }
        ]
        self.psychologists = [
            {
                "RFC": "XYZ987654",
                "nombre": "Dra. Ana Smith",
                "especialidad": "Terapia Cognitivo-Conductual",
                "cedula_profesional": "1234567",
            },
            {
                "RFC": "DEF456789",
                "nombre": "Dr. Carlos Gomez",
                "especialidad": "Psicoanálisis",
                "cedula_profesional": "7654321",
            },
        ]
        self.appointments = [
            {
                "id": 1,
                "paciente_CURP": "ABC123456",
                "psicologo_RFC": "XYZ987654",
                "fecha": datetime.date.today().isoformat(),
                "hora": "10:00",
                "consultorio": "1",
                "modalidad": "Presencial",
            },
            {
                "id": 2,
                "paciente_CURP": "ABC123456",
                "psicologo_RFC": "DEF456789",
                "fecha": (
                    datetime.date.today() + datetime.timedelta(days=1)
                ).isoformat(),
                "hora": "14:30",
                "consultorio": "2",
                "modalidad": "En línea",
            },
        ]
        self.tests = []
        self.is_loading = False
        return

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def prev_week(self):
        current_start = self.current_week_start
        self.current_date = (current_start - datetime.timedelta(days=7)).isoformat()

    @rx.event
    def next_week(self):
        current_start = self.current_week_start
        self.current_date = (current_start + datetime.timedelta(days=7)).isoformat()

    @rx.event
    def toggle_patient_modal(self, patient: Usuario | None):
        self.show_patient_modal = not self.show_patient_modal
        self.editing_patient = patient

    @rx.event
    def save_patient(self, form_data: dict):
        if self.editing_patient:
            index = next(
                (
                    i
                    for i, p in enumerate(self.patients)
                    if p["CURP"] == self.editing_patient["CURP"]
                ),
                None,
            )
            if index is not None:
                self.patients[index] = form_data
        else:
            self.patients.append(form_data)
        self.show_patient_modal = False
        self.editing_patient = None

    @rx.event
    def delete_patient(self, curp: str):
        self.patients = [p for p in self.patients if p["CURP"] != curp]

    @rx.event
    def toggle_psychologist_modal(self, psychologist: Psicologo | None):
        self.show_psychologist_modal = not self.show_psychologist_modal
        self.editing_psychologist = psychologist

    @rx.event
    def save_psychologist(self, form_data: dict):
        if self.editing_psychologist:
            index = next(
                (
                    i
                    for i, p in enumerate(self.psychologists)
                    if p["RFC"] == self.editing_psychologist["RFC"]
                ),
                None,
            )
            if index is not None:
                self.psychologists[index] = form_data
        else:
            self.psychologists.append(form_data)
        self.show_psychologist_modal = False
        self.editing_psychologist = None

    @rx.event
    def delete_psychologist(self, rfc: str):
        self.psychologists = [p for p in self.psychologists if p["RFC"] != rfc]

    @rx.event
    def toggle_appointment_modal(self, appointment: Cita | None):
        self.show_appointment_modal = not self.show_appointment_modal
        self.editing_appointment = appointment

    @rx.event
    def save_appointment(self, form_data: dict):
        if self.editing_appointment:
            index = next(
                (
                    i
                    for i, a in enumerate(self.appointments)
                    if a["id"] == self.editing_appointment["id"]
                ),
                None,
            )
            if index is not None:
                self.appointments[index].update(form_data)
        else:
            new_id = max([a["id"] for a in self.appointments] + [0]) + 1
            new_appointment = {**form_data, "id": new_id}
            self.appointments.append(new_appointment)
        self.show_appointment_modal = False
        self.editing_appointment = None

    @rx.event
    def create_appointment_at_slot(self, date: str, time: str):
        self.editing_appointment = Cita(
            id=0,
            paciente_CURP="",
            psicologo_RFC="",
            fecha=date,
            hora=time,
            consultorio="",
            modalidad="Presencial",
        )
        self.show_appointment_modal = True

    @rx.event
    def toggle_test_modal(self):
        self.show_test_modal = not self.show_test_modal

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        for i, file in enumerate(files):
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.upload_progress = int((i + 1) / len(files) * 100)
            yield
        self.is_uploading = False
        self.upload_progress = 0
        yield rx.clear_selected_files("upload_test")
        return