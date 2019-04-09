 # -*- coding: utf-8 -*-   
import random
from Id import Id
from helper import Helper as hlp

class Planete():
    def __init__(self,x,y):
        self.id=Id.prochainid()
        self.x=x
        self.y=y
        self.taille=random.randrange(10,15)
        self.gas=random.randrange(4000, 10000)
        self.minerals=random.randrange(4000, 10000)
        self.proprietaire = ""
        self.colorsTab = [str(99%self.minerals), str(random.randrange(0,99)), str(99%self.gas)] 
        self.color = "#" + random.choice(self.colorsTab) + random.choice(self.colorsTab) + random.choice(self.colorsTab)
        
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
        bordure=1
        for i in range(20):
            planX=random.randrange(self.largeur-(2*bordure))+bordure
            planY=random.randrange(self.hauteur-(2*bordure))+bordure
            self.planetes.append(Planete(planX, planY))
        
class Vaisseau():
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
        
    def avancer(self):
        if self.cible:
            x=self.cible.x
            y=self.cible.y
            ang=hlp.calcAngle(self.x,self.y,x,y)
            x1,y1=hlp.getAngledPoint(ang,self.vitesse,self.x,self.y)
            self.x,self.y=x1,y1 #int(x1),int(y1)
            if hlp.calcDistance(self.x,self.y,x,y) <=self.vitesse:
                if  self.cible == Etoile:
                    print("Etoile: ", self.cible.id)
                if self.cible == Planete:
                    print("RESSOURCES...",self.cible.id,self.cible.ressource,self.cible.proprietaire)
                    self.cible.proprietaire=self.proprietaire
                #tempo=input("Continuersvp")
                self.cible=None
                #print("Change cible")
        else:
            print("PAS DE CIBLE")
    
    def avancer1(self):
        if self.cible:
            x=self.cible.x
            if self.x>x:
                self.x-=self.vitesse
            elif self.x<x:
                self.x+=self.vitesse
            
            y=self.cible.y
            if self.y>y:
                self.y-=self.vitesse
            elif self.y<y:
                self.y+=self.vitesse
            if abs(self.x-x)<(2*self.cible.taille) and abs(self.y-y)<(2*self.cible.taille):
                self.cible=None
                    
              
class Joueur():
    def __init__(self,parent,nom,planetemere,couleur):
        self.id=Id.prochainid()
        self.parent=parent
        self.nom=nom
        self.planetemere=planetemere
        self.planetemere.proprietaire=self.nom
        self.couleur=couleur
        self.planetescontrolees=[planetemere]
        self.flotte=[]
        self.actions={"creervaisseau":self.creervaisseau,
                      "ciblerflotte":self.ciblerflotte}
        
    def creervaisseau(self,params):
        #etoile,cible,type=params
        #is type=="explorer":
        v=Vaisseau(self.nom,self.planetemere.x+10,self.planetemere.y)
        print("Vaisseau",v.id)
        self.flotte.append(v)
        
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
            #    i.cible=random.choice(self.parent.etoiles)
            
    def prochaineaction2(self):
        for i in self.flotte:
            i.avancer()
    

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
            
 