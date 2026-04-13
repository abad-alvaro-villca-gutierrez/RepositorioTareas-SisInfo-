# Sistema de Gestión Académica - Repositorio de Tareas

## Descripción
Aplicación de escritorio con interfaz Tkinter para gestionar tareas académicas.
Permite a docentes crear tareas y revisar entregas, y a estudiantes ver tareas publicadas y subir entregas digitales.

## Estructura del Proyecto

```
RepositorioTareas-SisInfo-/
├── config/              # Conexión y acceso a la base de datos
├── controllers/         # Validaciones y lógica de negocio
├── models/              # Modelos de datos (pendiente de completar)
├── uploads/             # Archivos subidos por los estudiantes
├── views/               # Interfaz gráfica con Tkinter
│   ├── mainView.py
│   ├── alumnoView.py
│   ├── docenteView.py
│   ├── entregaEstudiante.py
│   ├── formularioTarea.py
│   ├── lista_tareas_sistema.py
│   ├── evaluacionDocente.py
│   └── rounded_button.py
└── main.py              # Entrada principal de la aplicación
```

## Cómo Ejecutar

1. Instala Python 3.14.
2. Instala `pyodbc` y configura un driver compatible con SQL Server.
3. Ajusta los datos de conexión en `config/conexion_bd.py`.
4. Ejecuta:
   ```bash
   python main.py
   ```

## Funcionalidades Actuales

### Docente
- Crear nuevas tareas con título, descripción, puntaje, fecha de vencimiento y estado.
- Ver lista de tareas en un panel docente.
- Abrir ventana de evaluación para calificar entregas.
- Registrar calificaciones y comentarios de docente en la entrega.

### Estudiante
- Ver tareas publicadas en el panel de estudiante.
- Subir archivos de entrega desde un formulario.
- Validar extensiones permitidas y límite de 5 MB.
- Reemplazar entregas existentes cuando se detecta una entrega previa.
- Navegación tipo tarjeta con detalles de tarea.

### Base de datos
- Conexión a SQL Server a través de ODBC.
- Guardado de tareas en la tabla `Tareas`.
- Registro de entregas en la tabla `Entregas`.
- Registro de notificaciones en la tabla `Notificaciones` al calificar entregas.
- Almacenamiento de archivos en la carpeta `uploads/`.
- Recuperación de tareas y entregas para mostrarlas en la interfaz.

## Funcionalidades Pendientes

### Autenticación y usuarios
- Crear sistema de login para docentes y estudiantes.
- Asociar sesiones a usuarios reales en lugar de IDs ingresados manualmente.
- Controlar permisos según el rol (docente vs estudiante).

### Gestión completa de tareas
- Editar tareas existentes desde el panel docente.
- Cambiar estado de las tareas directamente en el listado.
- Filtrar tareas por estado, fecha de vencimiento y puntaje.
- Agregar categorías o asignaturas para organizar tareas.

### Entregas y calificaciones
- Mejorar el seguimiento de entregas por alumno y tarea con estado visible.
- Ofrecer al estudiante una vista de calificaciones recibidas y comentarios del docente.
- Habilitar descarga directa de archivos de entrega desde la interfaz.
- Añadir validaciones adicionales para garantizar integridad de datos en cargas y calificaciones.

### Notificaciones y seguimiento
- Crear una vista para que el alumno vea notificaciones de calificaciones y comentarios.
- Gestionar las notificaciones como leídas/no leídas desde la UI.
- Añadir alertas en la interfaz cuando se generan nuevas notificaciones.

### Modelo de datos y documentación
- Completar `models/` con clases para tareas, entregas, usuarios y notificaciones.
- Documentar las tablas necesarias en la base de datos.
- Añadir scripts de creación de tablas o migraciones.

### Mejoras de interfaz
- Hacer la vista de tareas más responsive para distintos tamaños.
- Añadir vista de detalle de tarea independiente.
- Mejorar el flujo de subida de archivos y mensajes de error.
- Añadir confirmaciones visuales al guardar datos.

### Robustez y validación
- Validar que `id_tarea` e `id_alumno` sean numéricos y válidos.
- Manejar casos de base de datos desconectada o datos incompletos.
- Registrar errores de forma consistente y mostrar mensajes claros.

## Requisitos
- Python 3.14
- Tkinter (incluido en Python)
- `pyodbc`
- SQL Server con base de datos `SistemaTareas`

## Notas
- Los archivos subidos se guardan en `uploads/`.
- Actualmente la autenticación de usuarios no está implementada.
- La conexión de base de datos se configura en `config/conexion_bd.py`.
- `models/` está preparado para ampliarse, pero no contiene lógica completa.
