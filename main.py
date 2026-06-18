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
ARCHIVO_SOLICITUDES = 'solicitudes.csv'
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


# Funciones de proceso: van a simular todo el flujo de la conversación
# solicitar_vacaciones() -> es la función principal. En esta función se da la mayoría de la conversación y el pedido de vacaciones.
# ver_solicitudes() -> función para ver las solicitudes que tiene registradas el empleado

def solicitar_vacaciones(empleado, empleados, solicitudes):
    # Se empieza verificando si el empleado tiene días disponibles. Si no los tiene, avisa.
    if int(empleado["saldo_dias"]) == 0:
        bot("REvisé tu saldo y lamentablemente no te quedan días disponibles para este año. ¿Puedo ayudarte con algo más?")
        return empleados, solicitudes

    # Si tiene dias disponibles, muestra la cantidad en un mensaje
    bot(f"Perfecto! Tenés {empleado['saldo_dias']} días disponibles.\n¿Desde qué fecha querés empezar las vacaciones? Ingresalo en el formato AAAA-MM-DD.")
    
    #Bloque para pedir la fecha y verificarla
    fecha_inicio = None
    while fecha_inicio is None:
        texto = usuario("Fecha de inciio: ")
        if texto == "":
            bot("Necesito que me indiques una fecha para continuar.\n¿Desde cuando querés tomar las vacaciones?")
            continue
        fecha_inicio = validar_fecha(texto)
        if fecha_inicio is None:
            bot("Esa fecha no es válida. \nRecordá que tiene que estar en formato AAAA-MM-DD y ser una fecha futura. Intentemos de nuevo.")
    bot(f"Anotado el día {fecha_inicio}. ¿Cuántos días necesitas tomar?")
    
    # Bloque para pedir cantidad de días y verificarlos
    cantidad_dias = None
    while cantidad_dias is None:
        texto = usuario("Cantidad de días: ")
        try:
            dias = int(texto)
            if dias <= 0:  # Verifica que los días sean numeor postivio
                bot("La cantidad de días tiene que ser al menos 1. ¿Cuántos días querés?")
            elif dias > int(empleado["saldo_dias"]):  # Verifica que la cant de dias pedidos no sobrepase los dias disponibles
                bot(f"Ese número supera tu saldo disponible({empleado['saldo_dias']} días). ¿querés pedir una cantidad menor?")
            else:
                cantidad_dias = dias
        except ValueError:
            bot("No entendí eso. Por favor, ingresá sólo el número de días. Por ejemplo: 5.")
    
    # Bloque para buscar el jefe a cargo del área donde está el empleado
    jefe = buscar_empleado(empleado["jefe_legajo"], empleados)
    nombre_jefe = jefe["nombre"] + " " + jefe["apellido"] if jefe else "El responsable de RRHH"
    
    # Simulacion de la decision del jefe
    decision = simular_decision_jefe(nombre_jefe)
    
    # Generar y registrar solicitud en el formato adecuado
    nuevo_id = generar_id_solicitud(solicitudes)
    fecha_hoy = datetime.today().strftime("%Y-%m-%d")
    
    nueva_solicitud = {  # Formateo el cuerpo de la soli
        "id_solictud": nuevo_id,
        "legajo_empleado": empleado["legajo"],
        "fecha_inicio": fecha_inicio,
        "cantidad_dias": str(cantidad_dias),
        "fecha_solicitud": fecha_hoy,
        "estado": decision
    }
    solicitudes.append(nueva_solicitud)  # Agrego a la lista de solicitudes
    
    # Guardo en el archivo CSV
    encabezado_sol = ["id_solicitud", "legajo_empleado", "fecha_inicio", "cantidad_dias", "fecha_solicitud", "estado"]
    escribir_csv(ARCHIVO_SOLICITUDES, solicitudes, encabezado_sol)
    
    # Si la decision fue aprobada, se actualiza el saldo de días
    if decision == "aprobada":
        for emp in empleados:
            if emp["legajo"] == empleado["legajo"]:  # Busco al empleado en los datos y actualizo la cantida de dias
                emp["saldo_dias"] = str(int(emp["saldo_dias"]) - cantidad_dias)
                break
        # Reescribe el CSV y lo guarda
        encabezado_emp = ["legajo", "nombre", "apellido", "departamento", "jefe_legajo", "saldo_dias"]
        escribir_csv(ARCHIVO_EMPLEADOS, empleados, encabezado_emp)
        saldo_restante = int(empleado["saldo_dias"]) - cantidad_dias
        bot(f"¡Buenas noticias! {nombre_jefe} aprobó tu solicitud ✓") # El bot avisa que la solicitud fue aprobada
        bot(f"Tus vacaciones quedaron registradas: {cantidad_dias} días a partir del {fecha_inicio}. Te quedan {saldo_restante} días disponibles. (ID solicitud: {nuevo_id})")
    elif decision == "rechazada":  # Si fueron rechazadas manda mensaje
        bot(f"Lamentablemente {nombre_jefe} rechazó la solicitud esta vez. Tu saldo de días no fue modificado. Si querés, podés intentar con otras fechas.")
    else:
        bot(f"La solicitud está penndiente. {nombre_jefe} la está evaluando a la brevedad.\nPpdés ir consultando el estado de la solictud cuando quieras por este medio.")
    return empleados, solicitudes


def ver_solicitudes(empleado, solicitudes):
    # Se busca en la base de datos si el empleado tiene solicitudes registradas
    mis_solicitudes = buscar_solicitudes_empleado(empleado["legajo"], solicitudes)

    if len(mis_solicitudes) == 0:   # Si no hay solitudes, lo avisa
        bot("Todavía no tenés ninguna solicitud registrada. ¿Querés hacer una ahora?")
        return

    # Si hay solicitudes, las imprime en pantalla 
    # 
    bot(f"Encontré {len(mis_solicitudes)} solicitud/es tuya/s:")
    for sol in mis_solicitudes:
        estado = sol["estado"].upper()
        print(f"\n 📋 {sol['id_solicitud']} — {estado}")
        print(f" Inicio    : {sol['fecha_inicio']}")
        print(f" Días      : {sol['cantidad_dias']}")
        print(f" Solicitado: {sol['fecha_solicitud']}")


# Funcion principal
# menu() -> va a manejar el flujo del chat

def menu():
    print("\n" + "-" * 45)
    print("  TechSoluciones - Asistente de RRHH")
    print("-" * 45)

    # Lee los archivos CSV
    empleados = leer_csv(ARCHIVO_EMPLEADOS)
    solicitudes = leer_csv(ARCHIVO_SOLICITUDES)

    # Si no hay empleados muestra un aviso 
    if len(empleados) == 0:
        bot("Hubo un problema al cargar los datos. Verificá que los archivos CSV estén en la misma carpeta.")
        return

    # Identificación del empleado
    bot("¡Hola! Soy el asistente de RRHH de TechSoluciones. Para empezar, ¿me decís tu número de legajo?")
    empleado = None
    intentos = 0
    while empleado is None:
        if intentos >= 3:
            bot("Demasiados intentos fallidos. Por seguridad, voy a cerrar la sesión. Comunicate con RRHH si necesitás ayuda.")
            return
        legajo = usuario("Legajo: ").upper()
        empleado = buscar_empleado(legajo, empleados)
        if empleado is None:
            intentos += 1
            restantes = 3 - intentos
            bot(f"No encontré ese legajo. Verificá el número e intentá de nuevo. ({restantes} intento/s restante/s)")

    bot(f"¡Bienvenido/a, {empleado['nombre']}! ¿En qué puedo ayudarte hoy?")
    bot("Podés escribir: \"vacaciones\", \"mis solicitudes\", \"saldo\" o \"salir\"")

    # Conversación principal
    continuar = True
    while continuar:
        respuesta = usuario("").lower()

        if "vacacion" in respuesta:
            empleados_actualizados = leer_csv(ARCHIVO_EMPLEADOS)
            solicitudes_actualizadas = leer_csv(ARCHIVO_SOLICITUDES)
            for emp in empleados_actualizados:
                if emp["legajo"] == empleado["legajo"]:
                    empleado = emp
                    break
            empleados, solicitudes = solicitar_vacaciones(
                empleado, empleados_actualizados, solicitudes_actualizadas
            )
            bot("¿Hay algo más en lo que pueda ayudarte? (\"mis solicitudes\", \"saldo\" o \"salir\")")

        elif "solicitud" in respuesta or "historial" in respuesta:
            solicitudes = leer_csv(ARCHIVO_SOLICITUDES)
            ver_solicitudes(empleado, solicitudes)
            bot("¿Necesitás algo más?")

        elif "saldo" in respuesta or "días" in respuesta or "dias" in respuesta:
            empleado_actualizado = buscar_empleado(empleado["legajo"], leer_csv(ARCHIVO_EMPLEADOS))
            bot(f"Tu saldo actual es de {empleado_actualizado['saldo_dias']} días disponibles.")
            bot("¿Puedo ayudarte con algo más?")

        elif "salir" in respuesta or "chau" in respuesta or "exit" in respuesta:
            bot(f"¡Hasta luego, {empleado['nombre']}! Que tengas un buen día. 👋")
            continuar = False

        else:
            bot("No entendí bien eso. Podés escribir: \"vacaciones\", \"mis solicitudes\", \"saldo\" o \"salir\".")


menu()