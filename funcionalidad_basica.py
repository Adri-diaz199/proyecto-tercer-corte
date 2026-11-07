import hashlib
import os
import pygame

pygame.mixer.init()
registered_users = {}

def sing_up_request():
    mail = input("Ingrese su correo electronico: ")
    mail_confirmation = mail_verification(mail)
    while(mail_confirmation == False):
        print("Correo invalido, no cumple con los estandares basicos de un correo electronico")
        mail = input("Ingrese su correo electronico: ")
        mail_confirmation = mail_verification(mail)

    print("Correo guardado exitosamente")

    password = input("Ingrese la contraseña de su cuentas: ")
    password_verification = input("Ingrese de nuevo su contraseña: ")

    while(password != password_verification):
        print("Error. La contraseña debe ser igual en los dos campos, por favor ingreselas de nuevo: ")
        password = input("Ingrese la contraseña de su cuentas: ")
        password_verification = input("Ingrese de nuevo su contraseña: ")
    
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

    registered_users[mail] = {
        'mail': mail,
        'salt': salt,
        'hash': hashed_password
    }

    index(mail)

def sing_in_request():
    mail = input("Ingrese su correo: ")
    password = input("Ingrese su contraseña: ")

    if mail not in registered_users:
        print("Error: El correo ingresado no está registrado.")
        return False

    saved_mail = registered_users[mail]['mail']
    saved_salt = registered_users[mail]['salt']
    saved_hash = registered_users[mail]['hash']

    new_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        saved_salt, 
        100000
    )

    if(new_hash == saved_hash) and (mail == saved_mail):
        print("Inicio de sesion valido")
        return True, saved_mail
    else:
        return False
    
def boot_menu():
    print("1 para registrarse")
    print("2 para iniciar sesion")
    print("3 para terminar el programa")
    option_boot_menu = int(input("Ingrese una opcion de navegacion: "))

    if(option_boot_menu == 1):
        sing_up_request()

    elif(option_boot_menu == 2):
        verification_valid, mail = sing_in_request()
        while(verification_valid == False):
            verification_valid, mail = sing_in_request()
        index(mail)

def mail_verification(mail):
    at_counter = 0
    point_counter = 0
    count_aux = 0
    for i in mail:
        if(mail[count_aux] == "@"):
            at_counter = at_counter + 1
        if(mail[count_aux] == "."):
            point_counter = point_counter + 1

        count_aux = count_aux + 1

    if(at_counter == 1):
        split_mail = mail.split("@")
        if(4 <= len(split_mail[0]) < 15):
            if(point_counter != 0):
                split_mail_after_at = split_mail[1].split(".")
                if(2 < len(split_mail_after_at[0]) < 20) and (2 <= len(split_mail_after_at[point_counter]) < 5):
                    return True
                
    return False
                
def create_folder():
    folder = []
    folder_name = input("Ingrese el nombre de la carpeta creada: ")
    folder.append(0)
    folder[0] = folder_name
    return folder

def folder_menu(folder):
    navegation_option = 0

    while (navegation_option != 9):
        print("Agregue una cancion con la opcion 1")
        print("Reproduzca canciones con la opcion 2")
        print("Detener la musica con la opcion 3")
        print("Salir al menu principal con el 9")

        navegation_option = input("Ingrese una opcoin de navegacion: ")
        navegation_option = number_validation(navegation_option)

        if(navegation_option == 1):
            local_url_music = input("Ingrese la ruta de la musica en el computador que deseas agregar: ")

            if os.path.exists(local_url_music):
                folder.append(local_url_music)
                print("Cancion agregada a la carpeta con exito")
            else:
                print("Error: El archivo no existe en esa ruta.")

        if(navegation_option == 2):
            if(len(folder) > 1):
                print(f"---- {folder[0]} ----")

                for i in range(1, len(folder)):
                    print(f"{i}. {folder[i]}")

                selection = input("Ingrese el número de la canción a reproducir (o 0 para cancelar): ")
                selection = number_validation(selection)

                if 0 < selection < len(folder):
                    pygame.mixer.music.load(folder[selection])
                    pygame.mixer.music.play()
                    print(f"Reproduciendo: {folder[selection]}")
                else:
                    print("Operación cancelada.")

            else:
                print("Esta carpeta esta vacia")

        if(navegation_option == 3):
            pygame.mixer.music.stop()
            print("Reproducción detenida.")


def number_validation(number):
    while(number.isdigit() == False):
        number = input("Ingrese por favor un valor numerico: ")
    number = int(number)
    return number

def index(mail):
    folders_list = []
    option_index = 0
    while(option_index != 9):
        print()
        print("1 para crear carpeta")
        print("2 para abrir una carpeta (escribir el nombre de la carpeta exacta)")

        print("9 para salir de la sesion")
        print()
        option_index = int(input("Ingrese una opcion de navegacion: "))

        if(option_index == 1):
            folders_list.append(0)
            folder = create_folder()

            folders_list[len(folders_list) - 1] = folder

        if(option_index == 2):
            option_folder = input("Ingrese el nombre exacto de la carpeta que quiere abrir: ")
            for i in range(len(folders_list)):
                if(option_folder == folders_list[i][0]):
                    folder_menu(folder)
                else:
                    print("carpeta no encontrada")

        if(option_index == 9):
            boot_menu()

        for i in range(len(folders_list)):
            print("====================")
            print(folders_list[i][0])

    boot_menu()

boot_menu()