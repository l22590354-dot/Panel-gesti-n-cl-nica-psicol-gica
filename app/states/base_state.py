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
    telefono: str
    correo: str
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
    is_authenticated: bool = False
    auth_error: str = ""
    is_loading: bool = False
    is_uploading: bool = False
    upload_progress: int = 0
    patients: list[Usuario] = []
    psychologists: list[Psicologo] = []
    appointments: list[Cita] = []
    tests: list[Prueba] = []
    show_patient_modal: bool = False
    editing_patient: Usuario | None = None
    selected_patient: Usuario | None = None
    show_psychologist_modal: bool = False
    editing_psychologist: Psicologo | None = None
    show_appointment_modal: bool = False
    editing_appointment: Cita | None = None
    show_view_appointment_modal: bool = False
    viewing_appointment: Cita | None = None
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
    def get_psychologist_name(self) -> dict[str, str]:
        return {p["RFC"]: p["nombre"] for p in self.psychologists}

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
                "CURP": "PERJ990115HDFRPA01",
                "nombre": "Jorge Pérez Rojas",
                "fecha_nacimiento": "1999-01-15",
                "motivo": "Ansiedad y estrés laboral",
                "profesion": "Ingeniero de Software",
                "domicilio": "Av. de los Árboles 123, Col. Centro",
                "telefono": "4421234567",
                "correo": "jorge.perez@email.com",
                "alergias": "Ninguna",
                "medicamento": "Ninguno",
            },
            {
                "CURP": "GOMG010320MDFRPA02",
                "nombre": "Marisol Gómez Cruz",
                "fecha_nacimiento": "2001-03-20",
                "motivo": "Problemas de autoestima",
                "profesion": "Estudiante",
                "domicilio": "Calle de la Luna 45, Col. Sol",
                "telefono": "4422345678",
                "correo": "marisol.gomez@email.com",
                "alergias": "Penicilina",
                "medicamento": "Loratadina ocasional",
            },
            {
                "CURP": "SMLU880710HDFRPA03",
                "nombre": "Luis Sánchez Morales",
                "fecha_nacimiento": "1988-07-10",
                "motivo": "Depresión y falta de motivación",
                "profesion": "Contador",
                "domicilio": "Privada del Sol 8, Col. Jardines",
                "telefono": "4423456789",
                "correo": "luis.sanchez@email.com",
                "alergias": "Polvo",
                "medicamento": "Sertralina",
            },
            {
                "CURP": "RAMA951105MDFRPA04",
                "nombre": "Ana Ramírez Mendoza",
                "fecha_nacimiento": "1995-11-05",
                "motivo": "Manejo de la ira",
                "profesion": "Diseñadora Gráfica",
                "domicilio": "Paseo de las Flores 789, Col. Rosales",
                "telefono": "4424567890",
                "correo": "ana.ramirez@email.com",
                "alergias": "Ninguna",
                "medicamento": "Ninguno",
            },
            {
                "CURP": "VAFL920925HDFRPA05",
                "nombre": "Fernando Vargas Flores",
                "fecha_nacimiento": "1992-09-25",
                "motivo": "Terapia de seguimiento",
                "profesion": "Abogado",
                "domicilio": "Boulevard Principal 101, Col. las Fuentes",
                "telefono": "4425678901",
                "correo": "fernando.vargas@email.com",
                "alergias": "Mariscos",
                "medicamento": "Ninguno",
            },
        ]
        self.psychologists = [
            {
                "RFC": "GARM850101ABC",
                "nombre": "Mónica García Robles",
                "telefono": "4421112233",
                "correo": "monica.garcia@clinicapsi.com",
                "especialidad": "Terapia Cognitivo-Conductual",
                "cedula_profesional": "87654321",
            },
            {
                "RFC": "LOPE900202DEF",
                "nombre": "Juan López Castillo",
                "telefono": "4422223344",
                "correo": "juan.lopez@clinicapsi.com",
                "especialidad": "Psicología Infantil",
                "cedula_profesional": "87654322",
            },
            {
                "RFC": "MART780303GHI",
                "nombre": "Laura Martínez Soto",
                "telefono": "4423334455",
                "correo": "laura.martinez@clinicapsi.com",
                "especialidad": "Terapia de Pareja",
                "cedula_profesional": "87654323",
            },
            {
                "RFC": "RODR820404JKL",
                "nombre": "Carlos Rodríguez Peña",
                "telefono": "4424445566",
                "correo": "carlos.rodriguez@clinicapsi.com",
                "especialidad": "Psicoanálisis",
                "cedula_profesional": "87654324",
            },
            {
                "RFC": "FERN950505MNO",
                "nombre": "Ana Fernández Luna",
                "telefono": "4425556677",
                "correo": "ana.fernandez@clinicapsi.com",
                "especialidad": "Neuropsicología",
                "cedula_profesional": "87654325",
            },
        ]
        self.appointments = [
            {
                "id": 1,
                "paciente_CURP": "PERJ990115HDFRPA01",
                "psicologo_RFC": "GARM850101ABC",
                "fecha": "2025-10-20",
                "hora": "10:00",
                "consultorio": "1",
                "modalidad": "Presencial",
            },
            {
                "id": 2,
                "paciente_CURP": "SMLU880710HDFRPA03",
                "psicologo_RFC": "MART780303GHI",
                "fecha": "2025-10-21",
                "hora": "12:30",
                "consultorio": "2",
                "modalidad": "En línea",
            },
            {
                "id": 3,
                "paciente_CURP": "GOMG010320MDFRPA02",
                "psicologo_RFC": "LOPE900202DEF",
                "fecha": "2025-10-15",
                "hora": "16:00",
                "consultorio": "3",
                "modalidad": "Presencial",
            },
            {
                "id": 4,
                "paciente_CURP": "RAMA951105MDFRPA04",
                "psicologo_RFC": "RODR820404JKL",
                "fecha": "2025-10-10",
                "hora": "09:00",
                "consultorio": "4",
                "modalidad": "Presencial",
            },
            {
                "id": 5,
                "paciente_CURP": "VAFL920925HDFRPA05",
                "psicologo_RFC": "GARM850101ABC",
                "fecha": "2025-10-22",
                "hora": "11:00",
                "consultorio": "1",
                "modalidad": "En línea",
            },
        ]
        self.tests = [
            {
                "id": 1,
                "paciente_CURP": "PERJ990115HDFRPA01",
                "psicologo_RFC": "GARM850101ABC",
                "tipo_prueba": "Inventario de Ansiedad de Beck (BAI)",
                "fecha_aplicacion": "2025-10-20",
                "resultados": "Nivel de ansiedad moderado, puntaje de 24.",
                "archivo_url": "",
            },
            {
                "id": 2,
                "paciente_CURP": "GOMG010320MDFRPA02",
                "psicologo_RFC": "LOPE900202DEF",
                "tipo_prueba": "Escala de Autoestima de Rosenberg",
                "fecha_aplicacion": "2025-10-15",
                "resultados": "Nivel de autoestima bajo, puntaje de 18.",
                "archivo_url": "",
            },
            {
                "id": 3,
                "paciente_CURP": "SMLU880710HDFRPA03",
                "psicologo_RFC": "MART780303GHI",
                "tipo_prueba": "Inventario de Depresión de Beck (BDI)",
                "fecha_aplicacion": "2025-10-21",
                "resultados": "Síntomas de depresión severa, puntaje de 35.",
                "archivo_url": "",
            },
            {
                "id": 4,
                "paciente_CURP": "RAMA951105MDFRPA04",
                "psicologo_RFC": "RODR820404JKL",
                "tipo_prueba": "Cuestionario de Agresión (AQ)",
                "fecha_aplicacion": "2025-10-10",
                "resultados": "Puntuaciones altas en la subescala de ira.",
                "archivo_url": "",
            },
            {
                "id": 5,
                "paciente_CURP": "VAFL920925HDFRPA05",
                "psicologo_RFC": "FERN950505MNO",
                "tipo_prueba": "Test de inteligencia de Wechsler para adultos (WAIS)",
                "fecha_aplicacion": "2025-10-22",
                "resultados": "CI de 115, en el rango promedio-alto.",
                "archivo_url": "",
            },
        ]
        self.is_loading = False
        return

    @rx.event
    def login(self, form_data: dict):
        username = form_data.get("username")
        password = form_data.get("password")
        if username == "Admin" and password == "123456789":
            self.is_authenticated = True
            self.auth_error = ""
            return rx.redirect("/")
        else:
            self.auth_error = "Usuario o contraseña incorrectos."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        return rx.redirect("/login")

    @rx.event
    def require_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

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
    async def get_patient_by_curp(self):
        if not self.patients:
            await self.on_load()
        curp = self.router.page.params.get("CURP", "")
        self.selected_patient = next(
            (p for p in self.patients if p["CURP"] == curp), None
        )
        self.is_loading = False
        return

    @rx.event
    def view_appointment_details(self, appointment: Cita | None):
        self.show_view_appointment_modal = appointment is not None
        self.viewing_appointment = appointment

    @rx.event
    def toggle_appointment_modal(self, appointment: Cita | None, edit_mode: bool):
        self.show_appointment_modal = edit_mode
        self.editing_appointment = appointment
        if edit_mode:
            self.show_view_appointment_modal = False

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