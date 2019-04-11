 # -*- coding: utf-8 -*-   
import random
from Id import Id
from helper import Helper as hlp
        
class Planete():
    def __init__(self,x,y):
        self.id=Id.prochainid()
        self.proprietaire="inconnu"
        self.x=x
        self.y=y
        self.taille=random.randrange(4,6)
        self.minerai = 1000
        self.gaz = 1000
        self.batiment=[]

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
    def __init__(self,nom,x,y):   
        self.id=Id.prochainid()
        self.proprietaire=nom
        self.x=x
        self.y=y
        self.cargo=0
        self.energie=100
        self.vitesse=2
        self.cible=None 
       
    def avancer(self):
        if self.cible:
            x=self.cible.x
            y=self.cible.y
            ang=hlp.calcAngle(self.x,self.y,x,y)
            x1,y1=hlp.getAngledPoint(ang,self.vitesse,self.x,self.y)
            self.x,self.y=x1,y1 #int(x1),int(y1)
            if hlp.calcDistance(self.x,self.y,x,y) <=self.vitesse:
                self.cible.proprietaire=self.proprietaire
                #tempo=input("Continuersvp")
                self.cible=None
                #print("Change cible")
        else:
            print("PAS DE CIBLE")
              
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
        self.actions={"creervaisseau":self.creervaisseau,
                      "ameliorerBatiment":self.ameliorerBatiment,  #Ajouter le 9 avril par Nic
                      "vendreBatiment":self.vendreBatiment,  #Ajouter le 9 avril par Nic
                      "creerBatiment":self.creerBatiment,  #Ajouter le 9 avril par Nic
                      "ciblerflotte":self.ciblerflotte}
        
    def creervaisseau(self,params):
        #planete,cible,type=params
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
                for j in self.parent.planetes:
                    if j.id== int(iddesti):
                        i.cible=j
                        print("GOT TARGET")
                        return
        
        
    def prochaineaction(self):
        for i in self.flotte:
            if i.cible:
                i.avancer()
            #else:
                #i.cible=random.choice(self.parent.planetes)
            
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
                    i.cible=random.choice(self.parent.planetes)
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
        self.planetes=[]
        self.terrain=[]
        self.creerplanetes(joueurs,2)
        self.creerterrain()
        
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
        
    def creerplanetes(self,joueurs,ias=1):
        bordure=0
        for i in range(200):
            x=random.randrange(self.largeur-(2*bordure))+bordure
            y=random.randrange(self.hauteur-(2*bordure))+bordure
            self.planetes.append(Planete(x,y))
        np=len(joueurs)+ias
        planes=[]
        while np:
            p=random.choice(self.planetes)
            if p not in planes:
                planes.append(p)
                self.planetes.remove(p)
                np-=1
        couleurs=["red","blue","lightgreen","yellow",
                  "lightblue","pink","gold","purple"]
        for i in joueurs:
            self.joueurs[i]=Joueur(self,i,planes.pop(0),couleurs.pop(0))
        
        # IA- creation des ias - max 2 
        couleursia=["orange","green"]
        for i in range(ias):
            self.ias.append(IA(self,"IA_"+str(i),planes.pop(0),couleursia.pop(0)))  
            
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
        
 