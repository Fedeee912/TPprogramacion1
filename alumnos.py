# Constantes de notas
NOTA_MINIMA = 0
NOTA_MAXIMA = 10
NOTA_APROBACION = 4
NOTA_PROMOCION = 7

# Base de datos en memoria
alumnos = []

def crear_alumno(alumnos):
    """Crea un nuevo alumno y lo agrega a la lista de alumnos.

    Recibe la lista de alumnos, pide los datos del alumno y evita
    duplicados por padrón.
    """
    padron = input("Padron: ")
    
    #evitar duplicados
    for a in alumnos:
        if a["padron"] == padron:
            print("Ya existe un alumno con ese padron")
            return

    nombre = input("Nombre: ")
    carrera = input("Carrera: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")    

    alumno = {
        "padron": padron,
        "nombre": nombre,
        "apellido": apellido,
        "carrera": carrera,
        "dni": dni,
        "notas": {}
    }

    alumnos.append(alumno)
    print("Alumno creado correctamente")


def listar_alumnos(alumnos):
    """Muestra en pantalla todos los alumnos almacenados.

    Si la lista está vacía, informa que no hay alumnos cargados.
    """
    if not alumnos:
        print("No hay alumnos cargados")
        return

    for a in alumnos:
        print(f'{a["padron"]} - {a["nombre"]} {a["apellido"]} ({a["carrera"]}) - DNI: {a["dni"]}')


def buscar_alumno(alumnos, padron):
    return next(filter(lambda a: a["padron"] == padron, alumnos), None)

# ---------------------------------------------------------------------------
# GESTIÓN DE NOTAS — Adrián Chiapella
# ---------------------------------------------------------------------------

def validar_nota(nota):
    """Verifica que la nota sea un número entre 0 y 10."""
    try:
        nota_float = float(nota)
        return NOTA_MINIMA <= nota_float <= NOTA_MAXIMA
    except (ValueError, TypeError):
        return False
    
def registrar_nota(alumnos, padron, materia, nota):
    """Registra una calificación para un alumno en una materia.

    No sobreescribe si ya existe una nota; usar modificar_nota() para eso.
    """
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    materia = materia.strip()
    if not materia:
        print("  [ERROR] El nombre de la materia no puede estar vacío.")
        return False

    if not validar_nota(nota):
        print(f"  [ERROR] Nota inválida. Debe ser un número entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")
        return False

    if materia in alumno["notas"]:
        print(f"  [AVISO] Ya existe una nota para '{materia}'. Use 'Modificar nota' para actualizarla.")
        return False

    alumno["notas"][materia] = float(nota)
    print(f"  [OK] Nota {float(nota)} registrada para {alumno['nombre']} {alumno['apellido']} en '{materia}'.")
    return True

def modificar_nota(alumnos, padron, materia, nota_nueva):
    """Actualiza la calificación de un alumno en una materia ya registrada."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    materia = materia.strip()
    if materia not in alumno["notas"]:
        print(f"  [ERROR] No hay nota registrada para '{materia}'.")
        return False

    if not validar_nota(nota_nueva):
        print(f"  [ERROR] Nota inválida. Debe ser un número entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")
        return False

    nota_anterior = alumno["notas"][materia]
    alumno["notas"][materia] = float(nota_nueva)
    print(f"  [OK] Nota actualizada en '{materia}': {nota_anterior} → {float(nota_nueva)}")
    return True