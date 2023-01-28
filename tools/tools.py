from os import system, name,path
import csv
import webbrowser

# CONSTANTES
URL_MATERIAS = "https://www.nuevosemestre.com/_next/data/XbStiufFj8jq_WMgi_X0A/programacion-docente/xxx.json"
URL_MAESTRO = "https://www.nuevosemestre.com/_next/data/XbStiufFj8jq_WMgi_X0A/profesor/xxx.json"
VER_OPINIONES = "https://www.nuevosemestre.com/profesor/"
HEADER = ["NRC", "Profesor", "Materia", "Seccion","Horario","Campus"]

# FUNCIONES
def print_info(datos:list,ver:bool=True):
    """Funcion para imprimir los datos pedidos, retorna un diccionario de canditados
    que sera usado para luego guardarlos si es necesario"""
    candidatos = {}
    for i,dato in enumerate(datos,start=1):
        if ver:
            print(f"\n{'_'*10} Opcion #{i} {'_'*10}")
            print(f"NRC: {dato['nrc']}")
            print(f"Profesor: {dato['teacher']}")
            print(f"Materia: {dato['subject']}")
            print(f"Seccion: {dato['section']}")
            print(f"Horario: {dato['days']}, {dato['schedule']}")
            print(f"Campus: {dato['campus']}")
            
        candidatos[i] = dato
        if i == 100: # Pueden quitar esta condicional y si hay mas de 100 opciones las imprime todas
            break
    
    return candidatos

def convertir_diccionario_a_lista(obj:dict,virtuales:bool = True):
    """Funcion para convertir el diccioario a una lista, el parametro virtuales por 
    defecto verdadero,esta funcion retorna todas las materias o solo las virtuales"""
    if virtuales:
        return list({k: v for k, v in obj.items() if "(Virtual)" in v["subject"]}.values())
    else:
        return  list({k: v for k, v in obj.items()}.values())

def imprimir_informacion_materias(materias:list,solo_virtuales:bool=False):
    """Funcion encargada de imprimir los resultados de la materia deseada"""

    if solo_virtuales:
        opciones = print_info(materias,False) # Falso para capturar los datos solamente
        solo_v =  convertir_diccionario_a_lista(opciones)
        opciones = print_info(solo_v)
    else:
        opciones = print_info(materias)
    continuar = input("Desea guardar candidato?(escribir si o s): ").lower()
    if continuar == "si" or continuar == "s":
        seleccionados = input("\nElija uno o varios numeros separados por un espacio: ")
        numeros = []
        if seleccionados and (seleccionados != " "):
            for element in seleccionados.split(' '):
                try:
                    numeros.append(int(element))
                except ValueError:
                    print(f"Error \"{element}\" no es valido")
                except TypeError:
                    print("Error")
            guardar_candidatos(opciones,numeros)
    


def profesores(teacher:list):

    print(f"{'-'*20}{teacher['name']}{'-'*20}")
    print(f"Departamento: {teacher['chair']}")
    print(f"Secciones: {teacher['subjects_count']}")
    print(f"Opiniones: {teacher['opinions_count']}")

    if teacher["statistics"]:
        print(f"Porcentajes del maestro: ")
        statistics = teacher["statistics"]
        print(f"Explicando: {statistics['explication_rate']}%")
        print(f"Evaluando estudiantes: {statistics['fair_rate']}%")
        print(f"Tomarian clases otra vez:  {statistics['takeagain_rate']}%")
        print(f"Asistencia: {statistics['asistance_rate']}%")

        res = input("\nDesea ver opiniones?(si o s): ").lower()
        if res == "si" or res == "s":
            formato = VER_OPINIONES + teacher['name'].replace(" ","-")
            webbrowser.open_new_tab(formato)


def guardar_candidatos(obj:dict,elegidos:list[int]):
    """Funcion para guardar los candidatos por los que etemos interesados en el archivo llamado
    uasd.csv"""
    # ["NRC", "Profesor", "Materia", "Seccion","Horario","Campus"]
    for x in obj.keys():
        if x in elegidos:
            horario = f"{obj[x]['days']}, {obj[x]['schedule']}"
            guardar_csv([obj[x]["nrc"],obj[x]["teacher"],obj[x]["subject"],obj[x]["section"],horario,obj[x]["campus"]])

def guardar_csv(information:list):
    is_new = False
    if path.exists("./uasd.csv") == False: # verificamos que el archivo uasd.csv exista
        is_new = True

    with open('uasd.csv', 'a',newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        if is_new:
            # header es la primera linea del archivo csv, esta es importante ya que es el titulo
            writer.writerow(HEADER) 
            writer.writerow(information)
        else:
            writer.writerow(information)

# codigo honestamente robado de geeksforgeeks para limpiar la consola
def clear():
    # for windows
    if name == 'nt':
       system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
       system('clear')

if __name__ == "__main__":
    guardar_csv([1251215,"Jean Carlos CR","Bebedores 0140","69","Miercoles 2 a 4","Santo domingo"])

# la linea ## retorna una arreglo(lista) de objetos con la siguiente estructura
# {
# 'teacher': string,
# 'code': string,
# 'nrc': entero,
# 'key': string,
# 'section': string,
# 'type': string,
# 'schedule': string,
# 'days': string,
# 'classroom': string,
# 'subject': string,
# 'campus': 'string
# }