#proyecto
import cv2, numpy, os
size = 2
#anadimos la instancia "haarcascade_frontalface_default.xml" en la variable "fn_haar"
fn_haar = 'haarcascade_frontalface_default.xml'
#anadimos la carpeta "recoFacial" a la variable fn_dir
fn_dir = 'recoFacial'

print('Cargando...')


(images, lables, names, id) = ([], [], {}, 0)

#creamos un loop con las variables "subdirs, dirs, files" en os.walk(fn_dir) que hara un recorido por la carpeta que le enviamos 
for (subdirs, dirs, files) in os.walk(fn_dir):
    #lopp "subdir" en dirs
    for subdir in dirs:
        names[id] = subdir
        #ingresamos a la carpeta "fn_dir" al sub directorio "subdir"
        subjectpath = os.path.join(fn_dir, subdir)

        for filename in os.listdir(subjectpath):

            f_name, f_extension = os.path.splitext(filename)
            if(f_extension.lower() not in['.png','.jpg','.jpeg','.gif','.pgm']):
                print("El archivo "+filename+" ha sido saltado, tipo incorrecto")
                continue
            path = subjectpath + '/' + filename
            lable = id
            
            #insertar la imagen leida por la camara al array "images"
            images.append(cv2.imread(path, 0))
            #convertir lable en entero al array "lables"
            lables.append(int(lable))
        id += 1
#inicializamos las variables "im_width, im_heigth" que son los valores del tamaño de la pantalla
(im_width, im_height) = (112, 92)
#hacemos un list comprehesion con numpy
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# model = cv2.face.FisherFaceRecognizer_create()
model = cv2.face.FisherFaceRecognizer_create()
model.train(images, lables)


haar_cascade = cv2.CascadeClassifier(fn_haar)
#instanciamos el objeto "cv2.VideoCapture(0)" en la variable webcam
webcam = cv2.VideoCapture(0)
while True:

    rval = False
    while(not rval):
            
        (rval, frame) = webcam.read()
        if(not rval):
            print("Error en abrir webcam, intente de nuevo...")
    #guardamos el frame detectado en la variable frame
    frame=cv2.flip(frame,1,0)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

    faces = haar_cascade.detectMultiScale(mini)
    for i in range(len(faces)):
        face_i = faces[i]

        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        prediction = model.predict(face_resize)
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        
        cara = '%s' % (names[prediction[0]])
        if cara[0] == 's':
            cv2.putText(frame,'Desconocido',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        else:
            cv2.putText(frame,'%s' % (names[prediction[0]]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

        

    cv2.imshow('OpenCV', frame)


    if cv2.waitKey(33) == 27:
        break

