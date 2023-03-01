from pygame.locals import *
import pygame

from assets.classes.fonction_auxiliere import *

class Boutons :

    def __init__(self, largeur_ecran, hauteur_ecran, resource_path0) :
        self.taille_bouton = (conv_sizex(550, largeur_ecran), conv_sizey(90, hauteur_ecran))
        self.image_bouton_shape = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/boutons/bouton_shape.png")).convert_alpha(), (self.taille_bouton[0], self.taille_bouton[1]))
        self.image_bouton_shape_survol = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/boutons/bouton_shape_survol.png")).convert_alpha(), (self.taille_bouton[0], self.taille_bouton[1]))
        self.liste_bouton = [] #liste contenant tout les boutons affiché et effectif sur l'écran

    def creation_bouton(self, position_x, position_y, texte, type, info_sup) : #info sup est utile pour y mettre des information utile au bouton des choix de dés
        self.liste_bouton.append({"type_bouton" : type,
                                  "position_x" : position_x-self.taille_bouton[0]//2,
                                  "position_y" : position_y-self.taille_bouton[1]//2,
                                  "texte" : texte,
                                  "survol" : False, #survol est True sur on passe la sourie par dessus le bouton
                                  "clic" : False,
                                  "info_sup" : info_sup}) #clic est True si on clic sur le bouton
    
    def destruction_bouton(self, indice) :
        self.liste_bouton.pop(indice)
    
    def destruction_tout_les_boutons(self) :
        self.liste_bouton = []
    
    def test_survole(self, pos_sourie_X, pos_sourie_Y, clic) :
        for bouton in self.liste_bouton :
            bouton["survol"] = False
            if bouton["position_x"] < pos_sourie_X < bouton["position_x"]+self.taille_bouton[0] and bouton["position_y"] < pos_sourie_Y < bouton["position_y"]+self.taille_bouton[1] :
                bouton["survol"] = True
                if clic == 1 :               
                    bouton["clic"] = True
