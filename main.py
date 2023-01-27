import requests # importamos el modulo que usaremos para hacer la solicitud a la pagina
import pyinputplus as pyip
from tools import tools
import time


try:
    while True:
        
        opciones = ["Materias","Profesores","Salir"] # para nuestro menu
        opcion =  pyip.inputMenu(opciones,prompt="Seleccione un numero:\n",numbered=True)
        user_input = ""

        tools.clear()
        match opcion:
            case "Salir": # [-1] en una lista toma el ultimo elemento
                print("Buena suerte en la seleccion! 👋🏽")
                time.sleep(1.5)
                break
            case "Materias":
                user_input = input("Clave de la asignatura (ej. MAT0140): ").replace(" ","").upper()
                # tomamos variable URL_MATERIAS y reemplazamos "xxx" con el nombre de la materia ingresada por teclado
                respuesta = requests.get(tools.URL_MATERIAS.replace("xxx",user_input))
            case "Profesores":
                user_input = input("Nombre COMPLETO del profesor: ").replace(" ","-")
                respuesta = requests.get(tools.URL_MAESTRO.replace("xxx",user_input))
                
        tools.clear()
        match respuesta.status_code:
            case 200:
                # opciones =  pyip.inputMenu(opciones,prompt="Que desea buscar")
                # el objeto retornado por json es un diccionario, similar a un objeto en JavaScript o a struct in CPP
                solo_virtual = False
                if opcion == "Materias":
                    res = pyip.inputMenu(["Todas","Virtules"],prompt="Tipo materias:\n",numbered=True)
                    datos = respuesta.json()["pageProps"]["subjects"]
                    if res == "Todas":
                        tools.imprimir_informacion_materias(datos)
                    else:
                        tools.imprimir_informacion_materias(datos,True)

                    break
                else:
                    datos = respuesta.json()["pageProps"]["teacher"]
                    tools.profesores(datos)
            
            case 404:
                print(f"Error no se encontro \"{user_input}\", revise que la clave este bien.")
            
            case 502:
                print("Pagina presenta problemas, trate luego")

        tools.clear()

except KeyboardInterrupt:
    print("See you later.")

#TODO: EXE file