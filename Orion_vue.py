# -*- coding: utf-8 -*-
from tkinter import *
from PIL import Image, ImageOps, ImageTk, ImageChops
import random
import os,os.path
from PIL.ImageOps import expand
from PIL._imaging import font
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
        #self.modele=self.parent.modele
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
        self.selectionBatiment=None
        self.batimentChoisi="minerai"
        self.upgBatiment= None

        self.couleurLabelMenu  = "white"
        self.couleurBackgroundMenu  = "gray27"
        self.couleurBackgroundCotes = "SteelBlue4"
        self.espacementDonneesMenu = 20


        ###################################################
        #             Images redimensionnées              #
        ###################################################
        self.plan = Image.open("./images/planete.png")
        self.resized = self.plan.resize((30, 30),Image.ANTIALIAS)
        self.planete = ImageTk.PhotoImage(self.resized)

        self.electricite = Image.open("./images/electricite.png")
        self.resized = self.electricite.resize((30, 30),Image.ANTIALIAS)
        self.light = ImageTk.PhotoImage(self.resized)

        self.rock = Image.open("./images/rock.png")
        self.resized = self.rock.resize((30, 30),Image.ANTIALIAS)
        self.minerais = ImageTk.PhotoImage(self.resized)

        self.gas = Image.open("./images/gas.png")
        self.resized = self.gas.resize((30, 30),Image.ANTIALIAS)
        self.gaz = ImageTk.PhotoImage(self.resized)

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
        ##########################################################################
        #                          Principaux Frames                             #
        ##########################################################################
        #Zone globale
        self.cadrepartie=Frame(self.cadreapp)
        self.cadrejeu=Frame(self.cadrepartie)
        ##########################################################################
        #Zone Dessus    KIM:)
        #Cadre Statistiques (upperFrame)
        self.upperFrame=Frame(self.cadrepartie,width=1100,height=50,bg= self.couleurBackgroundMenu)
        self.upperFrame.grid(row=0, column=0, sticky="we")

        self.espaceVide0 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=1)

        self.lab_planete = Label(self.upperFrame, image = self.planete, bg = self.couleurBackgroundMenu)
        self.lblPlanConquises=Label(self.upperFrame,text="Planètes conquises: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu)
        self.lab_planete.grid(row=0, column=2)
        self.lblPlanConquises.grid(row=0, column=3)

        self.espaceVide1 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=4)

        self.lab_eclair = Label(self.upperFrame, image = self.light, bg = self.couleurBackgroundMenu)
        self.lblElectricite=Label(self.upperFrame,text="Électricité: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu)
        self.lab_eclair.grid(row=0, column=5)
        self.lblElectricite.grid(row=0, column=6)

        self.espaceVide2 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=7)

        self.lab_rock = Label(self.upperFrame, image = self.minerais, bg = self.couleurBackgroundMenu)
        self.lblMinerais=Label(self.upperFrame,text="Minerais: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu)
        self.lab_rock.grid(row=0, column=8)
        self.lblMinerais.grid(row=0, column=9)

        self.espaceVide3 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=10)

        self.lab_gaz = Label(self.upperFrame, image = self.gaz, bg = self.couleurBackgroundMenu)
        self.lblGaz=Label(self.upperFrame,text="Gaz: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu)
        self.lab_gaz.grid(row=0, column=11)
        self.lblGaz.grid(row=0, column=12)


        #Zone Dessous
        #Cadre perspectives (lowerFrame)
        self.lowerFrame=Frame(self.cadrepartie,width=1100,height=625,bg="red")
        self.lowerFrame.grid(row=2, column=0, sticky="ns")
        ###########################################################################
        ###########################################################################

        ###########################################################################
        ###########################################################################
        #                              Aire de jeu                                #
        #                            Ne pas toucher!                              #
        ###########################################################################
        #
        self.canevas=Canvas(self.lowerFrame,width=800,height=600,bg="grey11")
        self.canevas.grid(row=0, column=1, sticky="ns")

        self.canevas.bind("<Button>",self.cliquecosmos) # Event MouseClick li� au canevas (Aire de jeu)
        ############################################################################
        #############################################################################




        ###########################################################################
        #                           Frames de travail                             #
        #                       (Sous-Zone de "lowerFrame")                       #
        ###########################################################################
        ###########################################################################

        ###########################################################################
        #                           Zone Dessous-Gauche                           #
        ###########################################################################
        #lowerLeftFrame
        self.lowerLeftFrame=Frame(self.lowerFrame,width=150,height=625,bg="pink")
        self.lowerLeftFrame.grid(row=0, column=0, sticky="ns")
        self.lowerLeftFrame.columnconfigure(0, minsize=150)
        self.lowerLeftFrame.grid_propagate(0)
        #self.lowerLeftFrame.rowconfigure(0, minsize=313)
        #self.lowerLeftFrame.rowconfigure(1, minsize=313)

        #Labels et sous-frames du lowerLeftFrame
        #Frames creation et upgrade
        self.creationFrame=Frame(self.lowerLeftFrame,width=150, height=313, bg="blue")
        self.creationFrame.grid(row=0, column=0, sticky="ns")
        self.creationFrame.grid_propagate(0)
        self.upgradeFrame=Frame(self.lowerLeftFrame,width=150, height=312, bg="black")
        self.upgradeFrame.grid(row=1, column=0, sticky="ns")
        self.upgradeFrame.grid_propagate(0)

        self.creationFrame.columnconfigure(0, minsize=150)
        self.upgradeFrame.columnconfigure(0, minsize=150)

        #Label Creation
        self.creationLabel = Label(self.creationFrame, text="CREATION", anchor='center', fg="white", bg='#34344f')
        self.creationLabel.grid(row=0, column=0, sticky="we")
        self.vaisseauLabel = Label(self.creationFrame, text="Vaisseau", anchor='center', fg="white", bg='#34344f')
        self.vaisseauLabel.grid(row=1, column=0, sticky="we")
        self.batimentLabel = Label(self.creationFrame, text="Bâtiments", anchor='center', fg="white", bg='#34344f')
        self.batimentLabel.grid(row=3, column=0, sticky="we")

        #Label Upgrade
        self.upgLabel = Label(self.upgradeFrame, text="UPGRADE", anchor='center', fg="white", bg='#34344f')
        self.upgLabel.grid(row=0, column=0, sticky="we")
        self.upgVaisseauLabel = Label(self.upgradeFrame, text="Vaisseau", anchor='center', fg="white", bg='#34344f')
        self.upgVaisseauLabel.grid(row=1, column=0, sticky="we")
        self.upgBatimentLabel = Label(self.upgradeFrame, text="Bâtiments", anchor='center', fg="white", bg='#34344f')
        self.upgBatimentLabel.grid(row=3, column=0, sticky="we")







        #Boutons du lowerLeftFrame
        #Boutons du creationFrame
        self.btncreervaisseau=Button(self.creationFrame,text="Vaisseau",command=self.creervaisseau)
        self.btncreervaisseau.grid(row=2, column=0, sticky="we")
        self.btncreervaisseau.config(height=3)

        self.mines=Button(self.creationFrame,text="Mine")
        self.mines.grid(row=4, column=0, sticky="we")
        self.mines.config(height=3)
        self.mines.bind("<Button>", self.initMine)

        self.extracteurs=Button(self.creationFrame,text="Gaz")
        self.extracteurs.grid(row=5, column=0, sticky="we")
        self.extracteurs.config(height=3)
        self.extracteurs.bind("<Button>", self.initGaz)

        self.electricite=Button(self.creationFrame,text="Électricité")
        self.electricite.grid(row=6, column=0, sticky="we")
        self.electricite.config(height=3)
        self.electricite.bind("<Button>", self.initEnergie)

        #Boutons du upgradeFrame
        self.upgVaisseau=Button(self.upgradeFrame,text="Upg Vaisseau")
        self.upgVaisseau.grid(row=2, column=0, sticky="we")
        self.upgVaisseau.config(height=3)
        self.upgMines=Button(self.upgradeFrame,text="Upg Mines",command=self.upgradeBatiment)
        self.upgMines.grid(row=4, column=0, sticky="we")
        self.upgMines.config(height=3)
        #self.upgExtracteurs=Button(self.upgradeFrame,text="Upg Extracteurs",command=self.upgradeBatiment) Pas besoin de 3 boutons pour upgrade un batiment
        #self.upgExtracteurs.grid(row=5, column=0, sticky="we")
        #self.upgExtracteurs.config(height=3)
        #self.upgElectricite=Button(self.upgradeFrame,text="Upg Électricité",command=self.upgradeBatiment)
        #self.upgElectricite.grid(row=6, column=0, sticky="we")
        #self.upgElectricite.config(height=3)

        #self.cadreinfo=Frame(self.rightFrame,width=200,height=200,bg="blue")
        #self.cadreinfo.grid(row=0, column=0, sticky="we")





        ###########################################################################

        ###########################################################################
        #                            Zone Dessous-Droite                          #
        ###########################################################################
        #lowerRightFrame
        self.lowerRightFrame=Frame(self.lowerFrame,width=150,height=626,bg="green")
        self.lowerRightFrame.grid(row=0, column=2, rowspan=2, sticky="ns")

        #Labels  et sous-frames du lowerRighttFrame

        self.cadreinfogen=Frame(self.lowerRightFrame,width=150,height=200,bg=self.couleurBackgroundCotes)
        self.cadreinfogen.grid(row=0, column=0, sticky="we")


        self.lblJoueurs = Label(self.cadreinfogen, text=" .: AUTRES JOUEURS :. ",fg="white", bg=self.couleurBackgroundCotes)
        self.lblJoueurs.grid(row=1,column=1,sticky="we")


        self.labid=Label(self.cadreinfogen,text=self.nom,fg=mod.joueurs[self.nom].couleur,bg=self.couleurBackgroundCotes)
        self.labid.grid(row=2, column=0, sticky="we")


        self.cadreminimap=Frame(self.lowerRightFrame,height=150,width=200,bg="green")
        self.cadreminimap.grid(row=3, column=0, sticky="we")

        self.canevasMini=Canvas(self.cadreminimap,width=200,height=200,bg="orange")
        self.canevasMini.grid(row=4, column=0, sticky="we")
        self.canevasMini.bind("<Button>",self.moveCanevas)



        #Boutons du lowerRightFrame
        self.labid.bind("<Button>",self.afficherplanetemere)
        self.canevasMini.bind("<Button>",self.moveCanevas)



        ##############################################################################
        #                             Zone Dessous-Dessous                           #
        ##############################################################################
        #################################################Charles!!!!!!#####################################################
        #lowerLowerFrame
        self.lowerLowerFrame=Frame(self.lowerFrame,width=800,height=75,bg="blue")
        self.lowerLowerFrame.grid(row=1, column=1, sticky="ns")

        #Labels du lowerLeftFrame
        #Bouton pour modifier la vue
        #bouton zoom
        #self.boutonZoom = Button(self.cadreminimap,text="Zoom", bg="LightCyan3", borderwidth=None,font=self.simpleFont, pady=2, width= 25, height=3, cursor="hand2")
        self.boutonZoom = Button(self.lowerLowerFrame,text="Vue suivante", bg="#003182", width= 56, height=2, cursor="hand2", activebackground="red", fg="white")
        self.boutonZoom.bind("<Button>")
        self.boutonZoom.grid(row=0, column=1)
        #bouton d�-zomm
        self.boutonDzoom=Button(self.lowerLowerFrame,text="Vue precedente", bg="#003182", width= 56, height=2, cursor="hand2", activebackground="red", fg="white")
        self.boutonDzoom.bind("<Button>")
        self.boutonDzoom.grid(row=0, column=0)





        #Boutons du lowerLeftFrame






        ###############################################################################


        #self.cadreinfo=Frame(self.rightFrame,width=200,height=200,bg="blue")
        #self.cadreinfo.grid(row=0, column=0, sticky="we")
        #self.cadreinfochoix=Frame(self.cadreinfo,height=200,width=200,bg="red")
        #self.cadreinfochoix.grid(row=1, column=0, sticky="we")
        #self.lbselectecible=Label(self.cadreinfo,text="Choisir cible",bg="yellow")
        #self.lbselectecible.grid(row=3, column=0, sticky="we")




        self.afficherdecor(mod)
        self.changecadre(self.cadrepartie)        #Label d'affichage des atrributs d'une planète lors de la VUE_PLANÉTAIRE
        self.textGeneriquePlanete =  StringVar()
        self.textMinerai =  StringVar()
        self.textGaz = StringVar()
        self.attributMineraiEtoile = 0
        self.attributGazEtoile = 0

        self.attributPlaneteSelectionne = Label(self.cadreminimap,  width= 25, height=10, bg="white",borderwidth=1,font=self.simpleFont)
        self.attributPlaneteSelectionne.grid(row=3, column=0, sticky="we")

        self.textMinerai =  StringVar()
        self.attributMinerai = Label(self.cadreminimap,  width= 25, height=2, bg="white",borderwidth=1,font=self.simpleFont)
        self.attributMinerai.grid(row=4, column=0, sticky="we")

        self.attributGaz = Label(self.cadreminimap,  width= 25, height=2, bg="white",borderwidth=1,font=self.simpleFont)
        self.attributGaz.grid(row=5, column=0, sticky="we")

        self.afficherdecor(mod)

        self.bindWidgets()
        self.afficherdecor(self.mod)
        self.changecadre(self.cadrepartie)


    def bindWidgets(self):
        self.boutonZoom.config(command = lambda: self.zoom(self.mod))
        self.boutonDzoom.config(command = lambda: self.dezoom(self.mod))
        self.etatBouton()

    def etatBouton(self):

        self.attributPlaneteSelectionne.grid_forget()
        self.attributMinerai.grid_forget()
        self.attributGaz.grid_forget()
        self.boutonZoom.grid_forget()
        self.boutonDzoom.grid_forget()

        if self.vueactive==2:
            self.boutonZoom.config(width=113, text = "Vue du système solaire", border=4)
            self.boutonZoom.grid(row=0, column=0, sticky="we")

        elif self.vueactive == 1:
            self.attributMineraiEtoile = 0
            self.attributGazEtoile = 0
            self.boutonZoom.config(width = 56, text = "Vue planétaire", border=2)
            self.boutonDzoom.config(width = 56, text = "Vue de la galaxie", border=2)
            self.boutonZoom.grid(row=0, column=1, sticky="we")
            self.boutonDzoom.grid(row=0, column=0, sticky="we")

            for i in self.etoileselect.planetes:
                self.attributMineraiEtoile+= i.minerai
                self.attributGazEtoile+= i.gaz

            self.textGeneriquePlanete = "\n\n\n\nL'étoile possède :  \n"
            self.textMinerai = "Minerai : " + str (self.attributMineraiEtoile) + "\n"
            self.textGaz = "Gaz : " + str(self.attributGazEtoile) + "\n"
            self.attributPlaneteSelectionne.config(text =  self.textGeneriquePlanete + self.textMinerai + self.textGaz )
            self.attributPlaneteSelectionne.grid(row = 3)


        elif self.vueactive == 0:
            self.boutonDzoom.config(width=113, text = "Vue du système solaire", border=4)
            self.boutonDzoom.grid(row=1, column=0, sticky="we")

            if self.planeteselect.proprietaire == " ":
                self.textGeneriquePlanete = "Aucun propriétaire" + "\n\n\n\nLa planète possède :  \n"
            else:
                self.textGeneriquePlanete = "Le propriétaire de la planète est\n " + self.planeteselect.proprietaire + "\n\n\n\nLa planète possède :  \n"

            self.textMinerai = "Minerai : " + str (self.planeteselect.minerai) + "\n"
            self.textGaz = "Gaz : " + str(self.planeteselect.gaz) + "\n"
            self.attributPlaneteSelectionne.config(text =  self.textGeneriquePlanete + self.textMinerai + self.textGaz )
            self.attributPlaneteSelectionne.grid(row = 3)


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
        self.etatBouton()

    def dezoom (self, mod):
        if self.vueactive == 2:
            self.vueactive= 2
            self.afficherdecor(self.mod)
            self.etatBouton()

        elif self.vueactive == 1:
            self.vueactive=2
            self.afficherdecor(self.mod)
            self.etatBouton()
            self.etoileselect=None
            self.flotteselect=None
        elif self.vueactive == 0:
            self.vueactive=1
            self.afficherdecor(self.mod)
            self.etatBouton()
            self.planeteselect=None
            self.flotteselect=None
        self.etatBouton()


    def afficherdecor(self, mod):

        self.canevas.delete(ALL)
        if self.vueactive == 2: #vue de la galaxy
            for i in range(len(mod.etoiles)*5):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))

            for i in mod.etoiles:
                t=i.taille
                self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                        tags=("etoile", str(i.id)))

        if self.vueactive == 1: #vue systeme solaire
            #self.etoileselect = random.choice(mod.etoiles)
            for i in range(len(mod.etoiles)*5):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))
                self.canevas.create_oval(-100, -100, 100, 100, fill="orange", tags=("soleil", "fond"))

            for i in self.etoileselect.planetes:
                s=i.planetImage
                t=i.taille
                """
                if s == 1:
                    self.planet1 = Image.open("./images/planet1.png")
                    self.resized = self.planet1.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet1 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet1, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 2:
                    self.planet2 = Image.open("./images/planet2.png")
                    self.resized = self.planet2.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet2 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet2, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 3:
                    self.planet3 = Image.open("./images/planet3.png")
                    self.resized = self.planet3.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet3 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet3, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 4:
                    self.planet4 = Image.open("./images/planet4.png")
                    self.resized = self.planet4.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet4 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet4, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 5:
                    self.planet5 = Image.open("./images/planet5.png")
                    self.resized = self.planet5.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet5 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet5, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 6:
                    self.planet6 = Image.open("./images/planet6.png")
                    self.resized = self.planet6.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet6 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet6, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 7:
                    self.planet7 = Image.open("./images/planet7.png")
                    self.resized = self.planet7.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet7 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet7, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 8:
                    self.planet8 = Image.open("./images/planet8.png")
                    self.resized = self.planet8.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet8 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet8, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 9:
                    self.planet9 = Image.open("./images/planet9.png")
                    self.resized = self.planet9.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet9 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet9, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                elif s == 10:
                    self.planet10 = Image.open("./images/planet10.png")
                    self.resized = self.planet10.resize((t+30,t+30),Image.ANTIALIAS)
                    self.planet10 = ImageTk.PhotoImage(self.resized)
                    self.canevas.create_image(i.x, i.y, image=self.planet10, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))

                """

                #self.resized = self.planet10.resize((t+30,t+30),Image.ANTIALIAS)
                #self.planet10 = ImageTk.PhotoImage(self.resized)

                #self.resized = self.planet10.resize((t+30,t+30),Image.ANTIALIAS)
                #self.planet10 = ImageTk.PhotoImage(self.resized)
                self.canevas.create_image(i.x, i.y, image=i.planetImage, anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                print(s, )
                #self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                #                       tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))


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
            for i in range(len(mod.etoiles)*4):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))

            #affichage de l'espace ou envoyer un vaisseau pour le retourner a la vue 1
            self.canevas.create_oval(mod.largeur-40, mod.hauteur-40, mod.largeur+40, mod.hauteur+40,fill="purple", tags=("retour1"))

            t=self.planeteselect.taille
            self.canevas.create_oval(mod.largeur/2-(t*20),mod.hauteur/2-(t*20),mod.largeur/2+(t*20),mod.hauteur/2+(t*20), width=2, outline="white", fill=self.planeteselect.color,
                                    tags=("planetezoom", str(self.planeteselect.id), self.planeteselect.proprietaire, str(self.etoileselect.id)))
            
            #affiche les batiment
            self.afficherBatiment()

    def afficherBatiment(self):
        for j in self.mod.joueurs:
            if self.mod.joueurs[j].nom == self.planeteselect.proprietaire:
                for b in self.planeteselect.batiment:
                    if b.typeBatiment == "minerai":
                        self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="red",tags=("batiment",b.id)) #Affiche le batiment
                        self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="white",tags="niveau") #affiche le niveau du batiment
                    elif b.typeBatiment == "gaz":
                        self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="blue",tags=("batiment",b.id))
                        self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="white",tags="niveau") #affiche le niveau du batiment
                    elif b.typeBatiment == "energie":
                        self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="yellow",tags=("batiment",b.id))
                        self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="black",tags="vitesse") #affiche le niveau du batiment


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
            self.attributMinerai.set(textvariable = "Minerai : " + str(self.planeteselect.minerai)) #nombre de minerai restant sur la planet a collecter
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
        self.canevas.delete("marqueur")
        self.btncreervaisseau.pack_forget()
        self.maselection=None

    def creerBatiment(self,evt):
        if self.selectionBatiment != None:
            print("Creer batiment")
            self.parent.creerBatiment(self.selectionBatiment[1],self.selectionBatiment[0],evt.x,evt.y)
            self.canevas.delete("marqueur")
        else:
            self.selectionBatiment=[self.batimentChoisi,1]

    def initMine(self,evt):
        self.selectionBatiment=None
        self.batimentChoisi="minerai"
        self.creerBatiment(evt)

    def initGaz(self,evt):
        self.selectionBatiment=None
        self.batimentChoisi="gaz"
        self.creerBatiment(evt)

    def initEnergie(self,evt):
        self.selectionBatiment=None
        self.batimentChoisi="energie"
        self.creerBatiment(evt)

    def upgradeBatiment(self):
        if self.upgBatiment != None:
            #for j in self.mod.joueurs:
                #if self.mod.joueurs[j].nom == self.planeteselect.proprietaire:
            self.parent.upgBatiment(self.upgBatiment)
            self.upgBatiment = None
            self.canevas.delete("BatimentSelection")
                        

    def afficherpartie(self,mod):
        self.canevas.delete("artefact")
        self.etatBouton()

        #if self.maselection!=None:

            #joueur=mod.joueurs[self.maselection[0]]
            #if self.maselection[0]=="etoile":
                #for i in joueur.planetescontrolees:
                    #if i.id == int(self.maselection[2]):
                        #x=i.x
                        #y=i.y
                        #t=10
                        #self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
                        #                         tags=("select","marqueur"))
            #if self.maselection[0]=="flotte":
            #    for i in joueur.flotte:
            #        if i.id == int(self.maselection[1]):
            #            print(self.maselection)
            #            x=i.x
            #            y=i.y
            #            t=10
            #            self.canevas.create_rectangle(x-t,y-t,x+t,y+t,dash=(2,2),outline=mod.joueurs[self.nom].couleur,
            #                                     tags=("select","marqueur"))
        #else:
        #    self.canevas.delete("marqueur")


        for i in self.mod.joueurs.keys():
            i=mod.joueurs[i]
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-5,j.y-5,j.x+5,j.y+5,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-7,j.y-7,j.x+7,j.y+7,fill=i.couleur,
                                                tags=("flotte", str(j.id), j.proprietaire, "artefact"))


                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-11,j.y-11,j.x+11,j.y+11,fill=i.couleur,
                                                tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                for k in j.projectiles:
                    if self.vueactive == 2:
                        if k.sysplanetecur == None and j.planetecur == None:
                            if (k.etat=="detruit"):
                                self.canevas.create_rectangle(k.x-2,k.y-2,k.x+2,j.y+2,fill="red",
                                                    tags=("projectile", str(k.id), j.proprietaire, "artefact"))
                            else:
                                self.canevas.create_rectangle(k.x-2,k.y-2,k.x+2,j.y+2,fill=i.couleur,
                                                    tags=("projectile", str(k.id), j.proprietaire, "artefact"))

                    if self.vueactive == 1:
                        if k.sysplanetecur == self.etoileselect and j.planetecur == None:
                            if (k.etat=="detruit"):
                                self.canevas.create_rectangle(k.x-4,k.y-4,k.x+4,k.y+4,fill="red",
                                                    tags=("projectile", str(k.id), j.proprietaire, "artefact"))
                            else:
                                self.canevas.create_rectangle(k.x-4,k.y-4,k.x+4,k.y+4,fill=i.couleur,
                                                    tags=("projectile", str(k.id), j.proprietaire, "artefact"))

                    if self.vueactive == 0:
                        if k.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                            if (k.etat=="detruit"):
                                self.canevas.create_rectangle(k.x-7,k.y-7,k.x+7,k.y+7, fill="red",
                                                        tags=("projectile", str(k.id), j.proprietaire, "artefact"))
                            else:
                                self.canevas.create_rectangle(k.x-7,k.y-7,k.x+7,k.y+7,fill=i.couleur,
                                                        tags=("projectile", str(k.id), j.proprietaire, "artefact"))


                #self.canevas.create_rectangle(j.x,j.y,image=self.imgs["vaiss"],
                #                     tags=(j.proprietaire,"flotte",str(j.id),"artefact"))


        for i in self.mod.ias:
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-5,j.y-5,j.x+5,j.y+5,fill=i.couleur,
                                            tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_rectangle(j.x-7,j.y-7,j.x+7,j.y+7,fill=i.couleur,
                                                tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_rectangle(j.x-11,j.y-11,j.x+11,j.y+11,fill=i.couleur,
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
                        t=self.etoileselect.taille
                        if self.flotteselect.x <= (self.etoileselect.x + t) and self.flotteselect.x >= (self.etoileselect.x - t):
                            if self.flotteselect.y <= (self.etoileselect.y + t) and self.flotteselect.y >= (self.etoileselect.y - t):
                                self.parent.versvue1(self.flotteselect.id, self.etoileselect.id)
                        else:
                            self.parent.ciblerflotte(self.flotteselect.id, self.etoileselect.id, "etoile")
                            print(self.flotteselect.id, self.etoileselect.id)

                        self.flotteselect = None
                        self.etoileselect = None

            if tag and tag[0] == "flotte":
                
                if self.flotteselect == None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print(self.maselection)
                    j=self.mod.joueurs[self.nom]
                    for i in j.flotte:
                        if i.id == int(self.maselection[1]):
                            self.flotteselect = i
                            break
                elif self.flotteselect != None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print("Dans le else de flotte vue 2")
                    self.parent.ciblerflotte(self.flotteselect.id, self.maselection[1], "flotte")
                    self.flotteselect = None

                self.maselection = None

        if self.vueactive == 1:
            if tag and tag[0] == "planete":
                self.maselection=[tag[0], tag[1], tag[2]]
                print(self.maselection)
                for i in self.etoileselect.planetes:
                    if str(i.id) == tag[1]:
                        self.planeteselect = i
                        #afficheAttributsPlanete(self.maselection, self.planeteselect)
                        break

                if self.flotteselect != None:
                    t=self.planeteselect.taille
                    if self.flotteselect.x <= (self.planeteselect.x + t) and self.flotteselect.x >= (self.planeteselect.x - t):
                        if self.flotteselect.y <= (self.planeteselect.y + t) and self.flotteselect.y >= (self.planeteselect.y - t):
                            #self.flotteselect.planetecur = self.planeteselect
                            #self.flotteselect.x = self.mod.largeur-random.randrange(30, 45)
                            #self.flotteselect.y = self.mod.hauteur-random.randrange(30, 45)
                            self.parent.versvue0(self.flotteselect.id,self.planeteselect.id)
                    else:
                        print("dans else")
                        self.parent.ciblerflotteplanete(self.flotteselect.id, self.planeteselect.id, self.etoileselect.id)
                        print(self.flotteselect.id, self.planeteselect.id)

                    self.flotteselect=None
                    self.planeteselect=None

            if tag and tag[0] == "flotte":
                
                if self.maselection == None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print(self.maselection)
                    j=self.mod.joueurs[self.nom]
                    for i in j.flotte:
                        if i.id == int(self.maselection[1]):
                            self.flotteselect = i
                            self.maselection=None
                            break
                elif self.flotteselect != None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print("Dans le else de flotte vue 1")
                    self.parent.ciblerflotte(self.flotteselect.id, self.maselection[1], "flotte")
                    self.flotteselect = None

                self.maselection = None

            if tag and tag[0] == "retour2":
                if self.flotteselect != None:
                    self.parent.cibleretour(self.flotteselect.id)


        if self.vueactive == 0:
            if self.selectionBatiment != None:
                self.selectionBatiment=[self.selectionBatiment[0],tag[1]]
                self.creerBatiment(evt)
                self.selectionBatiment=None

<<<<<<< HEAD
            if self.upgBatiment != None:
                self.upgBatiment = None
            elif "batiment" in tag:
                self.upgBatiment = tag[1]
                print(tag[1])
                self.canevas.create_oval(evt.x-50,evt.y-50,evt.x+50,evt.y+50,outline="white",tags="BatimentSelection")
                



=======
>>>>>>> création des explosion et des eclats
        if tag and tag[0] == "flotte":
                
                if self.maselection == None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print(self.maselection)
                    j=self.mod.joueurs[self.nom]
                    for i in j.flotte:
                        if i.id == int(self.maselection[1]):
                            self.flotteselect = i
                            self.maselection=None
                            break
                elif self.flotteselect != None:
                    self.maselection=[tag[0], tag[1], tag[2], tag[3]]
                    print("Dans le else de flotte vue 0")
                    self.parent.ciblerflotte(self.flotteselect.id, self.maselection[1], "flotte")
                    self.flotteselect = None

                self.maselection = None

        if tag and tag[0] == "retour1":
                if self.flotteselect != None:
                    self.parent.cibleretour(self.flotteselect.id)

        self.maselection=None

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