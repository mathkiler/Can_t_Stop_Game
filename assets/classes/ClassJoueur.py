from pygame.locals import *
import pygame

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *


class Joueur :

    def __init__(self, joueur, largeur_ecran, hauteur_ecran, get_chemin) :
        self.hauteur_ecran = hauteur_ecran
        self.largeur_ecran = largeur_ecran
        self.taille_tour = (conv_sizex(50, self.largeur_ecran), conv_sizey(50, self.hauteur_ecran))
        self.taille_pion = (conv_sizex(50, self.largeur_ecran), conv_sizey(50, self.hauteur_ecran))
        self.joueur = joueur #numéro du joueur (1 ou 2)
        if self.joueur == 1 :
            couleur_joueur = "jaune" #variable utile uniquement pour savoir quel image importer (pion_jaune ou pion_rouge)
        else :
            couleur_joueur = "rouge"

        #on importe l'image d'un pion et d'une tour
        self.pion = pygame.transform.scale(pygame.image.load(get_chemin(f"./assets/images/Pions_tour/pion_{couleur_joueur}.png")).convert_alpha(), (conv_sizex(50, self.largeur_ecran), conv_sizey(50, self.hauteur_ecran)))
        self.tour = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/Pions_tour/tour.png")).convert_alpha(), (conv_sizex(50, self.largeur_ecran), conv_sizey(50, self.hauteur_ecran)))
        self.pre_position = pygame.transform.scale(pygame.image.load(get_chemin(f"./assets/images/Pions_tour/forme_pre_position_{couleur_joueur}.png")).convert_alpha(), (conv_sizex(50, self.largeur_ecran), conv_sizey(50, self.hauteur_ecran)))
        #le .convert_alpha est utile pour les image avec des parties transparent

        #placement des tours en haut à gauche de l'écran par défaut
        self.coords_tour = {
            "coords_tour1" : [self.largeur_ecran//38.4, self.hauteur_ecran//21.6],
            "coords_tour2" : [self.largeur_ecran//11.29, self.hauteur_ecran//21.6], 
            "coords_tour3" : [self.largeur_ecran//38.4, self.hauteur_ecran//6.35]
        }
        #dictionnaire qui sauvegarde les coordonnées des pions
        self.coords_pion = {f"coords_pion{k}" : [0, self.hauteur_ecran+self.hauteur_ecran//40] for k in range(2,13)} #liste qui contient les coordonnés en [x, y] des pions. Par défaut ils sont placé en bas à gauche e, dehors de l'écran (on ne les vois pas)

        self.animation_tour = [] #liste qui va comprendre les tours devant effectuer un déplacement (animation)
        self.animation_pion = [] #liste qui va comprendre les pion devant effectuer un déplacement (animation)

        self.pion_placement = [None for k in range(13)] #pion placé qui ne se déplace qu'à la fin d'un tour de jeu. la variable enregistré pour chaque pion est la hauteur (None si le pion n'est pas placé) On met range(13) pour avoir 12 mais on n'utilisera uniquement les pions de 2 à 12 (on initialise quand même les pions 0 et 1 pour éviter des problèmes d'out of range)
        self.progression_tour = {"colonne" : [None, None, None], "hauteur" : [None, None, None]} #tour qui se déplace à chaque choix de lancer un dés. Si aucun choix n'es possible, la progression est perdu
        self.colonne_fini = [] #liste des colonnes que le joueur a fini
        self.colonne_fini_residu = [] #liste des colonnes fini utilisé lorsqu'un tour n'est pas fini et qu'un joueur perd sa progression alors qu'il à atteint un sommet
        self.animation_en_cours = False


    def delplace_Tour(self, colonnes) :#fonction qui va initialiser le déplacement des tours (colonnes sont les colonnes où les tours doivent se déplacer) (il peut y avoir au maximum 2 déplacement)
        #quand on arrive ici, le test si on peut déplacer les tours on déjà été fait. Donc chaque colonne où une tour doit se déplacer, se déplacera. C'est pourquoi il n'y a pas besoin de mettre une sécurité
        self.animation_en_cours = True
        var_tamp = None #variable utile quand les 2 déplacements se font sur la même colonne et qu'il n'y a pas encore eu de déplacement sur cette colonne
        for colonne in colonnes : #on parcours toutes les colonnes où l'on veux qu'une tour se déplace
            if colonne != None : #si colonne est None, c'est 'il n'y a pas de déplacement sur celle-ci
                #on sépare en 2 catégorie : 1 -> une tour est déjà présent sur la colonne. 2 -> aucune tour n'est présent sur la colonne 
                if colonne in self.progression_tour["colonne"] : #True si une tour est déjà sur cette colonne (on avance de 1 dans cette colonne)
                    ind_tour = self.progression_tour["colonne"].index(colonne) #on récupère l'indice de la tour qui est déjà sur la colonne
                    arrive_y = self.hauteur_ecran-(conv_sizey(112, self.hauteur_ecran)+(abs(7-colonne)+(self.progression_tour["hauteur"][ind_tour]))*conv_sizey(72, self.hauteur_ecran)) #calcule de coordonnées d'arrivé de la tour en y
                    self.progression_tour["hauteur"][ind_tour]+=1 #on augmente sa hauteur de 1
                    if test_end_colonne(self.progression_tour["hauteur"][ind_tour], colonne) : #si une tour atteint un sommet, on ajoute cette colonne dans la liste des colonne_fini et la liste des colonne_fini_residu
                        self.colonne_fini.append(colonne)
                        self.colonne_fini_residu.append(colonne)
                    #pour prévoir si on se déplace 2 fois d'un coup sur la même colonne
                    if colonnes[0] == colonnes[1] and var_tamp != None :
                        coords_tour_tamp = var_tamp
                    else :
                        coords_tour_tamp = self.coords_tour[f"coords_tour{ind_tour+1}"][1]
                    #ajout des informations calculé dans la liste d'animation
                    self.animation_tour.append({
                        "pas_X" : 0,
                        "pas_Y" : ((arrive_y)-(coords_tour_tamp))/vitesse_animation,
                        "colonne" : colonne,
                        "images_par_restante" : vitesse_animation,
                        "ind_tour" : ind_tour+1
                    })
                    

                else :
                    ind_tour = 0 #indice de la tour
                    for tour in self.progression_tour["colonne"] : #on regarde chaque tour
                        if tour == None : #si la tour n'est pas encore utilisé
                            self.progression_tour["colonne"][ind_tour] = colonne #on initialise la tour avec colonne et hauteur (à 1 par défaut)
                            if self.pion_placement[colonne] == None : #si un pion n'est pas encore placé dans cette colonne, on l'initialise à 1
                                self.progression_tour["hauteur"][ind_tour] = 1
                            else : #sinon on augmente la hauteur du pion + 1
                                self.progression_tour["hauteur"][ind_tour] = self.pion_placement[colonne]+1 #si un pion est déjà placé dans la colonne. On place la tour un cran au dessus

                            if test_end_colonne(self.progression_tour["hauteur"][ind_tour], colonne) : #si une tour atteint un sommet, on ajoute cette colonne dans la liste des colonne_fini et la liste des colonne_fini_residu
                                self.colonne_fini.append(colonne)
                                self.colonne_fini_residu.append(colonne)
                            arrive_y = self.hauteur_ecran-(conv_sizey(112, self.hauteur_ecran)+(abs(7-colonne)+(self.progression_tour["hauteur"][ind_tour]-1))*conv_sizey(72, self.hauteur_ecran)) #calcule de coordonnées d'arrivé de la tour en y
                            arrive_x = conv_sizex(197, self.largeur_ecran)+(colonne-2)*(conv_sizex(70, self.largeur_ecran)) #calcule de coordonnées d'arrivé de la tour en x
                            #ajout des informations calculé dans la liste d'animation
                            self.animation_tour.append({
                                "pas_X" : ((arrive_x)-(self.coords_tour[f"coords_tour{ind_tour+1}"][0]))/vitesse_animation,
                                "pas_Y" : ((arrive_y)-(self.coords_tour[f"coords_tour{ind_tour+1}"][1]))/vitesse_animation,
                                "colonne" : colonne,
                                "images_par_restante" : vitesse_animation,
                                "ind_tour" : ind_tour+1
                            })
                            if colonnes[0] == colonnes[1] :
                                var_tamp = arrive_y
                            break
                        ind_tour+=1
                            

            
    def deplace_Pion(self) : #fonction qui initialise le déplacement des pions
        self.animation_en_cours = True
        ind_tour = 1 #indice de la tour ici on commence à 1 car on est pas en mode indice. On l'utilise dans coords_tour1, coords_tour2, coords_tour3
        for colonne in self.progression_tour["colonne"] :
            if colonne != None :
                #calcule et ajout des coordonnées et information dans la liste d'animation des pions
                self.animation_pion.append({
                    "pas_X" : (self.coords_tour[f"coords_tour{ind_tour}"][0]-self.coords_pion[f"coords_pion{colonne}"][0])/vitesse_animation,
                    "pas_Y" : (self.coords_tour[f"coords_tour{ind_tour}"][1]-self.coords_pion[f"coords_pion{colonne}"][1])/vitesse_animation,
                    "colonne" : colonne,
                    "images_par_restante" : vitesse_animation
                })
            ind_tour+=1


    def test_si_gagnant(self) : #fonction qui test si le joueur self est un gagnant
        if len(self.colonne_fini) == 3 :#s'il a fini 3 colonne : 3 pion (et non tour) on atteint le sommet
            return True
        return False


    def reinitialisation(self) : #fonction qui réinitialise la classe
        self.coords_tour = {
            "coords_tour1" : [self.largeur_ecran//38.4, self.hauteur_ecran//21.6],
            "coords_tour2" : [self.largeur_ecran//11.29, self.hauteur_ecran//21.6], 
            "coords_tour3" : [self.largeur_ecran//38.4, self.hauteur_ecran//6.35]
        }

        self.coords_pion = {f"coords_pion{k}" : [0, self.hauteur_ecran+self.hauteur_ecran//40] for k in range(2,13)} #liste qui contient les coordonnés en [x, y] des pions. Par défaut ils sont placé en bas à gauche e, dehors de l'écran (on ne les vois pas)

        self.animation_tour = [] #liste qui va comprendre les tours devant effectuer un déplacement (animation)
        self.animation_pion = []

        self.pion_placement = [None for k in range(13)] #pion placé qui ne se déplace qu'à la fin d'un tour de jeu. On met range(13) pour avoir 12 mais on n'utilisera uniquement les pions de 2 à 12 (on initialise quand même les pions 0 et 1 pour éviter des problèmes d'out of range)
        self.progression_tour = {"colonne" : [None, None, None], "hauteur" : [None, None, None]} #tour qui se déplace à chaque choix de lancer un dés. Si aucun choix n'es possible, la progression est perdu
        self.colonne_fini = [] #liste des colonnes que le joueur a fini
        self.animation_en_cours = False


