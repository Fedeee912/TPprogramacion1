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
    for a in alumnos:
        if a["padron"] == padron:
            return a
    return None

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