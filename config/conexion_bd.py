import pyodbc

# 1. CONFIGURACIÓN DE LA CONEXIÓN
def conectar():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.\\SQLEXPRESS;" 
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
        query = "SELECT id_tarea, nombre_tarea, puntaje, fecha_vencimiento, estado FROM Tareas ORDER BY id_tarea DESC"
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
        else:
            # Se inserta la ruta y el peso_archivo por primera vez
            query = """
                INSERT INTO Entregas (id_tarea, id_alumno, ruta_archivo, peso_archivo) 
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (id_tarea, id_alumno, ruta_archivo, peso_decimal))
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        # Este error saldría si los nombres de columnas no coinciden con la BD
        print(f"❌ Error al procesar la entrega en BD: {e}")
        return False

        # verificaccion 
    
# Línea 121
def verificar_entrega_existente(id_tarea, id_alumno):
    # Línea 122: AQUÍ DEBE HABER 4 ESPACIOS (o un Tab)
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