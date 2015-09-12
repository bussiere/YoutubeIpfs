import os
import re
def listefile(subdirectory=''):
    liste = []
    if subdirectory:
        path = subdirectory
    else:
        path = os.getcwd()
    for root, dirs, names in os.walk(path):
         for filename in names:
            if filename == "models.py" :
                liste.append(os.path.join(root, filename))
    return liste

liste = listefile()
prog = re.compile("class.*")
print(liste)
for models in liste :
    classes = []
    f = open(models, 'r')
    for ligne in f:
        if prog.match(ligne):
            temp = ligne.replace("class ","")
            temp =  temp.split("(")[0]
            classes.append(temp)
    print (classes)
    app = models.split("/")[-2:][0]
    folder =  models.replace("/models.py","")
    f.close()

    importa = ""
    for ap in classes :
        importa += "%s,"%ap
  
    importa = importa[:-1]
    f = open("%s/admin.py"%folder, 'w')
    f.write("from django.contrib import admin\r\n")
    f.write("from %s.models import %s\r\n"%(app,importa))
    for ap in classes :
        ap = ap.replace(" ","")
        f.write("admin.site.register(%s)\r\n"%ap)
    f.close()
    print(app)
    print(folder)