import re
import json
import os

# Ruta del archivo de datos (queda al lado de alumnos.py)
ARCHIVO_DATOS = os.path.join(os.path.dirname(__file__), "datos_alumnos.json")

# Constantes de notas
NOTA_MINIMA = 0
NOTA_MAXIMA = 10
NOTA_APROBACION = 4
NOTA_PROMOCION = 7

# Base de datos en memoria
alumnos = []
padrones = set()
materias = []

def crear_alumno(alumnos):
    """Crea un nuevo alumno y lo agrega a la lista de alumnos.

    Recibe la lista de alumnos, pide los datos del alumno y evita
    duplicados por padrón.
    """
    padron = input("Padron: ").strip()

    if padron in padrones:
        print("Ya existe un alumno con ese padron")
        return

    nombre = input("Nombre: ")
    carrera = input("Carrera: ")
    apellido = input("Apellido: ")
    dni = input("DNI: ")

    email = input("Email: ").strip()
    while not re.search(r'^[\w.+-]+@[\w.-]+\.\w+$', email):
        print("  [ERROR] Email inválido. Ejemplo: juan@universidad.edu")
        email = input("Email: ").strip()

    alumno = {
        "padron": padron,
        "nombre": nombre,
        "apellido": apellido,
        "carrera": carrera,
        "dni": dni,
        "email": email,
        "estado": "Activo",
        "notas": {}
    }

    alumnos.append(alumno)
    padrones.add(padron)
    guardar_datos(alumnos, materias)
    print("Alumno creado correctamente")


def listar_alumnos(alumnos):
    """Muestra en pantalla todos los alumnos almacenados.

    Si la lista está vacía, informa que no hay alumnos cargados.
    """
    if not alumnos:
        print("No hay alumnos cargados")
        return

    for a in alumnos:
        resumen = alumno_a_tupla(a)
        print(f'{resumen[0]} - {resumen[1]} {resumen[2]} ({resumen[3]}) - DNI: {resumen[4]} - {resumen[5]} [{resumen[6]}]')


def buscar_alumno(alumnos, padron):
    resultado = list(filter(lambda a: a["padron"] == padron, alumnos))
    return resultado[0] if resultado else None


def alumno_a_tupla(alumno):
    """Devuelve una tupla del alumno.

    Formato: (padron, nombre, apellido, carrera, dni)
    """
    return (alumno["padron"], alumno["nombre"], alumno["apellido"], alumno["carrera"], alumno["dni"], alumno.get("email", ""), alumno.get("estado", "Activo"))


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
    email = input(f"  Email [{alumno.get('email', '')}]: ").strip()
    estado = input(f"  Estado [{alumno.get('estado', 'Activo')}] (Activo/Inactivo/Egresado): ").strip()

    if nombre:
        alumno["nombre"] = nombre
    if apellido:
        alumno["apellido"] = apellido
    if carrera:
        alumno["carrera"] = carrera
    if dni:
        alumno["dni"] = dni
    if email:
        if re.search(r'^[\w.+-]+@[\w.-]+\.\w+$', email):
            alumno["email"] = email
        else:
            print("  [AVISO] Email inválido, se conserva el anterior.")
    if estado in ("Activo", "Inactivo", "Egresado"):
        alumno["estado"] = estado
    elif estado:
        print("  [AVISO] Estado inválido, se conserva el anterior.")

    guardar_datos(alumnos, materias)
    print("  [OK] Datos del alumno actualizados correctamente.")
    return True


def eliminar_alumno(alumnos, padron):
    """Elimina un alumno de la lista por su padrón."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    alumnos[:] = [a for a in alumnos if a["padron"] != padron]
    padrones.discard(padron)
    guardar_datos(alumnos, materias)
    print(f"  [OK] Alumno con padrón {padron} eliminado correctamente.")
    return True



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
    guardar_datos(alumnos, materias)
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
    guardar_datos(alumnos, materias)
    print(f"  [OK] Nota actualizada en '{materia}': {nota_anterior} → {float(nota_nueva)}")
    return True

def eliminar_nota(alumnos, padron, materia):
    """Elimina la calificación de un alumno en una materia registrada."""
    alumno = buscar_alumno(alumnos, padron)
    if alumno is None:
        print(f"  [ERROR] No se encontró ningún alumno con padrón {padron}.")
        return False

    materia = materia.strip()
    if materia not in alumno["notas"]:
        print(f"  [ERROR] No hay nota registrada para '{materia}'.")
        return False

    nota_eliminada = alumno["notas"].pop(materia)
    guardar_datos(alumnos, materias)
    print(f"  [OK] Nota {nota_eliminada} de '{materia}' eliminada para {alumno['nombre']} {alumno['apellido']}.")
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

def sumaRecursiva (lista):
    """Suma todos los elementos de una lista utilizando recursividad"""
    if len(lista)==1:
        return lista[0]
    return lista[0]+sumaRecursiva(lista[1:])

def calcular_promedio_alumno(alumno):
    """Devuelve el promedio de notas de un alumno. Retorna 0.0 si no tiene notas."""
    notas = list(alumno["notas"].values())
    if not notas:
        return 0.0
    return sum(notas) / len(notas)


def calcular_promedio_materia(alumnos, materia):
    """Calcula el promedio general de una materia entre todos los alumnos que la tienen registrada."""
    notas = [a["notas"][materia] for a in alumnos if materia in a["notas"]]
    if not notas:
        return None
    return sum(notas) / len(notas)

def listar_alumnos_por_materia(alumnos, materia):
    """Muestra todos los alumnos que tienen nota en una materia, con su estado y el promedio general."""
    encontrados = [(a, a["notas"][materia]) for a in alumnos if materia in a["notas"]]

    if not encontrados:
        print(f"  [INFO] Ningún alumno tiene nota registrada para '{materia}'.")
        return

    print(f"\n  Alumnos en '{materia}'")
    print("  " + "-" * 50)

    for alumno, nota in encontrados:
        if nota >= NOTA_PROMOCION:
            estado = "Promocionado"
        elif nota >= NOTA_APROBACION:
            estado = "Aprobado"
        else:
            estado = "Desaprobado"
        print(f"  {alumno['padron']} - {alumno['nombre']} {alumno['apellido']:<20} {nota:>4.1f}  [{estado}]")

    promedio = sum(n for _, n in encontrados) / len(encontrados)
    print("  " + "-" * 50)
    print(f"  Promedio de la materia: {promedio:.2f}  ({len(encontrados)} alumno{'s' if len(encontrados) != 1 else ''})")



def clasificar_estado(nota):
    """Devuelve el estado académico según la nota: Promocionado, Aprobado o Desaprobado."""
    if nota >= NOTA_PROMOCION:
        return "Promocionado"
    elif nota >= NOTA_APROBACION:
        return "Aprobado"
    return "Desaprobado"


def obtener_materias(alumnos):
    """Devuelve un conjunto con todas las materias que tienen al menos una nota registrada."""
    materias = set()
    for a in alumnos:
        for materia in a["notas"].keys():
            materias.add(materia)
    return materias


def estadisticas_materia(alumnos, materia):
    """Calcula estadísticas de una materia: total de alumnos con nota, aprobados,
    desaprobados, promocionados, promedio y tasa de promoción.

    Devuelve un diccionario con los resultados, o None si nadie tiene nota en esa materia.
    """
    notas = [a["notas"][materia] for a in alumnos if materia in a["notas"]]
    if not notas:
        return None

    total = len(notas)
    promocionados = sum(1 for n in notas if n >= NOTA_PROMOCION)
    aprobados = sum(1 for n in notas if NOTA_APROBACION <= n < NOTA_PROMOCION)
    desaprobados = sum(1 for n in notas if n < NOTA_APROBACION)

    return {
        "materia": materia,
        "total": total,
        "promocionados": promocionados,
        "aprobados": aprobados,
        "desaprobados": desaprobados,
        "promedio": sum(notas) / total,
        "tasa_promocion": promocionados / total * 100,
    }


def mostrar_estadisticas_materia(alumnos, materia):
    """Muestra por pantalla las estadísticas de una materia."""
    est = estadisticas_materia(alumnos, materia)
    if est is None:
        print(f"  [INFO] Ningún alumno tiene nota registrada para '{materia}'.")
        return

    print(f"\n  Estadísticas de '{est['materia']}'")
    print("  " + "-" * 50)
    print(f"  Alumnos con nota:       {est['total']}")
    print(f"  Promocionados (>= {NOTA_PROMOCION}):   {est['promocionados']}")
    print(f"  Aprobados ({NOTA_APROBACION} a <{NOTA_PROMOCION}):     {est['aprobados']}")
    print(f"  Desaprobados (< {NOTA_APROBACION}):     {est['desaprobados']}")
    print("  " + "-" * 50)
    print(f"  Promedio de la clase:   {est['promedio']:.2f}")
    print(f"  Tasa de promoción:      {est['tasa_promocion']:.1f}%")


def reporte_promociones_desaprobaciones(alumnos):
    """Muestra, para cada materia registrada, cuántos alumnos promocionaron y cuántos desaprobaron."""
    materias = obtener_materias(alumnos)
    if not materias:
        print("  [INFO] No hay notas registradas en el sistema.")
        return

    print("\n  Promociones y desaprobaciones por materia")
    print("  " + "-" * 58)
    print(f"  {'Materia':<30}{'Promocion.':>12}{'Desaprob.':>12}")
    print("  " + "-" * 58)

    for materia in sorted(materias):
        est = estadisticas_materia(alumnos, materia)
        print(f"  {materia:<30}{est['promocionados']:>12}{est['desaprobados']:>12}")


def reporte_por_carrera(alumnos):
    """Muestra el desempeño por carrera: cantidad de alumnos y promedio general de notas."""
    carreras = {a["carrera"] for a in alumnos}
    if not carreras:
        print("  [INFO] No hay alumnos registrados.")
        return

    print("\n  Reporte por carrera")
    print("  " + "-" * 55)
    print(f"  {'Carrera':<30}{'Alumnos':>10}{'Promedio':>12}")
    print("  " + "-" * 55)

    for carrera in sorted(carreras):
        alumnos_carrera = [a for a in alumnos if a["carrera"] == carrera]
        notas = [n for a in alumnos_carrera for n in a["notas"].values()]
        promedio = sum(notas) / len(notas) if notas else 0.0
        print(f"  {carrera:<30}{len(alumnos_carrera):>10}{promedio:>12.2f}")


def resumen_ejecutivo(alumnos):
    """Muestra un resumen general: totales de alumnos, materias, notas y tasa de promoción global."""
    if not alumnos:
        print("  [INFO] No hay alumnos registrados.")
        return

    materias = obtener_materias(alumnos)
    todas_las_notas = [n for a in alumnos for n in a["notas"].values()]

    print("\n  Resumen ejecutivo")
    print("  " + "=" * 45)
    print(f"  Total de alumnos:   {len(alumnos)}")
    print(f"  Total de materias:  {len(materias)}")
    print(f"  Total de notas:     {len(todas_las_notas)}")

    if todas_las_notas:
        promocionados = sum(1 for n in todas_las_notas if n >= NOTA_PROMOCION)
        promedio = sum(todas_las_notas) / len(todas_las_notas)
        print(f"  Promedio general:   {promedio:.2f}")
        print(f"  Tasa de promoción:  {promocionados / len(todas_las_notas) * 100:.1f}%")
    else:
        print("  Sin notas registradas todavía.")
    print("  " + "=" * 45)


def registrar_materia(materias):
    """Registra una nueva materia en la lista de materias."""
    nombre = input("  Nombre de la materia: ").strip()
    if not nombre:
        print("  [ERROR] El nombre no puede estar vacío.")
        return
    if list(filter(lambda m: m["nombre"].lower() == nombre.lower(), materias)):
        print("  [AVISO] Ya existe una materia con ese nombre.")
        return
    codigo = input("  Código (ej: PROG-001): ").strip()
    try:
        semestre = int(input("  Semestre (número): ").strip())
    except ValueError:
        print("  [ERROR] El semestre debe ser un número entero.")
        return
    materias.append({"nombre": nombre, "codigo": codigo, "semestre": semestre})
    guardar_datos(alumnos, materias)
    print(f"  [OK] Materia '{nombre}' registrada correctamente.")


def listar_materias(materias):
    """Muestra todas las materias registradas."""
    if not materias:
        print("  No hay materias registradas.")
        return
    print(f"\n  {'Nombre':<30}{'Código':<15}{'Semestre':>10}")
    print("  " + "-" * 55)
    for m in sorted(materias, key=lambda x: x["semestre"]):
        print(f"  {m['nombre']:<30}{m['codigo']:<15}{m['semestre']:>10}")


def reporte_por_semestre(alumnos, materias, semestre):
    """Muestra estadísticas de todas las materias de un semestre dado."""
    materias_semestre = [m["nombre"] for m in materias if m["semestre"] == semestre]
    if not materias_semestre:
        print(f"  [INFO] No hay materias registradas para el semestre {semestre}.")
        return
    print(f"\n  Reporte semestre {semestre}")
    print("  " + "-" * 58)
    for nombre in materias_semestre:
        est = estadisticas_materia(alumnos, nombre)
        if est:
            print(f"  {nombre:<30} Promedio: {est['promedio']:.2f}  Tasa prom.: {est['tasa_promocion']:.1f}%")
        else:
            print(f"  {nombre:<30} Sin notas registradas")


def reporte_por_rango_notas(alumnos, nota_min, nota_max):
    """Muestra los alumnos y materias cuyas notas están dentro del rango indicado."""
    if not validar_nota(nota_min) or not validar_nota(nota_max):
        print(f"  [ERROR] Rango inválido. Las notas deben estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}.")
        return
    if nota_min > nota_max:
        print("  [ERROR] La nota mínima no puede ser mayor que la máxima.")
        return

    print(f"\n  Notas entre {nota_min} y {nota_max}")
    print("  " + "-" * 58)

    encontrados = False
    for alumno in alumnos:
        notas_en_rango = {
            m: n for m, n in alumno["notas"].items()
            if nota_min <= n <= nota_max
        }
        if notas_en_rango:
            encontrados = True
            print(f"  {alumno['padron']} - {alumno['nombre']} {alumno['apellido']}:")
            for materia, nota in notas_en_rango.items():
                print(f"    {materia:<30} {nota:>4.1f}")

    if not encontrados:
        print("  [INFO] No hay notas en ese rango.")


def guardar_datos(alumnos, materias):
    """Guarda alumnos y materias en el archivo JSON."""
    datos = {"alumnos": alumnos, "materias": materias}
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_datos():
    """Carga alumnos y materias desde el archivo JSON.

    Si el archivo no existe o está dañado, devuelve listas vacías.
    """
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos.get("alumnos", []), datos.get("materias", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return [], []


def buscar_por_nombre(alumnos, texto):
    """Devuelve los alumnos cuyo nombre o apellido contiene el texto (sin distinguir mayúsculas)."""
    texto = texto.strip().lower()
    return [a for a in alumnos if re.findall(texto, a["nombre"].lower() + " " + a["apellido"].lower())]


def buscar_por_carrera(alumnos, carrera):
    """Devuelve los alumnos de una carrera (sin distinguir mayúsculas)."""
    carrera = carrera.strip().lower()
    return [a for a in alumnos if a["carrera"].lower() == carrera]


def buscar_por_estado(alumnos, estado):
    """Devuelve los alumnos que tienen el estado académico indicado."""
    estado = estado.strip().title()
    if estado not in ("Activo", "Inactivo", "Egresado"):
        print("  [ERROR] Estado inválido. Opciones: Activo, Inactivo, Egresado.")
        return []
    return [a for a in alumnos if a.get("estado", "Activo") == estado]


def _confirmar(mensaje):
    """Pide confirmación al usuario. Devuelve True solo si responde 's'."""
    respuesta = input(f"  {mensaje} (s/n): ").strip().lower()
    return respuesta == "s"


def _pedir_padron():
    """Solicita y valida un número de padrón (1 a 6 dígitos)."""
    padron = input("  Número de padrón: ").strip()
    if not re.match(r'^\d{4,6}$', padron):
        print("  [ERROR] El padrón debe tener entre 4 y 6 dígitos numéricos.")
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
        print("  6. Buscar por nombre o apellido")
        print("  7. Buscar por carrera")
        print("  8. Buscar por estado (Activo/Inactivo/Egresado)")
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
                if _confirmar(f"¿Seguro que querés eliminar al alumno {padron}?"):
                    eliminar_alumno(alumnos, padron)
                else:
                    print("  Operación cancelada.")
        elif eleccion == "6":
            texto = input("  Nombre o apellido a buscar: ").strip()
            encontrados = buscar_por_nombre(alumnos, texto)
            if not encontrados:
                print("  [INFO] No se encontraron alumnos.")
            else:
                for a in encontrados:
                    print(f"  {a['padron']} - {a['nombre']} {a['apellido']} ({a['carrera']})")
        elif eleccion == "7":
            carrera = input("  Carrera a buscar: ").strip()
            encontrados = buscar_por_carrera(alumnos, carrera)
            if not encontrados:
                print("  [INFO] No se encontraron alumnos en esa carrera.")
            else:
                for a in encontrados:
                    print(f"  {a['padron']} - {a['nombre']} {a['apellido']} ({a['carrera']})")
        elif eleccion == "8":
            estado = input("  Estado a buscar (Activo/Inactivo/Egresado): ").strip()
            encontrados = buscar_por_estado(alumnos, estado)
            if not encontrados:
                print("  [INFO] No se encontraron alumnos con ese estado.")
            else:
                for a in encontrados:
                    print(f"  {a['padron']} - {a['nombre']} {a['apellido']} ({a['carrera']}) [{a.get('estado', 'Activo')}]")
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
        print("  3. Eliminar nota")
        print("  4. Consultar notas de un alumno")
        print("  5. Ver alumnos por materia")
        print("  6. Promedio de una materia")
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
                materia = input("  Nombre de la materia: ").strip()
                if _confirmar(f"¿Seguro que querés eliminar la nota de '{materia}'?"):
                    eliminar_nota(alumnos, padron, materia)
                else:
                    print("  Operación cancelada.")
        elif eleccion == "4":
            padron = _pedir_padron()
            if padron is not None:
                consultar_notas_alumno(alumnos, padron)
        elif eleccion == "5":
            materia = input("  Nombre de la materia: ").strip()
            listar_alumnos_por_materia(alumnos, materia)
        elif eleccion == "6":
            materia = input("  Nombre de la materia: ").strip()
            promedio = calcular_promedio_materia(alumnos, materia)
            if promedio is None:
                print(f"  [INFO] Ningún alumno tiene nota registrada para '{materia}'.")
            else:
                print(f"  Promedio de '{materia}': {promedio:.2f}")
        elif eleccion == "0":
            break
        else:
            print("  [ERROR] Opción inválida.")


def menu_reportes():
    """Submenú de reportes y estadísticas."""
    while True:
        print("\n" + "=" * 45)
        print("       REPORTES Y ESTADÍSTICAS")
        print("=" * 45)
        print("  1. Estadísticas de una materia")
        print("  2. Promociones y desaprobaciones por materia")
        print("  3. Reporte por carrera")
        print("  4. Resumen ejecutivo")
        print("  5. Filtrar notas por rango")
        print("  0. Volver al menú principal")
        print("=" * 45)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            materia = input("  Nombre de la materia: ").strip()
            mostrar_estadisticas_materia(alumnos, materia)
        elif eleccion == "2":
            reporte_promociones_desaprobaciones(alumnos)
        elif eleccion == "3":
            reporte_por_carrera(alumnos)
        elif eleccion == "4":
            resumen_ejecutivo(alumnos)
        elif eleccion == "5":
            try:
                nota_min = float(input("  Nota mínima: ").strip())
                nota_max = float(input("  Nota máxima: ").strip())
                reporte_por_rango_notas(alumnos, nota_min, nota_max)
            except ValueError:
                print("  [ERROR] Ingrese números válidos.")
        elif eleccion == "0":
            break
        else:
            print("  [ERROR] Opción inválida.")


def menu_materias():
    """Submenú de gestión de materias."""
    while True:
        print("\n" + "=" * 45)
        print("         GESTIÓN DE MATERIAS")
        print("=" * 45)
        print("  1. Registrar materia")
        print("  2. Listar materias")
        print("  3. Reporte por semestre")
        print("  0. Volver al menú principal")
        print("=" * 45)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            registrar_materia(materias)
        elif eleccion == "2":
            listar_materias(materias)
        elif eleccion == "3":
            try:
                semestre = int(input("  Número de semestre: ").strip())
                reporte_por_semestre(alumnos, materias, semestre)
            except ValueError:
                print("  [ERROR] Ingrese un número válido.")
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
        print("  3. Reportes y estadísticas")
        print("  4. Gestión de materias")
        print("  0. Salir")
        print("=" * 50)

        eleccion = input("  Seleccione una opción: ").strip()

        if eleccion == "1":
            menu_alumnos()
        elif eleccion == "2":
            menu_notas()
        elif eleccion == "3":
            menu_reportes()
        elif eleccion == "4":
            menu_materias()
        elif eleccion == "0":
            print("\n  Hasta luego.")
            break
        else:
            print("  [ERROR] Opción inválida.")


if __name__ == "__main__":
    alumnos_guardados, materias_guardadas = cargar_datos()
    for alumno_guardado in alumnos_guardados:
        alumnos.append(alumno_guardado)
        padrones.add(alumno_guardado["padron"])
    for materia_guardada in materias_guardadas:
        materias.append(materia_guardada)
    menu_principal()
