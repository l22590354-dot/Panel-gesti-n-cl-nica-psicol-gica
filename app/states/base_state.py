import reflex as rx
from typing import TypedDict
from sqlalchemy import text
import logging


class Status(TypedDict):
    id: int
    estado: str


class Psicologo(TypedDict):
    RFC: str
    nombre: str
    telefono: str | None
    correo: str | None
    especialidad: str | None
    cedula_profesional: str | None


class Usuario(TypedDict):
    CURP: str
    nombre: str
    fecha_nacimiento: str | None
    motivo: str | None
    profesion: str | None
    domicilio: str | None
    telefono: str | None
    correo: str | None
    alergias: str | None
    medicamento: str | None


class Cita(TypedDict):
    id: int
    psicologo_RFC: str
    paciente_CURP: str
    fecha: str
    hora: str
    status_id: int
    notas: str | None


class Prueba(TypedDict):
    id: int
    psicologo_RFC: str
    paciente_CURP: str
    tipo_prueba: str | None
    resultado: str | None
    archivo_adjunto: bytes | None
    notas: str | None


class State(rx.State):
    """The base state for the app."""

    sidebar_open: bool = True
    statuses: list[Status] = []
    psychologists: list[Psicologo] = []
    patients: list[Usuario] = []
    appointments: list[Cita] = []
    tests: list[Prueba] = []
    is_loading: bool = False
    show_patient_modal: bool = False
    show_psychologist_modal: bool = False
    show_test_modal: bool = False
    editing_patient: Usuario | None = None
    editing_psychologist: Psicologo | None = None
    uploaded_files: list[str] = []
    upload_progress: int = 0
    is_uploading: bool = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def on_load(self):
        self.is_loading = True
        return [
            State.get_statuses,
            State.get_psychologists,
            State.get_patients,
            State.get_appointments,
            State.get_tests,
        ]

    @rx.event
    def finish_loading(self):
        self.is_loading = False

    @rx.event(background=True)
    async def get_statuses(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                result = await session.execute(text("SELECT id, estado FROM Status;"))
                statuses = result.fetchall()
                async with self:
                    self.statuses = [{"id": s[0], "estado": s[1]} for s in statuses]
        except Exception as e:
            logging.exception(f"Error fetching statuses: {e}")
            async with self:
                self.statuses = []
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def get_psychologists(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT RFC, nombre, telefono, correo, especialidad, cedula_profesional FROM Psicologo;"
                    )
                )
                psychs = result.fetchall()
                async with self:
                    self.psychologists = [
                        {
                            "RFC": p[0],
                            "nombre": p[1],
                            "telefono": p[2],
                            "correo": p[3],
                            "especialidad": p[4],
                            "cedula_profesional": p[5],
                        }
                        for p in psychs
                    ]
        except Exception as e:
            logging.exception(f"Error fetching psychologists: {e}")
            async with self:
                self.psychologists = []
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def get_patients(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT CURP, nombre, fecha_nacimiento, motivo, profesion, domicilio, telefono, correo, alergias, medicamento FROM Usuario;"
                    )
                )
                patients_data = result.fetchall()
                async with self:
                    self.patients = [
                        {
                            "CURP": p[0],
                            "nombre": p[1],
                            "fecha_nacimiento": str(p[2]) if p[2] else None,
                            "motivo": p[3],
                            "profesion": p[4],
                            "domicilio": p[5],
                            "telefono": p[6],
                            "correo": p[7],
                            "alergias": p[8],
                            "medicamento": p[9],
                        }
                        for p in patients_data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching patients: {e}")
            async with self:
                self.patients = []
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def get_appointments(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, psicologo_RFC, paciente_CURP, fecha, hora, status_id, notas FROM Citas;"
                    )
                )
                appts = result.fetchall()
                async with self:
                    self.appointments = [
                        {
                            "id": a[0],
                            "psicologo_RFC": a[1],
                            "paciente_CURP": a[2],
                            "fecha": str(a[3]),
                            "hora": str(a[4]),
                            "status_id": a[5],
                            "notas": a[6],
                        }
                        for a in appts
                    ]
        except Exception as e:
            logging.exception(f"Error fetching appointments: {e}")
            async with self:
                self.appointments = []
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def get_tests(self):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, psicologo_RFC, paciente_CURP, tipo_prueba, resultado, notas FROM Pruebas;"
                    )
                )
                tests_data = result.fetchall()
                async with self:
                    self.tests = [
                        {
                            "id": t[0],
                            "psicologo_RFC": t[1],
                            "paciente_CURP": t[2],
                            "tipo_prueba": t[3],
                            "resultado": t[4],
                            "archivo_adjunto": None,
                            "notas": t[5],
                        }
                        for t in tests_data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching tests: {e}")
            async with self:
                self.tests = []
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def toggle_patient_modal(self, patient: Usuario | None = None):
        self.show_patient_modal = not self.show_patient_modal
        self.editing_patient = patient
        if not self.show_patient_modal:
            self.editing_patient = None

    @rx.event
    def toggle_psychologist_modal(self, psychologist: Psicologo | None = None):
        self.show_psychologist_modal = not self.show_psychologist_modal
        self.editing_psychologist = psychologist
        if not self.show_psychologist_modal:
            self.editing_psychologist = None

    @rx.event
    def toggle_test_modal(self):
        self.show_test_modal = not self.show_test_modal

    @rx.event(background=True)
    async def save_patient(self, form_data: dict):
        async with self:
            self.is_loading = True
        try:
            curp = form_data.get("CURP")
            if not curp:
                raise ValueError("CURP is required.")
            processed_form_data = {
                k: v if v != "" else None for k, v in form_data.items()
            }
            async with rx.asession() as session:
                async with session.begin():
                    if self.editing_patient:
                        query = text("""UPDATE Usuario SET 
                               nombre = :nombre, fecha_nacimiento = :fecha_nacimiento, motivo = :motivo, 
                               profesion = :profesion, domicilio = :domicilio, telefono = :telefono, 
                               correo = :correo, alergias = :alergias, medicamento = :medicamento
                               WHERE CURP = :CURP;""")
                    else:
                        query = text("""INSERT INTO Usuario (CURP, nombre, fecha_nacimiento, motivo, profesion, domicilio, telefono, correo, alergias, medicamento)
                               VALUES (:CURP, :nombre, :fecha_nacimiento, :motivo, :profesion, :domicilio, :telefono, :correo, :alergias, :medicamento);""")
                    await session.execute(query, processed_form_data)
        except Exception as e:
            logging.exception(f"Error saving patient: {e}")
            yield rx.toast.error(f"Error al guardar paciente: {e}")
        else:
            async with self:
                self.show_patient_modal = False
                self.editing_patient = None
            yield State.get_patients()
            yield rx.toast.success("Paciente guardado exitosamente.")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def delete_patient(self, curp: str):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM Usuario WHERE CURP = :CURP")
                    await session.execute(query, {"CURP": curp})
        except Exception as e:
            logging.exception(f"Error deleting patient: {e}")
            yield rx.toast.error(f"Error al eliminar paciente: {e}")
        else:
            yield State.get_patients()
            yield rx.toast.success("Paciente eliminado exitosamente.")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def save_psychologist(self, form_data: dict):
        async with self:
            self.is_loading = True
        try:
            rfc = form_data.get("RFC")
            if not rfc:
                raise ValueError("RFC is required.")
            processed_form_data = {
                k: v if v != "" else None for k, v in form_data.items()
            }
            async with rx.asession() as session:
                async with session.begin():
                    if self.editing_psychologist:
                        query = text("""UPDATE Psicologo SET 
                               nombre = :nombre, telefono = :telefono, correo = :correo, 
                               especialidad = :especialidad, cedula_profesional = :cedula_profesional
                               WHERE RFC = :RFC;""")
                    else:
                        query = text("""INSERT INTO Psicologo (RFC, nombre, telefono, correo, especialidad, cedula_profesional)
                               VALUES (:RFC, :nombre, :telefono, :correo, :especialidad, :cedula_profesional);""")
                    await session.execute(query, processed_form_data)
        except Exception as e:
            logging.exception(f"Error saving psychologist: {e}")
            yield rx.toast.error(f"Error al guardar psicólogo: {e}")
        else:
            async with self:
                self.show_psychologist_modal = False
                self.editing_psychologist = None
            yield State.get_psychologists()
            yield rx.toast.success("Psicólogo guardado exitosamente.")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def delete_psychologist(self, rfc: str):
        async with self:
            self.is_loading = True
        try:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM Psicologo WHERE RFC = :RFC")
                    await session.execute(query, {"RFC": rfc})
        except Exception as e:
            logging.exception(f"Error deleting psychologist: {e}")
            yield rx.toast.error(f"Error al eliminar psicólogo: {e}")
        else:
            yield State.get_psychologists()
            yield rx.toast.success("Psicólogo eliminado exitosamente.")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        self.upload_progress = 0
        try:
            for i, file in enumerate(files):
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / file.name
                with outfile.open("wb") as f:
                    f.write(upload_data)
                self.uploaded_files.append(file.name)
                self.upload_progress = int((i + 1) / len(files) * 100)
                yield
            yield rx.toast.success(f"Uploaded {len(files)} files.")
        except Exception as e:
            logging.exception(f"Error during upload: {e}")
            yield rx.toast.error("File upload failed.")
        finally:
            self.is_uploading = False
            self.upload_progress = 0