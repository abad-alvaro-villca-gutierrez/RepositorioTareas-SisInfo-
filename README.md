# Sistema de Gestión Académica - Repositorio de Tareas

## Descripción
Sistema de gestión de tareas académicas con interfaz gráfica que permite a docentes crear y gestionar tareas, y a estudiantes ver tareas pendientes y subir entregas digitales.

## Estructura del Proyecto

```
RepositorioTareas-SisInfo-/
├── config/              # Configuración de base de datos
├── controllers/         # Lógica de controladores
├── models/             # Modelos de datos
├── uploads/            # Carpeta para archivos subidos
├── views/              # Interfaz gráfica (Tkinter)
│   ├── mainView.py             # Pantalla principal
│   ├── alumnoView.py           # Panel del estudiante
│   ├── docenteView.py          # Panel del docente
│   ├── entregaEstudiante.py    # Formulario de carga de archivos
│   ├── formularioTarea.py      # Formulario para crear tareas
│   ├── lista_tareas_sistema.py # Listado general de tareas
│   └── alerta_subida.py        # Notificaciones
└── main.py            # Archivo principal para ejecutar la aplicación
```

## Cómo Ejecutar

1. Asegúrate de tener Python 3.x instalado
2. Instala las dependencias necesarias (si las hay)
3. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```

## Características Principales

### Panel del Estudiante
- ✅ **Vista de Tareas Pendientes**: Muestra todas las tareas publicadas con:
  - Nombre de la tarea
  - Descripción
  - Fecha de vencimiento
  
- ✅ **Carga de Archivos**: 
  - Seleccionar archivos para entregar
  - Validación de extensiones permitidas: PDF, DOC, DOCX, ZIP, RAR, PNG, JPG
  - Validación de tamaño máximo: 5 MB
  - Muestra información del archivo (nombre y tamaño)
  - Reemplazo automático de entregas existentes

- ✨ **Interfaz Mejorada con Paleta de Colores**:
  - Color principal: Marrón (#6D4145)
  - Colores secundarios: Verde menta (#96D1AA) y Verde oscuro (#555832)
  - Amarillo acentuado (#FFEFAE)
  - Fondo cálido (#FFFBF0)

### Panel del Docente
- Crear nuevas tareas
- Gestionar estados de tareas
- Revisar entregas de estudiantes
- Cambiar estado de entregas (Pendiente, En revisión, Completada)

## Cambios Realizados

### 1. Aplicación de Paleta de Colores
Se implementó una paleta de colores consistente en toda la interfaz:
- **mainView.py**: Actualizado con colores nuevos en botones y encabezados
- **alumnoView.py**: Panel del estudiante con diseño mejorado y colores de la paleta
- **entregaEstudiante.py**: Formulario de carga con interfaz modernizada

### 2. Mejoras en la Vista del Estudiante
- Encabezado destacado con fondo de color marrón
- Información clara sobre límites de archivo y extensiones
- Tarjetas de tareas con mejor espaciado y legibilidad
- Botones con estados visuales (hover effects)

### 3. Validaciones de Seguridad
- ✓ Validación de extensiones de archivo
- ✓ Límite de tamaño de archivo (5 MB)
- ✓ Verificación de entregas duplicadas
- ✓ Manejo de errores y mensajes informativos

### 4. Archivo Principal
Se creó `main.py` como punto de entrada principal de la aplicación para facilitar su ejecución.

## Requisitos
- Python 3.x
- Tkinter (incluido en Python)
- Base de datos SQL configurada en `config/conexion_bd.py`

## Notas para el Usuario
- Los archivos subidos se guardan en la carpeta `/uploads/` con nomenclatura: `tarea_{id}_alumno_{id}_{nombre_archivo}`
- Las entregas se registran automáticamente en la base de datos
- La interfaz es intuitiva y muestra claramente todas las opciones disponibles
- Los mensajes de error le informarán si hay problemas con el archivo seleccionado

## Autor
Desarrollado para Sistemas de Información 2
