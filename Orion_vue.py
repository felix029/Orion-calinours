# -*- coding: utf-8 -*-
from tkinter import *
import random
import os,os.path
#from numpy.distutils.conv_template import file

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
        #self.posSouris=None
        self.root.title(os.path.basename(sys.argv[0]))
        self.modele=None
        self.nom=""
        self.cadreapp=Frame(self.root,width=800,height=600)
        self.cadreapp.pack()
        self.creercadresplash(ip,nom)
        self.creercadrelobby()
        self.changecadre(self.cadresplash)        
        self.vueactive = 2 # 0: vue planetaire, 1: vue systeme solaire, 2: vue galaxy
        self.etoileselect=None
        self.planeteselect=None
        self.flotteselect=None

    
    def fermerfenetre(self):
        self.parent.fermefenetre()

    def changecadre(self,cadre):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        self.cadreactif.pack()

    def creercadresplash(self,ip,nom):
        #Variables
        self.texteTitre = "Helvetica 20 bold"

        self.cadresplash=Frame(self.cadreapp)

        #Affichage d'un titre
        self.champ_Titre = Label(self.cadresplash,font = self.texteTitre,text = "ORION", anchor = W)
        self.champ_Titre.pack(side = TOP)

        self.canevassplash=Canvas(self.cadresplash,width=640,height=480,bg="dark blue")
        self.canevassplash.pack()

        self.nomsplash=Entry(bg="light grey")
        self.nomsplash.insert(0, nom)

        self.ipsplash=Entry(bg="light grey")
        self.ipsplash.insert(0, ip)

        labip=Label(text=ip,bg="light grey",borderwidth=0,relief=RIDGE)
        btncreerpartie=Button(text="Creer partie",bg="light grey",command=self.creerpartie)
        btnconnecterpartie=Button(text="Connecter partie",bg="light grey",command=self.connecterpartie)


        self.canevassplash.create_window(310,150,window=self.nomsplash,width=100,height=30)
        self.canevassplash.create_window(310,210,window=self.ipsplash,width=100,height=30)
        self.canevassplash.create_window(310,270,window=labip,width=100,height=30)
        self.canevassplash.create_window(310,330,window=btncreerpartie,width=100,height=30)
        self.canevassplash.create_window(310,390,window=btnconnecterpartie,width=100,height=30)


    def creercadrelobby(self):

        self.cadrelobby=Frame(self.cadreapp)

        #Affichage d'un titre
        self.champ_Titre = Label(self.cadrelobby,font = self.texteTitre,text = "Creation d'une partie", anchor = W)
        self.champ_Titre.pack(side = TOP)

        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480,bg="dark blue")
        self.canevaslobby.pack()

        self.listelobby=Listbox(bg="light grey",borderwidth=0,relief=FLAT)
        self.nbetoile=Entry(bg="light grey")
        self.nbetoile.insert(0, 100)
        self.largeespace=Entry(bg="light grey")
        self.largeespace.insert(0, 1000)
        self.hautespace=Entry(bg="light grey")
        self.hautespace.insert(0, 800)
        btnlancerpartie=Button(text="Lancer partie",bg="light grey",command=self.lancerpartie)
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

        self.simpleFont=("MS Sans Serif", 11, "bold")

        j=self.mod.joueurs[self.nom]
        
        for i in self.parent.modele.etoiles:
            if j.planetemere in i.planetes:
                self.etoileselect = i
                break

        self.planeteselect = j.planetemere

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
        #Cadre fonctionnalit�s (lowerLeftFrame)
        self.lowerLeftFrame=Frame(self.lowerFrame,width=150,height=625,bg="green")
        self.lowerLeftFrame.grid(row=0, column=0, rowspan=2, sticky="ns")

        #Zone Dessous-Droite
        #Cadre fonctionnalit�s (lowerRightFrame)
        self.lowerRightFrame=Frame(self.lowerFrame,width=150,height=625,bg="green")
        self.lowerRightFrame.grid(row=0, column=2, rowspan=2, sticky="ns")

        #Zone Dessous-Centre
        #Aire de jeu - Interstellaire
        self.canevas=Canvas(self.lowerFrame,width=800,height=600,bg="grey11")
        self.canevas.grid(row=0, column=1, sticky="ns")

        self.canevas.bind("<Button>",self.cliquecosmos) # Event MouseClick li� au canevas (Aire de jeu)

        #Zone Dessous-Dessous
        #Cadre fonctionnalit�s (lowerRightFrame)
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
        self.labid.bind("<Button>",self.afficherplanetemere)

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

        #Bouton pour modifier la vue
        #bouton zoom
        #self.boutonZoom = Button(self.cadreminimap,text="Zoom", bg="LightCyan3", borderwidth=None,font=self.simpleFont, pady=2, width= 25, height=3, cursor="hand2")
        self.boutonZoom = Button(self.cadreminimap,text="Vue suivante", bg="green2", width= 25, height=3, cursor="hand2", activebackground="red")
        self.boutonZoom.bind("<Button>")
        self.boutonZoom.grid(row=1, column=0, sticky="we")
        #bouton d�-zomm
        self.boutonDzoom=Button(self.cadreminimap,text="Vue precedente", bg="green2", width= 25, height=3, cursor="hand2", activebackground="red")
        self.boutonDzoom.bind("<Button>")
        self.boutonDzoom.grid(row=2, column=0, sticky="we")
        
        #Label d'affichage des atrributs d'une planète lors de la VUE_PLANÉTAIRE
        self.textMinerai =  StringVar()
        self.textMinerai = str("Minerai : ")
        self.attributMinerai = Label(self.cadreminimap,  width= 25, height=2, text=self.textMinerai , bg="white",borderwidth=1,font=self.simpleFont)
        self.attributMinerai.grid(row=3, column=0, sticky="we")

        self.textMinerai =  StringVar()
        self.textGaz = str("Gaz : ")
        self.attributGaz = Label(self.cadreminimap,  width= 25, height=2, text=self.textGaz, bg="white",borderwidth=1,font=self.simpleFont)
        self.attributGaz.grid(row=4, column=0, sticky="we")

        self.bindWidgets()
        self.afficherdecor(self.mod)
        self.changecadre(self.cadrepartie)

    def moveCanevas(self,evt):
        x=evt.x
        y=evt.y
        px=self.mod.largeur/x/100
        py=self.mod.hauteur/y/100
        self.canevas.xview(MOVETO,px)
        self.canevas.yview(MOVETO,py)
        print("SCROLL",px,py)

    def souris(self, event):
        self.posSouris = self.normInterprePos(COORD(event.x, event.y))

    def zoom (self, mod):
        if self.vueactive == 0:
            self.afficherdecor(self.mod)
        else:
            if (self.vueactive == 2 and self.etoileselect != None) or (self.vueactive == 1 and self.planeteselect != None):
                self.vueactive-=1
                self.afficherdecor(self.mod)
            else:
                print("Aucune planete ou etoile select")

    def dezoom (self, mod):
        if self.vueactive == 2:
            self.afficherdecor(self.mod)
        if self.vueactive == 1:
            self.vueactive+=1
            self.afficherdecor(self.mod)
            self.etoileselect=None
        if self.vueactive == 0:
            self.vueactive+=1
            self.afficherdecor(self.mod)
            self.planeteselect=None

    def bindWidgets(self):
        self.boutonZoom.config(command = lambda: self.zoom(self.mod))
        self.boutonDzoom.config(command = lambda: self.dezoom(self.mod))

    def afficherdecor(self, mod):

        self.canevas.delete(ALL)
        if self.vueactive == 2: #vue de la galaxy
            for i in range(len(mod.etoiles)*3):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))

            for i in mod.etoiles:
                t=i.taille
                self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                        tags=("etoile", str(i.id)))

        if self.vueactive == 1: #vue systeme solaire
            #self.etoileselect = random.choice(mod.etoiles)
            
            self.canevas.create_oval(-100, -100, 100, 100, fill="orange", tags=("soleil", "fond"))

            for i in self.etoileselect.planetes:
                t=i.taille
                self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                        tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))

            for i in mod.joueurs.keys():
                for j in mod.joueurs[i].planetescontrolees:
                    if j in self.etoileselect.planetes:
                        t=j.taille
                        self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=mod.joueurs[i].couleur,
                                            tags=("planete", str(j.id), j.proprietaire, str(self.etoileselect.id)))
            # dessine planetes IAs

            for i in mod.ias:
                for j in i.planetescontrolees:
                    if j in self.etoileselect.planetes:
                        t=j.taille
                        self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=i.couleur,
                                            tags=("planete", str(j.id), j.proprietaire, str(self.etoileselect.id)))

            #affichage de l'espace ou envoyer un vaisseau pour le retourner a la vue 2
            self.canevas.create_oval(mod.largeur-40, mod.hauteur-40, mod.largeur+40, mod.hauteur+40,fill="purple", tags=("retour2"))


        if self.vueactive == 0: #vue plan�te

            #affichage de l'espace ou envoyer un vaisseau pour le retourner a la vue 1
            self.canevas.create_oval(mod.largeur-40, mod.hauteur-40, mod.largeur+40, mod.hauteur+40,fill="purple", tags=("retour1"))

            t=self.planeteselect.taille
            self.canevas.create_oval(mod.largeur/2-(t*25),mod.hauteur/2-(t*25),mod.largeur/2+(t*25),mod.hauteur/2+(t*25), width=2, outline="white", fill=self.planeteselect.color,
                                    tags=("planetezoom", str(self.planeteselect.id), self.planeteselect.proprietaire, str(self.etoileselect.id)))
            #afficheAttributsPlanete(self.planeteselect)
            
            

################################################################################################ Charles
    def afficheAttributsPlanete(self, maselection, planeteselect=None, etoileselect=None):

        tag = self.maselection.tag[1]
        self.calculMinerai+=0
        self.calculGaz+=0

        if tag == "etoile":
            print(self.etoileselect)
            print(tag)
            for i in self.etoileselect.planetes:
                self.calculMinerai+=self.planeteselect.minerai
                self.calculGaz+=self.planeteselect.gaz
            
            print(str(self.calculMinerai))
            print(str(self.calculGaz))
            self.planeteselect.gaz
            self.planeteselect.minerai

        if tag == "planete":
            print(self.planeteselect)
            print(tag)
            self.planeteselect.gaz
            self.planeteselect.minerai
            self.attributMinerai.set(textvariable = "Minerai : " + str(self.planeteselect.minerai)) 
            self.attributGaz.set(textvariable = "Gaz : " + str(self.planeteselect.gaz)) 

        self.planeteselect.id
        self.planeteselect.propriétaire
        self.planeteselect.color
     
##########################################################################################################

    def afficherplanetemere(self,evt):
        if self.vueactive == 2:
            j=self.mod.joueurs[self.nom]
            
            for i in self.parent.modele.etoiles:
                if j.planetemere in i.planetes:
                    etoileplanetemere = i
                    break

            couleur=j.couleur
            x=etoileplanetemere.x
            y=etoileplanetemere.y
            t=30
            self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(3,3),width=2,outline=couleur,
                                 tags=("planetemere","marqueur"))


    def creervaisseau(self):
        print("Creer vaisseau")
        self.parent.creervaisseau()
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()
    
    def creerBatiment(self,event): #Ajouter le 9 avril par nic pour la creation d'un batiment        
        x=event.x
        y=event.y
        print("Creer batiment")

        joueur=self.parent.modele.joueurs[self.maselection[0]]
        for i in joueur.planetescontrolees:
            if i.id == int(self.maselection[2]):
                p=i.id

        self.parent.creerBatiment(p,"Minerai",x,y)
        self.maselection=None
        self.canevas.delete("marqueur")
        self.btncreerbatiment.pack_forget()
        
    def afficherpartie(self,mod):
        self.canevas.delete("artefact")

        if self.maselection!=None:

            #joueur=mod.joueurs[self.maselection[0]]
            #if self.maselection[0]=="etoile":
                #for i in joueur.planetescontrolees:
                    #if i.id == int(self.maselection[2]):
                        #x=i.x
                        #y=i.y
                        #t=10
                        #self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
                        #                         tags=("select","marqueur"))
            if self.maselection[0]=="flotte":
                for i in joueur.flotte:
                    if i.id == int(self.maselection[1]):
                        print(self.maselection)
                        x=i.x
                        y=i.y
                        t=10
                        self.canevas.create_rectangle(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
                                                 tags=("select","marqueur"))
        #else:
        #    self.canevas.delete("marqueur")


        for i in self.mod.joueurs.keys():
            i=mod.joueurs[i]
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                #self.canevas.create_rectangle(j.x,j.y,image=self.imgs["vaiss"],
                #                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))


        for i in self.mod.ias:
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-3,j.y-3,j.x+3,j.y+3,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))

    def cliquecosmos(self,evt):
        self.btncreervaisseau.pack_forget()
        tag=self.canevas.gettags(CURRENT)

        if self.vueactive == 2:
            if tag and tag[0] == "etoile":
                    self.maselection=[tag[0], tag[1]]
                    print(self.maselection)
                    for i in self.mod.etoiles:
                        if str(i.id) == self.maselection[1]:
                            self.etoileselect = i
                            #afficheAttributsPlanete(self.maselection, self.etoileselect)
                            break
                    if self.flotteselect != None:
                        self.parent.ciblerflotte(self.flotteselect.id, self.etoileselect.id)
                        print(self.flotteselect.id, self.etoileselect.id)
                        self.flotteselect = None
                        self.etoileselect = None

            if tag and tag[0] == "flotte":
                self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                print(self.maselection)
                j=self.mod.joueurs[self.nom]
                for i in j.flotte:
                    if i.id == int(self.maselection[1]):
                        self.flotteselect = i
                        break
        


        if self.vueactive == 1 or self.vueactive == 0:
            if tag and tag[0] == "planete":
                self.maselection=[tag[0], tag[1], tag[2]]
                print(self.maselection)
                for i in self.etoileselect.planetes:
                    if str(i.id) == tag[1]:
                        self.planeteselect = i
                        #afficheAttributsPlanete(self.maselection, self.planeteselect)
                        break

        self.maselection = None

        #else
            #1- clearer les sélection, dnc enlever les encadrer de sur les objet
            #2- faire en sorte de .pack_forget() les label inutiles
            #3- Reprinter les bouton avec une grosseur normale


###Code à clearer 
        #if t and t[0]==self.nom:
        #    self.maselection=self.canevas.find_withtag(CURRENT)#[0]
        #    self.maselection=[self.nom,t[1],t[2]]  #self.canevas.find_withtag(CURRENT)#[0]
        #    print(self.maselection)
        #    if t[1] == "etoile":
        #        self.montreetoileselection()
        #    elif t[1] == "flotte":
        #        self.montreflotteselection()
        #elif "etoile" in t and t[0]!=self.nom:
        #    if self.maselection:
        #        pass # attribuer cette etoile a la cible de la flotte selectionne
        #        self.parent.ciblerflotte(self.maselection[2],t[2])
        #    print("Cette etoile ne vous appartient pas - elle est a ",t[0])
        #    self.maselection=None
        #    self.lbselectecible.pack_forget()
        #    self.canevas.delete("marqueur")
        #else:
        #    print("Region inconnue")
        #    self.maselection=None
        #    self.lbselectecible.pack_forget()
        #    self.canevas.delete("marqueur")

    def montreetoileselection(self):
        self.btncreervaisseau.pack()
        self.btncreerbatiment.pack()
    def montreflotteselection(self):
        self.lbselectecible.pack()
    def afficherartefacts(self,joueurs):
        pass #print("ARTEFACTS de ",self.nom)
