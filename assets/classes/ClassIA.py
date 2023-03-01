from pygame.locals import *
import pygame

from assets.classes.ClassDes import Des

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *


class IA :
    
    def __init__(self, largeur_ecran, hauteur_ecran, resource_path0) :
        self.nombre_iterration = 10
        self.des = Des(largeur_ecran, hauteur_ecran, resource_path0)


    def calcule_meilleur_choix(self, choix) : #on reçoit par choix les boutons sur lesquelles on peut clicker
        if len(choix) == 1 : #ici, on n'as qu'un bouton/choix possible. On choisi donc ce bouton
            choix[0]["clic"] = True
        else :


            for choi in choix :
                for iterration in range(self.nombre_iterration) :
                    pass



