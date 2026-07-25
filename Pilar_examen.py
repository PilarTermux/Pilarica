#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#   PILAR IPTV - Generador de Combos
#   Compatible con QPython3 / Termux
# ============================================================

import os
import sys
import time
import random
import glob

# ============================================================
# COLORES ANSI
# ============================================================
LILA   = '\033[95m'
ROSA   = '\033[35m'
BOLD   = '\033[1m'
GREEN  = '\033[92m'
DGREEN = '\033[32m'
RESET  = '\033[0m'

# ============================================================
# RUTAS
# ============================================================
# Detectar raíz del dispositivo (Termux usa /sdcard)
ROOT_DIR  = "/sdcard" if os.path.exists("/sdcard") else os.path.expanduser("~")
PILAR_DIR = os.path.join(ROOT_DIR, "Termux", "Pilar")
COMBO_DIR = os.path.join(ROOT_DIR, "combo")

# ============================================================
# UTILIDADES
# ============================================================
def clear():
    os.system('clear')

def pause():
    input(GREEN + "\nPresiona Enter para continuar..." + RESET)

def banner():
    clear()
    print(LILA + BOLD + """
  ██████╗ ██╗██╗      █████╗ ██████╗
  ██╔══██╗██║██║     ██╔══██╗██╔══██╗
  ██████╔╝██║██║     ███████║██████╔╝
  ██╔═══╝ ██║██║     ██╔══██║██╔══██╗
  ██║     ██║███████╗██║  ██║██║  ██║
  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝""" + RESET)
    print(ROSA + BOLD + """
  ██╗██████╗ ████████╗██╗   ██╗
  ██║██╔══██╗╚══██╔══╝██║   ██║
  ██║██████╔╝   ██║   ██║   ██║
  ██║██╔═══╝    ██║   ╚██╗ ██╔╝
  ██║██║        ██║    ╚████╔╝
  ╚═╝╚═╝        ╚═╝     ╚═══╝""" + RESET + "\n")

# ============================================================
# LEER ARCHIVO DE NOMBRES
# ============================================================
def leer_nombres():
    print(GREEN + "\nIntroduce la ruta completa del archivo de nombres.")
    print("Ejemplo: /sdcard/nombres.txt" + RESET)
    while True:
        ruta = input(GREEN + "> " + RESET).strip()
        if os.path.isfile(ruta):
            try:
                with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                    nombres = [l.strip() for l in f if l.strip()]
                if nombres:
                    print(GREEN + "  -> " + str(len(nombres)) + " nombres cargados." + RESET)
                    return nombres
                else:
                    print(GREEN + "El archivo esta vacio. Prueba con otro." + RESET)
            except Exception as e:
                print(GREEN + "Error al leer: " + str(e) + RESET)
        else:
            print(GREEN + "Archivo no encontrado. Comprueba la ruta." + RESET)

# ============================================================
# GENERADOR DE LINEAS
# ============================================================
def generar_lineas(opcion, nombres, cantidad, num_length):
    generadas = 0
    if opcion == '1':
        for n in nombres:
            if generadas >= cantidad:
                return
            yield n + ":" + n + "\n"
            generadas += 1
    elif opcion == '2':
        for n in nombres:
            if generadas >= cantidad:
                return
            yield n + "123:" + n + "123\n"
            generadas += 1
    elif opcion == '3':
        for n in nombres:
            if generadas >= cantidad:
                return
            yield n + "1234:" + n + "1234\n"
            generadas += 1
    elif opcion == '4':
        for n in nombres:
            if generadas >= cantidad:
                return
            for year in range(1950, 2041):
                if generadas >= cantidad:
                    return
                sy = str(year)
                yield n + sy + ":" + n + sy + "\n"
                generadas += 1
    elif opcion == '5':
        for _ in range(cantidad):
            num = ''.join(str(random.randint(0, 9)) for _ in range(num_length))
            yield num + ":" + num + "\n"

# ============================================================
# CREAR COMBO
# ============================================================
def crear_combo():
    banner()
    print(GREEN + "=" * 50)
    print("  CREAR COMBO")
    print("=" * 50 + RESET + "\n")

    nombre_combo = input(GREEN + "Nombre del combo: " + RESET).strip()
    if not nombre_combo:
        print(GREEN + "Nombre vacio. Volviendo al menu." + RESET)
        pause()
        return

    print(GREEN + "\nSelecciona el formato de las lineas:")
    print("  1. nombre:nombre")
    print("  2. nombre123:nombre123")
    print("  3. nombre1234:nombre1234")
    print("  4. nombre(anio):nombre(anio)  [anios 1950-2040]")
    print("  5. numero:numero  [aleatorio]" + RESET + "\n")

    while True:
        opcion = input(GREEN + "Elige formato (1-5): " + RESET).strip()
        if opcion in ('1', '2', '3', '4', '5'):
            break
        print(GREEN + "Opcion no valida." + RESET)

    nombres    = []
    num_length = 0

    if opcion in ('1', '2', '3', '4'):
        nombres = leer_nombres()

    if opcion == '5':
        while True:
            try:
                num_length = int(input(GREEN + "\nLongitud de los numeros: " + RESET))
                if num_length > 0:
                    break
                print(GREEN + "Debe ser mayor que 0." + RESET)
            except ValueError:
                print(GREEN + "Introduce un numero entero." + RESET)

    if opcion == '4':
        max_pos = len(nombres) * (2040 - 1950 + 1)
    elif opcion == '5':
        max_pos = 1000000
    else:
        max_pos = len(nombres)

    limite = min(1000000, max_pos)
    print(GREEN + "\nMaximo de lineas posibles: " + str(limite) + RESET)

    while True:
        try:
            cantidad = int(input(GREEN + "Cantidad de lineas a generar (1 - " + str(limite) + "): " + RESET))
            if 1 <= cantidad <= limite:
                break
            print(GREEN + "Valor fuera de rango." + RESET)
        except ValueError:
            print(GREEN + "Introduce un numero entero." + RESET)

    # Asegurar directorio de salida
    os.makedirs(PILAR_DIR, exist_ok=True)
    archivo_salida = os.path.join(PILAR_DIR, nombre_combo + ".txt")

    # Generación con barra de progreso
    BAR_WIDTH  = 50
    print(GREEN + "\nGenerando " + str(cantidad) + " lineas...\n" + RESET)

    gen        = generar_lineas(opcion, nombres, cantidad, num_length)
    escritas   = 0
    pct_actual = 0

    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for linea in gen:
                f.write(linea)
                escritas += 1
                nuevo_pct = int(escritas * 100 / cantidad)
                while pct_actual < nuevo_pct:
                    pct_actual += 1
                    filled = int(BAR_WIDTH * pct_actual / 100)
                    empty  = BAR_WIDTH - filled
                    bar    = "\u2588" * filled + "\u2591" * empty
                    print(GREEN + "[" + bar + "] " + str(pct_actual).rjust(3) + "%" + RESET)

        while pct_actual < 100:
            pct_actual += 1
            filled = int(BAR_WIDTH * pct_actual / 100)
            empty  = BAR_WIDTH - filled
            bar    = "\u2588" * filled + "\u2591" * empty
            print(GREEN + "[" + bar + "] " + str(pct_actual).rjust(3) + "%" + RESET)

        print(GREEN + "\nCombo guardado en:" + RESET)
        print(DGREEN + "  " + archivo_salida + RESET)

    except Exception as e:
        print(GREEN + "\nError al guardar: " + str(e) + RESET)

    pause()

# ============================================================
# ELIMINAR DUPLICADOS
# ============================================================
def eliminar_duplicados():
    banner()
    print(GREEN + "=" * 50)
    print("  ELIMINAR DUPLICADOS")
    print("=" * 50 + RESET + "\n")

    if not os.path.isdir(COMBO_DIR):
        print(GREEN + "La carpeta " + COMBO_DIR + " no existe." + RESET)
        pause()
        return

    archivos = glob.glob(os.path.join(COMBO_DIR, "*.txt"))
    if not archivos:
        print(GREEN + "No hay archivos .txt en " + COMBO_DIR + RESET)
        pause()
        return

    print(GREEN + "Combos disponibles en " + COMBO_DIR + ":\n" + RESET)
    for i, fp in enumerate(archivos, 1):
        print(GREEN + "  " + str(i) + ". " + os.path.basename(fp) + RESET)

    while True:
        try:
            sel = int(input(GREEN + "\nSelecciona un archivo (1-" + str(len(archivos)) + "): " + RESET))
            if 1 <= sel <= len(archivos):
                elegido = archivos[sel - 1]
                break
            print(GREEN + "Numero fuera de rango." + RESET)
        except ValueError:
            print(GREEN + "Introduce un numero entero." + RESET)

    print(GREEN + "\nProcesando " + os.path.basename(elegido) + "..." + RESET)

    try:
        with open(elegido, 'r', encoding='utf-8', errors='ignore') as f:
            lineas = f.readlines()

        total_orig  = len(lineas)
        unicas      = list(dict.fromkeys(lineas))
        total_unico = len(unicas)
        eliminadas  = total_orig - total_unico

        if eliminadas == 0:
            print(GREEN + "No se encontraron duplicados." + RESET)
        else:
            with open(elegido, 'w', encoding='utf-8') as f:
                f.writelines(unicas)
            print(GREEN + "Duplicados eliminados : " + str(eliminadas))
            print("Lineas originales     : " + str(total_orig))
            print("Lineas unicas         : " + str(total_unico) + RESET)

    except Exception as e:
        print(GREEN + "Error: " + str(e) + RESET)

    pause()

# ============================================================
# MENU PRINCIPAL
# ============================================================
def menu_principal():
    while True:
        banner()
        print(GREEN + "=" * 50)
        print("  MENU PRINCIPAL")
        print("=" * 50)
        print("  1. Crear combo")
        print("  2. Eliminar duplicados")
        print("  3. Salir")
        print("=" * 50 + RESET + "\n")

        opcion = input(GREEN + "Elige una opcion (1-3): " + RESET).strip()

        if opcion == '1':
            crear_combo()
        elif opcion == '2':
            eliminar_duplicados()
        elif opcion == '3':
            clear()
            print(LILA + BOLD + "\n  Hasta luego! -- Pilar IPTV\n" + RESET)
            sys.exit(0)
        else:
            print(GREEN + "Opcion no valida. Intenta de nuevo." + RESET)
            time.sleep(1)

# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(GREEN + "\n\nScript interrumpido. Hasta luego!\n" + RESET)
        sys.exit(0)
