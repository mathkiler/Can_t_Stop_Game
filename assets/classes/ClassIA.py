from random import choice, randint
import copy
import threading
import sys

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *


class IA (threading.Thread):
    def __init__(self, choix, j1, j2) : #on prend en paramètre les choix possible (boutons) et l'état actuel du jeu à travers les classes joueur 1 et joueur 2
        #les choix sont directement la liste boutons.liste_bouton et hérite de ces propriété comme "clic" pour simuler un clic sur un bouton en particulier
        threading.Thread.__init__(self) #le thread permet au jeu de continuer à faire des animation pendant le calcule du prochain choix de l'IA
        self.choix = choix
        self.j1 = j1
        self.j2 = j2
        self.joueur_actuel = "IA" #ici, l'IA commence toujours à jouer
        #variable/listes qui vont simuler les nombre_iterration de jeu
        self.progression_tour = {"IA" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}, 
                                  "joueur" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}}
        self.pion_placement = {"IA" : [None for k in range(13)], 
                               "joueur" : [None for k in range(13)]}
        self.colonne_fini = {"IA" : [], 
                             "joueur" : []}
        self.colonne_fini_residu = {"IA" : [], 
                             "joueur" : []}

    def run(self) : #on reçoit par choix les boutons sur lesquelles on peut cliquer #on considère que j1 = joueur et j2 = IA
        if len(self.choix) == 0 :
            sys.exit() #permet de fermer le thread
        elif len(self.choix) == 1 : #ici, on n'as qu'un bouton/choix possible. On choisi donc ce bouton
            self.choix[0]["clic"] = True
            sys.exit() #permet de fermer le thread
        else :
            #rajout d'amélioration de l'IA : s'il lui reste au moins une tour, l'IA peut forcément jouer au prochain tour en relancent les dés. Donc on force le choix de relancer les dés  
            if self.choix[0]["type_bouton"] == "lancer_des" :
                if self.j2.progression_tour["colonne"].count(None) >=1 :#l'IA a au moins une tour de disponible
                    self.choix[0]["clic"] = True #on force le choix à "lancer_des"
                    sys.exit() #permet de fermer le thread

            nombre_gagnant = [{"IA" : 0, "joueur" : 0} for k in range(len(self.choix))] #initialisation de la liste du nombre de gagnant IA et joueur pour calculer le ratio après
            ratio = []

            for iterration in range(nombre_iterration) : #on boucle nombre_iterration de fois chaque choix possible pour avoir un ratio plus précis (loi des grand nombre)
                for choi in self.choix : #on regarde chaque choix possible
                    self.initialisation_simulation(self.j1, self.j2) #on initialise le jeu à l'état qu'est en réalité le jeu
                    ind_choix = self.choix.index(choi) #indice du choix dans la liste des choix (bouton) possible
                    #on initialise avant de boucler à l'infini pour synchroniser tout les choix à "lancer les dés"
                    #on ramène donc à "lancer les dés" (cheminement expliqué dans la boucle en dessous)
                    if choi["type_bouton"] == "stop" :
                        self.deplacement_pion()
                        if self.test_joueur_gagnant() :
                            nombre_gagnant[ind_choix][f"{self.joueur_actuel}"]+=1
                            break
                        self.changement_joueur()
                    elif choi["type_bouton"] == "progression" :
                        self.deplacement_tour(choi["info_sup"])
 
                    
                    #boucle d'une partie. On tourne en boucle tant qu'il n'y a pas de gagnant 
                    while True :
                        result_lancer_des = self.lancer_des() #on lance les dés
                        if result_lancer_des == False : #si aucun choix n'est possible
                            self.suppression_sauvegarde_tour() #réinitialisation de la position des tour (et donc suppression de cette "sauvegarde des tour")
                            self.changement_joueur() #on change de joueur 
                        else : #sinon si au moins un choix est possible
                            self.deplacement_tour(choice(result_lancer_des)) #on choisis au hasard parmi tout les choix possible dans result_lancer_des avec la fonction choice du module random. On affecte directement le déplacement des tours
                            choix_lancer_stop = choice(["lancer_des", "stop"]) #ensuite on choisis au hasard entre lancer les dés et "stop"
                            if choix_lancer_stop == "stop" : #si on a choisis de s'arrêter
                                self.deplacement_pion()#déplacement des pions
                                if self.test_joueur_gagnant() : #test si la partie est fini
                                    nombre_gagnant[ind_choix][f"{self.joueur_actuel}"]+=1 #si oui, on ajoute +1 au nombre de partie gagné au joueur self.joueur_actuel
                                    break #puis on sort de la boucle
                                self.changement_joueur() #s'il n'y a pas de gagnant, on change de joueur et repart à "lancer les dés" en haut de la boucle
                            #else : si on a choisis "lancer_des" on remonte en haut de la boucle où on lance les dés
            
            #on calcule le ratio gagnant pour l'IA uniquement (nombre de partie gagné par l'IA/nombre de partie total)
            for choix_gagnant in nombre_gagnant :
                ratio.append(choix_gagnant["IA"]/nombre_iterration) 
            #on choisi le meilleur choix pour cliquer sur ce bouton
            print(f"{ratio=}", f"{nombre_gagnant=}", f"{self.choix=}", "\n\n")
            while True : #choix du meilleur choix. On a un boucle car si 2 choix on le même ratio, on ne choisis pas le premier mais de manière aléatoire entre les meilleur choix
                ind_meilleur_choix = randint(0,len(ratio)-1)
                if ratio[ind_meilleur_choix] == max(ratio) : #on sort de la boucle ssi on le choix a le meilleur ratio
                    break
            self.choix[ind_meilleur_choix]["clic"] = True #on change la valeur du choix(bouton) du clic à True pou qu'on puisse simuler un clic interne et que le jeu puisse continuer
            print("choix : " +self.choix[ind_meilleur_choix]["type_bouton"]+"\n\__________________n")
        sys.exit() #permet de fermer le thread



    #on redéfini les fonction du jeu mais sans prendre en compte des coordonnées.
    #ces fonction sont donc très similaire voir copier coller au jeu et au classes respective. Mise à part qu'elle on été simplifié dans un usage faîte pour l'IA uniquement (donc aucune interface) et optimisé

    def lancer_des(self) :
        des = [randint(1,6) for k in range(4)]
        colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}

        colonne_association["possibilité_1"].append(des[0]+des[1])
        colonne_association["possibilité_1"].append(des[2]+des[3])
        colonne_association["possibilité_2"].append(des[0]+des[2])
        colonne_association["possibilité_2"].append(des[1]+des[3])
        colonne_association["possibilité_3"].append(des[0]+des[3])
        colonne_association["possibilité_3"].append(des[1]+des[2])
        nombre_choix_impossible = 0
        choix_possible = []
        
        for possibilite in colonne_association.values() :
            #choix où les deux déplacement sont possible
            cas_figure = -1 #var qui indique le cas de figure des dés comme par exemple cas 0, la progression sur les 2 combinaison est possible
            if self.progression_tour[f"{self.joueur_actuel}"]["colonne"].count(None) >= 2 :
                if possibilite[0] not in self.colonne_fini[f"{self.joueur_actuel}"] and possibilite[1] not in self.colonne_fini[f"{self.joueur_actuel}"] :
                    cas_figure = 0
                elif possibilite[0] in self.colonne_fini[f"{self.joueur_actuel}"] :
                    cas_figure = 2
                elif possibilite[1] in self.colonne_fini[f"{self.joueur_actuel}"] :
                    cas_figure = 1
            elif self.progression_tour[f"{self.joueur_actuel}"]["colonne"].count(None) == 1 :
                if (possibilite[0] not in self.colonne_fini[f"{self.joueur_actuel}"] and possibilite[1] not in self.colonne_fini[f"{self.joueur_actuel}"]) and (possibilite[0] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] or possibilite[1] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"]):
                    cas_figure = 0
                elif possibilite[0] not in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] and possibilite[1] not in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] :
                    if possibilite[0] in self.colonne_fini[f"{self.joueur_actuel}"] :
                        cas_figure = 2
                    elif possibilite[1] in self.colonne_fini[f"{self.joueur_actuel}"] :
                        cas_figure = 1
                    else :
                        cas_figure = 3
            elif self.progression_tour[f"{self.joueur_actuel}"]["colonne"].count(None) == 0 :
                if (possibilite[0] not in self.colonne_fini[f"{self.joueur_actuel}"] and possibilite[1] not in self.colonne_fini[f"{self.joueur_actuel}"]) and possibilite[0] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] and possibilite[1] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] :
                    if possibilite[0] in self.colonne_fini[f"{self.joueur_actuel}"] :
                        cas_figure = 2
                    if possibilite[1] in self.colonne_fini[f"{self.joueur_actuel}"] :
                        cas_figure = 1
                if possibilite[0] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] and possibilite[0] not in self.colonne_fini[f"{self.joueur_actuel}"] :
                    cas_figure = 1
                if possibilite[1] in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] and possibilite[1] not in self.colonne_fini[f"{self.joueur_actuel}"] :
                    cas_figure = 2

            #test pour éviter de faire un double alors que le sommet n'es que à une seul case. Si ce cas se présente, on force l'affichage et le choix d'une seul possibilité (on remplace par exemple un "Progresser sur 7 et 7" par un "Progresser sur 7")
            for ind_tour in range(3) :
                if self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] == None and self.pion_placement[f"{self.joueur_actuel}"][possibilite[0]] != None:
                    tamp = self.pion_placement[f"{self.joueur_actuel}"][possibilite[0]]+1
                elif self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] != None :
                    tamp = self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour]+1
                else :
                    tamp = None
                if cas_figure == 0 and possibilite[0] == possibilite[1] and test_end_colonne(tamp, possibilite[0]) :
                    cas_figure = 1

            if cas_figure == 0 :
                choix_possible.append(possibilite)
            elif cas_figure == 1 :
                choix_possible.append([possibilite[0]])
            elif cas_figure == 2 :
                choix_possible.append([possibilite[1]])
            elif cas_figure == 3 :
                choix_possible.append([possibilite[0]])
                choix_possible.append([possibilite[1]])
            if cas_figure == -1 :
                nombre_choix_impossible+=1
        if nombre_choix_impossible == 3 :
            return False
        return choix_possible
            

    def changement_joueur(self) :
        if self.joueur_actuel == "IA" :
            self.joueur_actuel = "joueur"
        else :
            self.joueur_actuel = "IA"


    def deplacement_tour(self, movement) :

        for colonne in movement :
            if colonne in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] :
                ind_tour = self.progression_tour[f"{self.joueur_actuel}"]["colonne"].index(colonne)
                self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour]+=1
            else :
                ind_tour = 0
                for tour in self.progression_tour[f"{self.joueur_actuel}"]["colonne"] :
                    if tour == None :
                        self.progression_tour[f"{self.joueur_actuel}"]["colonne"][ind_tour] = colonne #on initialise la tour avec colonne et hauteur (à 1 par défaut)
                        if self.pion_placement[f"{self.joueur_actuel}"][colonne] == None :
                            self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] = 1
                        else :
                            self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] = self.pion_placement[f"{self.joueur_actuel}"][colonne]+1 #si un pion est déjà placé dans la colonne. On place la tour un cran au dessus
                            
                        if test_end_colonne(self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour], colonne) :
                            self.colonne_fini[f"{self.joueur_actuel}"].append(colonne)
                            self.colonne_fini_residu[f"{self.joueur_actuel}"].append(colonne)
                    ind_tour+=1



    def deplacement_pion(self) :

        #assignation de la nouvelle hauteur pour chaque pion en fonction de la hauteur des tours
        for ind_tour in range(3) :
            if self.progression_tour[f"{self.joueur_actuel}"]["colonne"][ind_tour] != None :
                self.pion_placement[f"{self.joueur_actuel}"][self.progression_tour[f"{self.joueur_actuel}"]["colonne"][ind_tour]] = self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour]
        #on réinitialise les tours
        self.progression_tour = {"IA" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}, 
                                  "joueur" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}}
        


    def test_joueur_gagnant(self) :
        if len(self.colonne_fini[f"{self.joueur_actuel}"]) == 3 :
            return True
        return False

    def initialisation_simulation(self, j1, j2) : #sachant que j2 est toujours l'IA
        #copy du jeu actuel pour y faire des simulations
        #copy des tours
        self.progression_tour["joueur"]["colonne"] = j1.progression_tour["colonne"].copy()
        self.progression_tour["joueur"]["hauteur"] = j1.progression_tour["hauteur"].copy()
        self.progression_tour["IA"]["colonne"] = j2.progression_tour["colonne"].copy()
        self.progression_tour["IA"]["hauteur"] = j2.progression_tour["hauteur"].copy()
        #copy des pions
        self.pion_placement["joueur"] = j1.pion_placement.copy()
        self.pion_placement["IA"] = j2.pion_placement.copy()
        #copy des colonnes fini
        self.colonne_fini["joueur"] = j1.colonne_fini.copy()
        self.colonne_fini["IA"] = j2.colonne_fini.copy()
        #copy des colonnes résidu fini (rappel des colonnes fini résidu : sauvegarde les tour arrivé au sommet mais pas encore enregistré en tant que pion. Si le joueur décide de ne pas arrêter son tour de jeu, il risque de perdre la progression de ses tours arrivé au sommet)
        self.colonne_fini_residu["joueur"] = j1.colonne_fini_residu.copy()
        self.colonne_fini_residu["IA"] = j2.colonne_fini_residu.copy()


    def suppression_sauvegarde_tour(self) :
        self.progression_tour[f"{self.joueur_actuel}"] = {"colonne" : [None, None, None], "hauteur" : [None, None, None]}
        for col in self.colonne_fini_residu[f"{self.joueur_actuel}"] :
            self.colonne_fini[f"{self.joueur_actuel}"].pop(self.colonne_fini[f"{self.joueur_actuel}"].index(col))
        self.colonne_fini_residu[f"{self.joueur_actuel}"] = []
