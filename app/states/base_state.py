import reflex as rx
from typing import TypedDict, Optional
import asyncio


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
    editing_patient: Optional[Usuario] = None
    show_psychologist_modal: bool = False
    editing_psychologist: Optional[Psicologo] = None
    show_test_modal: bool = False

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
            }
        ]
        self.appointments = [
            {
                "id": 1,
                "paciente_CURP": "ABC123456",
                "psicologo_RFC": "XYZ987654",
                "fecha": "2024-08-01",
                "hora": "10:00",
                "consultorio": "1",
                "modalidad": "Presencial",
            }
        ]
        self.tests = []
        self.is_loading = False
        return

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def toggle_patient_modal(self, patient: Optional[Usuario]):
        self.show_patient_modal = not self.show_patient_modal
        self.editing_patient = patient

    @rx.event
    def save_patient(self, form_data: dict):
        curp = form_data.get("CURP")
        if self.editing_patient:
            index = next(
                (i for i, p in enumerate(self.patients) if p["CURP"] == curp), None
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
    def toggle_psychologist_modal(self, psychologist: Optional[Psicologo]):
        self.show_psychologist_modal = not self.show_psychologist_modal
        self.editing_psychologist = psychologist

    @rx.event
    def save_psychologist(self, form_data: dict):
        rfc = form_data.get("RFC")
        if self.editing_psychologist:
            index = next(
                (i for i, p in enumerate(self.psychologists) if p["RFC"] == rfc), None
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