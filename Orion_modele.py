 # -*- coding: utf-8 -*-   
import random
from Id import Id
from helper import Helper as hlp

class Planete():
    def __init__(self,x,y):
        self.id=Id.prochainid()
        self.x=x
        self.y=y
        self.taille=random.randrange(7,12)
        self.gaz=random.randrange(4000, 10000)
        self.minerai=random.randrange(4000, 10000)
        self.proprietaire = ""
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
        self.taille=random.randrange(4,6)
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
        self.type = typeBatiment
        self.x = x
        self.y = y
        self.niveau = 1
        self.cout = 100
        self.nom=""
        self.etat=""

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
        self.delaidetir=5
        self.etat="actif"
       
    def avancer(self):
        if self.cible:
            x=self.cible.x
            y=self.cible.y
            ang=hlp.calcAngle(self.x,self.y,x,y)
            x1,y1=hlp.getAngledPoint(ang,self.vitesse,self.x,self.y)
            self.x,self.y=x1,y1 #int(x1),int(y1)
            if hlp.calcDistance(self.x,self.y,x,y) <=self.vitesse:
                if self.cible == Etoile:
                    print("Etoile: ", self.cible.id)
                if self.cible == Planete:
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
        elif self.cible.etat!="detruit":  ###ajouter le délai de tir
            p=Projectile(self.cible,self.x,self.y,self.cible.x,self.cible.y)
            self.projectiles.append(p)

        else:
            self.cible=None

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
        self.detruits=[]
        self.actions={"creervaisseau":self.creervaisseau,
                      "ameliorerBatiment":self.ameliorerBatiment,  #Ajouter le 9 avril par Nic
                      "vendreBatiment":self.vendreBatiment,  #Ajouter le 9 avril par Nic
                      "creerBatiment":self.creerBatiment,  #Ajouter le 9 avril par Nic
                      "ciblerflotte":self.ciblerflotte,
                      "detruire": self.detruire}
        
    def creervaisseau(self,params):
        #etoile,cible,type=params
        #is type=="explorer":
        v=Vaisseau(self.nom,self.planetemere.x+10,self.planetemere.y)
        print("Vaisseau",v.id)
        self.flotte.append(v)

    def creerBatiment(self,params): #Ajouter le 8 avril par nic

        indice = 0

        p,typeBatiment,x,y = params
        b = Batiment(self.nom,p,typeBatiment,x,y)
        print("Batiment",b.id)

        for i in self.planetescontrolees:
            if i.id == p:
                self.planetescontrolees[indice].batiment.append(b)
                indice += 1

    #Ajouter le 9 avril par nic
    def vendreBatiment(self,batiment): 
        self.minerai+=batiment.cout*0.5
        batiment.etat="detruit"

     #Ajouter le 9 avril par Nic
    def ameliorerBatiment(self,batiment):
        if batiment.cout <= self.minerai:
            self.minerai -= batiment.cout
            batiment.niveau += 1
        else:
            print("MANQUE ARGENT")

        
    def ciblerflotte(self,ids):
        idori,iddesti=ids
        for i in self.flotte:
            if i.id== int(idori):
                for j in self.parent.etoiles:
                    if j.id== int(iddesti):
                        i.cible=j
                        print("GOT TARGET")
                        return
        
        
    def prochaineaction(self):
        for i in self.flotte:
            if i.cible:
                i.avancer()
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
                        j.etat="detruit"
                        
            if i.projectiles:
                for j in i.projectiles:
                    if j.etat=="detruit":
                        self.detruits.append(j)


        for i in self.detruits:
            self.detruits.remove(i)

# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self,parent,nom,planetemere,couleur):
        Joueur.__init__(self, parent, nom, planetemere, couleur)  
        self.tempo=random.randrange(100)+20
        
    def prochaineaction(self):
        if self.flotte:
            for i in self.flotte:
                if i.cible:
                    i.avancer()
                else:
                    #i.cible=random.choice(self.parent.planetes)  
                    i.cible=random.choice(self.parent.etoiles)
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
        for i in range(200):
            x=random.randrange(self.largeur-(2*bordure))+bordure
            y=random.randrange(self.hauteur-(2*bordure))+bordure
            self.etoiles.append(Etoile(x,y,self))
    
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

    def modifRessource(self): 
        #Ajouter le 8 avril par nic ( Gere l'incrémentation des ressources des joueurs avec batiment et diminuer les ressource restante sur la planete du joueur)
        for j in self.joueurs:
            for p in j.planetes:
                for b in p.batiment:
                    if b.typeBatiment == "minerai":
                        j.minerai += b.niveau
                        p.minerai -= b.niveau
                    elif b.typeBatiment == "gaz":
                        j.gaz += b.niveau
                        p.gaz -= b.niveau
                    elif b.typeBatiment == "energie":
                        j.energie += b.niveau
        
 