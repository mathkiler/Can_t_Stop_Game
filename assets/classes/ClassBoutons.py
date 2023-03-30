from pygame.locals import *
import pygame

from assets.classes.fonction_auxiliere import *

class Boutons :

    def __init__(self, largeur_ecran, hauteur_ecran, get_chemin) :
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.taille_bouton = (conv_sizex(550, largeur_ecran), conv_sizey(90, hauteur_ecran))
        self.image_bouton_shape = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/boutons/bouton_shape.png")).convert_alpha(), (self.taille_bouton[0], self.taille_bouton[1]))
        self.image_bouton_shape_survol = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/boutons/bouton_shape_survol.png")).convert_alpha(), (self.taille_bouton[0], self.taille_bouton[1]))
        self.liste_bouton = [] #liste contenant tout les boutons affiché et effectif sur l'écran
        self.bouton_retour_menu = None #variable du bouton de retour au menu (il est séparé des autres boutons car il est spécial (effet différent))
        #images survol et non survol du bouton retour au menu
        self.image_bouton_croix = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/boutons/bouton_croix.png")).convert_alpha(), (conv_sizex(77, self.largeur_ecran), conv_sizey(78, self.hauteur_ecran)))
        self.image_bouton_croix_survol = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/boutons/bouton_croix_survol.png")).convert_alpha(), (conv_sizex(360, self.largeur_ecran), conv_sizey(78, self.hauteur_ecran)))

    def creation_bouton(self, position_x, position_y, texte, type, info_sup) : #info sup est utile pour y mettre des information utile au bouton des choix de dés
        if type == "retour_menu" : #le bouton retour au menu dans une partie est spécial (taille différente) et doit rester affiché tout du long d'une partie
            self.bouton_retour_menu = {"type_bouton" : type,
                                    "position_x" : position_x,
                                    "position_y" : position_y,
                                    "texte" : texte,
                                    "survol" : False, #survol est True sur on passe la sourie par dessus le bouton
                                    "clic" : False,
                                    "info_sup" : info_sup} #clic est True si on clic sur le bouton
            return 
        self.liste_bouton.append({"type_bouton" : type,
                                  "position_x" : position_x-self.taille_bouton[0]//2,
                                  "position_y" : position_y-self.taille_bouton[1]//2,
                                  "texte" : texte,
                                  "survol" : False, #survol est True sur on passe la sourie par dessus le bouton
                                  "clic" : False,
                                  "info_sup" : info_sup}) #clic est True si on clic sur le bouton
    
    def destruction_bouton_retour_menu(self) : #destruction du bouton retour au menu
        self.bouton_retour_menu = None
    
    def destruction_tout_les_boutons(self) : #destruction de tout les boutons créé
        self.liste_bouton = []
    
    def test_survole(self, pos_sourie_X, pos_sourie_Y, clic, text_joueur_actuel, IA_joue) : #fonction qui test le survole avec la sourie et s'il y a un clic sur le bouton
        for bouton in self.liste_bouton : #on regarde chaque bouton
            bouton["survol"] = False #par default, le survole est False
            if bouton["position_x"] < pos_sourie_X < bouton["position_x"]+self.taille_bouton[0] and bouton["position_y"] < pos_sourie_Y < bouton["position_y"]+self.taille_bouton[1] : #si la position de la sourie est dans la hitbox (au dessus du bouton en X et Y)
                bouton["survol"] = True
                if clic == 1 : #si il y a eu un clic avec le clic gauche (qui est 1)
                    if IA_joue and text_joueur_actuel == 2 : #si l'IA est activé et c'est au tour de l'IA (car l'IA prend la place du joueur 2) alors on bloque la possibilité de clic à la place de l'IA
                        pass 
                    else : #sinon on met le clic à True
                        bouton["clic"] = True
        if self.bouton_retour_menu != None : #si le bouton retour au menu est présent, on effectue des calcules différents 
            if self.bouton_retour_menu["survol"] :
                if conv_sizex(1560, self.largeur_ecran) < pos_sourie_X < self.largeur_ecran and 0 < pos_sourie_Y < conv_sizey(78, self.hauteur_ecran) :
                    if clic == 1 :
                        self.bouton_retour_menu["clic"] = True
                else :
                    self.bouton_retour_menu["survol"] = False
            else :
                if conv_sizex(1843, self.largeur_ecran) < pos_sourie_X < self.largeur_ecran and 0 < pos_sourie_Y < conv_sizey(78, self.hauteur_ecran) :
                    self.bouton_retour_menu["survol"] = True
                    if clic == 1 :
                        self.bouton_retour_menu["clic"] = True
                else :
                    self.bouton_retour_menu["survol"] = False