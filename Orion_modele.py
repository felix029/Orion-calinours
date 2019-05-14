 # -*- coding: utf-8 -*-
import random
from PIL import Image, ImageTk
from Id import Id
from helper import Helper as hlp

class Planete():
    def __init__(self,x,y,etoileparent):
        self.id=Id.prochainid()
        self.x=x
        self.y=y
        self.taille=random.randrange(13,17)
        self.planeteImages=[];
        #1- Génèrer un int aléatoire pour choisir une image de planète
        planetImage=random.randrange(1,8)
        #2- Créer une string représentant le chemin relatif de l'image, et ce, à l'aide du int aléatoire obtenu
        img="./images/planet"+str(planetImage)+".png"
        #3- Créer une variable image à l'aide de la fonction Image.open qui prend en paramètre le chemin relatif créé à l'étape précédente
        #       Pour ce faire, on utilise "Image" de la librairie "PIL" que l'on a importé
        planet1 = Image.open(img)
        #4- Redimensionner l'image et stocker le tout dans une nouvelle variable
        #Vue système solaire
        resized = planet1.resize((self.taille+50,self.taille+50),Image.ANTIALIAS)
        self.planeteImages.append(ImageTk.PhotoImage(resized))
        #Vue planete
        resized = planet1.resize((550,550),Image.ANTIALIAS)
        self.planeteImages.append(ImageTk.PhotoImage(resized))
        #resized = planet1.resize((self.taille+50,self.taille+50),Image.ANTIALIAS)
        #5- Reformater la variable "Image" en variable "ImageTK" afin que TkInter la supporte, puis stocker le tout dans une variable d'instance "self.planetImage"
<<<<<<< HEAD
        #self.planetImage = ImageTk.PhotoImage(resized)




=======
        self.planetImage = ImageTk.PhotoImage(resized)
>>>>>>> encerclage des planète, des étoiles et des mines qui fonctionne
        self.gaz=random.randrange(4000, 10000)
        self.minerai=random.randrange(4000, 10000)
        self.proprietaire = " "
        self.colorsTab = [self.minerai%10, random.randrange(4000,10000)%10, self.gaz%10, self.minerai%10, random.randrange(4000,10000)%10, self.gaz%10]
        self.color = "#" + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab))
        self.setXY()
        self.batiment=[]
        self.toursDefense=[] ####ajout GM 29 avril##
        self.etoileparent=etoileparent

    #fonction qui va permettre aux planetes de ne pas etre par dessus le soleil
    def setXY(self):
        if self.x <=100:
            self.x+=100

        if self.y <=100:
            self.y+=100


class Etoile():
    def __init__(self,x,y,parent):
        self.id=Id.prochainid()
        self.x=x
        self.y=y
        self.taille=random.randrange(15,25)
        self.ressource=random.randrange(10)
        self.planetes=[]
        self.largeur = parent.largeur
        self.hauteur = parent.hauteur
        self.creerplanetes()

    def creerplanetes(self):
        bufferX=0
        bufferY=0
        numRand = random.randrange(5,8)
        for i in range(numRand):
            planX=random.randrange(150, 200)+bufferX
            planY=random.randrange(150, 200)+bufferY
            bufferX+=90
            bufferY+=75
            self.planetes.append(Planete(planX, planY, self))

class Batiment(): #Ajouter le 8 avril par nic
    def __init__(self,nom,plan,typeBatiment,x,y):
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.planete=plan
        self.typeBatiment = typeBatiment
        self.x = x
        self.y = y
        self.vitesse = 1
        self.nom=""
        self.etat=""

class TourDefense():   ### à ajouter git
    def __init__(self,nom,plan,x,y):
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.planete=plan
        self.x = x
        self.y = y
        self.cout = 100
        self.etat="" ##peut être inclu dans la destruction
        self.energie=100
        self.typecible=""
        self.projectiles=[]
        self.explosions=[]
        self.delaidetir=0
        self.delaimax=5
        self.cible=None
        self.range=10
        self.typeBatiment = "tourDefense"
        self.niveau = 1

    def tirer(self):  ###modifications GM 29 avril###
        d=hlp.calcDistance(self.x,self.y,self.cible.x,self.cible.y)

        if self.cible.etat!="detruit" and d<=self.range:
            if self.delaidetir==0:
                if self.cible.attaquant==None:  ###ok
                    self.cible.attaquant=self
                p=Projectile(self.cible,self.x,self.y,self.cible.x,self.cible.y)
                self.projectiles.append(p)
                self.delaidetir=self.delaimax
            self.delaidetir-=1

        else:
            ex=Explosion(self, self.cible.x,self.cible.y, False)
            self.explosions.append(ex)
            self.cible=None
            self.delaidetir=0

        for i in self.projectiles:
            if i.etat!="detruit":
                i.deplacer()
            else:
                ex=Explosion(self, i.x, i.y, True)
                self.explosions.append(ex)

class Vaisseau():

    ###définition des types de vaisseaux [energie,vitesse, puissance de feu]
    typevaisseau={"chasseur":[100,3,10],
                    "cargo":[100,2,0],
                    "colonisateur":[150,1,0]}

    def __init__(self,nom,etoile,planete):
        self.id=Id.prochainid()
        self.sysplanetecur=etoile
        self.planetecur=planete
        self.proprietaire=nom
        self.x=planete.x+10
        self.y=planete.y+10
        self.cargo=0
        self.energie=100
        self.vitesse=5
        self.cible=None
        self.typecible=""
        self.range=100
        self.projectiles=[]
        self.delaidetir=0
        self.delaimax=15 ###à modifier avec le dictionnaire si on fait d'autres vaisseaux
        self.etat="actif"
        self.attaquant=None
        self.explosions=[]

    def avancer(self):
        if self.cible:
            x=self.cible.x
            y=self.cible.y
            ang=hlp.calcAngle(self.x,self.y,x,y)
            x1,y1=hlp.getAngledPoint(ang,self.vitesse,self.x,self.y)
            self.x,self.y=x1,y1 #int(x1),int(y1)
            if hlp.calcDistance(self.x,self.y,x,y) <=self.vitesse:
                if self.typecible=="Vaisseau":
                    print("Vaisseau: ", self.cible.id)
                elif self.cible == Etoile:
                    print("Etoile: ", self.cible.id)
                elif isinstance(self.cible, Planete):
                    if self.cible.proprietaire==" ":
                        self.etat="colonisation"                  #tempo=input("Continuersvp")
                if self.etat!="colonisation":
                    self.cible=None
                #print("Change cible")
        else:
            print("PAS DE CIBLE")

    def tirer(self):
        d=hlp.calcDistance(self.x,self.y,self.cible.x,self.cible.y)
        if self.cible and d>self.range:
            self.avancer()
        elif isinstance(self.cible,Vaisseau):
            if self.cible.etat!="detruit":
                if self.delaidetir==0:
                    if self.cible.attaquant==None:
                        self.cible.attaquant=self
                    p=Projectile(self, self.cible,self.x,self.y,self.cible.x,self.cible.y)
                    self.projectiles.append(p)
                    self.delaidetir=self.delaimax
                self.delaidetir-=1

            elif self.cible.etat == "detruit":
                ex=Explosion(self, self.cible.x,self.cible.y, True)
                self.explosions.append(ex)
                self.cible=None
                self.delaidetir=0
                self.typecible=None

            for i in self.projectiles:
                if i.etat!="detruit":
                    i.deplacer()
                else:
                    ex=Explosion(self, i.x, i.y, True)
                    self.explosions.append(ex)
        else:
            self.typecible=""

    def defense(self):
        d=hlp.calcDistance(self.x,self.y,self.attaquant.x,self.attaquant.y)
        if self.attaquant and self.attaquant.etat!="detruit" and d<=self.range:
            if self.delaidetir==0:
                p=Projectile(self, self.attaquant,self.x,self.y,self.attaquant.x,self.attaquant.y)
                self.projectiles.append(p)
                self.delaidetir=self.delaimax
            self.delaidetir-=1

        elif self.attaquant.etat=="detruit":
            ex=Explosion(self, self.attaquant.x, self.attaquant.y, False)
            self.explosions.append(ex)
            self.attaquant=None
            self.delaidetir=0

        for i in self.projectiles:
            if i.etat!="detruit":
                i.deplacer()
            else:
                ex=Explosion(self, self.x, self.y, True)
                self.explosions.append(ex)

    def toucher(self,puissance):
        self.energie-=puissance
        ex=Explosion(self, self.x, self.y, True)
        self.explosions.append(ex)
        if self.energie<=0:
            ex=Explosion(self, self.x, self.y, False)
            self.explosions.append(ex)
            self.etat="detruit"


class Projectile():
    ###définition des types de projectiles [puissance,vitesse, aire d'effet]
    #typeprojectile={"tetechercheuse":[25,15,0],
                    #"normal":[15,25,0],
                    #"grenade":[50,10,50]}

    def __init__(self, parent, cible,x,y,ciblex,cibley):
        self.cible=cible
        self.x=x
        self.y=y
        self.ciblex=ciblex
        self.cibley=cibley
        self.parent=parent
        self.puissance=20
        self.proprietaire=self.parent.proprietaire
        self.sysplanetecur=self.parent.sysplanetecur
        self.planetecur=self.parent.planetecur
        self.vitesse=5
        self.etat="actif"
        self.angle=hlp.calcAngle(self.x,self.y,self.ciblex,self.cibley)

    def deplacer(self):
            self.angle=hlp.calcAngle(self.x,self.y,self.ciblex,self.cibley)
            self.x,self.y=hlp.getAngledPoint(self.angle,self.vitesse, self.x, self.y)
            d=hlp.calcDistance(self.x,self.y,self.ciblex,self.cibley)
            if d<=self.vitesse:
                self.cible.toucher(self.puissance)
                self.etat="detruit"



class Explosion():

    def __init__(self, parent, x, y, type):
        self.parent=parent
        self.x=x
        self.y=y
        self.proprietaire=self.parent.proprietaire
        self.sysplanetecur=self.parent.sysplanetecur
        self.planetecur=self.parent.planetecur
        self.etat="actif"
        self.vie=40
        self.etats=[]
        self.rayon=0
        self.type = type

        if self.type:
            self.rayon=5
        else:
            self.rayon=20

    # def exploToucher(self):
    #     e = Eclat(self, 360-(9*1), self.vitesse % 1, self.x, self.y, self.rangeEx)
    #     self.eclats.append(e)

    # def explose(self):
    #     self.vie =self.vie-1

    #     if self.vie <=0:
    #         self.etat="detruit"


# class Eclat():

#     def __init__(self, parent, orientation, vitesse, x, y, rangeEx):
#         self.x=x
#         self.y=y
#         self.xdep=x
#         self.ydep=y
#         self.parent=parent
#         self.proprietaire = self.parent.proprietaire
#         self.sysplanetecur=self.parent.sysplanetecur
#         self.planetecur=self.parent.planetecur
#         self.rangeEx = rangeEx/2
#         self.vitesse=vitesse
#         self.etat="actif"
#         self.orientation=orientation

#     def explose(self):
#             self.x,self.y=hlp.getAngledPoint(self.orientation,self.vitesse, self.x, self.y)

#             if self.y >=(self.ydep+self.rangeEx) and self.x >=(self.xdep+self.rangeEx):
#                 self.etat="detruit"
#                 print("explosion morte")
#                 self.parent.explose()


class Joueur():
    def __init__(self,parent,nom,planetemere,couleur,num):
        self.numNavette = num
        self.id=Id.prochainid()
        self.parent=parent
        self.nom=nom
        self.planetemere=planetemere
        self.planetemere.proprietaire=self.nom
        self.couleur=couleur
        self.planetescontrolees=[planetemere]
        self.minerai = 600
        self.energie = 600
        self.gaz = 600
        self.flotte=[]
        self.detruits=[]
        self.navetteImage=[]
        self.demandes=[]
        self.cout = {"minerai":[100,"energie"],
                    "gaz":[100,"energie"],
                    "energie":[100,"minerai"],
                    "upgminerai":[500,"minerai"],
                    "upggaz":[500,"minerai"],
                    "upgenergie":[500,"minerai"],
                    "vaisseau":[200,"minerai"]}
        self.joueurami=[]  ### id des joueurs ###
        self.actions={"creervaisseau":self.creervaisseau,
                      "upgBatiment":self.upgBatiment,  #Ajouter le 9 avril par Nic
                      "creerBatiment":self.creerBatiment,  #Ajouter le 9 avril par Nic
                      "ciblerflotte":self.ciblerflotte,
                      "detruire": self.detruire,
                      "ciblerflotteplanete":self.ciblerflotteplanete, #Ajout Felix-O
                      "modifRessource":self.modifRessource,
                      "cibleretour":self.cibleretour, #Ajout Felix-O 16 avril
                      "versvue1":self.versvue1, #Ajout Felix-O 23 Avril
                      "versvue0":self.versvue0,
                      "creerTourDefense":self.creerTourDefense,#Ajout Nick le 30 avril
                      "demandeAmi":self.demandeAmi} #Ajout Felix-O 14 mai

        #2- Créer une string représentant le chemin relatif de l'image, et ce, à l'aide du int aléatoire obtenu
        img="./images/navette"+str(self.numNavette)+".png"
        #3- Créer une variable image à l'aide de la fonction Image.open qui prend en paramètre le chemin relatif créé à l'étape précédente
        #       Pour ce faire, on utilise "Image" de la librairie "PIL" que l'on a importé
        navette = Image.open(img)
        #4- Redimensionner l'image et stocker le tout dans une nouvelle variable
        resized = navette.resize((50,50),Image.ANTIALIAS)
        self.navetteImage.append(ImageTk.PhotoImage(resized))
        #5- Reformater la variable "Image" en variable "ImageTK" afin que TkInter la supporte, puis stocker le tout dans une variable d'instance "self.planetImage"
        resized = navette.resize((30,30),Image.ANTIALIAS)
        self.navetteImage.append(ImageTk.PhotoImage(resized))

        resized = navette.resize((15,15),Image.ANTIALIAS)
        self.navetteImage.append(ImageTk.PhotoImage(resized))



    def creervaisseau(self,idplanete):
        #etoile,cible,type=params
        #is type=="explorer":
        if self.minerai >= self.cout["vaisseau"][0]:
            for i in self.parent.etoiles:
                for j in i.planetes:
                    if j.id == idplanete:
                        planetevaisseau = j
                        v=Vaisseau(self.nom,planetevaisseau.etoileparent,planetevaisseau)
                        self.minerai -= self.cout["vaisseau"][0]
                        print("Vaisseau",v.id)
                        self.flotte.append(v)
                        break
        else:
            print("MANQUE DE FOND")


    def creerBatiment(self,params): #Ajouter le 8 avril par nic

        p,typeBatiment,x,y = params

        if self.minerai >= self.cout[typeBatiment][0]:
            b = Batiment(self.id,p,typeBatiment,x,y)
            print("Batiment",b.id)

            for i in self.planetescontrolees:
                if i.id == int(p):
                    i.batiment.append(b)
                    self.parent.parent.vue.afficherBatiment()

            self.minerai -= self.cout[typeBatiment][0]
        else :
            print("MANQUE DE FOND")
            print(self.minerai)

    def creerTourDefense(self,params): #Ajouter le 8 avril par nic

        p,x,y = params

        b = TourDefense(self.id,p,x,y)
        print("tour defense",b.id)

        for i in self.planetescontrolees:
            if i.id == int(p):
                i.toursDefense.append(b)
                self.parent.parent.vue.afficherBatiment()

     #Ajouter le 9 avril par Nic
    def upgBatiment(self,idBatiment):
        for p in self.planetescontrolees:
            for b in p.batiment:
                if int(idBatiment) == b.id:
                    if self.cout["upg"+str(b.typeBatiment)][1] == "minerai":
                        if self.minerai >= self.cout["upg"+str(b.typeBatiment)][0]:
                            self.minerai -= self.cout["upg"+str(b.typeBatiment)][0]
                            b.vitesse += 1
                            self.parent.parent.vue.afficherBatiment()
                        else:
                            print("MANQUE DE FOND")
                    elif self.cout["upg"+str(b.typeBatiment)][1] == "energie":
                        if self.energie >= self.cout["upg"+str(b.typeBatiment)][0]:
                            self.energie -= self.cout["upg"+str(b.typeBatiment)][0]
                            b.vitesse += 1
                            self.parent.parent.vue.afficherBatiment()
                        else:
                            print("MANQUE DE FOND")
                    elif self.cout["upg"+str(b.typeBatiment)][1] == "gaz":
                        if self.gaz >= self.cout["upg"+str(b.typeBatiment)][0]:
                            self.gaz -= self.cout["upg"+str(b.typeBatiment)][0]
                            b.vitesse += 1
                            self.parent.parent.vue.afficherBatiment()
                        else:
                            print("MANQUE DE FOND")

    def modifRessource(self):
        #Ajouter le 8 avril par nic ( Gere l'incrémentation des ressources des joueurs avec batiment et diminuer les ressource restante sur la planete du joueur)
        for p in self.planetescontrolees:
            for b in p.batiment:
                if b.typeBatiment == "minerai":
                    if p.minerai-b.vitesse > 0:
                        self.minerai += b.vitesse
                        p.minerai -= b.vitesse
                    elif p.minerai > 0:
                        self.minerai += p.minerai
                        p.minerai -= p.minerai
                elif b.typeBatiment == "gaz":
                    if p.gaz-b.vitesse > 0:
                        self.gaz += b.vitesse
                        p.gaz -= b.vitesse
                    elif p.gaz > 0:
                        self.gaz += p.gaz
                        p.gaz -= p.gaz
                elif b.typeBatiment == "energie":
                    self.energie += b.vitesse

    def ciblerflotte(self,ids):
        idori,iddesti,typedestination=ids
        for i in self.flotte:
            if i.id== int(idori):
                if typedestination == "etoile":
                    for j in self.parent.etoiles:
                        if j.id== int(iddesti):
                            i.cible=j
                            self.typecible=""
                            print("GOT TARGET")
                            return
                elif typedestination == "flotte":
                    #for j in self.parent.ias:
                        #for k in j.flotte:
                        #    if k.id == int(iddesti):
                        #        print("TARGETED SHIP")

                        #        i.cible=k
                        #        i.typecible="Vaisseau"
                    for j in self.parent.joueurs:
                        for k in self.parent.joueurs[j].flotte:
                            if self.parent.joueurs[j]!= self:
                                if k.id == int(iddesti):
                                    print("TARGETED SHIP")
                                    i.cible=k
                                    i.typecible="Vaisseau"

    def ciblerflotteplanete(self,ids):
        idori,iddesti,etoile=ids
        for i in self.flotte:
            if i.id == int(idori):
                for e in self.parent.etoiles:
                    if e.id == int(etoile):
                        for j in e.planetes:
                            if j.id == int(iddesti):
                                i.cible=j
                                self.typecible=""
                                print("GOT TARGET")
                                return
                #for j in self.parent.ias:
                #    for k in j.flotte:
                #        if k.id == int(iddesti):
                #            i.cible=k
                #            i.typecible="Vaisseau"
                for j in self.parent.joueurs:
                    for k in self.parent.joueurs[j].flotte:
                        if k.id == int(iddesti):
                            i.cible=k
                            i.typecible="Vaisseau"

    def ciblerTourDefense(self):  #### Ajout Guillaume-29 avril, à voir si impact de performance###
        for i in self.ToursDefense:
            #for j in self.parent.ias:
            #    if j.id not in self.joueurami:
            #        for k in j.flotte:
            #            d=hlp.calcDistance(i.x,i.y,k.x,k.y)
            #            if d<=i.range:
            #                i.cible=k
            #                i.typecible="Vaisseau" ##peut-être pas nécessaire pour les tours
            for j in self.parent.joueurs:
                if self.parent.joueurs[j].id not in self.joueurami:
                    for k in self.parent.joueurs[j].flotte:
                        d=hlp.calcDistance(i.x,i.y,k.x,k.y)
                        if d<=i.range:
                            i.cible=k
                            i.typecible="Vaisseau"


    def cibleretour(self,idori):
        for i in self.flotte:
            if i.id == int(idori):
                ptemp=Planete(self.parent.largeur,self.parent.hauteur,None)
                ptemp.taille=0
                i.cible=ptemp

    def prochaineaction(self):

        self.modifRessource()
        #if self.detruits:
         #   self.detruire()
        self.detruire()
        self.colonisation()
        for i in self.flotte:
            if i.etat=="colonisation":
                i.cible=None
                i.etat=""
            if i.cible and i.typecible == "Vaisseau":
                i.tirer()
            elif i.cible:
                i.avancer()
                if i.x >= 796 and i.y >= 596:
                    if i.sysplanetecur != None and i.planetecur == None:
                        self.flotteretour2(i.id)
                    elif i.sysplanetecur != None and i.planetecur != None:
                        self.flotteretour1(i.id)
            if i.attaquant!=None:
                i.defense()
            #else:
            #    i.cible=random.choice(self.parent.planetes)
            #    i.cible=random.choice(self.parent.etoiles)



    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()

    def detruire(self):

        for i in self.flotte:
            if i.etat=="detruit":
                self.detruits.append(i)
                #self.flotte.remove(i)
                if i.projectiles:  ###assure la destruction des projectiles reliés au vaisseau détruit
                    for j in i.projectiles:
                        i.projectiles.remove(j)

            if i.projectiles:
                for j in i.projectiles:
                    if j.etat=="detruit":
                        i.projectiles.remove(j)

            if isinstance(i.cible, Vaisseau):
                if i.cible.etat == "detruit":
                    for j in i.projectiles:
                        i.projectiles.remove(j)


        for i in self.detruits:
            self.flotte.remove(i)
            self.detruits.remove(i)

    def colonisation(self):
        for i in self.flotte:
            if i.etat=="colonisation" and i.cible != None:
                i.cible.proprietaire=self.nom
                self.planetescontrolees.append(i.cible)
                i.cible.batiment.append(Batiment(self.id,i.cible.id,"base",400,300))
                i.etat="detruit"
            else:
                i.etat = " "




    #Ajout Felix-O 23 Avril
    def versvue1(self,ids):
        idflotte,idetoile=ids
        for i in self.flotte:
            if i.id == idflotte:
                flottecur = i
                break
        for e in self.parent.etoiles:
            if e.id == idetoile:
                flottecur.sysplanetecur = e
                flottecur.x = random.randrange(self.parent.largeur-50, self.parent.largeur)
                flottecur.y = random.randrange(self.parent.hauteur-50, self.parent.hauteur)
                break

    #Ajout Felix-O 23 Avril
    def versvue0(self,ids):
        idflotte,idplanete=ids
        for i in self.flotte:
            if i.id == idflotte:
                flottecur = i
                break
        syscur = flottecur.sysplanetecur
        for p in syscur.planetes:
            if p.id == idplanete:
                flottecur.planetecur = p
                flottecur.x = random.randrange(self.parent.largeur-50, self.parent.largeur)
                flottecur.y = random.randrange(self.parent.hauteur-50, self.parent.hauteur)
                break

    #Ajout Felix-O 23 Avril
    def flotteretour2(self,id):
        idflotte=id
        for i in self.flotte:
            if i.id == idflotte:
                flottecur = i
                break
        if flottecur.sysplanetecur != None:
            flottecur.x = flottecur.sysplanetecur.x+25
            flottecur.y = flottecur.sysplanetecur.y+25
            flottecur.sysplanetecur = None
            flottecur.cible = None


    #Ajout Felix-O 23 Avril
    def flotteretour1(self,id):
        idflotte=id
        for i in self.flotte:
            if i.id == idflotte:
                flottecur = i
                break

        if flottecur.planetecur != None:
            flottecur.x = flottecur.planetecur.x+25
            flottecur.y = flottecur.planetecur.y+25
            flottecur.planetecur = None
            flottecur.cible = None

    #Ajout Felix-O 14 mai
    def demandeAmi(self, infos):
        idjoueur=infos
        print("Dans demande ami modele" + self.nom)
        self.demandes.append(idjoueur)

# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self,parent,nom,planetemere,couleur):
        Joueur.__init__(self, parent, nom, planetemere, couleur)
        self.tempo=random.randrange(100)+20

    def prochaineaction(self):
        #if self.detruits:
         #   self.detruire()
        self.detruire()

        if self.flotte:
            for i in self.flotte:
                if i.cible:
                    i.avancer()
                else:
                    if i.sysplanetecur == None and i.planetecur == None:
                        #i.cible=random.choice(self.parent.planetes)
                        i.cible=random.choice(self.parent.etoiles)
                    else:
                        if i.x >= self.parent.largeur-8 and i.y >= self.parent.hauteur-8:
                            if i.sysplanetecur != None and i.planetecur != None:
                                self.flotteretour1(i.id)
                            elif i.sysplanetecur != None and i.planetecur == None:
                                self.flotteretour2(i.id)
                        else:
                            self.cibleretour(i.id)
                if i.attaquant:
                    i.defense()
        else:
            self.creervaisseau(self.planetemere.id)

        #if self.planetemere.batiment:
        #    print("FULL")
        #else:
        #    self.creerBatimentIA("minerai")

    def creerBatimentIA(self,typeBatiment):
        x = 50
        y = 50
        self.parent.parent.creerBatiment(self.planetemere.id,typeBatiment,x,y)

class Modele():
    def __init__(self,parent,joueurs):
        self.parent=parent
        self.largeur=800 #self.parent.vue.root.winfo_screenwidth()
        self.hauteur=600 #self.parent.vue.root.winfo_screenheight()
        self.joueurs={}
        #self.ias=[]
        self.actionsafaire={}
        self.etoiles=[]
        self.terrain=[]
        self.xEtoile=[]
        self.yEtoile=[]
        self.creeretoiles()
        self.creerterrain()
        self.numNavette=1
        self.assignerplanetes(joueurs,2)
        self.wrongValue=0
        #self.taileRayon=0

    def creerterrain(self):
        self.terrain=[]
        for i in range(10):
            ligne=[]
            for j in range(10):
                n=random.randrange(5)
                if n==0:
                    ligne.append(1)
                else:
                    ligne.append(0)
            self.terrain.append(ligne)

    def creeretoiles(self):
        bordure=0
        nbEtoile = 12
        #self.xEtoile = [nbEtoile+1]
        #self.yEtoile = [nbEtoile+1]
        for i in range(nbEtoile):
            x=random.randrange(20, self.largeur-20)
            y=random.randrange(20, self.hauteur-20)
            verifValue = True

            while verifValue:
                self.wrongValue=0
                #self.taileRayon = j.taille
                for j in self.etoiles:
                    if x > j.x-40 and x < j.x+40 and y > j.y-40 and y < j.y+40:
                        self.wrongValue+=1

                if self.wrongValue == 0:
                    self.etoiles.append(Etoile(x,y,self))
                    verifValue=False
                    break

                elif  self.wrongValue >= 1:
                    x=random.randrange(20,self.largeur-20) #largeur
                    y=random.randrange(20,self.hauteur-20) #hauteur
                    self.goodValue=0




       #     self.xEtoile[i]=random.randrange(self.largeur-(2*bordure))
        #    self.yEtoile[i]=random.randrange(self.hauteur-(2*bordure))
#
 #           for z in range(i):
  #              if self.xEtoile[i] - self.xEtoile[z] < 15 and self.yEtoile[i] - self.yEtoiley[z] < 15:
   #                 self.xEtoile[i] =  self.xEtoile[i] + 25
    #                self.yEtoile[i] =  self.yEtoile[i] + 25
     #       self.etoiles.append(Etoile(self.xEtoile[i],self.yEtoile[i],self))

    def assignerplanetes(self, joueurs, ias=1):
        np=len(joueurs)#+ias
        etoilej=[]
        planetej=[]
        while np != 0:
            e=random.choice(self.etoiles)
            if e not in etoilej:
                etoilej.append(e)
                p=random.choice(e.planetes)
                if p not in planetej:
                    planetej.append(p)
                np-=1
            else:
                np = np

        couleurs=["red","blue","lightgreen","yellow",
                  "lightblue","pink","gold","purple"]
        for i in joueurs:
            self.joueurs[i]=Joueur(self,i,planetej.pop(0),couleurs.pop(0), self.numNavette)
            self.numNavette +=1
            self.joueurs[i].planetescontrolees[0].batiment.append(Batiment(self.joueurs[i].id,planetej,"base",400,300))

        # IA- creation des ias - max 2
        #couleursia=["orange","green"]
        #for i in range(ias):
        #    self.ias.append(IA(self,"IA_"+str(i),planetej.pop(0),couleursia.pop(0)))

    def prochaineaction(self,cadre):
        if cadre in self.actionsafaire:
            for i in self.actionsafaire[cadre]:
                #print(i)
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                print("4- le modele distribue les actions au divers participants")
                print("4...- en executant l'action qui est identifie par i[1] le dico")
                print("4...- qui est dans l'attribut actions",i[0],i[1],i[2])
                print("NOTE: ici on applique immediatement cette action car elle consiste soit")
                print("NOTE... a changer la vitesse (accelere/arrete) soit l'angle de l'auto")
                print("NOTE... dans ce cas-ci faire la prochaine action (le prochain for en bas)")
                print("NOTE... c'est seulement changer la position de l'auto si sa vitesse est non-nul")
                """
            del self.actionsafaire[cadre]

        for i in self.joueurs:
            self.joueurs[i].prochaineaction()

        # IA- appelle prochaine action
        #for i in self.ias:
        #    i.prochaineaction()
