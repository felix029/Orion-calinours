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
        self.nom=""
        self.cadreapp=Frame(self.root,width=800,height=600)
        self.cadreapp.pack()
        self.creercadresplash(ip,nom)
        self.creercadrelobby()
        self.changecadre(self.cadresplash)
        self.vueactive = 0 # 0: vue planetaire, 1: vue systeme solaire, 2: vue galaxy
        self.etoileselect=None
        self.planeteselect=None
        self.flotteselect=None
        self.selectionBatiment=None
        self.batimentChoisi="minerai"
        self.upgBatiment= None

        self.couleurLabelMenu  = "white"
        self.couleurBackgroundMenu  = "gray27"
        self.couleurBackgroundCotes = "SteelBlue4"
        self.couleurTitreCadre = "#34344f"
        self.espacementDonneesMenu = 20



#################################################################################################################################################################################
#                                                                 IMAGES REDIMENSIONNÉES                                                                                        #
#################################################################################################################################################################################

        #Planete du menu
        self.plan = Image.open("./images/planete.png")
        self.resized = self.plan.resize((30, 30),Image.ANTIALIAS)
        self.planete = ImageTk.PhotoImage(self.resized)

        #Electricite du menu
        self.electricite = Image.open("./images/electricite.png")
        self.resized = self.electricite.resize((30, 30),Image.ANTIALIAS)
        self.light = ImageTk.PhotoImage(self.resized)

        #Minerais du menu
        self.rock = Image.open("./images/rock.png")
        self.resized = self.rock.resize((30, 30),Image.ANTIALIAS)
        self.minerais = ImageTk.PhotoImage(self.resized)

        #Gaz du menu
        self.gas = Image.open("./images/gas.png")
        self.resized = self.gas.resize((30, 30),Image.ANTIALIAS)
        self.gas = ImageTk.PhotoImage(self.resized)

        #Boutons vaisseau
        self.vaisseau = Image.open("./images/vaisseau.png")
        self.resized = self.vaisseau.resize((50, 50),Image.ANTIALIAS)
        self.vaisseauMenuGauche = ImageTk.PhotoImage(self.resized)
        #Boutons bâtiments
        self.mine=Image.open("./images/goldmine.png")
        self.resized = self.mine.resize((35, 35),Image.ANTIALIAS)
        self.mineMenuGauche = ImageTk.PhotoImage(self.resized)

        #Bouton tour de defense
        self.defense=Image.open("./images/tourDefense.png")
        self.resized = self.defense.resize((35, 35),Image.ANTIALIAS)
        self.tourDefenseMenuGauche = ImageTk.PhotoImage(self.resized)

        #Gaz du bouton
        self.gaz=Image.open("./images/can.png")
        self.resized = self.gaz.resize((45, 45),Image.ANTIALIAS)
        self.gazMenuGauche = ImageTk.PhotoImage(self.resized)

        self.electric=Image.open("./images/electric.png")
        self.resized = self.electric.resize((40, 40),Image.ANTIALIAS)
        self.electricMenuGauche = ImageTk.PhotoImage(self.resized)

        self.spaceship=Image.open("./images/falcon.png")
        self.resized = self.spaceship.resize((45, 45),Image.ANTIALIAS)
        self.spaceshipMenuGauche = ImageTk.PhotoImage(self.resized)
        #Boutons upgrade
        self.goldmine=Image.open("./images/goldmine.png")
        self.resized = self.goldmine.resize((45, 45),Image.ANTIALIAS)
        self.goldmineMenuGauche = ImageTk.PhotoImage(self.resized)

        #self.electricStation=Image.open("./images/electricity.png")
        #self.resized = self.electricStation.resize((85, 45),Image.ANTIALIAS)
        #self.electricStationMenuGauche = ImageTk.PhotoImage(self.resized)

        #self.gazCan=Image.open("./images/gaz.png")
        #self.resized = self.gazCan.resize((85, 50),Image.ANTIALIAS)
        #self.gazCanMenuGauche = ImageTk.PhotoImage(self.resized)

        #Étoile (vue Galaxie)
        #self.star = Image.open("./images/star.png")
        self.starImage = Image.open("./images/star.png")
        self.resized = self.starImage.resize((50,50),Image.ANTIALIAS)
        self.starImage = ImageTk.PhotoImage(self.resized)

        #Soleil
        self.soleil = Image.open("./images/soleil.png")
        self.resized = self.soleil.resize((200,200),Image.ANTIALIAS)
        self.soleil = ImageTk.PhotoImage(self.resized)

        #Bâtiments (vue Planète)
        #Base
        self.base1 = Image.open("./images/batibase1.png")
        self.resized = self.base1.resize((100,100),Image.ANTIALIAS)
        self.base1 = ImageTk.PhotoImage(self.resized)

        #Batiment Mine
        self.mine1 = Image.open("./images/goldmine.png")
        self.resized = self.mine1.resize((75,75),Image.ANTIALIAS)
        self.mine1 = ImageTk.PhotoImage(self.resized)
        #Batiment Gaz
        self.gaz1 = Image.open("./images/can.png")
        self.resized = self.gaz1.resize((75,75),Image.ANTIALIAS)
        self.gaz1 = ImageTk.PhotoImage(self.resized)
        #Batiment Electricite
        self.elec1 = Image.open("./images/electric.png")
        self.resized = self.elec1.resize((100,100),Image.ANTIALIAS)
        self.elec1 = ImageTk.PhotoImage(self.resized)

        #Tour de defense sur planete
        self.def1=Image.open("./images/tourDefense.png")
        self.resized = self.def1.resize((35, 35),Image.ANTIALIAS)
        self.tourDefense = ImageTk.PhotoImage(self.resized)

        #Baleine cosmique
        self.baleine=Image.open("./images/baleine.png")
        self.resized = self.baleine.resize((150, 150),Image.ANTIALIAS)
        self.baleine = ImageTk.PhotoImage(self.resized)

        #Navette
        #self.navette = Image.open("./images/navette1.png")
        #self.resized = self.elec1.resize((50,50),Image.ANTIALIAS)
        #self.navette = ImageTk.PhotoImage(self.resized)

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

        self.cadresplash=Frame(self.cadreapp, bg="midnightblue")

        #Affichage d'un titre
        self.champ_Titre = Label(self.cadresplash,font = self.texteTitre,fg= "white",bg="midnightblue",text = "ORION",anchor = W)
        self.champ_Titre.pack(side = TOP)

        #Affichage du corps
        self.canevassplash=Canvas(self.cadresplash,width=640,height=480)
        self.filename = PhotoImage(file ="./images/univers.png")
        self.background_label = Label(self.cadresplash, image=self.filename)
        self.background_label.place(x=0, y=35, width=645, relheight=1)
        self.canevassplash.pack()

        #Etiquette pour la boite d'info nom
        self.labelNomJoueur = Label(self.cadresplash, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="NOM:")
        self.labelNomJoueur.place(x=266, y=110)

        self.nomsplash=Entry(bg="light grey")
        self.nomsplash.insert(0, nom)

        #Etiquette pour la boite d'info ip serveur
        self.labelIpServeur = Label(self.cadresplash, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="IP SERVEUR:")
        self.labelIpServeur.place(x=266, y=200)

        self.ipsplash=Entry(bg="light grey")
        self.ipsplash.insert(0, ip)

        #Etiquette pour la boite d'info ip
        self.labelIP = Label(self.cadresplash, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="IP:")
        self.labelIP.place(x=266, y=290)

        labip=Label(text=ip,bg="light grey",borderwidth=0,relief=RIDGE)
        btncreerpartie=Button(text="Creer partie",bg="light grey",command=self.creerpartie)
        btnconnecterpartie=Button(text="Connecter partie",bg="light grey",command=self.connecterpartie)

        self.canevassplash.create_window(320,110,window=self.nomsplash,width=100,height=30)
        self.canevassplash.create_window(320,200,window=self.ipsplash,width=100,height=30)
        self.canevassplash.create_window(320,290,window=labip,width=100,height=30)
        self.canevassplash.create_window(220,410,window=btncreerpartie,width=100,height=30)
        self.canevassplash.create_window(420,410,window=btnconnecterpartie,width=100,height=30)


    def creercadrelobby(self):
        self.cadrelobby=Frame(self.cadreapp,bg="midnightblue")

        #Affichage d'un titre
        self.champ_Titre = Label(self.cadrelobby,font = self.texteTitre,fg= "white",bg="midnightblue",text = "Création de partie", anchor = W)
        self.champ_Titre.pack(side = TOP)

        #Affichage du corps
        self.canevaslobby=Canvas(self.cadrelobby,width=640,height=480)
        self.filename2 = PhotoImage(file ="./images/univers.png")
        self.background_label2 = Label(self.cadrelobby, image=self.filename2)
        self.background_label2.place(x=0, y=35, width=645, relheight=1)
        self.canevaslobby.pack()

        self.listelobby=Listbox(bg="light grey",borderwidth=0,relief=FLAT)

        self.labelEspace = Label(self.cadrelobby, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="ESPACE")
        self.labelEspace.place(x=150, y=160)
        self.largeespace=Entry(bg="light grey")
        self.largeespace.insert(0, 1000)

        self.labelHaut = Label(self.cadrelobby, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="HAUTE")
        self.labelHaut.place(x=150, y=230)
        self.hautespace=Entry(bg="light grey")
        self.hautespace.insert(0, 800)

        self.labelNbEtoile = Label(self.cadrelobby, fg= "white",bg="midnightblue",font='Helvetica 9 bold',text="NOMBRE D'ÉTOILES")
        self.labelNbEtoile.place(x=140, y=300)
        self.nbetoile=Entry(bg="light grey")
        self.nbetoile.insert(0, 100)


        btnlancerpartie=Button(text="Lancer partie",bg="light grey",command=self.lancerpartie)
        self.canevaslobby.create_window(440,240,window=self.listelobby,width=200,height=400)
        self.canevaslobby.create_window(200,155,window=self.largeespace,width=100,height=30)
        self.canevaslobby.create_window(200,225,window=self.hautespace,width=100,height=30)
        self.canevaslobby.create_window(200,295,window=self.nbetoile,width=100,height=30)
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


#################################################################################################################################################################################
#                                                                                                                                                                               #
#                                                                       PRINCIPAUX FRAMES                                                                                       #
#                                                                                                                                                                               #
#################################################################################################################################################################################


        #########################################################################################################################################################################
        ############################################################### ZONE GLOBALE ############################################################################################
        #########################################################################################################################################################################
        self.cadrepartie=Frame(self.cadreapp)
        self.cadrejeu=Frame(self.cadrepartie)


        #########################################################################################################################################################################
        ################################################################# FRAME MENU ############################################################################################
        #########################################################################################################################################################################
        self.planetConquisesStats = StringVar()
        self.electriciteStats = StringVar()
        self.mineraisStats = StringVar()
        self.gazStats = StringVar()

        #Frame du menu
        self.upperFrame=Frame(self.cadrepartie,width=1100,height=50,bg= self.couleurBackgroundMenu)
        self.upperFrame.grid(row=0, column=0, sticky="we")

        #Tous les label identifiant les variables + tous les label avec les images contextuelles
        self.espaceVide0 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=1)

        self.lab_planete = Label(self.upperFrame, image = self.planete, bg = self.couleurBackgroundMenu).grid(row=0, column=2)
        self.lblPlanConquises=Label(self.upperFrame,text="Planètes conquises: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu).grid(row=0, column=3)
        self.statsPlanetConquisesLabel = Label(self.upperFrame, fg="red", bg= self.couleurBackgroundMenu, textvariable = self.planetConquisesStats).grid(row=0, column=4)

        self.espaceVide1 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=5)

        self.lab_eclair = Label(self.upperFrame, image = self.light, bg = self.couleurBackgroundMenu).grid(row=0, column=14)
        self.lblElectricite=Label(self.upperFrame,text="Électricité: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu).grid(row=0, column=15)
        self.statsElectriciteLabel=Label(self.upperFrame, fg="red", bg= self.couleurBackgroundMenu, textvariable = self.electriciteStats).grid(row=0, column=16)

        self.espaceVide2 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=9)

        self.lab_rock = Label(self.upperFrame, image = self.minerais, bg = self.couleurBackgroundMenu).grid(row=0, column=6)
        self.lblMinerais=Label(self.upperFrame,text="Minerais: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu).grid(row=0, column=7)
        self.statsMineraisLabel=Label(self.upperFrame, fg="red", bg= self.couleurBackgroundMenu, textvariable = self.mineraisStats).grid(row=0, column=8)

        self.espaceVide3 = Label(self.upperFrame, bg = self.couleurBackgroundMenu,width=self.espacementDonneesMenu).grid(row=0, column=13)

        self.lab_gaz = Label(self.upperFrame, image = self.gas, bg = self.couleurBackgroundMenu).grid(row=0, column=10)
        self.lblGaz=Label(self.upperFrame,text="Gaz: ", fg=self.couleurLabelMenu, bg= self.couleurBackgroundMenu).grid(row=0, column=11)
        self.statsGazLabel=Label(self.upperFrame, fg="red", bg= self.couleurBackgroundMenu, textvariable = self.gazStats).grid(row=0, column=12)


        #########################################################################################################################################################################
        ################################################################## FRAME DESSOUS ########################################################################################
        #########################################################################################################################################################################
        #Frame qui reçoit TOUT ce qui n'est pas dans le menu
        self.lowerFrame=Frame(self.cadrepartie,width=1100,height=625,bg=self.couleurBackgroundMenu)
        self.lowerFrame.grid(row=2, column=0, sticky="ns")


        ########################################################## AIRE DE JEU (NE PAS TOUCHER !!!) #############################################################################
        #Le canevas (surface de jeu est dans le frame dessous)
        self.canevas=Canvas(self.lowerFrame,width=800,height=600,bg="grey11")
        self.canevas.grid(row=0, column=1, sticky="ns")
        self.canevas.bind("<Button>",self.cliquecosmos) # Event MouseClick lie au canevas (Aire de jeu)


        ################################################################# BANDE COTE GAUCHE ######################################################################################
        #Le frame gauche est dans le frame dessous
        self.lowerLeftFrame=Frame(self.lowerFrame,width=150,height=625,bg="pink")
        self.lowerLeftFrame.grid(row=0, column=0, sticky="ns")
        self.lowerLeftFrame.columnconfigure(0, minsize=150)
        self.lowerLeftFrame.grid_propagate(0)

        #Sous-frames du frame gauche (avec leurs labels et leurs boutons)
        #Frames creation et upgrade
        self.creationFrame=Frame(self.lowerLeftFrame,width=150, height=313, bg=self.couleurBackgroundCotes)
        self.creationFrame.grid(row=0, column=0, sticky="ns")
        self.creationFrame.grid_propagate(0)
        self.upgradeFrame=Frame(self.lowerLeftFrame,width=150, height=312, bg=self.couleurBackgroundCotes)
        self.upgradeFrame.grid(row=1, column=0, sticky="ns")
        self.upgradeFrame.grid_propagate(0)
        self.creationFrame.columnconfigure(0, minsize=150)
        self.upgradeFrame.columnconfigure(0, minsize=150)

        #Label Creation
        self.creationLabel = Label(self.creationFrame, text=".: CREATION :.", anchor='center', fg="white", bg='#34344f',borderwidth=3, relief="solid").grid(row=0, column=0, sticky="we")
        self.vaisseauLabel = Label(self.creationFrame, text="Vaisseau", anchor='center', fg="white", bg='#34344f').grid(row=1, column=0, sticky="we")
        self.batimentLabel = Label(self.creationFrame, text="Bâtiments", anchor='center', fg="white", bg='#34344f').grid(row=3, column=0, sticky="we")

        #Label Upgrade
        self.upgLabel = Label(self.upgradeFrame, text=".: UPGRADE :.", anchor='center', fg="white", bg='#34344f',borderwidth=3, relief="solid").grid(row=0, column=0, sticky="we")
        self.upgVaisseauLabel = Label(self.upgradeFrame, text="Vaisseau", anchor='center', fg="white", bg='#34344f').grid(row=1, column=0, sticky="we")
        self.upgBatimentLabel = Label(self.upgradeFrame, text="Bâtiments", anchor='center', fg="white", bg='#34344f').grid(row=3, column=0, sticky="we")

        #Boutons de creation
        self.btncreervaisseau=Button(self.creationFrame,image=self.vaisseauMenuGauche,width = "50",height = "50",command=self.creervaisseau,bg =self.couleurBackgroundCotes)
        self.btncreervaisseau.grid(row=2, column=0, sticky="we")
        self.btncreervaisseau.config(height=45)

        self.mines=Button(self.creationFrame,image=self.mineMenuGauche,width = "50",height = "50",bg =self.couleurBackgroundCotes)
        self.mines.grid(row=4, column=0, sticky="we")
        self.mines.config(height=45)
        self.mines.bind("<Button>", self.initMine)

        self.extracteurs=Button(self.creationFrame,image=self.gazMenuGauche,bg =self.couleurBackgroundCotes)
        self.extracteurs.grid(row=5, column=0, sticky="we")
        self.extracteurs.config(height=45)
        self.extracteurs.bind("<Button>", self.initGaz)

        self.electricite=Button(self.creationFrame,image=self.electricMenuGauche,bg =self.couleurBackgroundCotes)
        self.electricite.grid(row=6, column=0, sticky="we")
        self.electricite.config(height=45)
        self.electricite.bind("<Button>", self.initEnergie)

        self.tourdefense=Button(self.creationFrame,image=self.tourDefenseMenuGauche,fg="white",bg =self.couleurBackgroundCotes)
        self.tourdefense.grid(row=7, column=0, sticky="we")
        self.tourdefense.config(height=45)
        self.tourdefense.bind("<Button>", self.creerTourDefense)

        #Boutons upgrade
        self.upgVaisseau=Button(self.upgradeFrame,image=self.spaceshipMenuGauche,bg =self.couleurBackgroundCotes)
        self.upgVaisseau.grid(row=2, column=0, sticky="we")
        self.upgVaisseau.config(height=45)

        self.upgMines=Button(self.upgradeFrame,image=self.goldmineMenuGauche,bg =self.couleurBackgroundCotes)
        self.upgMines.grid(row=4, column=0, sticky="we")
        self.upgMines.config(height=45)
        self.upgMines.bind("<Button>",self.upgradeBatiment)


        ################################################################# BANDE COTE DROIT ######################################################################################
        #Le frame droit est dans le frame dessous
        self.lowerRightFrame=Frame(self.lowerFrame,width=150,height=626,bg=self.couleurBackgroundCotes)
        self.lowerRightFrame.grid(row=0, column=2, sticky="ns")

        #Sous-frames du frame droit (avec leurs labels)
        #Frames info miniMap et stats
        self.cadreinfogen=Frame(self.lowerRightFrame,width=150,height=200,bg=self.couleurBackgroundCotes)
        self.cadreinfogen.grid(row=0, column=0, sticky="we")

        self.lblJoueurs = Label(self.cadreinfogen, text=" .: AUTRES JOUEURS :. ",fg="white", width= 38, height=2, bg=self.couleurTitreCadre,borderwidth=3, relief="solid").grid(row=0,column=0,sticky = "we")

        self.labid=Label(self.cadreinfogen,text=self.nom,fg=mod.joueurs[self.nom].couleur,bg=self.couleurBackgroundCotes)
        self.labid.grid(row=1, column=0, sticky="we")

        self.cadreminimap=Frame(self.lowerRightFrame,height=200,width=150,bg=self.couleurBackgroundCotes)
        self.cadreminimap.grid(row=1, column=0, sticky="we")

        self.labelCadreMini = Label(self.cadreminimap, text=".: STATISTIQUES :.",fg="white", width= 25, height=2, bg=self.couleurTitreCadre,borderwidth=3, relief="solid").pack(fill=X)

        self.statsFrame = Frame(self.lowerRightFrame, width=150,height=200)
        self.statsFrame.grid(row=2, column=0, sticky="we")

        self.canevasMini=Canvas(self.statsFrame,width=150,height=200,bg=self.couleurBackgroundCotes)
        self.canevasMini.pack(fill=X)
        self.canevasMini.bind("<Button>",self.moveCanevas)

        self.labid.bind("<Button>",self.afficherplanetemere)
        self.canevasMini.bind("<Button>",self.moveCanevas)


        ###################################################################### BANDE DU BAS #####################################################################################
        #Le frame du bas est dans le frame dessous
        self.lowerLowerFrame=Frame(self.lowerFrame,width=800,height=75,bg=self.couleurTitreCadre)
        self.lowerLowerFrame.grid(row=1, column=1, sticky="ns")

        #Bouton pour modifier la vue (zoom et de-zoom)
        self.boutonZoom = Button(self.lowerLowerFrame,text="Vue suivante", bg=self.couleurTitreCadre, width= 56, height=2, cursor="hand2", activebackground="red", fg="white")
        self.boutonZoom.bind("<Button>")
        self.boutonZoom.grid(row=0, column=1)

        self.boutonDzoom=Button(self.lowerLowerFrame,text="Vue precedente", bg=self.couleurTitreCadre, width= 56, height=2, cursor="hand2", activebackground="red", fg="white")
        self.boutonDzoom.bind("<Button>")
        self.boutonDzoom.grid(row=0, column=0)


        #########################################################################################################################################################################
        self.afficherdecor(mod)
        self.changecadre(self.cadrepartie)        #Label d'affichage des atrributs d'une planète lors de la VUE_PLANÉTAIRE
        self.textGeneriquePlanete =  StringVar()
        self.textMinerai =  StringVar()
        self.textGaz = StringVar()
        self.attributMineraiEtoile = 0
        self.attributGazEtoile = 0

        self.attributPlaneteSelectionne = Label(self.canevasMini, width= 30, height=10, bg=self.couleurBackgroundCotes,fg=self.couleurLabelMenu,font=self.simpleFont)
        self.attributPlaneteSelectionne.grid(row=0, column=0, sticky="we")

        self.textMinerai =  StringVar()
        self.attributMinerai = Label(self.canevasMini,  width=30, height=2, bg=self.couleurBackgroundCotes,fg=self.couleurLabelMenu,font=self.simpleFont)
        self.attributMinerai.grid(row=1, column=0, sticky="we")

        self.attributGaz = Label(self.canevasMini,  width= 30, height=2, bg=self.couleurBackgroundCotes,fg=self.couleurLabelMenu,font=self.simpleFont)
        self.attributGaz.grid(row=2, column=0, sticky="we")

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
            self.boutonZoom.config(width=113, text = "VUE SYSTÈME SOLAIRE", border=4)
            self.boutonZoom.grid(row=1, column=0, sticky="we")

        elif self.vueactive == 1:
            self.attributMineraiEtoile = 0
            self.attributGazEtoile = 0
            self.boutonZoom.config(width = 56, text = "VUE PLANÉTAIRE", border=2)
            self.boutonDzoom.config(width = 56, text = "VUE GALAXIE", border=2)
            self.boutonZoom.grid(row=1, column=1, sticky="we")
            self.boutonDzoom.grid(row=1, column=0, sticky="we")

            for i in self.etoileselect.planetes:
                self.attributMineraiEtoile+= i.minerai
                self.attributGazEtoile+= i.gaz

            self.textGeneriquePlanete = "L'étoile possède :  \n"
            self.textMinerai = "Minerai : " + str (self.attributMineraiEtoile) + "\n"
            self.textGaz = "Gaz : " + str(self.attributGazEtoile) + "\n"
            self.attributPlaneteSelectionne.config(text = self.textGeneriquePlanete + self.textMinerai + self.textGaz )
            self.attributPlaneteSelectionne.grid(row = 1)


        elif self.vueactive == 0:
            self.boutonDzoom.config(width=113, text = "VUE SYSTÈME SOLAIRE", border=4)
            self.boutonDzoom.grid(row=1, column=0, sticky="we")

            if self.planeteselect.proprietaire == " ":
                self.textGeneriquePlanete = "Aucun propriétaire" + "\n\n\n\nLa planète possède :  \n"
            else:
                self.textGeneriquePlanete = "Le propriétaire de la planète est\n " + self.planeteselect.proprietaire + "\n\n\n\nLa planète possède :  \n"

            self.textMinerai = "Minerai : " + str (self.planeteselect.minerai) + "\n"
            self.textGaz = "Gaz : " + str(self.planeteselect.gaz) + "\n"
            self.attributPlaneteSelectionne.config(text =  self.textGeneriquePlanete + self.textMinerai + self.textGaz )
            self.attributPlaneteSelectionne.grid(row = 1)


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
            for i in range(len(mod.etoiles)*50):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))

            for i in mod.etoiles:
                t=i.taille
                self.canevas.create_image(i.x - t, i.y - t, image=self.starImage, anchor=CENTER, tags=("etoile", str(i.id)))
                #self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                                       #tags=("etoile", str(i.id)))

        if self.vueactive == 1: #vue systeme solaire
            #self.etoileselect = random.choice(mod.etoiles)
            for i in range(len(mod.etoiles)*20):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))
                #Insertion de l'image du soleil
                self.canevas.create_image(0, 0, image=self.soleil, anchor=NW, tags=("soleil", "fond"))

            for i in self.etoileselect.planetes:
                #s=i.planeteImages[0]
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

                # Afficher l'image de chaque planètes du array "planetes" de l'étoile sélectionnée
                self.canevas.create_image(i.x - t, i.y - t, image=i.planeteImages[0], anchor=NW, tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))
                #self.canevas.create_oval(i.x-t,i.y-t,i.x+t,i.y+t,fill="grey80",
                #                       tags=("planete", str(i.id), i.proprietaire, str(self.etoileselect.id)))


            #for i in mod.joueurs.keys():
            #    for j in mod.joueurs[i].planetescontrolees:
            #        if j in self.etoileselect.planetes:
            #            t=j.taille
            #            self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=mod.joueurs[i].couleur,
            #                                tags=("planete", str(j.id), j.proprietaire, str(self.etoileselect.id)))
            # dessine planetes IAs

            #for i in mod.ias:
            #    for j in i.planetescontrolees:
            #        if j in self.etoileselect.planetes:
            #            t=j.taille
            #            self.canevas.create_oval(j.x-t,j.y-t,j.x+t,j.y+t,fill=i.couleur,
            #                                tags=("planete", str(j.id), j.proprietaire, str(self.etoileselect.id)))

            #affichage de l'espace ou envoyer un vaisseau pour le retourner a la vue 2
            self.canevas.create_oval(mod.largeur-40, mod.hauteur-40, mod.largeur+40, mod.hauteur+40,fill="purple", tags=("retour2"))


        if self.vueactive == 0: #vue plan�te
            for i in range(len(mod.etoiles)*15):
                x=random.randrange(mod.largeur)
                y=random.randrange(mod.hauteur)
                self.canevas.create_oval(x,y,x+1,y+1,fill="white",tags=("fond"))

            #affichage de l'espace ou envoyer un vaisseau pour le retourner a la vue 1
            self.canevas.create_oval(mod.largeur-40, mod.hauteur-40, mod.largeur+40, mod.hauteur+40,fill="purple", tags=("retour1"))

            t=self.planeteselect.taille
            self.canevas.create_image((mod.largeur-550)/2, (mod.hauteur-550)/2, image=self.planeteselect.planeteImages[1], anchor=NW, tags=("planetezoom", str(self.planeteselect.id), self.planeteselect.proprietaire, str(self.etoileselect.id)))
            #self.canevas.create_oval(mod.largeur/2-(t*20),mod.hauteur/2-(t*20),mod.largeur/2+(t*20),mod.hauteur/2+(t*20), width=2, outline="white", fill=self.planeteselect.color,
                                   #tags=("planetezoom", str(self.planeteselect.id), self.planeteselect.proprietaire, str(self.etoileselect.id)))

            #affiche les batiment
            self.afficherBatiment()


    def afficherBatiment(self):
        for j in self.mod.joueurs:
            if self.planeteselect != None:
                if self.mod.joueurs[j].nom == self.planeteselect.proprietaire:
                    for b in self.planeteselect.batiment:
                        if b.typeBatiment == "minerai":
                            self.canevas.create_image(b.x - 20, b.y - 20, image=self.mine1, anchor=NW, tags=("batiment",b.id))
                            #self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="red",tags=("batiment",b.id)) #Affiche le batiment
                            #self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="white",tags="niveau") #affiche le niveau du batiment
                        elif b.typeBatiment == "gaz":
                            self.canevas.create_image(b.x - 25, b.y - 25, image=self.gaz1, anchor=NW, tags=("batiment",b.id))
                            #self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="blue",tags=("batiment",b.id))
                            #self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="white",tags="niveau") #affiche le niveau du batiment
                        elif b.typeBatiment == "energie":
                            self.canevas.create_image(b.x - 50, b.y - 50, image=self.elec1, anchor=NW, tags=("batiment",b.id))
                            #self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="yellow",tags=("batiment",b.id))
                            #self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="black",tags="vitesse") #affiche le niveau du batiment
                        elif b.typeBatiment == "base":
                            self.canevas.create_image(b.x - 50, b.y - 50, image=self.base1, anchor=NW, tags=("batiment",b.id))
                            #self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="purple",tags=("batiment",b.id))
                            #self.canevas.create_text(b.x,b.y-20,text=b.vitesse,fill="white",tags="vitesse") #affiche le niveau du batiment

                    for b in self.planeteselect.toursDefense:
                        #self.canevas.create_text(b.x,b.y-20,text=b.niveau,fill="white",tags="vitesse") #affiche le niveau du batiment
                        self.canevas.create_image(b.x-10,b.y-40, image=self.tourDefense,anchor=NW,tags=("batiment",b.id))


    def afficheAttributsPlanete(self, maselection, planeteselect=None, etoileselect=None):

        tag = self.maselection.tag[1]
        self.calculMinerai+=0
        self.calculGaz+=0

        if tag == "etoile":
            for i in self.etoileselect.planetes:
                self.calculMinerai+=self.planeteselect.minerai
                self.calculGaz+=self.planeteselect.gaz

            self.planeteselect.gaz
            self.planeteselect.minerai

        if tag == "planete":
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
            x=etoileplanetemere.x+8
            y=etoileplanetemere.y+8
            t=etoileplanetemere.taille+15
            self.canevas.create_oval(x-t-2,y-t-2,x+t+2,y+t+2,dash=(3,3),width=2,outline=couleur,
                                 tags=("planetemere","marqueur"))

        if self.vueactive == 1:
            j=self.mod.joueurs[self.nom]

            if self.etoileselect == j.planetemere.etoileparent:
                couleur=j.couleur
                x=j.planetemere.x+(j.planetemere.taille)-10
                y=j.planetemere.y+(j.planetemere.taille)-10
                t=j.planetemere.taille+20
                self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(3,3),width=2,outline=couleur,
                                 tags=("planetemere","marqueur"))

    def creervaisseau(self):
        if self.vueactive == 0:
            if self.planeteselect.proprietaire == self.nom:
                print("Creer vaisseau")
                self.parent.creervaisseau(self.planeteselect.id)
                self.canevas.delete("marqueur")
                self.btncreervaisseau.pack_forget()
                self.maselection=None


    def creerBatiment(self,evt):
        if self.selectionBatiment != None:
            wid = str(evt.widget)
            widget = wid.split("!")
            if widget[len(widget)-1] == "canvas":
                print("Creer batiment")
                self.parent.creerBatiment(self.selectionBatiment[1],self.selectionBatiment[0],evt.x,evt.y)
                self.canevas.delete("marqueur")
            else:
                self.selectionBatiment=[self.batimentChoisi,1]
        else:
            self.selectionBatiment=[self.batimentChoisi,1]


    def creerTourDefense(self,evt):
        if self.selectionBatiment != None:
            wid = str(evt.widget)
            widget = wid.split("!")
            if widget[len(widget)-1] == "canvas":
                print("Creer Tour Defense")
                self.parent.creerTourDefense(self.selectionBatiment[1],evt.x,evt.y)
                self.canevas.delete("marqueur")
            else:
                self.selectionBatiment=["tourDefense",1]
        else:
            self.selectionBatiment=["tourDefense",1]

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


    def upgradeBatiment(self,evt):
        if self.upgBatiment != None:
            self.parent.upgBatiment(self.upgBatiment)
            self.upgBatiment = None
            self.canevas.delete("BatimentSelection")


    def afficherpartie(self,mod):
        self.canevas.delete("artefact")
        self.etatBouton()

        #Vérification si le joueur à recu une demande d'alliance
        if self.mod.joueurs[self.nom].demandes:
            self.demandeAmi(self.mod.joueurs[self.nom].demandes.pop(0))

        for j in self.mod.joueurs:
            if self.mod.joueurs[j].nom == self.nom:
                self.planetConquisesStats.set(len(self.mod.joueurs[j].planetescontrolees))
                self.electriciteStats.set(self.mod.joueurs[j].energie)
                self.mineraisStats.set(self.mod.joueurs[j].minerai)
                self.gazStats.set(self.mod.joueurs[j].gaz)

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
        if self.vueactive == 2:
            self.canevas.delete("baleine")
            #self.canevas.create_rectangle(mod.baleine.x-50,mod.baleine.y-50,mod.baleine.x+50,mod.baleine.y+50,fill="blue",tags="baleine")
            self.canevas.create_image(mod.baleine.x, mod.baleine.y, image=self.baleine, anchor=CENTER, tags="baleine")

        for i in self.mod.joueurs.keys():
            i=mod.joueurs[i]
            for j in i.flotte:
                if self.vueactive == 2:
                    if j.sysplanetecur == None and j.planetecur == None:
                        self.canevas.create_image(j.x, j.y, image=i.navetteImage[2], anchor=NW, tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                        items=self.canevas.find_enclosed(self.mod.baleine.x-50,self.mod.baleine.y-50,self.mod.baleine.x+50,self.mod.baleine.y+50)
                        for k in items:
                            tags=self.canevas.gettags(k)
                            if tags:
                                if tags[0] == "flotte":
                                    j.etat = "detruit"

                if self.vueactive == 1:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == None:
                        self.canevas.create_image(j.x - 7, j.y - 7, image=i.navetteImage[1], anchor=NW, tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                        #self.canevas.create_rectangle(j.x-7,j.y-7,j.x+7,j.y+7,fill=i.couleur,
                                                #tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                if self.vueactive == 0:
                    if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                        self.canevas.create_image(j.x - 5, j.y - 5, image=i.navetteImage[0], anchor=NW, tags=("flotte", str(j.id), j.proprietaire, "artefact"))
                        #self.canevas.create_rectangle(j.x-11,j.y-11,j.x+11,j.y+11,fill=i.couleur,
                                                #tags=("flotte", str(j.id), j.proprietaire, "artefact"))

                for k in j.projectiles:
                    if self.vueactive == 2:
                        if k.sysplanetecur == None and j.planetecur == None:
                            self.canevas.create_rectangle(k.x-2, k.y-2, k.x+2, k.y+2, fill=i.couleur,tags=("projectile", k.proprietaire, "artefact"))

                    if self.vueactive == 1:
                        if k.sysplanetecur == self.etoileselect and j.planetecur == None:
                            self.canevas.create_rectangle(k.x-4,k.y-4,k.x+4,k.y+4,fill=i.couleur, tags=("projectile", k.proprietaire, "artefact"))

                    if self.vueactive == 0:
                        if k.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                            self.canevas.create_rectangle(k.x-7,k.y-7,k.x+7,k.y+7,fill=i.couleur,tags=("projectile", k.proprietaire, "artefact"))

                if len(j.explosions) > 0:
                    for l in j.explosions:
                        if self.vueactive == 2:
                            if l.sysplanetecur == None and j.planetecur == None:
                                self.canevas.create_rectangle(l.x-l.rayon, l.y-l.rayon, l.x+l.rayon, l.y+l.rayon, fill="white",tags=("projectile", l.proprietaire, "artefact"))

                        elif self.vueactive == 1:
                            if l.sysplanetecur == self.etoileselect and j.planetecur == None:
                                self.canevas.create_rectangle(l.x-40,l.y-40,l.x+40,l.y+40,fill="white", tags=("projectile", l.proprietaire, "artefact"))

                        elif self.vueactive == 0:
                            if l.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
                                self.canevas.create_rectangle(l.x-7,l.y-7,l.x+7,l.y+7,fill="white",tags=("projectile", l.proprietaire, "artefact"))
                        j.explosions.remove(l)



        #Affichage des AIs
        #for i in self.mod.ias:
        #    for j in i.flotte:
        #        if self.vueactive == 2:
        #            if j.sysplanetecur == None and j.planetecur == None:
        #                self.canevas.create_rectangle(j.x-5,j.y-5,j.x+5,j.y+5,fill=i.couleur,
        #                                    tags=("flotte", str(j.id), j.proprietaire, "artefact"))
        #        if self.vueactive == 1:
        #            if j.sysplanetecur == self.etoileselect and j.planetecur == None:
        #                self.canevas.create_rectangle(j.x-7,j.y-7,j.x+7,j.y+7,fill=i.couleur,
        #                                        tags=("flotte", str(j.id), j.proprietaire, "artefact"))
        #

        #        if self.vueactive == 0:
        #            if j.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
        #                self.canevas.create_rectangle(j.x-11,j.y-11,j.x+11,j.y+11,fill=i.couleur,
        #                                        tags=("flotte", str(j.id), j.proprietaire, "artefact"))
        #        if len(j.explosions) > 0:
        #            for l in j.explosions:
        #                if self.vueactive == 2:
        #                    if l.sysplanetecur == None and j.planetecur == None:
        #                        self.canevas.create_rectangle(l.x-l.rayon, l.y-l.rayon, l.x+l.rayon, l.y+l.rayon, fill="white",tags=("projectile", l.proprietaire, "artefact"))
    	#
        #                elif self.vueactive == 1:
        #                    if l.sysplanetecur == self.etoileselect and j.planetecur == None:
        #                        self.canevas.create_rectangle(l.x-40,l.y-40,l.x+40,l.y+40,fill="white", tags=("projectile", l.proprietaire, "artefact"))
        #
        #               elif self.vueactive == 0:
        #                   if l.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
        #                        self.canevas.create_rectangle(l.x-7,l.y-7,l.x+7,l.y+7,fill="white",tags=("projectile", l.proprietaire, "artefact"))
        #                j.explosions.remove(l)

        #    for k in j.projectiles:
            #         if self.vueactive == 2:
            #             if k.sysplanetecur == None and j.planetecur == None:
            #                     self.canevas.create_rectangle(k.x-2, k.y-2, k.x+2, k.y+2, fill=i.couleur,tags=("projectile", k.proprietaire, "artefact"))

            #         if self.vueactive == 1:
            #             if k.sysplanetecur == self.etoileselect and j.planetecur == None:
            #                     self.canevas.create_rectangle(k.x-4,k.y-4,k.x+4,k.y+4,fill=i.couleur, tags=("projectile", k.proprietaire, "artefact"))

            #         if self.vueactive == 0:
            #             if k.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
            #                     self.canevas.create_rectangle(k.x-7,k.y-7,k.x+7,k.y+7,fill=i.couleur,tags=("projectile", k.proprietaire, "artefact"))

            # if len(j.explosions) > 0:
            #         for l in j.explosions:
            #             if self.vueactive == 2:
            #                 if l.sysplanetecur == None and j.planetecur == None:
            #                     self.canevas.create_rectangle(l.x-l.rayon, l.y-l.rayon, l.x+l.rayon, l.y+l.rayon, fill="white",tags=("projectile", l.proprietaire, "artefact"))

            #             elif self.vueactive == 1:
            #                 if l.sysplanetecur == self.etoileselect and j.planetecur == None:
            #                     self.canevas.create_rectangle(l.x-40,l.y-40,l.x+40,l.y+40,fill="white", tags=("projectile", l.proprietaire, "artefact"))

            #             elif self.vueactive == 0:
            #                 if l.sysplanetecur == self.etoileselect and j.planetecur == self.planeteselect:
            #                     self.canevas.create_rectangle(l.x-7,l.y-7,l.x+7,l.y+7,fill="white",tags=("projectile", l.proprietaire, "artefact"))
            #             j.explosions.remove(l)


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
                        self.parent.ciblerflotteplanete(self.flotteselect.id, self.planeteselect.id, self.etoileselect.id)
                        print(self.flotteselect.id, self.planeteselect.id)

                    self.flotteselect=None
                    self.planeteselect=None

            if tag and tag[0] == "flotte":
                if self.flotteselect == None:
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
                if (self.selectionBatiment[0] == "tourDefense"):
                    print(evt.widget)
                    self.creerTourDefense(evt)
                    self.selectionBatiment=None
                else:
                    self.creerBatiment(evt)
                    self.selectionBatiment=None

            if self.upgBatiment != None:
                self.upgBatiment = None
                self.canevas.delete("BatimentSelection")

            elif "batiment" in tag:
                #self.canevas.create_oval(evt.x-50,evt.y-50,evt.x+50,evt.y+50,outline="white",tags="BatimentSelection")
                self.upgBatiment = tag[1]
                for e in self.mod.joueurs:
                    couleur = self.mod.joueurs[e].couleur
                    for p in self.mod.joueurs[e].planetescontrolees:
                        for b in p.batiment:
                            print("oui3")
                            print(self.upgBatiment)
                            print(b.id)
                            if str(b.id)==str(self.upgBatiment):
                                print("oui4")
                                if b.typeBatiment == "minerai":
                                    t=45
                                    x=b.x+10
                                    y=b.y+10
                                    self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(3,3),width=2,outline=couleur,
                                            tags=("BatimentSelection"))
                                elif b.typeBatiment == "gaz":
                                    t=40
                                    x=b.x+12
                                    y=b.y+14
                                    self.canevas.create_oval(x-t,y-t,x+t,y+t,dash=(3,3),width=2,outline=couleur,
                                            tags=("BatimentSelection"))
                                elif b.typeBatiment == "energie":
                                    t=55
                                    x=b.x+15
                                    y=b.y+27
                                    self.canevas.create_oval(b.x-t,b.y-t,b.x+t,b.y+t,dash=(3,3),width=2,outline=couleur,
                                            tags=("BatimentSelection"))
                                elif b.typeBatiment == "base":
                                    t=50
                                    self.canevas.create_oval(b.x-t,b.y-t,b.x+t,b.y+t,dash=(3,3),width=2,outline=couleur,
                                            tags=("BatimentSelection"))
                                break

                #for b in self.planeteselect.toursDefense:
                #    self.canevas.create_rectangle(b.x-10,b.y,b.x+10,b.y-40, fill="green",tags=("batiment",b.id))
                #    self.canevas.create_text(b.x,b.y-20,text=b.niveau,fill="white",tags="vitesse") #affiche le niveau du batiment





            if tag and tag[0] == "flotte":

                if self.flotteselect == None:
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

            if tag and tag[0] == "planetezoom":
                if self.flotteselect != None:
                    j = self.mod.joueurs[self.nom]
                    if tag[2] != self.nom and tag[2] not in j.joueurami:
                        self.amiOuAttaque(self.planeteselect.proprietaire)

            if tag and tag[0] == "retour1":
                if self.flotteselect != None:
                    self.parent.cibleretour(self.flotteselect.id)

        self.maselection=None

        #else
            #1- clearer les sélection, dnc enlever les encadrer de sur les objet
            #2- faire en sorte de .pack_forget() les label inutiles
            #3- Reprinter les bouton avec une grosseur normale


    def montreetoileselection(self):
        self.btncreervaisseau.pack()
        self.btncreerbatiment.pack()


    def montreflotteselection(self):
        self.lbselectecible.pack()


    def afficherartefacts(self,joueurs):
        pass

    def amiOuAttaque(self, nomjoueur):
        positionRight = int(self.root.winfo_screenwidth()/2 - self.largeur/2)
        positionDown = int(self.root.winfo_screenheight()/2 - self.hauteur/2)

        self.popChoix = Toplevel(master=self.canevas, width=80, height=80)
        self.popChoix.geometry("+{}+{}".format(positionRight,positionDown))
        self.popChoix.title("Amitiée/Attaque")
        self.popChoix.grid()

        self.msg = Message(self.popChoix, text="Faites un choix", width=80, anchor=CENTER).grid(row=0, columnspan=2)

        self.btnAmi = Button(self.popChoix, text = "Ajouter un ami", width = 40, command = lambda: self.parent.demandeAmi(nomjoueur, self.mod.joueurs[self.nom].id)).grid(row=1, column=0)
        self.btnAttaque = Button(self.popChoix, text= "Attaquer", width = 40, command = lambda: self.popChoix.destroy()).grid(row=1, column=1) #COMMANDE À MODIFIER


    def demandeAmi(self, idjoueur):
        positionRight = int(self.root.winfo_screenwidth()/2 - self.largeur/2)
        positionDown = int(self.root.winfo_screenheight()/2 - self.hauteur/2)

        demandeami = StringVar()

        nom=""

        for j in self.mod.joueurs:
            if self.mod.joueurs[j].id == idjoueur:
                nom=self.mod.joueurs[j].nom
                break

        demandeami.set("Vous avez reçu une demande d'alliance de " + nom)

        self.popAmi = Toplevel(master=self.canevas, width=80, height=80)
        self.popAmi.geometry("+{}+{}".format(positionRight,positionDown))
        self.popAmi.title("Demande d'alliance")
        self.popAmi.grid()

        self.msg = Label(self.popAmi, textvariable=demandeami, width=80).grid(row=0, columnspan=2)

        self.btnAccepter = Button(self.popAmi, text = "Accepter", width = 40, command = lambda: self.popAmi.destroy()).grid(row=1, column=0) #COMMANDES À MODIFIER
        self.btnRefuser = Button(self.popAmi, text= "Refuser", width = 40, command = lambda: self.popAmi.destroy()).grid(row=1, column=1)

    def planeteDefense(self):
        popDefense = Toplevel(master=self.canevas, padx=100, pady=60)
