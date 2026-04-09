from datetime import datetime

def validar_tarea(nombre, fecha_vencimiento, puntaje):
    # Criterio de Aceptación: Validación de Integridad
    if not nombre or nombre.strip() == "":
        return False, "El campo 'Título' es obligatorio."
    
    # Criterio de Aceptación: Control de Cronograma
    try:
        fecha_dt = datetime.strptime(fecha_vencimiento, '%Y-%m-%d')
        if fecha_dt.date() < datetime.now().date():
            return False, "La fecha no puede ser anterior a la actual."
    except ValueError:
        return False, "Formato de fecha inválido."

    if int(puntaje) <= 0:
        return False, "El puntaje debe ser mayor a 0."

    return True, "Validación exitosa"