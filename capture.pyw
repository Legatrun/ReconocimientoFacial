import cv2,os
from shutil import rmtree
from tkinter import *
from datetime import date, datetime

root = Tk()
root.title('                                                                      Registro de Usuario')
root.geometry('728x410')
root.resizable(False,False)
root.iconbitmap('images/icon.ico')
user=''

imagenFondo = PhotoImage(file='images/fondo.png')
title= PhotoImage(file='images/logo.png')
name= StringVar()


fondo = Label(root, image=imagenFondo)
fondo.place(x=0,y=0,relwidth=1,relheight=1)
logo= Label(fondo,image=title, background="#0f161e")
logo.place(x=200,y=30)


#-----------------Label--------------------------------
nombre = Label(root, text='Nombre:')
nombre.place(x=200,y=150)
nombre.config(width=10,bg='#0f161e',fg='#FFF')

entryNombre = Entry(root,textvariable=name)
entryNombre.place(x=300,y=150)
entryNombre.config(justify='center')

password = Label(root, text='Contraseña:')
password.place(x=200,y=200)
password.config(width=10,bg='#0f161e',fg='#FFF')

entryPassword = Entry(root)
entryPassword.place(x=300,y=200)
entryPassword.config(show='*', justify='center')


#-----------------Buttons------------------------
cancelarButton = Button(root, text='cancelar')
cancelarButton.place(x=270, y=250)

def guardarNombre(nombre):
    global user

    user=nombre
    root.destroy()


registrarButton = Button(root, text='registrar', command=lambda:guardarNombre(name.get()))
registrarButton.place(x=330, y=250)



#----------------Menu---------------------

barraMenu=Menu(root)
root.config(menu=barraMenu)

#---------------------------------Mas----------------------------
archivoMas=Menu(barraMenu,tearoff=0)
archivoMas.add_command(label='Soporte')
archivoMas.add_command(label='Licencia')
archivoMas.add_separator()
archivoMas.add_command(label='Salir')


#----------------------------------Contacto----------------------------------------------
archivoContacto=Menu(barraMenu,tearoff=0)
archivoContacto.add_command(label='Univalle')
archivoContacto.add_separator()
archivoContacto.add_command(label='Docente')


#-----------------------------------Ayuda---------------------------
archivoAyuda=Menu(barraMenu,tearoff=0)
archivoAyuda.add_command(label='Errores')





barraMenu.add_cascade(label='Más', menu=archivoMas)

barraMenu.add_cascade(label='Contacto', menu=archivoContacto)

barraMenu.add_cascade(label='Ayuda', menu=archivoAyuda)



size = 4
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'recoFacial'

root.mainloop()

def eliminarTilde(nombre):
    indice = nombre.maketrans('áéíóú','aeiou')
    nombre = nombre.translate(indice)
    return nombre

today = date.today()
now = datetime.now()
new_date = datetime(today.year, today.month, today.day, now.hour, now.minute, now.second)

def append(nombre):
    with open("database.txt" , "a", encoding = "utf-8") as f:
        f.write('\n')
        f.write(nombre + str(new_date))

def nuevoUsuario(name):

    name = eliminarTilde(name)
    nombre = name.replace(' ','')

    if len(name) == 0:
        print('Entro')
        assert len(name) < 0, '\033[31mDebe ingresar un nombre\033'

    while len(name) < 27:
        name = name + ' '
    append(name)

    return nombre

def crear(nombreDirectorio, nombreDeUsuario):
    path = os.path.join(nombreDirectorio, nombreDeUsuario)
    try:
        rmtree(f'./{nombreDirectorio}/{nombreDeUsuario}')
        os.mkdir(path)
    except:
        os.mkdir(path)

    return path

fn_name = nuevoUsuario(user)
path = crear(fn_dir,fn_name)

#indicamos el ancho y algo de la imagen
(im_width, im_height) = (112, 92)

haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)

# Generar nombre para cada imagen
#funcion sorted= devuelve una nueva lista ordenada
pin = sorted([int(n[:n.find('.')]) for n in os.listdir(path) if n[0]!='.' ]+[0])[-1] + 1
#con 033/n cambiamos el color y "negrita"
print("\n\033[94mEl programa guardara 15 imagenes. \
Mueva un poco su cabeza para tenermejor percepcion.\033[0m\n")

count = 0
pause = 0
count_max = 30
while count < count_max:

    rval = False
    #preguntamos si existe el objeto webcam y hacemos una instancia del objeto para guardarlo a rval y preguntar si existe
    while(not rval):
        (rval, frame) = webcam.read()
        if(not rval):
            print("Error en abrir webcam, intente de nuevo...")


    #guardamos "height" "width" y "channels" del objeto frame.shape
    height, width, channels = frame.shape

    #hacemos una instancia del objeto cv2.flip() y lo guardamos en el "frame"
    frame = cv2.flip(frame, 1, 0)

    #indicamos el color de las fotos que sacaremos
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

    faces = haar_cascade.detectMultiScale(mini)
    
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]

        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

        if(w * 6 < width or h * 6 < height):
            print("Tu cara es muy pequena")
        else:


            if(pause == 0):

                print(str(count+1)+"/"+str(count_max)+" imagenes guardadas")

                cv2.imwrite('%s/%s.png' % (path, pin), face_resize)

                pin += 1
                count += 1

                pause = 1

    if(pause > 0):
        pause = (pause + 1) % 5
    cv2.imshow('OpenCV', frame)
    if cv2.waitKey(1) and 0xFF == ord ('q'):
        break



