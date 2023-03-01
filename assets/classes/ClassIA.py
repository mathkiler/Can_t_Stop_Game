from random import choice, randint
import copy
from time import sleep

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *


class IA :
    
    def __init__(self) :
        self.nombre_iterration = 100
        self.joueur_actuel = "IA" #ici, l'IA commence toujours à jouer
        self.progression_tour = {"IA" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}, 
                                  "joueur" : {"colonne" : [None, None, None], "hauteur" : [None, None, None]}}
        self.pion_placement = {"IA" : [None for k in range(13)], 
                               "joueur" : [None for k in range(13)]}
        self.colonne_fini = {"IA" : [], 
                             "joueur" : []}
        self.colonne_fini_residu = {"IA" : [], 
                             "joueur" : []}

    def calcule_meilleur_choix(self, choix, j1, j2) : #on reçoit par choix les boutons sur lesquelles on peut clicker #on considaire que j1 = joueur et j2 = IA
        if len(choix) == 1 : #ici, on n'as qu'un bouton/choix possible. On choisi donc ce bouton
            choix[0]["clic"] = True
        else :
            nombre_gagnant = [{"IA" : 0, "joueur" : 0} for k in range(len(choix))]
            ratio = []

            for iterration in range(self.nombre_iterration) :
                self.initialisation_simulation(j1, j2)
                for choi in choix :
                    ind_choix = choix.index(choi)
                    #variable qui contient le nombre de partie gagné par joueur (j2 = IA)
                    #on ramène notre choix à "lancer les dés" pour synchroniser toutes les simulations possible 
                    if choi["type_bouton"] == "stop" :
                        self.deplacement_pion()
                        if self.test_joueur_gagnant() :
                            nombre_gagnant[ind_choix][f"{self.joueur_actuel}"]+=1
                            break
                        self.changement_joueur()
                    elif choi["type_bouton"] == "progression" :
                        self.deplacement_tour(choi["info_sup"])
 
                    
                    #boucle d'une partie. On tourne en boucle tant qu'il n'y a pas un gagnant 
                    while True :
                        result_lancer_des = self.lancer_des()
                        if result_lancer_des == False :
                            self.suppression_sauvegarde_tour()
                            self.changement_joueur()
                        else :
                            self.deplacement_tour(choice(result_lancer_des))
                            choix_lancer_stop = choice(["lancer_des", "stop"])
                            if choix_lancer_stop == "stop" :
                                self.deplacement_pion()
                                if self.test_joueur_gagnant() :
                                    nombre_gagnant[ind_choix][f"{self.joueur_actuel}"]+=1
                                    break
                                self.changement_joueur()
            
            #on calcule le ratio gagnant pour l'IA uniquement (nombre de partie gagné par l'IA/nombre de partie total)
            for choix_gagnant in nombre_gagnant :
                ratio.append(choix_gagnant["IA"]/self.nombre_iterration)
            #on choisi le meilleur choix pour clicker sur ce bouton
            print(ratio, nombre_gagnant, choix, "\n\n")
            while True :
                ind_meilleur_choix = randint(0,len(ratio)-1)
                if ratio[ind_meilleur_choix] == max(ratio) :
                    break

            
            choix[ind_meilleur_choix]["clic"] = True
            print("choix : " +choix[ind_meilleur_choix]["type_bouton"]+"\n\__________________n")
            





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
            cas_figure = -1 #var qui indiue le cas de figure des dés comme par exemple cas 0, la progression sur les 2 combinaison est possible
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
                        self.progression_tour[f"{self.joueur_actuel}"]["colonne"][ind_tour] = colonne #on initialise la tour avec colonne et hauteur (à 1 par défault)
                        if self.pion_placement[f"{self.joueur_actuel}"][colonne] == None :
                            self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] = 1
                        else :
                            self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour] = self.pion_placement[f"{self.joueur_actuel}"][colonne]+1 #si un pion est déjà placé dans la colonne. On place la tour un cran au dessus
                            
                        if test_end_colonne(self.progression_tour[f"{self.joueur_actuel}"]["hauteur"][ind_tour], colonne) :
                            self.colonne_fini[f"{self.joueur_actuel}"].append(colonne)
                            self.colonne_fini_residu[f"{self.joueur_actuel}"].append(colonne)
                    ind_tour+=1



    def deplacement_pion(self) :

        #asignation de la nouvelle hauteur pour chaque pion en fonction de la hauteur des tours
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
        #copy des colonnes résidu fini (rappel des colonnes fini résidu : sauvegarde les tour arrivé au sommet mais pas encore enregistré en tant que pion. Si le joueur désside de ne pas arrêter son tour de jeu, il risque de perdre la progression de ses tours arrivé au sommet)
        self.colonne_fini_residu["joueur"] = j1.colonne_fini_residu.copy()
        self.colonne_fini_residu["IA"] = j2.colonne_fini_residu.copy()


    def suppression_sauvegarde_tour(self) :
        self.progression_tour[f"{self.joueur_actuel}"] = {"colonne" : [None, None, None], "hauteur" : [None, None, None]}
        for col in self.colonne_fini_residu[f"{self.joueur_actuel}"] :
            self.colonne_fini[f"{self.joueur_actuel}"].pop(self.colonne_fini[f"{self.joueur_actuel}"].index(col))
        self.colonne_fini_residu[f"{self.joueur_actuel}"] = []
