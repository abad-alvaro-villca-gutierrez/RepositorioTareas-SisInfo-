import pyodbc

# 1. CONFIGURACIÓN DE LA CONEXIÓN
def conectar():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;" 
            "DATABASE=SistemaTareas;" 
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        print("✅ Conexión exitosa")
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None
# ==========================================
# SECCIÓN: TAREAS (DOCENTE)
# ==========================================

# 2. GUARDAR UNA NUEVA TAREA (Persistencia con Estado)
def guardar_tarea(nombre, descripcion, puntaje, fecha_vencimiento, estado='Borrador'):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        # Aseguramos que los nombres coincidan con tu tabla física
        query = """
            INSERT INTO Tareas (nombre_tarea, descripcion, puntaje, fecha_vencimiento, estado) 
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, descripcion, puntaje, fecha_vencimiento, estado))
        
        conn.commit() # PERSISTENCIA: Guarda los cambios físicamente
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error al guardar la tarea: {e}")
        return False

# 3. OBTENER TODAS LAS TAREAS
def traer_tareas():
    try:
        conn = conectar()
        if conn is None: return []
        
        cursor = conn.cursor()
        # Seleccionamos las columnas que ya verificamos que existen
        query = "SELECT id_tarea, nombre_tarea, descripcion, puntaje, fecha_vencimiento, estado FROM Tareas ORDER BY id_tarea DESC"
        cursor.execute(query)
        
        datos = cursor.fetchall()
        conn.close()
        
        # Convertimos los objetos Row a una lista simple de Python
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al traer tareas: {e}")
        return []

# ==========================================
# SECCIÓN: ENTREGAS (ALUMNO)
# ==========================================

# 4. VERIFICAR SI YA EXISTE UNA ENTREGA
def existe_entrega(id_tarea, id_alumno):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_entrega FROM Entregas WHERE id_tarea = ? AND id_alumno = ?",
            (id_tarea, id_alumno)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado is not None
    except Exception as e:
        print(f"❌ Error al verificar entrega: {e}")
        return False

# 5. GUARDAR O ACTUALIZAR UNA ENTREGA
# 5. GUARDAR O ACTUALIZAR UNA ENTREGA (Actualizado con peso_archivo)
def guardar_entrega(id_tarea, id_alumno, ruta_archivo, peso_decimal):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        
        # Verificamos si ya existe para decidir entre UPDATE o INSERT
        if existe_entrega(id_tarea, id_alumno):
            # Se actualiza la ruta y el nuevo atributo peso_archivo
            query = """
                UPDATE Entregas 
                SET ruta_archivo = ?, peso_archivo = ?, fecha_entrega = GETDATE() 
                WHERE id_tarea = ? AND id_alumno = ?
            """
            cursor.execute(query, (ruta_archivo, peso_decimal, id_tarea, id_alumno))
            mensaje_notificacion = f"Tu entrega de la tarea {id_tarea} ha sido reemplazada y guardada correctamente."
        else:
            # Se inserta la ruta y el peso_archivo por primera vez
            query = """
                INSERT INTO Entregas (id_tarea, id_alumno, ruta_archivo, peso_archivo) 
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (id_tarea, id_alumno, ruta_archivo, peso_decimal))
            mensaje_notificacion = f"Tu entrega de la tarea {id_tarea} se ha registrado correctamente."
            
        conn.commit()
        conn.close()

        # Registrar la notificación del alumno cuando la entrega se guarda correctamente
        try:
            guardar_notificacion_alumno(id_alumno, id_tarea, mensaje_notificacion)
        except Exception as ne:
            print(f"⚠️ No se pudo guardar la notificación del alumno: {ne}")

        return True
    except Exception as e:
        # Este error saldría si los nombres de columnas no coinciden con la BD
        print(f"❌ Error al procesar la entrega en BD: {e}")
        return False


def guardar_notificacion_alumno(id_alumno, id_tarea, mensaje, leida=0):
    try:
        conn = conectar()
        if conn is None: return False

        cursor = conn.cursor()
        query = """
            INSERT INTO Notificaciones (id_alumno, id_tarea, mensaje, fecha_creacion, leida)
            VALUES (?, ?, ?, GETDATE(), ?)
        """
        cursor.execute(query, (id_alumno, id_tarea, mensaje, leida))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error al guardar notificación del alumno: {e}")
        return False


def traer_entregas():
    """Devuelve lista de entregas con columnas básicas.
    Cada entrega es una lista: [id_entrega, id_tarea, id_alumno, ruta_archivo, fecha_entrega]
    """
    try:
        conn = conectar()
        if conn is None:
            return []

        cursor = conn.cursor()
        query = "SELECT id_entrega, id_tarea, id_alumno, ruta_archivo, fecha_entrega FROM Entregas ORDER BY fecha_entrega DESC"
        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()

        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al traer entregas: {e}")
        return []


def calificar_entrega(id_entrega, calificacion, retroalimentacion):
    try:
        conn = conectar()
        if conn is None:
            return False

        cursor = conn.cursor()
        cursor.execute("SELECT id_tarea, id_alumno FROM Entregas WHERE id_entrega = ?", (id_entrega,))
        entrega_info = cursor.fetchone()

        if entrega_info is None:
            print(f"❌ Entrega no encontrada para id_entrega {id_entrega}")
            conn.close()
            return False

        id_tarea, id_alumno = entrega_info

        # Actualizamos el registro de entrega en la BD (T-5.2)
        query = """
            UPDATE Entregas 
            SET calificacion = ?, comentario_docente = ? 
            WHERE id_entrega = ?
        """
        cursor.execute(query, (calificacion, retroalimentacion, id_entrega))

        conn.commit()
        conn.close()

        mensaje_notificacion = f"Tu entrega de la tarea {id_tarea} ha sido calificada con {calificacion} puntos."
        if not guardar_notificacion_alumno(id_alumno, id_tarea, mensaje_notificacion):
            print(f"⚠️ No se pudo guardar la notificación del alumno tras calificar la entrega {id_entrega}")

        return True
    except Exception as e:
        print(f"❌ Error al calificar la entrega: {e}")
        return False   
def obtener_archivo_anterior(id_tarea, id_alumno):
    """Devuelve la ruta del archivo previamente entregado para poder eliminarlo físicamente."""
    try:
        conn = conectar()
        if conn is None: return None
        
        cursor = conn.cursor()
        query = "SELECT ruta_archivo FROM Entregas WHERE id_tarea = ? AND id_alumno = ?"
        cursor.execute(query, (id_tarea, id_alumno))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado and resultado[0]:
            return resultado[0] # Retorna solo el texto de la ruta
        return None
    except Exception as e:
        print(f"❌ Error al obtener archivo anterior: {e}")
        return None
    
# 9. OBTENER PUNTAJE MÁXIMO DE UNA TAREA
def obtener_puntaje_maximo_tarea(id_tarea):
    """Consulta en la base de datos el puntaje máximo asignado a una tarea específica."""
    try:
        conn = conectar()
        if conn is None: return 100 # Valor por defecto seguro si falla la BD
        
        cursor = conn.cursor()
        query = "SELECT puntaje FROM Tareas WHERE id_tarea = ?"
        cursor.execute(query, (id_tarea,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado and resultado[0]:
            return int(resultado[0])
        return 100
    except Exception as e:
        print(f"❌ Error al obtener puntaje de la tarea: {e}")
        return 100

# ==========================================
# SECCIÓN: NOTIFICACIONES (T5.4)
# ==========================================

def traer_notificaciones(id_alumno):
    """Trae todas las notificaciones de un alumno ordenadas por fecha más reciente.
    Devuelve lista: [id_notificacion, id_tarea, mensaje, fecha_creacion, leida]
    """
    try:
        conn = conectar()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        query = """
            SELECT id_notificacion, id_tarea, mensaje, fecha_creacion, leida 
            FROM Notificaciones 
            WHERE id_alumno = ? 
            ORDER BY fecha_creacion DESC
        """
        cursor.execute(query, (id_alumno,))
        datos = cursor.fetchall()
        conn.close()
        
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al traer notificaciones: {e}")
        return []

def marcar_notificacion_leida(id_notificacion):
    """Marca una notificación como leída (leida = 1)."""
    try:
        conn = conectar()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        query = "UPDATE Notificaciones SET leida = 1 WHERE id_notificacion = ?"
        cursor.execute(query, (id_notificacion,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error al marcar notificación como leída: {e}")
        return False

# ==========================================
# SECCIÓN: ALUMNOS (LISTA TAREAS SISTEMA)
# ==========================================

def traer_alumnos():
    """Trae lista de todos los alumnos registrados.
    Devuelve lista: [id_alumno, nombre_alumno]
    """
    try:
        conn = conectar()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        # Ajusta esta consulta según el nombre de tu tabla de alumnos
        query = "SELECT id_alumno, nombre_alumno FROM Alumnos ORDER BY nombre_alumno"
        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()
        
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al traer alumnos: {e}")
        return []

def traer_tareas_pendientes(id_alumno):
    """Trae las tareas que un alumno aún no ha entregado completamente.
    Devuelve lista: [id_tarea, nombre_tarea, descripcion, puntaje, fecha_vencimiento, estado]
    """
    try:
        conn = conectar()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        # Trae tareas publicadas que el alumno no ha entregado o está pendiente de calificación
        query = """
            SELECT t.id_tarea, t.nombre_tarea, t.descripcion, t.puntaje, t.fecha_vencimiento, t.estado
            FROM Tareas t
            WHERE t.estado = 'Publicada'
            AND t.id_tarea NOT IN (
                SELECT DISTINCT e.id_tarea 
                FROM Entregas e 
                WHERE e.id_alumno = ? AND e.calificacion IS NOT NULL
            )
            ORDER BY t.fecha_vencimiento
        """
        cursor.execute(query, (id_alumno,))
        datos = cursor.fetchall()
        conn.close()
        
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al traer tareas pendientes: {e}")
        return []

def verificar_entrega_existente(id_tarea, id_alumno):
    """Alias de existe_entrega para compatibilidad con código existente.
    Verifica si ya existe una entrega para una tarea/alumno específico.
    """
    return existe_entrega(id_tarea, id_alumno)