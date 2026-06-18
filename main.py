'''
Trabajo Práctico Integrador - Organización Empresarial
Tecnicatura Universitaria en Programación a Distancia - UTN
Sofía Sachetti - Comisón 7
Junio 2026
'''

# Importamos módulo 'datetime' para utilizar en la gestión de las fechas de los usuarios
from datetime import datetime 


# Funciones auxiliares de archivo:
# Estas funciones van a acompañar la gestión de los archivos CSV (abrir, escribir y guardar)
# leer_csv() -> utiliza método 'open' en formato lectura, justamente lo que va a hacer es traer la info del archivo.
# Además, va a formatear la info en uan lista de deccionarios para poder utilizar la infromación en el programa.
# escribir_csv() -> utiliza el metodo 'open' en formato escritura. Sirve para alamcenar todos los cambios realizados.

def leer_csv(nombre_archivo):
    registros = []  # Acá vamos a ir almacenando los registros que esten en el CSV
    try:
        archivo = open(nombre_archivo, "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
    except FileNotFoundError:  # Si el archivo no se encuentra, entonces avisa de un error
        print(f"[ERROR] No se encontró el archivo '{nombre_archivo}'.")
        return []

    # Formateo de la info que viene desde el CSV
    encabezado = lineas[0].strip().split(",")
    for linea in lineas[1:]:
        linea = linea.strip()
        if linea == "":
            continue
        valores = linea.split(",")
        registro = {}
        for i in range(len(encabezado)):
            if i < len(valores):
                registro[encabezado[i]] = valores[i]
            else:
                registro[encabezado[i]] = ""
        registros.append(registro)
    return registros


def escribir_csv(nombre_archivo, registros, encabezado):
    try:
        archivo = open(nombre_archivo, "w", encoding="utf-8")
        archivo.write(",".join(encabezado) + "\n")
        for registro in registros:
            fila = []
            for campo in encabezado:
                fila.append(registro.get(campo, ""))
            archivo.write(",".join(fila) + "\n")
        archivo.close()
    except Exception:
        print("[ERROR] No se pudo guardar el archivo.")


# Funcoines de búsqueda:
# Van a ayudar a buscar usuarios o buscar solcitudes de vacaciones
# buscar_empleado() -> recorre un diccionario de empleados y busca por legajo
# buscra_solicitudes_empleado() -> filtra las solicitudes de un empleado en especifico
def buscar_empleado(legajo, empleados):
    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado
    return None


def buscar_solicitudes_empleado(legajo, solicitudes):
    resultado = []
    for solicitud in solicitudes:
        if solicitud["legajo_empleado"] == legajo:
            resultado.append(solicitud)
    return resultado


# archivo_empleados = 'empleados.csv'
# archivo_solicitudes = 'solicitudes.csv'
# solicitudes = leer_csv(archivo_solicitudes)
# empleados = leer_csv(archivo_empleados)
# print(buscar_empleado("E003", empleados))
# print(buscar_solicitudes_empleado("E007", solicitudes))