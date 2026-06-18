'''
Trabajo Práctico Integrador - Organización Empresarial
Tecnicatura Universitaria en Programación a Distancia - UTN
Sofía Sachetti - Comisón 7
Junio 2026
'''

# Importamos módulo 'datetime' para utilizar en la gestión de las fechas de los usuarios
from datetime import datetime 


# Generamos variables para manejar las rutas a los archivos CSV
# Tambiénuna variable donde alamcenamos el valor inicial de vacaciones
ARCHIVO_EMPLEADOS = 'empleados.csv'
ARCHIVO_SOLICITUDES = 'solcitudes.csv'
SALDO_INICIAL = 14


# Funciones para ayudar con la interfaz del chat
# bot() -> el mensaje que envia el bot va a salir con este formato
# usuario() -> el espacio para que el suaurio escriba va a estar delimitado por esta función

def bot(mensaje):
    print(f"🤖 {mensaje}")

def usuario(prompt):
    return input(f"💬 Vos: ").strip()


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


# Funciones de búsqueda:
# Van a ayudar a buscar usuarios o buscar solcitudes de vacaciones
# buscar_empleado() -> recorre un diccionario de empleados y busca por legajo
# buscar_solicitudes_empleado() -> filtra las solicitudes de un empleado en especifico

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


# Funciones de lógica: acá va a estar desarrollada toda la lógica princiapl que gestiona las vacaciones
# validar_fecha() -> sirve para hacer la validación del ingreso de la fecha por parte del usuario
# generar_id_solicitud() -> va a generar automáticamente las id formateadas
# simular_decision_jefe() -> a forma de ejemplificar los resultados, se hace una función que simule la decisón del jefe.
# Se utiliza el modulo radnom para que la eleccion entre aprobada/rechazada sea aleatoria


def validar_fecha(texto):
    try: 
        fecha = datetime.strptime(texto, "%Y-%m-%d")  # Defino el formato de la fecha
        if fecha.date() < datetime.today().date(): # Comparo que sea una fecha actual y no una anterior
            return None
        return texto  # Si esta todo ok devuelvo el texto de la fecha
    except ValueError: # Except para cualquier error que pueda surgir
        None


def generar_id_solicitud(solcitudes):
    if len(solcitudes) == 0:  # Si no hay ninguna solicitud almacenada, arranca con la primera
        return "S001"
    ultima = solcitudes[-1]["id_solicitud"] # Toma la ultima solicitud registrada
    numero = int(ultima[1:]) + 1  # Le saca la letra S y obtiene solamente el ultimo numeor y le suma 1
    return "S" + str(numero).zfill(3)  # Retorna la nueva id formateada


def simular_decision_jefe(nombre_jefe):
    import time  # Modulo tima para simular espera de respuesta
    import random  # Modulo random para simular respuesta al azar
    bot(f"Perfecto! Ya tengo todos los datos. Voy a enviarle tu solicitud a {nombre_jefe} para que la revise.")
    print("Esperando respuesta", end="", flush=True)
    for _ in range(4):
        time.sleep(0.6)
        print(".", end="", flush=True)
    print()
    decision = random.choice(["aprobada", "rechazada"])
    return decision


