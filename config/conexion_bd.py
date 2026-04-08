import pyodbc

# 1. CONFIGURACIÓN DE LA CONEXIÓN
def conectar():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;" 
            "DATABASE=SistemaTareas;" # Asegúrate de que tu BD se llame así en SQL Server
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# ==========================================
# SECCIÓN: TAREAS (DOCENTE)
# ==========================================

# 2. GUARDAR UNA NUEVA TAREA (US-1)
def guardar_tarea(nombre, descripcion, puntaje, fecha_vencimiento, estado='Borrador'):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO Tareas (nombre_tarea, descripcion, puntaje, fecha_vencimiento, estado) 
               VALUES (?, ?, ?, ?, ?)""",
            (nombre, descripcion, puntaje, fecha_vencimiento, estado)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al guardar la tarea: {e}")
        return False

# 3. OBTENER TODAS LAS TAREAS (Para mostrarlas en una tabla)
def traer_tareas():
    try:
        conn = conectar()
        if conn is None: return []
        
        cursor = conn.cursor()
        # Traemos los datos más importantes para la interfaz
        cursor.execute("SELECT id_tarea, nombre_tarea, puntaje, fecha_vencimiento, estado FROM Tareas ORDER BY fecha_vencimiento ASC")
        datos = cursor.fetchall()
        conn.close()
        
        resultado = []
        for fila in datos:
            resultado.append([fila[0], fila[1], fila[2], fila[3], fila[4]])
        return resultado
    except Exception as e:
        print(f"Error al traer tareas: {e}")
        return []

# ==========================================
# SECCIÓN: ENTREGAS (ALUMNO)
# ==========================================

# 4. VERIFICAR SI YA EXISTE UNA ENTREGA (US-3: Para no duplicar)
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
    except:
        return False

# 5. GUARDAR O ACTUALIZAR UNA ENTREGA (US-2 y US-3)
def guardar_entrega(id_tarea, id_alumno, ruta_archivo, peso_kb):
    try:
        conn = conectar()
        if conn is None: return False
        
        cursor = conn.cursor()
        
        # Si ya existe, la actualizamos (Gestión de Versiones)
        if existe_entrega(id_tarea, id_alumno):
            cursor.execute(
                """UPDATE Entregas 
                   SET ruta_archivo = ?, peso_archivo_kb = ?, fecha_entrega = GETDATE() 
                   WHERE id_tarea = ? AND id_alumno = ?""",
                (ruta_archivo, peso_kb, id_tarea, id_alumno)
            )
        # Si no existe, la insertamos como nueva
        else:
            cursor.execute(
                """INSERT INTO Entregas (id_tarea, id_alumno, ruta_archivo, peso_archivo_kb) 
                   VALUES (?, ?, ?, ?)""",
                (id_tarea, id_alumno, ruta_archivo, peso_kb)
            )
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al procesar la entrega: {e}")
        return False