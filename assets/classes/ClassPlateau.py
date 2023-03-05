from pygame.locals import *
import pygame


class Plateau :

    def __init__(self, largeur_ecran, hauteur_ecran, get_chemin) :
        self.hauteur_ecran = hauteur_ecran
        self.largeur_ecran = largeur_ecran
        #on importe 2 background pour faire défiler le fond
        self.image_bg1 = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/back_ground/background_en _jeu/background.png")).convert(), (largeur_ecran, hauteur_ecran))
        self.image_bg2 = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/back_ground/background_en _jeu/background.png")).convert(), (largeur_ecran, hauteur_ecran))
        #le .convert_alpha est utile pour les image avec des parties transparent
        self.image_plateau = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/back_ground/background_en _jeu/plateau.png")).convert_alpha(), (largeur_ecran, hauteur_ecran))
        #importation es images pour le background du menu
        self.menu_bg = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/back_ground/back_ground_menu/bg_menu_bg_etoile.png")).convert(), (largeur_ecran, largeur_ecran))
        self.menu_fg = pygame.transform.scale(pygame.image.load(get_chemin("./assets/images/back_ground/back_ground_menu/fg_menu_forme.png")).convert_alpha(), (largeur_ecran, hauteur_ecran))

        #paramètre pour le jeu (position des 2 background en y)
        self.position_image_bg1 = 0
        self.position_image_bg2 = hauteur_ecran

        #paramètre pour les animation du menu
             #rotation du background
        self.menu_angle = 0
        self.menu_angle_pas = 0.2
            #mouvement du texte non linéaire
        self.menu_text_coords = -20
        self.menu_text_step = 1
        self.menu_text_sens = 1
        self.menu_text_step_sens = 1

        

    def defilement(self) :
        #défilement bg 1
        if self.position_image_bg1 > self.hauteur_ecran :
            self.position_image_bg1 = -self.hauteur_ecran+2
        else :
            self.position_image_bg1+=1
        #défilement bg 2
        if self.position_image_bg2 > self.hauteur_ecran :
            self.position_image_bg2 = -self.hauteur_ecran+2
        else :
            self.position_image_bg2+=1
        

    def rotation_bg_menu(self) : #rotation du bg du menu en augmentant son angle e rotation
        self.menu_angle+=self.menu_angle_pas
        return pygame.transform.rotate(self.menu_bg, self.menu_angle)



    def deplacement_text_menu(self) : #calcule de nouvelles coordonnées menu_text_coords. Cette variable à une allure similaire à une gaussienne
        if self.menu_text_coords < -20 :
            self.menu_text_sens = 1
            self.menu_text_step_sens = 1
            self.menu_text_step = 1
        elif self.menu_text_coords > 20 :
            self.menu_text_sens = -1
            self.menu_text_step_sens = 1
            self.menu_text_step = 1
      
        if self.menu_text_coords < 0 < self.menu_text_coords+self.menu_text_step*self.menu_text_sens :
            tamp = True
        else :
            tamp = False
        self.menu_text_coords+=self.menu_text_step*self.menu_text_sens
        self.menu_text_step+=1*self.menu_text_step_sens
        if tamp :
            self.menu_text_step_sens = -1
        return self.menu_text_coords



