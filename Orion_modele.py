 # -*- coding: utf-8 -*-
import random
from PIL import Image, ImageTk
from Id import Id
from helper import Helper as hlp

class Planete():
    def __init__(self,x,y):
        self.id=Id.prochainid()
        self.x=x
        self.y=y
        self.taille=random.randrange(13,17)
        #1- Génèrer un int aléatoire pour choisir une image de planète
        planetImage=random.randrange(1,11)
        #2- Créer une string représentant le chemin relatif de l'image, et ce, à l'aide du int aléatoire obtenu
        img="./images/planet"+str(planetImage)+".png"
        #3- Créer une variable image à l'aide de la fonction Image.open qui prend en paramètre le chemin relatif créé à l'étape précédente
        #       Pour ce faire, on utilise "Image" de la librairie "PIL" que l'on a importé
        planet1 = Image.open(img)
        #4- Redimensionner l'image et stocker le tout dans une nouvelle variable
        resized = planet1.resize((self.taille+30,self.taille+30),Image.ANTIALIAS)
        #5- Reformater la variable "Image" en variable "ImageTK" afin que TkInter la supporte, puis stocker le tout dans une variable d'instance "self.planetImage"
        self.planetImage = ImageTk.PhotoImage(resized)




        self.gaz=random.randrange(4000, 10000)
        self.minerai=random.randrange(4000, 10000)
        self.proprietaire = " "
        self.colorsTab = [self.minerai%10, random.randrange(4000,10000)%10, self.gaz%10, self.minerai%10, random.randrange(4000,10000)%10, self.gaz%10]
        self.color = "#" + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab)) + str(random.choice(self.colorsTab))
        self.setXY()
        self.batiment=[]

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
        numRand = random.randrange(7,10)
        for i in range(numRand):
            planX=random.randrange(150, 200)+(i*60)
            planY=random.randrange(150, 200)+(i*random.randrange(20,40))+10
            self.planetes.append(Planete(planX, planY))

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

class TourDefense():   ### GM 29 avril
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
        self.delaidetir=0
        self.delaimax=5
        self.cible=None
        self.range=10

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
            self.cible=None
            self.delaidetir=0

        for i in self.projectiles:
            if i.etat!="detruit":
                i.deplacer()

class Vaisseau():

    ###définition des types de vaisseaux [energie,vitesse, puissance de feu]
    typevaisseau={"chasseur":[100,3,10],
                    "cargo":[100,2,0],
                    "colonisateur":[150,1,0]}

    def __init__(self,nom,x,y):
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.x=x
        self.y=y
        self.cargo=0
        self.energie=100
        self.vitesse=2
        self.cible=None
        self.sysplanetecur=None
        self.planetecur=None
        self.typecible=""
        self.range=10
        self.projectiles=[]
        self.delaidetir=0
        self.delaimax=5 ###à modifier avec le dictionnaire si on fait d'autres vaisseaux
        self.etat="actif"
        self.attaquant=None

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
                elif self.cible == Planete:
                    print("RESSOURCES...",self.cible.id,self.cible.ressource,self.cible.proprietaire)
                    self.cible.proprietaire=self.proprietaire                #tempo=input("Continuersvp")

                self.cible=None
                #print("Change cible")
        else:
            print("PAS DE CIBLE")

    def tirer(self):
        d=hlp.calcDistance(self.x,self.y,self.cible.x,self.cible.y)
        if self.cible and d>self.range:
            self.avancer()
        elif self.cible.etat!="detruit":
            if self.delaidetir==0:
                if self.cible.attaquant==None:  ###ok
                    self.cible.attaquant=self
                p=Projectile(self.cible,self.x,self.y,self.cible.x,self.cible.y)
                self.projectiles.append(p)
                self.delaidetir=self.delaimax
            self.delaidetir-=1

        else:
            self.cible=None
            self.delaidetir=0
            self.typecible = None

        for i in self.projectiles:
            if i.etat!="detruit":
                i.deplacer()

    def defense(self):
        d=hlp.calcDistance(self.x,self.y,self.attaquant.x,self.attaquant.y)
        if self.attaquant and self.attaquant.etat!="detruit" and d<=self.range:
            if self.delaidetir==0:
                p=Projectile(self.attaquant,self.x,self.y,self.attaquant.x,self.attaquant.y)
                self.projectiles.append(p)
                self.delaidetir=self.delaimax
            self.delaidetir-=1

        elif self.attaquant.etat=="detruit":
            self.attaquant=None
            self.delaidetir=0

        for i in self.projectiles:
            if i.etat!="detruit":
                i.deplacer()

    def toucher(self,puissance):
        self.energie-=puissance
        if(self.energie<=0):
            self.etat="detruit"

class Projectile():
    ###définition des types de projectiles [puissance,vitesse, aire d'effet]
    #typeprojectile={"tetechercheuse":[25,15,0],
                    #"normal":[15,25,0],
                    #"grenade":[50,10,50]}

    def __init__(self,cible,x,y,ciblex,cibley):
        #self.choixprojectile=choixprojectile
        self.cible=cible
        self.x=x
        self.y=y
        self.ciblex=ciblex
        self.cibley=cibley
        self.puissance=20
        self.vitesse=5
        self.etat="actif"
        self.angle=hlp.calcAngle(self.x,self.y,self.ciblex,self.cibley)

    def deplacer(self):
            self.angle=hlp.calcAngle(self.x,self.y,self.ciblex,self.cibley)
            self.x,self.y=hlp.getAngledPoint(self.angle,self.vitesse, self.x, self.y)
            d=hlp.calcDistance(self.x,self.y,self.ciblex,self.cibley)
            if d<=self.vitesse:
                self.cible.toucher(self.puissance)
                print(self.cible.etat)
                print(self.cible.energie)
                self.etat="detruit"


class Joueur():
    def __init__(self,parent,nom,planetemere,couleur):
        self.id=Id.prochainid()
        self.parent=parent
        self.nom=nom
        self.planetemere=planetemere
        self.planetemere.proprietaire=self.nom
        self.couleur=couleur
        self.planetescontrolees=[planetemere]
        self.minerai = 0
        self.energie = 0
        self.gaz = 0
        self.flotte=[]
        self.ToursDefense=[] ####ajout GM 29 avril##
        self.detruits=[]
        self.joueurami=[]  ### id des joueurs ###
        self.actions={"creervaisseau":self.creervaisseau,
                      "upgBatiment":self.upgBatiment,  #Ajouter le 9 avril par Nic
                      "vendreBatiment":self.vendreBatiment,  #Ajouter le 9 avril par Nic
                      "creerBatiment":self.creerBatiment,  #Ajouter le 9 avril par Nic
                      "ciblerflotte":self.ciblerflotte,
                      "detruire": self.detruire,
                      "ciblerflotteplanete":self.ciblerflotteplanete, #Ajout Felix-O
                      "modifRessource":self.modifRessource,
                      "cibleretour":self.cibleretour, #Ajout Felix-O 16 avril
                      "versvue1":self.versvue1, #Ajout Felix-O 23 Avril
                      "versvue0":self.versvue0} #Ajout Felix-O 23 Avril

    def creervaisseau(self,params):
        #etoile,cible,type=params
        #is type=="explorer":
        v=Vaisseau(self.nom,self.planetemere.x+10,self.planetemere.y)
        print("Vaisseau",v.id)
        self.flotte.append(v)

    def creerBatiment(self,params): #Ajouter le 8 avril par nic

        p,typeBatiment,x,y = params

        b = Batiment(self.id,p,typeBatiment,x,y)
        print("Batiment",b.id)

        for i in self.planetescontrolees:
            if i.id == int(p):
                i.batiment.append(b)
                self.parent.parent.vue.afficherBatiment()

    #Ajouter le 9 avril par nic
    def vendreBatiment(self,batiment):
        self.minerai+=batiment.cout*0.5
        batiment.etat="detruit"

     #Ajouter le 9 avril par Nic
    def upgBatiment(self,idBatiment):
        for p in self.planetescontrolees:
            for b in p.batiment:
                if int(idBatiment[0]) == b.id:
                    b.vitesse += 1
                    self.parent.parent.vue.afficherBatiment()

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
                            print("GOT TARGET")
                            return
                elif typedestination == "flotte":
                    for j in self.parent.ias:
                        for k in j.flotte:
                            if k.id == int(iddesti):
                                print("TARGETED SHIP")
                                i.cible=k
                                i.typecible="Vaisseau"
                    for j in self.parent.joueurs:
                        for k in self.parent.joueurs[j].flotte:
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
                                print("GOT TARGET")
                                return
                for j in self.parent.ias:
                    for k in j.flotte:
                        if k.id == int(iddesti):
                            i.cible=k
                            i.typecible="Vaisseau"
                for j in self.parent.joueurs:
                    for k in self.parent.joueurs[j].flotte:
                        if k.id == int(iddesti):
                            i.cible=k
                            i.typecible="Vaisseau"

    def ciblerTourDefense(self):  #### Ajout Guillaume-29 avril, à voir si impact de performance###
        for i in self.ToursDefense:
            for j in self.parent.ias:
                if j.id not in self.joueurami:
                    for k in j.flotte:
                        d=hlp.calcDistance(i.x,i.y,k.x,k.y)
                        if d<=i.range:
                            i.cible=k
                            i.typecible="Vaisseau" ##peut-être pas nécessaire pour les tours
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
                ptemp=Planete(self.parent.largeur,self.parent.hauteur)
                ptemp.taille=0
                i.cible=ptemp

    def prochaineaction(self):

        self.modifRessource()
        #if self.detruits:
         #   self.detruire()
        self.detruire()
        for i in self.flotte:
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
                if i.projectiles:  ###assure la destruction des projectiles reliés au vaisseau détruit
                    for j in i.projectiles:
                        i.projectiles.remove(j)

            if i.projectiles:
                for j in i.projectiles:
                    if j.etat=="detruit":
                        i.projectiles.remove(j)


        for i in self.detruits:
            self.flotte.remove(i)
            self.detruits.remove(i)

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
                    #i.cible=random.choice(self.parent.planetes)
                    i.cible=random.choice(self.parent.etoiles)
                if i.attaquant:
                    i.defense()
        else:
            self.creervaisseau(0)

class Modele():
    def __init__(self,parent,joueurs):
        self.parent=parent
        self.largeur=800 #self.parent.vue.root.winfo_screenwidth()
        self.hauteur=600 #self.parent.vue.root.winfo_screenheight()
        self.joueurs={}
        self.ias=[]
        self.actionsafaire={}
        self.etoiles=[]
        self.terrain=[]
        self.xEtoile=[]
        self.yEtoile=[]
        self.creeretoiles()
        self.creerterrain()
        self.assignerplanetes(joueurs,2)

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
            x=random.randrange(0, self.largeur-10)
            y=random.randrange(0, self.hauteur-10)
            self.etoiles.append(Etoile(x,y,self))
       #     self.xEtoile[i]=random.randrange(self.largeur-(2*bordure))
        #    self.yEtoile[i]=random.randrange(self.hauteur-(2*bordure))
#
 #           for z in range(i):
  #              if self.xEtoile[i] - self.xEtoile[z] < 15 and self.yEtoile[i] - self.yEtoiley[z] < 15:
   #                 self.xEtoile[i] =  self.xEtoile[i] + 25
    #                self.yEtoile[i] =  self.yEtoile[i] + 25
     #       self.etoiles.append(Etoile(self.xEtoile[i],self.yEtoile[i],self))

    def assignerplanetes(self, joueurs, ias=1):
        np=len(joueurs)+ias
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
            self.joueurs[i]=Joueur(self,i,planetej.pop(0),couleurs.pop(0))

        # IA- creation des ias - max 2
        couleursia=["orange","green"]
        for i in range(ias):
            self.ias.append(IA(self,"IA_"+str(i),planetej.pop(0),couleursia.pop(0)))

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
        for i in self.ias:
            i.prochaineaction()
