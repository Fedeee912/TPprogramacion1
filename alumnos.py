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


def actualizar_alumno(alumnos, padron):
    """Actualiza los datos personales de un alumno existente."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    print("  Deje en blanco para conservar el valor actual.")
    nombre = input(f"  Nombre [{alumno['nombre']}]: ").strip()
    apellido = input(f"  Apellido [{alumno['apellido']}]: ").strip()
    carrera = input(f"  Carrera [{alumno['carrera']}]: ").strip()
    dni = input(f"  DNI [{alumno['dni']}]: ").strip()

    if nombre:
        alumno["nombre"] = nombre
    if apellido:
        alumno["apellido"] = apellido
    if carrera:
        alumno["carrera"] = carrera
    if dni:
        alumno["dni"] = dni

    print("  [OK] Datos del alumno actualizados correctamente.")
    return True


def eliminar_alumno(alumnos, padron):
    """Elimina un alumno de la lista por su padrón."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    alumnos.remove(alumno)
    print(f"  [OK] Alumno con padrón {padron} eliminado correctamente.")
    return True


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

def consultar_notas_alumno(alumnos, padron):
    """Muestra todas las notas de un alumno y su promedio general."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return

    print(f"\n  Notas de {alumno['nombre']} {alumno['apellido']} (Padrón: {padron})")
    print("  " + "-" * 40)

    if not alumno["notas"]:
        print("  Sin calificaciones registradas.")
        return

    for materia, nota in alumno["notas"].items():
        if nota >= NOTA_PROMOCION:
            estado = "Promocionado"
        elif nota >= NOTA_APROBACION:
            estado = "Aprobado"
        else:
            estado = "Desaprobado"
        print(f"  {materia:<30} {nota:>4.1f}  [{estado}]")

    notas = list(alumno["notas"].values())
    promedio = sum(notas) / len(notas)
    print("  " + "-" * 40)
    print(f"  Promedio general: {promedio:.2f}")


def calcular_promedio_alumno(alumno):
    """Devuelve el promedio de notas de un alumno. Retorna 0.0 si no tiene notas."""
    notas = list(alumno["notas"].values())
    if not notas:
        return 0.0
    return sum(notas) / len(notas)

def _pedir_padron():
    """Solicita y valida un número de padrón."""
    padron = input("  Número de padrón: ").strip()
    if not padron.isdigit():
        print("  [ERROR] El padrón debe ser un número entero.")
        return None
    return padron


def _pedir_nota():
    """Solicita y valida una nota."""
    try:
        nota = float(input(f"  Nota ({NOTA_MINIMA}-{NOTA_MAXIMA}): ").strip())
        if not validar_nota(nota):
            print(f"  [ERROR] La nota debe estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")
            return None
        return nota
    except ValueError:
        print("  [ERROR] Ingrese un número válido.")
        return None


def menu_alumnos():
    """Submenú de gestión de alumnos."""
    while True:
        print("\n" + "=" * 45)
        print("         GESTIÓN DE ALUMNOS")
        print("=" * 45)
        print("  1. Crear alumno")
        print("  2. Listar alumnos")
        print("  3. Buscar alumno por padrón")
        print("  4. Actualizar alumno")
        print("  5. Eliminar alumno")
        print("  0. Volver al menú principal")
        print("=" * 45)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            crear_alumno(alumnos)
        elif eleccion == "2":
            listar_alumnos(alumnos)
        elif eleccion == "3":
            padron = _pedir_padron()
            if padron is not None:
                alumno = buscar_alumno(alumnos, padron)
                if alumno:
                    print(f"\n  {alumno['padron']} - {alumno['nombre']} {alumno['apellido']} "
                          f"({alumno['carrera']}) - DNI: {alumno['dni']}")
                else:
                    print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        elif eleccion == "4":
            padron = _pedir_padron()
            if padron is not None:
                actualizar_alumno(alumnos, padron)
        elif eleccion == "5":
            padron = _pedir_padron()
            if padron is not None:
                eliminar_alumno(alumnos, padron)
        elif eleccion == "0":
            break
        else:
            print("  [ERROR] Opción inválida.")


def menu_notas():
    """Submenú de gestión de notas."""
    while True:
        print("\n" + "=" * 45)
        print("          GESTIÓN DE NOTAS")
        print("=" * 45)
        print("  1. Registrar nota")
        print("  2. Modificar nota")
        print("  3. Consultar notas de un alumno")
        print("  0. Volver al menú principal")
        print("=" * 45)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            padron = _pedir_padron()
            if padron is not None:
                materia = input("  Nombre de la materia: ").strip()
                nota = _pedir_nota()
                if nota is not None:
                    registrar_nota(alumnos, padron, materia, nota)
        elif eleccion == "2":
            padron = _pedir_padron()
            if padron is not None:
                materia = input("  Nombre de la materia: ").strip()
                nota = _pedir_nota()
                if nota is not None:
                    modificar_nota(alumnos, padron, materia, nota)
        elif eleccion == "3":
            padron = _pedir_padron()
            if padron is not None:
                consultar_notas_alumno(alumnos, padron)
        elif eleccion == "0":
            break
        else:
            print("  [ERROR] Opción inválida.")


def menu_principal():
    """Menú principal del sistema."""
    while True:
        print("\n" + "=" * 50)
        print("  SISTEMA DE GESTIÓN DE ALUMNOS UNIVERSITARIOS")
        print("=" * 50)
        print("  1. Gestión de alumnos")
        print("  2. Gestión de notas")
        print("  0. Salir")
        print("=" * 50)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            menu_alumnos()
        elif eleccion == "2":
            menu_notas()
        elif eleccion == "0":
            print("\n  Hasta luego.")
            break
        else:
            print("  [ERROR] Opción inválida.")


if __name__ == "__main__":
    menu_principal()
