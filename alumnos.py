def crear_alumno(alumnos):
    padron = input("Padron: ")
    
    #evitar duplicados
    for a in alumnos:
        if a["padron"] == padron:
            print("Ya existe un alumno con ese padron")
            return

    nombre = input("Nombre: ")
    carrera = input("Carrera: ")

    alumno = {
        "padron": padron,
        "nombre": nombre,
        "carrera": carrera,
        "notas": {}
    }

    alumnos.append(alumno)
    print("Alumno creado correctamente")


def listar_alumnos(alumnos):
    if not alumnos:
        print("No hay alumnos cargados")
        return

    for a in alumnos:
        print(f'{a["padron"]} - {a["nombre"]} ({a["carrera"]})')


def buscar_alumno(alumnos, padron):
    for a in alumnos:
        if a["padron"] == padron:
            return a
    return None