"""
Pruebas unitarias del Sistema de Gestión de Alumnos.

Cómo ejecutarlas:
    pip install pytest
    pytest -v

(Parado en la carpeta del proyecto, junto a alumnos.py.)

Para medir el porcentaje de cobertura:
    pip install pytest-cov
    pytest --cov=alumnos
"""

import os
import builtins
import alumnos

# Durante los tests desactivamos la escritura en disco para que las pruebas
# NO modifiquen el archivo datos_alumnos.json real. Guardamos la función
# original por si algún test necesita la persistencia de verdad.
_guardar_real = alumnos.guardar_datos
alumnos.guardar_datos = lambda *args, **kwargs: None

_input_real = builtins.input


def datos_demo():
    """Devuelve una lista de alumnos de ejemplo (nueva en cada llamada)."""
    return [
        {"padron": "1001", "nombre": "Ana", "apellido": "Gomez", "carrera": "Sistemas",
         "dni": "40000001", "email": "ana@uni.edu", "estado": "Activo",
         "notas": {"Prog I": 9.0, "Algebra": 5.0}},
        {"padron": "1002", "nombre": "Luis", "apellido": "Perez", "carrera": "Sistemas",
         "dni": "40000002", "email": "luis@uni.edu", "estado": "Inactivo",
         "notas": {"Prog I": 3.0}},
        {"padron": "1003", "nombre": "Marta", "apellido": "Diaz", "carrera": "Industrial",
         "dni": "40000003", "email": "marta@uni.edu", "estado": "Egresado",
         "notas": {}},
    ]


def simular_input(respuestas):
    """Hace que input() devuelva las respuestas dadas, una por cada llamada."""
    valores = iter(respuestas)
    builtins.input = lambda prompt="": next(valores)


# ── validar_nota ────────────────────────────────────────────
def test_validar_nota_dentro_de_rango():
    assert alumnos.validar_nota(0) is True
    assert alumnos.validar_nota(7) is True
    assert alumnos.validar_nota(10) is True


def test_validar_nota_fuera_de_rango():
    assert alumnos.validar_nota(-1) is False
    assert alumnos.validar_nota(11) is False


def test_validar_nota_no_numerica():
    assert alumnos.validar_nota("hola") is False
    assert alumnos.validar_nota(None) is False


# ── clasificar_estado ───────────────────────────────────────
def test_clasificar_estado():
    assert alumnos.clasificar_estado(9) == "Promocionado"
    assert alumnos.clasificar_estado(7) == "Promocionado"
    assert alumnos.clasificar_estado(5) == "Aprobado"
    assert alumnos.clasificar_estado(4) == "Aprobado"
    assert alumnos.clasificar_estado(3) == "Desaprobado"
    assert alumnos.clasificar_estado(0) == "Desaprobado"


# ── sumaRecursiva ───────────────────────────────────────────
def test_suma_recursiva():
    assert alumnos.sumaRecursiva([5]) == 5
    assert alumnos.sumaRecursiva([1, 2, 3, 4]) == 10
    assert alumnos.sumaRecursiva([2.5, 2.5, 5.0]) == 10.0


# ── buscar_alumno ───────────────────────────────────────────
def test_buscar_alumno_existente():
    a = alumnos.buscar_alumno(datos_demo(), "1001")
    assert a is not None
    assert a["nombre"] == "Ana"


def test_buscar_alumno_inexistente():
    assert alumnos.buscar_alumno(datos_demo(), "9999") is None


# ── alumno_a_tupla ──────────────────────────────────────────
def test_alumno_a_tupla():
    t = alumnos.alumno_a_tupla(datos_demo()[0])
    assert len(t) == 7
    assert t[0] == "1001"
    assert t[5] == "ana@uni.edu"
    assert t[6] == "Activo"


# ── promedios ───────────────────────────────────────────────
def test_promedio_alumno_con_notas():
    assert alumnos.calcular_promedio_alumno(datos_demo()[0]) == 7.0  # (9+5)/2


def test_promedio_alumno_sin_notas():
    assert alumnos.calcular_promedio_alumno(datos_demo()[2]) == 0.0  # Marta sin notas


def test_promedio_materia():
    assert alumnos.calcular_promedio_materia(datos_demo(), "Prog I") == 6.0  # (9+3)/2


def test_promedio_materia_inexistente():
    assert alumnos.calcular_promedio_materia(datos_demo(), "Quimica") is None


# ── obtener_materias ────────────────────────────────────────
def test_obtener_materias():
    assert alumnos.obtener_materias(datos_demo()) == {"Prog I", "Algebra"}


def test_obtener_materias_sin_alumnos():
    assert alumnos.obtener_materias([]) == set()


# ── estadisticas_materia ────────────────────────────────────
def test_estadisticas_materia():
    est = alumnos.estadisticas_materia(datos_demo(), "Prog I")
    assert est["total"] == 2
    assert est["promocionados"] == 1
    assert est["aprobados"] == 0
    assert est["desaprobados"] == 1
    assert est["promedio"] == 6.0
    assert est["tasa_promocion"] == 50.0


def test_estadisticas_materia_inexistente():
    assert alumnos.estadisticas_materia(datos_demo(), "Quimica") is None


# ── búsquedas ───────────────────────────────────────────────
def test_buscar_por_nombre():
    r = alumnos.buscar_por_nombre(datos_demo(), "ana")
    assert len(r) == 1
    assert r[0]["padron"] == "1001"


def test_buscar_por_nombre_por_apellido():
    r = alumnos.buscar_por_nombre(datos_demo(), "perez")
    assert len(r) == 1
    assert r[0]["nombre"] == "Luis"


def test_buscar_por_carrera():
    assert len(alumnos.buscar_por_carrera(datos_demo(), "sistemas")) == 2
    assert len(alumnos.buscar_por_carrera(datos_demo(), "industrial")) == 1


def test_buscar_por_estado():
    assert len(alumnos.buscar_por_estado(datos_demo(), "Activo")) == 1
    assert len(alumnos.buscar_por_estado(datos_demo(), "Egresado")) == 1


def test_buscar_por_estado_invalido():
    assert alumnos.buscar_por_estado(datos_demo(), "Cualquiera") == []


# ── registrar / modificar / eliminar nota ───────────────────
def test_registrar_nota_nueva():
    data = datos_demo()
    assert alumnos.registrar_nota(data, "1003", "Fisica", 8) is True
    assert data[2]["notas"]["Fisica"] == 8.0


def test_registrar_nota_duplicada():
    assert alumnos.registrar_nota(datos_demo(), "1001", "Prog I", 6) is False


def test_registrar_nota_invalida():
    assert alumnos.registrar_nota(datos_demo(), "1001", "Quimica", 99) is False


def test_registrar_nota_alumno_inexistente():
    assert alumnos.registrar_nota(datos_demo(), "9999", "Prog I", 7) is False


def test_modificar_nota():
    data = datos_demo()
    assert alumnos.modificar_nota(data, "1001", "Prog I", 6) is True
    assert data[0]["notas"]["Prog I"] == 6.0


def test_modificar_nota_inexistente():
    assert alumnos.modificar_nota(datos_demo(), "1001", "Quimica", 6) is False


def test_eliminar_nota():
    data = datos_demo()
    assert alumnos.eliminar_nota(data, "1001", "Algebra") is True
    assert "Algebra" not in data[0]["notas"]


def test_eliminar_nota_inexistente():
    assert alumnos.eliminar_nota(datos_demo(), "1001", "Quimica") is False


# ── eliminar_alumno ─────────────────────────────────────────
def test_eliminar_alumno():
    data = datos_demo()
    assert alumnos.eliminar_alumno(data, "1002") is True
    assert len(data) == 2
    assert alumnos.buscar_alumno(data, "1002") is None


def test_eliminar_alumno_inexistente():
    assert alumnos.eliminar_alumno(datos_demo(), "9999") is False


# ── materias ────────────────────────────────────────────────
def test_registrar_materia():
    simular_input(["Fisica", "FIS-001", "2"])
    mats = []
    alumnos.registrar_materia(mats)
    assert len(mats) == 1
    assert mats[0]["nombre"] == "Fisica"
    assert mats[0]["semestre"] == 2


# ── funciones con input() ───────────────────────────────────
def test_confirmar_si():
    simular_input(["s"])
    assert alumnos._confirmar("¿Seguro?") is True


def test_confirmar_no():
    simular_input(["n"])
    assert alumnos._confirmar("¿Seguro?") is False


def test_pedir_padron_valido():
    simular_input(["1234"])
    assert alumnos._pedir_padron() == "1234"


def test_pedir_padron_invalido():
    simular_input(["abc"])
    assert alumnos._pedir_padron() is None


def test_pedir_nota_valida():
    simular_input(["7.5"])
    assert alumnos._pedir_nota() == 7.5


def test_pedir_nota_invalida():
    simular_input(["xyz"])
    assert alumnos._pedir_nota() is None


def test_crear_alumno():
    alumnos.padrones.clear()
    simular_input(["2001", "Pedro", "Sistemas", "Lopez", "40500500", "pedro@uni.edu"])
    data = []
    alumnos.crear_alumno(data)
    assert len(data) == 1
    assert data[0]["padron"] == "2001"
    assert data[0]["email"] == "pedro@uni.edu"
    assert data[0]["estado"] == "Activo"


def test_actualizar_alumno_cambia_estado():
    simular_input(["", "", "", "", "", "Inactivo"])  # solo cambia el estado
    data = datos_demo()
    assert alumnos.actualizar_alumno(data, "1001") is True
    assert data[0]["estado"] == "Inactivo"


def test_actualizar_alumno_inexistente():
    assert alumnos.actualizar_alumno(datos_demo(), "9999") is False


# ── persistencia (JSON) ─────────────────────────────────────
def test_guardar_y_cargar_datos():
    ruta_original = alumnos.ARCHIVO_DATOS
    alumnos.ARCHIVO_DATOS = "test_datos_temp.json"
    try:
        _guardar_real(datos_demo(), [{"nombre": "Prog I", "codigo": "P1", "semestre": 1}])
        a, m = alumnos.cargar_datos()
        assert len(a) == 3
        assert m[0]["nombre"] == "Prog I"
    finally:
        if os.path.exists("test_datos_temp.json"):
            os.remove("test_datos_temp.json")
        alumnos.ARCHIVO_DATOS = ruta_original


def test_cargar_datos_archivo_inexistente():
    ruta_original = alumnos.ARCHIVO_DATOS
    alumnos.ARCHIVO_DATOS = "no_existe_12345.json"
    try:
        a, m = alumnos.cargar_datos()
        assert a == []
        assert m == []
    finally:
        alumnos.ARCHIVO_DATOS = ruta_original


def test_exportar_datos_crea_archivo():
    ruta = os.path.join(os.path.dirname(alumnos.__file__), "datos_alumnos.txt")
    try:
        alumnos.exportar_datos(datos_demo())
        assert os.path.exists(ruta)
    finally:
        if os.path.exists(ruta):
            os.remove(ruta)


# ── smoke tests: reportes que solo imprimen ─────────────────
# Verifican que corren sin lanzar excepciones.
def test_reportes_no_crashean():
    data = datos_demo()
    mats = [{"nombre": "Prog I", "codigo": "P1", "semestre": 1}]
    assert alumnos.listar_alumnos(data) is None
    assert alumnos.consultar_notas_alumno(data, "1001") is None
    assert alumnos.mostrar_estadisticas_materia(data, "Prog I") is None
    assert alumnos.reporte_promociones_desaprobaciones(data) is None
    assert alumnos.reporte_por_carrera(data) is None
    assert alumnos.resumen_ejecutivo(data) is None
    assert alumnos.listar_alumnos_por_materia(data, "Prog I") is None
    assert alumnos.listar_materias(mats) is None
    assert alumnos.reporte_por_semestre(data, mats, 1) is None
    assert alumnos.reporte_por_rango_notas(data, 4, 10) is None


# ── menús (recorren cada opción usando el estado global) ────
def preparar_estado_global():
    """Carga datos de ejemplo en las variables globales que usan los menús."""
    alumnos.alumnos[:] = datos_demo()
    alumnos.materias[:] = []
    alumnos.padrones.clear()
    for a in alumnos.alumnos:
        alumnos.padrones.add(a["padron"])


def test_menu_alumnos_recorre_opciones():
    preparar_estado_global()
    simular_input([
        "1", "2001", "Pedro", "Sistemas", "Lopez", "40500500", "pedro@uni.edu",  # crear
        "2",                                # listar
        "3", "1001",                        # buscar por padrón
        "4", "1001", "", "", "", "", "", "",  # actualizar (6 campos en blanco)
        "5", "1001", "n",                   # eliminar (cancelado)
        "6", "ana",                         # buscar por nombre
        "7", "sistemas",                    # buscar por carrera
        "8", "Activo",                      # buscar por estado
        "x",                                # opción inválida
        "0",                                # salir
    ])
    assert alumnos.menu_alumnos() is None


def test_menu_notas_recorre_opciones():
    preparar_estado_global()
    simular_input([
        "1", "1001", "Fisica", "8",   # registrar nota
        "2", "1001", "Prog I", "6",   # modificar nota
        "3", "1001", "Algebra", "n",  # eliminar nota (cancelado)
        "4", "1001",                  # consultar notas
        "5", "Prog I",                # alumnos por materia
        "6", "Prog I",                # promedio de materia
        "x",                          # inválida
        "0",                          # salir
    ])
    assert alumnos.menu_notas() is None


def test_menu_reportes_recorre_opciones():
    preparar_estado_global()
    simular_input([
        "1", "Prog I",   # estadísticas de materia
        "2",             # promociones/desaprobaciones
        "3",             # por carrera
        "4",             # resumen ejecutivo
        "5", "4", "10",  # filtrar por rango
        "x",             # inválida
        "0",             # salir
    ])
    assert alumnos.menu_reportes() is None


def test_menu_materias_recorre_opciones():
    preparar_estado_global()
    simular_input([
        "1", "Quimica", "QUI-001", "1",  # registrar materia
        "2",                             # listar materias
        "3", "1",                        # reporte por semestre
        "x",                             # inválida
        "0",                             # salir
    ])
    assert alumnos.menu_materias() is None


def test_menu_principal_recorre_opciones():
    preparar_estado_global()
    ruta_txt = os.path.join(os.path.dirname(alumnos.__file__), "datos_alumnos.txt")
    simular_input([
        "1", "0",   # entra a alumnos y vuelve
        "2", "0",   # entra a notas y vuelve
        "3", "0",   # entra a reportes y vuelve
        "4", "0",   # entra a materias y vuelve
        "5",        # exportar a TXT
        "9",        # inválida
        "0",        # salir
    ])
    try:
        assert alumnos.menu_principal() is None
    finally:
        if os.path.exists(ruta_txt):
            os.remove(ruta_txt)
