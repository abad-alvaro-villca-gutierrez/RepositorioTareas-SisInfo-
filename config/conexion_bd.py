import pyodbc

# 1. CONFIGURACIÓN DE LA CONEXIÓN
def conectar():
    try:
        conn = pyodbc.connect(
          "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;" 
            "DATABASE=SistemaTareas;" 
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
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
        query = """
            INSERT INTO Tareas (nombre_tarea, descripcion, puntaje, fecha_vencimiento, estado) 
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, descripcion, puntaje, fecha_vencimiento, estado))
        
        conn.commit() 
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
        # Se agregaron descripcion y fecha para que no falle la vista
        query = """
            SELECT id_tarea, nombre_tarea, descripcion, puntaje, estado, fecha_vencimiento 
            FROM Tareas 
            ORDER BY id_tarea DESC
        """
        cursor.execute(query)
        
        datos = cursor.fetchall()
        conn.close()
        
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
def guardar_entrega(id_tarea, id_alumno, ruta_archivo, peso_decimal):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        
        if existe_entrega(id_tarea, id_alumno):
            query = """
                UPDATE Entregas 
                SET ruta_archivo = ?, peso_archivo_kb = ?, fecha_entrega = GETDATE() 
                WHERE id_tarea = ? AND id_alumno = ?
            """
            cursor.execute(query, (ruta_archivo, peso_decimal, id_tarea, id_alumno))
        else:
            query = """
                INSERT INTO Entregas (id_tarea, id_alumno, ruta_archivo, peso_archivo_kb, fecha_entrega) 
                VALUES (?, ?, ?, ?, GETDATE())
            """
            cursor.execute(query, (id_tarea, id_alumno, ruta_archivo, peso_decimal))
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error al procesar la entrega en BD: {e}")
        return False

# 6. VERIFICAR ENTREGA EXISTENTE (Conteo)
def verificar_entrega_existente(id_tarea, id_alumno):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM Entregas WHERE id_tarea = ? AND id_alumno = ?"
        cursor.execute(query, (id_tarea, id_alumno))
        
        existe = cursor.fetchone()[0] > 0
        conn.close()
        return existe
    except Exception as e:
        print(f"Error: {e}")
        return False

# 7. OBTENER ALUMNOS QUE ENTREGARON A TIEMPO
def alumnos_entregaron_a_tiempo(id_tarea):
    try:
        conn = conectar()
        if conn is None: return []
        
        cursor = conn.cursor()
        query = """
            SELECT e.id_alumno, e.fecha_entrega, t.fecha_vencimiento
            FROM Entregas e
            JOIN Tareas t ON e.id_tarea = t.id_tarea
            WHERE e.id_tarea = ?
            AND e.fecha_entrega <= t.fecha_vencimiento
            ORDER BY e.fecha_entrega ASC
        """
        cursor.execute(query, (id_tarea,))
        datos = cursor.fetchall()
        conn.close()
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al obtener alumnos a tiempo: {e}")
        return []
    
# 8. OBTENER ARCHIVO ANTERIOR DE UNA ENTREGA
def obtener_archivo_anterior(id_tarea, id_alumno):
    try:
        conn = conectar()
        if conn is None: return None
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ruta_archivo FROM Entregas WHERE id_tarea = ? AND id_alumno = ?",
            (id_tarea, id_alumno)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"❌ Error al obtener archivo anterior: {e}")
        return None

# ==========================================
# SECCIÓN: ALERTAS Y NOTIFICACIONES
# ==========================================

# 9. TRAER TAREAS VENCIDAS (Para alerta del Docente)
def traer_tareas_vencidas():
    """Busca tareas que ya pasaron su fecha de vencimiento y siguen publicadas"""
    try:
        conn = conectar()
        if conn is None: return []
        
        cursor = conn.cursor()
        query = """
            SELECT nombre_tarea, fecha_vencimiento 
            FROM Tareas 
            WHERE fecha_vencimiento < CAST(GETDATE() AS DATE) 
            AND estado = 'Publicada'
        """
        cursor.execute(query)
        
        datos = cursor.fetchall()
        conn.close()
        
        return [list(fila) for fila in datos]
    except Exception as e:
        print(f"❌ Error al buscar tareas vencidas: {e}")
        return []