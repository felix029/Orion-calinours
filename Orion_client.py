# -*- coding: utf-8 -*-
# version avec AI ajoute
import os,os.path
import sys
import xmlrpc.client
import socket
import random
from subprocess import Popen
from helper import Helper as hlp
from Orion_modele import *
from Orion_vue import *


class Controleur():
    def __init__(self):

        print("IN CONTROLEUR")
        self.attente=0
        self.cadre=0 # le no de cadre pour assurer la syncronisation avec les autres participants
        self.tempo=0 # insert a reconnaitre qu'on a lance le serveur et qu'on peut s'inscrire automatiquement sans cliquer sur inscription dans l'interface
                     # ne peut pas etre remplace par egoserveur car si cette variable test a vrai (1), l'inscription est effectuee et tempo remis a 0 pour ne pas reinscrire deux fois...
                     # NOTE le nom de variable est ici epouvantable, j'en conviens - devrait quelquechose comme 'autoInscription'
        self.egoserveur=0 # est-ce que je suis celui qui a demarre le serveur, a priori, non (0)
        self.actions=[]    # la liste de mes actions a envoyer au serveur pour qu'il les redistribue a tous les participants
        self.statut=0 # etat dans le quel je me trouve : 0 -> rien, 1 -> inscrit, 2 -> demarre, 3-> joue
        self.monip=self.trouverIP() # la fonction pour retourner mon ip
        self.monnom=self.generernom() # un generateur de nom pour faciliter le deboggage (comme il genere un nom quasi aleatoire et on peut demarrer plusieurs 'participants' sur une même machine pour tester)
        self.modele=None
        self.serveur=None
        self.vue=Vue(self,self.monip,self.monnom)
        self.vue.root.mainloop()

    def trouverIP(self): # fonction pour trouver le IP en 'pignant' gmail
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # on cree un socket
        s.connect(("gmail.com",80))    # on envoie le ping
        monip=s.getsockname()[0] # on analyse la reponse qui contient l'IP en position 0
        s.close() # ferme le socket
        return monip

    def generernom(self):  # generateur de nouveau nom - accelere l'entree de nom pour les tests - parfois � peut generer le meme nom mais c'est rare
        noms=["SimonCharles69", "Phoenix-O", "Guiyomm", "YAAAAS", "DIEU", "NicolasCage", "JabaTheSlutt", "Jonh-Marque", "TitusPinus", "AccepteToi", "OliPrime", "Tchoin", "LaStrap", "Bo_BB"]
        monnom=noms.pop(random.randrange(0,13))
        return monnom

    def creerpartie(self):
        if self.egoserveur==0:
            dir_path = os.path.dirname(os.path.realpath(__file__))

            print(dir_path)
            print(os.getcwd)

            pid = Popen([sys.executable, dir_path + '/Orion_serveur.py'],shell=1).pid # on lance l'application serveur
            self.egoserveur=1 # on note que c'est soi qui, ayant demarre le serveur, aura le privilege de lancer la simulation
            self.vue.btnlancerpartie.config(state=NORMAL)
            self.tempo=1 # on change d'etat pour s'inscrire automatiquement
                         # (parce que dans ce type de programme on prend pour acquis que celui qui prepare la simulation veut aussi y participer)

    # NOTE si on demarre le serveur, cette fonction est appellee pour nous (voir timer et variable tempo)
    #      ou par un clique sur le bouton 'Creerunclient' du layout
    def inscrirejoueur(self):
        ipserveur=self.vue.ipsplash.get() # lire le IP dans le champ du layout
        nom=self.vue.nomsplash.get() # noter notre nom
        if ipserveur and nom:
            ad="http://"+ipserveur+":9999"
            self.serveur=xmlrpc.client.ServerProxy(ad)
            self.monnom=nom
            rep=self.serveur.inscrireclient(self.monnom)    # on averti le serveur de nous inscrire
            #tester retour pour erreur de nom
            self.statut=1 # statut 1 == attente de lancement de partie
            random.seed(rep[2])

    ## ----------- FONCTION POUR CELUI QUI A CREE LA PARTIE SEULEMENT
    def lancerpartie(self): # reponse du bouton de lancement de simulation (pour celui qui a parti le serveur seulement)
        rep=self.serveur.lancerpartie()
        print("REP DU LANCER",rep)
        if rep==1:
            self.statut=3 # il change son statut pour lui permettre d'initer la simulation, les autres sont en 1 (attente) - voir timer.py
    ## ----------- FIN --

    def initierpartie(self,rep):  # initalisation locale de la simulation, creation du modele, generation des assets et suppression du layout de lobby
        if rep[1][0][0]=="lancerpartie":
            self.modele=Modele(self,rep[1][0][1]) # on cree le modele
            self.vue.creeraffichercadrepartie(self.modele)
            print(self.monnom,"LANCE PROCHAINTOUR")
            self.prochaintour()

    def boucleattente(self):
        print("IN BOUCLEATTENTE")
        rep=self.serveur.faireaction([self.monnom,0,0])
        print("RETOUR DU faire action  SERVEUR",rep)
        if rep[0]:
            print("Recu ORDRE de DEMARRER")
            # PATCH pour dico in xmlrpc qui requiert des chaines comme cles
            # On a recu un cle str qu'on retransforme en int (pour compter les cadres de jeu, servant a distribuer les taches)
            cle=list(rep[2].keys())[0]
            rep[2]={int(cle):rep[2][cle]}  # on transforme la cle de str à int avant le transfert - voir aussi prochaintour (plus bas)
            # fin de patch
            self.initierpartie(rep[2])
        elif rep[0]==0:
            self.vue.affichelisteparticipants(rep[2])
            self.vue.root.after(1000,self.boucleattente)

    def prochaintour(self): # la boucle de jeu principale, qui sera appelle par la fonction bouclejeu du timer
        if self.serveur: # s'il existe un serveur
            self.cadre=self.cadre+1 # increment du compteur de cadre
            if self.attente==0:
                self.modele.prochaineaction(self.cadre)    # mise a jour du modele
                self.vue.afficherpartie(self.modele)     # mise a jour de la vue
            if self.actions: # si on a des actions a partager
                rep=self.serveur.faireaction([self.monnom,self.cadre,self.actions]) # on les envoie
            else:
                rep=self.serveur.faireaction([self.monnom,self.cadre,0]) # sinon on envoie rien au serveur on ne fait que le pigner
                                                                        # (HTTP requiert une requete du client pour envoyer une reponse)
            self.actions=[] # on s'assure que les actions a`envoyer sont maintenant supprimer (on ne veut pas les envoyer 2 fois)
            if rep[0]: # si le premier element de reponse n'est pas vide

                # PATCH de dico in xmlrpc (vs Pyro utilise avant)
                cle=list(rep[2].keys())[0]
                #print("AVANT",rep[2])
                rep[2]={int(cle):rep[2][cle]}
                #print("APRES",rep[2])
                # FIN DE PATCH

                for i in rep[2]:   # pour chaque action a faire (rep[2] est dictionnaire d'actions en provenance des participants
                                   # dont les cles sont les cadres durant lesquels ses actions devront etre effectuees
                    if i not in self.modele.actionsafaire.keys(): # si la cle i n'existe pas
                        self.modele.actionsafaire[i]=[] #faire une entree dans le dictonnaire
                    for k in rep[2][i]: # pour toutes les actions lies a une cle du dictionnaire d'actions recu
                        self.modele.actionsafaire[i].append(k) # ajouter cet action au dictionnaire sous l'entree dont la cle correspond a i
            if rep[1]=="attend": # si jamais rep[0] est vide MAIS que rep[1] == 'attend', on veut alors patienter
                self.cadre=self.cadre-1  # donc on revient au cadre initial
                self.attente=1
                #print("ALERTE EN ATTENTE",self.monnom)
            else:
                self.attente=0
            self.vue.root.after(50,self.prochaintour)
        else:
            print("Aucun serveur connu")

    def fermefenetre(self):
        if self.serveur:
            self.serveur.jequitte(self.monnom)
        self.vue.root.destroy()

    def creervaisseau(self,idplanete):
        self.actions.append([self.monnom,"creervaisseau",idplanete])

    def ciblerflotte(self,idorigine,iddestination,typedestination):
        self.actions.append([self.monnom,"ciblerflotte",[idorigine,iddestination,typedestination]])

    #Ajouter 15 avril FelixO
    def ciblerflotteplanete(self,idorigine,iddestination,etoile):
        self.actions.append([self.monnom,"ciblerflotteplanete",[idorigine,iddestination,etoile]])

    #Ajouter le 9 avril par Nic
    def creerBatiment(self,p,typeBatiment,x,y):
        self.actions.append([self.monnom,"creerBatiment",[p,typeBatiment,x,y]])

    def creerTourDefense(self,p,x,y):
        self.actions.append([self.monnom,"creerTourDefense",[p,x,y]])

     #Ajouter le 9 avril par Nic
    def upgBatiment(self,idBatiment):
        self.actions.append([self.monnom,"upgBatiment",idBatiment])

    def detruire(self):
        self.actions.append([self.monnom,"detruire",""])

    def modifRessource(self):
        self.actions.append([self.monnom,"modifRessource",""])
    #Ajouter par Felix-O le 16 avril
    def cibleretour(self,idori):
        self.actions.append([self.monnom,"cibleretour",idori])

    #Ajouter par Felix-O le 23 avril
    def versvue1(self,idflotte,idetoile):
        self.actions.append([self.monnom, "versvue1",[idflotte, idetoile]])

    #Ajouter par Felix-O le 23 avril
    def versvue0(self,idflotte,idplanete):
        self.actions.append([self.monnom, "versvue0", [idflotte, idplanete]])
    #Ajouter par Guillaume le 6 mai
    def colonisation(self):
        self.actions.append([self.monnom, "colonisation", ""])

    #Ajouter par Felix-O 14 mai
    def demandeAmi(self,nom,idjoueur):
        self.actions.append([nom, "demandeAmi", idjoueur])
        self.vue.popChoix.destroy()

if __name__=="__main__":
    c=Controleur()
    print("End Orion_mini")