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
        self.cadreapp=Frame(self.root,width=800,height=600)
        self.cadreapp.pack()
        self.creercadresplash(ip,nom)
        self.creercadrelobby()
        self.changecadre(self.cadresplash)
        self.vueactive = 2 # 0: vue planétaire, 1: vue systeme planetaire, 2: vue galaxy
        self.etoileselect=None
        self.planeteselect=None

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
        self.cadrepartie=Frame(self.cadreapp)
        self.cadrejeu=Frame(self.cadrepartie)
        #self.scrollX=Scrollbar(self.cadrepartie,orientation=HORIZONTAL)
        #self.scrollY=Scrollbar(self.cadrepartie,orientation=VERTICAL)
        self.canevas=Canvas(self.cadrepartie,width=800,height=600,scrollregion=(0,0,mod.largeur,mod.hauteur),bg="grey11")
        #self.scrollX.
        self.canevas.pack(side=LEFT)
        self.canevas.bind("<Button>",self.cliquecosmos)

        self.cadreoutils=Frame(self.cadrepartie,width=200,height=200,bg="darkgrey")
        self.cadreoutils.pack(side=LEFT,fill=Y)

        self.cadreinfo=Frame(self.cadreoutils,width=200,height=200,bg="darkgrey")
        self.cadreinfo.pack(fill=Y)
        self.cadreinfogen=Frame(self.cadreinfo,width=200,height=200,bg="grey50")
        self.cadreinfogen.pack(padx=0, pady=0)
        self.labid=Label(self.cadreinfogen,text=self.nom,fg=mod.joueurs[self.nom].couleur)
        self.labid.bind("<Button>",self.afficherplanetemere)
        self.labid.pack(padx=0, pady=0)

        self.cadreinfochoix=Frame(self.cadreinfo,height=200,width=200,bg="grey30")
        self.cadreinfochoix.pack(padx=1, pady=1)
        self.btncreervaisseau=Button(self.cadreinfo,text="Vaisseau",command=self.creervaisseau)
        self.lbselectecible=Label(self.cadreinfo,text="Choisir cible",bg="darkgrey")
        self.lbselectecible.pack(padx=1, pady=1)

        self.cadreminimap=Frame(self.cadreoutils,height=200,width=200,bg="black")
        self.canevasMini=Canvas(self.cadreminimap,width=200,height=200,bg="pink")
        self.canevasMini.bind("<Button>",self.moveCanevas)
        self.canevasMini.pack(padx=0, pady=0)
        self.cadreminimap.pack(padx=0, pady=0)
        self.afficherdecor(self.mod)

        #try de bouton zoom
        self.boutonZoom = Button(self.cadreminimap,text="Zoom", bg="green2", width= 25, height=3, cursor="hand2", activebackground="red")
        self.boutonZoom.bind("<Button>")
        self.boutonZoom.pack(padx=1, pady=1)

        #try dde bouton dé-zomm
        self.boutonDzoom=Button(self.cadreminimap,text="Dé-zoom", bg="green2", width= 25, height=3, cursor="hand2", activebackground="red")
        self.boutonDzoom.bind("<Button>")
        self.boutonDzoom.pack(padx=1, pady=1)
        #fin du try de bouton

        self.changecadre(self.cadrepartie)

    def moveCanevas(self,evt):
        x=evt.x
        y=evt.y
        px=self.mod.largeur/x/100
        py=self.mod.hauteur/y/100
        self.canevas.xview(MOVETO,px)
        self.canevas.yview(MOVETO,py)
        print("SCROLL",px,py)

    def zoom (self, mod):
        self.vueactive-=1
        self.afficherdecor(self.mod)

    def dezoom (self, mod):
        self.vueactive+=1
        self.afficherdecor(self.mod)

    def bindWidgets(self):
        self.boutonZoom.config(command = self.zoom(self.mod))
        self.boutonDzoom.config(command = self.dezoom(self.mod))

    def afficherdecor(self, mod):

        if self.vueactive == 2: #vue de la galaxy
            for i in range(len(mod.etoiles)*3):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond",))

            for i in mod.etoiles:
                t=i.taille
                self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                        tags=("etoile",str(i.id)))

        if self.vueactive == 1: #vue systeme solaire
            self.etoileselect = random.choice(mod.etoiles)
            for i in self.etoileselect.planetes:
                t=i.taille
                self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                        tags=(i.proprietaire,"planete",str(i.id)))

            for i in mod.joueurs.keys():
                for j in mod.joueurs[i].planetescontrolees:
                    if j in self.etoileselect.planetes:
                        t=j.taille
                        self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=mod.joueurs[i].couleur,
                                            tags=(j.proprietaire,"planete",str(j.id),"possession"))
            # dessine IAs

            for i in mod.ias:
                for j in i.planetescontrolees:
                    if j in self.etoileselect.planetes:
                        t=j.taille
                        self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=i.couleur,
                                            tags=(j.proprietaire,"planete",str(j.id),"possession"))

        if self.vueactive == 0: #vue planète
            self.vueactive = 2

        #self.afficherpartie(mod)

    def afficherplanetemere(self,evt):
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
            if self.maselection[1]=="etoile":
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
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))
                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))
                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))

                #self.canevas.create_rectangle(j.x,j.y,image=self.imgs["vaiss"],
                #                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))


        for i in mod.ias:
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))
                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))
                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=(j.proprietaire,"flotte",str(j.id),"artefact"))

    def cliquecosmos(self,evt):
        self.btncreervaisseau.pack_forget()
        t=self.canevas.gettags(CURRENT)
        if t and t[0]==self.nom:
            #self.maselection=self.canevas.find_withtag(CURRENT)#[0]
            self.maselection=[self.nom,t[1],t[2]]  #self.canevas.find_withtag(CURRENT)#[0]
            print(self.maselection)
            if t[1] == "etoile":
                self.montreetoileselection()
            elif t[1] == "flotte":
                self.montreflotteselection()
        elif "etoile" in t and t[0]!=self.nom:
            if self.maselection:
                pass # attribuer cette etoile a la cible de la flotte selectionne
                self.parent.ciblerflotte(self.maselection[2],t[2])
            print("Cette etoile ne vous appartient pas - elle est a ",t[0])
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")
        else:
            print("Region inconnue")
            self.maselection=None
            self.lbselectecible.pack_forget()
            self.canevas.delete("marqueur")

    def montreetoileselection(self):
        self.btncreervaisseau.pack()
    def montreflotteselection(self):
        self.lbselectecible.pack()
    def afficherartefacts(self,joueurs):
        pass #print("ARTEFACTS de ",self.nom)
