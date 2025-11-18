# Plan de Integración de Base de Datos Clínica

## Fase 1: Configuración de Base de Datos y Modelos ✅
- [x] Crear módulo de configuración de base de datos (`app/db/config.py`)
- [x] Crear modelos SQLAlchemy para todas las tablas existentes (usuario, psicologo, citas, pruebas)
- [x] Crear modelos SQLAlchemy para nuevas tablas (status, familia, usuario_familia, metas)
- [x] Crear modelos SQLAlchemy para tablas de evaluación (antecedentes, evaluaciones, plan_tratamiento, sesiones)
- [x] Crear funciones helper para operaciones CRUD básicas

---

## Fase 2: Migrar CRUD de Entidades Principales a Base de Datos
- [ ] Actualizar State para incluir conexión a base de datos
- [ ] Migrar operaciones de Pacientes (crear, leer, actualizar, eliminar) a usar MySQL
- [ ] Migrar operaciones de Psicólogos (crear, leer, actualizar, eliminar) a usar MySQL
- [ ] Migrar operaciones de Citas (crear, leer, actualizar, eliminar) a usar MySQL con status
- [ ] Migrar operaciones de Pruebas (crear, leer, actualizar, eliminar) a usar MySQL con nuevos campos puntaje/nivel

---

## Fase 3: Implementar Nuevas Funcionalidades - Gestión de Familias y Metas
- [ ] Crear página de gestión de familiares por paciente (`/patients/[CURP]/family`)
- [ ] Implementar CRUD de familiares vinculados a pacientes
- [ ] Crear página de gestión de metas por paciente (`/patients/[CURP]/goals`)
- [ ] Implementar CRUD de metas con estados y fechas

---

## Fase 4: Implementar Módulo de Evaluaciones Clínicas
- [ ] Crear página de antecedentes del paciente (`/patients/[CURP]/background`)
- [ ] Crear formulario para registrar antecedentes familiares, personales, médicos y psicológicos
- [ ] Crear página de evaluaciones (`/patients/[CURP]/evaluations`)
- [ ] Implementar formulario de evaluación (Inicial, Seguimiento, Egreso) con diagnóstico y recomendaciones

---

## Fase 5: Implementar Planes de Tratamiento y Sesiones
- [ ] Crear página de plan de tratamiento (`/patients/[CURP]/treatment-plan`)
- [ ] Implementar formulario de plan con objetivos, técnicas, frecuencia y duración
- [ ] Crear página de registro de sesiones por cita (`/appointments/[id]/session`)
- [ ] Implementar formulario de sesión (tipo, tema, observaciones, avances, tareas)

---

## Fase 6: Actualizar Dashboard y Navegación
- [ ] Actualizar dashboard con estadísticas de base de datos real
- [ ] Agregar navegación a nuevas secciones desde detalles del paciente
- [ ] Agregar indicadores de progreso (metas completadas, sesiones realizadas)
- [ ] Mejorar visualización de calendario con estados de citas desde BD

---

## Fase 7: Testing y Validación Final
- [ ] Probar todas las operaciones CRUD de entidades principales
- [ ] Probar flujo completo de evaluación clínica
- [ ] Verificar integridad referencial de datos
- [ ] Validar UI con datos reales de múltiples pacientes
