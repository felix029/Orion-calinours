# -*- coding: utf-8 -*-
from tkinter import *

import random
import os,os.path

class Vue():
    def __init__(self,parent,ip,nom):
        self.parent=parent
        self.root=Tk()
        self.largeur=640
        self.hauteur=480
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.terrain=[]
        self.cadreactif=None
        self.maselection=None
        self.root.title(os.path.basename(sys.argv[0]))
        self.modele=None
        self.nom=""
        self.cadreapp=Frame(self.root,width=1100,height=700)
        self.cadreapp.pack()
        self.creercadresplash(ip,nom)
        self.creercadrelobby()
        self.changecadre(self.cadresplash)

    def fermerfenetre(self):
        self.parent.fermefenetre()

    def changecadre(self,cadre):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()

    def creercadresplash(self,ip,nom):
        self.cadresplash=Frame(self.cadreapp)
        self.canevassplash=Canvas(self.cadresplash,width=640,height=480,bg="red")
        self.canevassplash.pack()
        self.nomsplash=Entry(bg="pink")
        self.nomsplash.insert(0, nom)
        self.ipsplash=Entry(bg="pink")
        self.ipsplash.insert(0, ip)
        labip=Label(text=ip,bg="red",borderwidth=0,relief=RIDGE)
        btncreerpartie=Button(text="Creer partie",bg="pink",command=self.creerpartie)
        btnconnecterpartie=Button(text="Connecter partie",bg="pink",command=self.connecterpartie)
        self.canevassplash.create_window(200,200,window=self.nomsplash,width=100,height=30)
        self.canevassplash.create_window(200,250,window=self.ipsplash,width=100,height=30)
        self.canevassplash.create_window(200,300,window=labip,width=100,height=30)
        self.canevassplash.create_window(200,350,window=btncreerpartie,width=100,height=30)
        self.canevassplash.create_window(200,400,window=btnconnecterpartie,width=100,height=30)

    def creercadrelobby(self):
        self.cadrelobby=Frame(self.cadreapp)
        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480,bg="lightblue")
        self.canevaslobby.pack()
        self.listelobby=Listbox(bg="red",borderwidth=0,relief=FLAT)
        self.nbetoile=Entry(bg="pink")
        self.nbetoile.insert(0, 100)
        self.largeespace=Entry(bg="pink")
        self.largeespace.insert(0, 1000)
        self.hautespace=Entry(bg="pink")
        self.hautespace.insert(0, 800)
        btnlancerpartie=Button(text="Lancer partie",bg="pink",command=self.lancerpartie)
        self.canevaslobby.create_window(440,240,window=self.listelobby,width=200,height=400)
        self.canevaslobby.create_window(200,200,window=self.largeespace,width=100,height=30)
        self.canevaslobby.create_window(200,250,window=self.hautespace,width=100,height=30)
        self.canevaslobby.create_window(200,300,window=self.nbetoile,width=100,height=30)
        self.canevaslobby.create_window(200,400,window=btnlancerpartie,width=100,height=30)

    def connecterpartie(self):
        nom=self.nomsplash.get()
        ip=self.ipsplash.get()
        if nom and ip:
            self.parent.inscrirejoueur()
            self.changecadre(self.cadrelobby)
            print("BOUCLEATTENTE de CONNECTER")
            self.parent.boucleattente()

    def creerpartie(self):
        nom=self.nomsplash.get()
        ip=self.ipsplash.get()
        if nom and ip:
            self.parent.creerpartie()
            self.parent.inscrirejoueur()
            self.changecadre(self.cadrelobby)
            print("BOUCLEATTENTE de CREER")
            self.parent.boucleattente()

    def lancerpartie(self):
        self.parent.lancerpartie()

    def affichelisteparticipants(self,lj):
        self.listelobby.delete(0,END)
        self.listelobby.insert(0,lj)

    def creeraffichercadrepartie(self,mod):
        self.nom=self.parent.monnom
        self.mod=mod

        ##########################################################################
        #Zone globale
        self.cadrepartie=Frame(self.cadreapp)
        self.cadrejeu=Frame(self.cadrepartie)
        ##########################################################################
        #Zone Dessus
        #Cadre Statistiques (upperFrame)
        self.upperFrame=Frame(self.cadrepartie,width=1100,height=50,bg="black")
        self.upperFrame.grid(row=0, column=0, sticky="we")

        #Zone Dessous
        #Cadre perspectives (lowerFrame)
        self.lowerFrame=Frame(self.cadrepartie,width=1100,height=625,bg="red")
        self.lowerFrame.grid(row=2, column=0, sticky="ns")
        ###########################################################################
        #Sous-Zone Dessous

        #Zone Dessous-Gauche
        #Cadre fonctionnalités (lowerLeftFrame)
        self.lowerLeftFrame=Frame(self.lowerFrame,width=150,height=625,bg="green")
        self.lowerLeftFrame.grid(row=0, column=0, rowspan=2, sticky="ns")

        #Zone Dessous-Droite
        #Cadre fonctionnalités (lowerRightFrame)
        self.lowerRightFrame=Frame(self.lowerFrame,width=150,height=625,bg="green")
        self.lowerRightFrame.grid(row=0, column=2, rowspan=2, sticky="ns")

        #Zone Dessous-Centre
        #Aire de jeu - Interstellaire
        self.canevas=Canvas(self.lowerFrame,width=800,height=600,bg="grey11")
        self.canevas.grid(row=0, column=1, sticky="ns")

        self.canevas.bind("<Button>",self.cliquecosmos) # Event MouseClick lié au canevas (Aire de jeu)

        #Zone Dessous-Dessous
        #Cadre fonctionnalités (lowerRightFrame)
        self.lowerLowerFrame=Frame(self.lowerFrame,width=800,height=75,bg="blue")
        self.lowerLowerFrame.grid(row=1, column=1, sticky="ns")
        ###############################################################################
        #Sous-Zone Dessous-Gauche

        self.lowerLeftFrame.columnconfigure(0, minsize=150)

        #left Buttons
        self.btncreervaisseau=Button(self.lowerLeftFrame,text="Vaisseau",command=self.creervaisseau)
        self.btncreervaisseau.grid(row=0, column=0, sticky="we")

        #self.cadreinfo=Frame(self.rightFrame,width=200,height=200,bg="blue")
        #self.cadreinfo.grid(row=0, column=0, sticky="we")

        self.cadreinfogen=Frame(self.lowerRightFrame,width=150,height=200,bg="pink")
        self.cadreinfogen.grid(row=0, column=0, sticky="we")

        self.labid=Label(self.cadreinfogen,text=self.nom,fg=mod.joueurs[self.nom].couleur)
        self.labid.grid(row=0, column=0, sticky="we")
        self.labid.bind("<Button>",self.afficherplanemetemere)

        #self.cadreinfochoix=Frame(self.cadreinfo,height=200,width=200,bg="red")
        #self.cadreinfochoix.grid(row=1, column=0, sticky="we")


        #self.lbselectecible=Label(self.cadreinfo,text="Choisir cible",bg="yellow")
        #self.lbselectecible.grid(row=3, column=0, sticky="we")


        self.cadreminimap=Frame(self.lowerRightFrame,height=150,width=200,bg="green")
        self.cadreminimap.grid(row=1, column=0, sticky="we")
        self.canevasMini=Canvas(self.cadreminimap,width=200,height=200,bg="orange")
        self.canevasMini.grid(row=0, column=0, sticky="we")
        self.canevasMini.bind("<Button>",self.moveCanevas)


        self.afficherdecor(mod)

        self.changecadre(self.cadrepartie)

    def moveCanevas(self,evt):
        x=evt.x
        y=evt.y
        px=self.mod.largeur/x/100
        py=self.mod.hauteur/y/100
        self.canevas.xview(MOVETO,px)
        self.canevas.yview(MOVETO,py)
        print("SCROLL",px,py)

    def afficherdecor(self,mod):

        for i in range(len(mod.planetes)*3):
            x=random.randrange(mod.largeur)
            y=random.randrange(mod.hauteur)
            self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond",))

        for i in mod.planetes:
            t=i.taille
            self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                     tags=(i.proprietaire,"planete",str(i.id)))
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].planetescontrolees:
                t=j.taille
                self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=mod.joueurs[i].couleur,
                                     tags=(j.proprietaire,"planete",str(j.id),"possession"))
        # dessine IAs

        for i in mod.ias:
            for j in i.planetescontrolees:
                t=j.taille
                self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=i.couleur,
                                     tags=(j.proprietaire,"planete",str(j.id),"possession"))

        self.afficherpartie(mod)

    def afficherplanemetemere(self,evt):
        j=self.mod.joueurs[self.nom]
        couleur=j.couleur
        x=j.planetemere.x
        y=j.planetemere.y
        t=10
        self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(3,3),width=2,outline=couleur,
                                 tags=("planetemere","marqueur"))
    def creervaisseau(self):
        print("Creer vaisseau")
        self.parent.creervaisseau()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()

    def afficherpartie(self,mod):
        self.canevas.delete("artefact")

        if self.maselection!=None:
            joueur=mod.joueurs[self.maselection[0]]
            if self.maselection[1]=="planete":
                for i in joueur.planetescontrolees:
                    if i.id == int(self.maselection[2]):
                        x=i.x
                        y=i.y
                        t=10
                        self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
                                                 tags=("select","marqueur"))
            elif self.maselection[1]=="flotte":
                for i in joueur.flotte:
                    if i.id == int(self.maselection[2]):
                        x=i.x
                        y=i.y
                        t=10
                        self.canevas.create_rectangle(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
                                                 tags=("select","marqueur"))
        #else:
        #    self.canevas.delete("marqueur")


        for i in mod.joueurs.keys():
            i=mod.joueurs[i]
            for j in i.flotte:
                self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))

                #self.canevas.create_rectangle(j.x,j.y,image=self.imgs["vaiss"],
                #                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))


        for i in mod.ias:
            for j in i.flotte:
                self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))

    def cliquecosmos(self,evt):
        self.btncreervaisseau.pack_forget()
        t=self.canevas.gettags(CURRENT)
        if t and t[0]==self.nom:
            #self.maselection=self.canevas.find_withtag(CURRENT)#[0]
            self.maselection=[self.nom,t[1],t[2]]  #self.canevas.find_withtag(CURRENT)#[0]
            print(self.maselection)
            if t[1] == "planete":
                self.montreplaneteselection()
            elif t[1] == "flotte":
                self.montreflotteselection()
        elif "planete" in t and t[0]!=self.nom:
            if self.maselection:
                pass # attribuer cette planete a la cible de la flotte selectionne
                self.parent.ciblerflotte(self.maselection[2],t[2])
            print("Cette planete ne vous appartient pas - elle est a ",t[0])
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")
        else:
            print("Region inconnue")
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")

    def montreplaneteselection(self):
        self.btncreervaisseau.pack()
    def montreflotteselection(self):
        self.lbselectecible.pack()

    def afficherartefacts(self,joueurs):
        pass #print("ARTEFACTS de ",self.nom)


####################################################################################
##############  Classes pour les différentes perspectives de vue   #################
####################################################################################

class Planete():
    def __init__(self):
        self.root=Tk()

class Solaire():
    def __init__(self):
        self.root=Tk()

class Interstellaire():
    def __init__(self):
        self.root=Tk()