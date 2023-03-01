





###################################################################################
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                    ,ad8888ba,      ad88888ba       ,ad8888ba,                   #
#                   d8"'    `"8b    d8"     "8b     d8"'    `"8b                  #
#                  d8'              Y8,            d8'                            #
#                  88               `Y8aaaaa,      88                             #
#                  88                 `"""""8b,    88      88888                  #
#                  Y8,                      `8b    Y8,        88                  #
#                   Y8a.    .a8P    Y8a     a8P     Y8a.    .a88                  #
#                    `"Y8888Y"'      "Y88888P"       `"Y88888P"                   #
#                                                                                 #
#                        by : Mathieu, Jean, Kevin, João                          #
#                                                                                 #
#                                                                                 #
#                                                                                 #
###################################################################################



















from random import randint
from pygame.locals import *
import pygame
import sys
import os

from assets.classes.ClassPlateau import Plateau
from assets.classes.ClassJoueur import Joueur
from assets.classes.ClassBoutons import Boutons
from assets.classes.ClassDes import Des
from assets.classes.ClassIA import IA

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *




#utile pour le passage en .exe (les images seront dans une dossier local au .exe)
def resource_path0(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)







####initialisation pygame 
pygame.init()
pygame.display.set_caption("Can't Stop Game")

#Ouverture de la fenêtre Pygame
window = pygame.display.set_mode((0, 0)) #création d'une fenêtre en plein écran
clock = pygame.time.Clock()
largeur_ecran, hauteur_ecran = pygame.display.get_surface().get_size()


#fonts pour le texte
font1 = pygame.font.SysFont("comicsansms", int(largeur_ecran/40))
font_menu = pygame.font.SysFont("comicsansms", int(largeur_ecran/27))










#initialisation du jeu
plateau = Plateau(largeur_ecran, hauteur_ecran, resource_path0) #ces tois paramètres étant utilse pour l'importation et redimensionner les images
joueur_jaune1 = Joueur(1, largeur_ecran, hauteur_ecran, resource_path0)
joueur_rouge2 = Joueur(2, largeur_ecran, hauteur_ecran, resource_path0)

boutons = Boutons(largeur_ecran, hauteur_ecran, resource_path0)
#création des boutons du menu (Jouer et Quitter)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//6, "Jouer en J vs J", "jouer_jcj", None)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//50, "Jouer en J vs IA", "jouer_jcai", None)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4+hauteur_ecran//8, "Quitter", "quitter", None)
des = Des(largeur_ecran, hauteur_ecran, resource_path0)
ia = IA()



#Boucle Main principal
while main_loop:
    while menu_loop :
		#Limitation de vitesse de la boucle
        clock.tick(fps_menu) 

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                menu_loop = False
            if event.type == MOUSEBUTTONDOWN and clic == None:
                clic = event.button
            else :
                clic = None
  
        

        image = plateau.rotation_bg_menu()



        window.blit(image, (largeur_ecran//2-image.get_width()//2,hauteur_ecran//2-image.get_height()//2))
        window.blit(plateau.menu_fg, (0, 0))

        text_surf = font_menu.render("Can't Stop Game", True, (1, 236, 164))
        window.blit(text_surf, text_surf.get_rect(center = (largeur_ecran//2, hauteur_ecran//2-conv_sizey(200, hauteur_ecran)+plateau.deplacement_text_menu())))

        #affichage des boutons
        pos_sourie_X, pos_sourie_Y = pygame.mouse.get_pos()
        boutons.test_survole(pos_sourie_X, pos_sourie_Y, clic)
        clic = None
        for bouton in boutons.liste_bouton :
            if bouton["survol"] : #test si la sourie est par dessus le bouton pour l'afficher différemment
                window.blit(boutons.image_bouton_shape, (bouton["position_x"], bouton["position_y"]))
                couleur_texte = (255,255,255)
            else :
                window.blit(boutons.image_bouton_shape_survol, (bouton["position_x"], bouton["position_y"]))
                couleur_texte = (63,72,204)
            #affichage du texte du bouton
            text_surf = font1.render(bouton["texte"], True, couleur_texte)
            window.blit(text_surf, text_surf.get_rect(center = (bouton["position_x"]+boutons.taille_bouton[0]//2, bouton["position_y"]+boutons.taille_bouton[1]//2)))
            
            #test si le bouton a été pressé pour faire une action en fonction du "type" du bouton
            if bouton["clic"] :
                if bouton["type_bouton"] == "quitter" :
                    menu_loop = False
                    main_loop = False
                elif bouton["type_bouton"] == "jouer_jcj" :
                    #lancement d'une nouvelle partie (on passe dans la boucle game_loop)
                    boutons.destruction_tout_les_boutons()
                    text_joueur_actuel = randint(1,2)
                    if text_joueur_actuel == 1 :
                        joueur_actuel = joueur_jaune1 #variable qui contiendra la class du joueur actuel (utile pour simplifier le code)
                    else :
                        joueur_actuel = joueur_rouge2
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Lancer les dés", "lancer_des", None)
                    menu_loop = False
                    game_loop = True
                elif bouton["type_bouton"] == "jouer_jcia" :
                    IA_joue = True

        #Rafraîchissement de l'écran
        pygame.display.flip()



    while game_loop :


		#Limitation de vitesse de la boucle
        clock.tick(fps) 
        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                game_loop = False
            if event.type == MOUSEBUTTONDOWN and clic == None:
                clic = event.button
                
            else :
                clic = None


        #animation du background
        plateau.defilement()





        #---affichage des images/textes
        #plateau/background
        window.blit(plateau.image_bg1, (0, plateau.position_image_bg1))
        window.blit(plateau.image_bg2, (0, plateau.position_image_bg2))
        window.blit(plateau.image_plateau, (0, 0))
        #texte de qui doit jouer
        if message_fin_jeu == None :
            msg = f"Tour du joueur {text_joueur_actuel}"
        else :
            msg = message_fin_jeu
        text_surf = font1.render(msg, True, couleur_joueur[text_joueur_actuel])
        window.blit(text_surf, text_surf.get_rect(center = (5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//11)))

        #affichage des boutons
        pos_sourie_X, pos_sourie_Y = pygame.mouse.get_pos()
        boutons.test_survole(pos_sourie_X, pos_sourie_Y, clic)
        clic = None
        for bouton in boutons.liste_bouton :
            if bouton["survol"] : #test si la sourie est par dessus le bouton pour l'afficher différemment
                window.blit(boutons.image_bouton_shape, (bouton["position_x"], bouton["position_y"]))
                couleur_texte = (255,255,255)
            else :
                window.blit(boutons.image_bouton_shape_survol, (bouton["position_x"], bouton["position_y"]))
                couleur_texte = (63,72,204)
            #affichage du texte du bouton
            text_surf = font1.render(bouton["texte"], True, couleur_texte)
            window.blit(text_surf, text_surf.get_rect(center = (bouton["position_x"]+boutons.taille_bouton[0]//2, bouton["position_y"]+boutons.taille_bouton[1]//2)))
            
            #test si le bouton a été pressé pour faire une action en fonction du "type" du bouton
            if bouton["clic"] :
                if bouton["type_bouton"] == "lancer_des" :
                    boutons.destruction_tout_les_boutons()
                    des.lancer_des()
                    des.init_affichage(boutons, joueur_actuel)
                

                elif bouton["type_bouton"] == "progression" :
                    joueur_actuel.delplace_Tour(bouton["info_sup"])
                    boutons.destruction_tout_les_boutons()
                    #remise à 0 des textes des choix
                    des.choix_impossible = {"choix" : {"choix1" : None, "choix2" : None, "choix3" : None},  
                                                    "perdu_fin_du_tour" : False,     
                                                    "anim_static_image" : vitesse_animation*2}     
                    #remise à 0 des dé lancé
                    des.liste_des_lance = [] 
                    #remise à 0 des 3 association possible (on a ici que le 4 dés, exemple "possibilité_1" : [3,5,1,6])
                    des.affichage_resultat = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []} 
                    #remise à 0 des 3 association possible (ici, on les 2 possible colonnes enregistré dans les listes)
                    des.colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}
                elif bouton["type_bouton"] == "stop" :
                    joueur_actuel.colonne_fini_residu = [] #vide la liste des residus
                    joueur_actuel.deplace_Pion()
                    boutons.destruction_tout_les_boutons()
                    #remise à 0 des textes des choix
                    des.choix_impossible = {"choix" : {"choix1" : None, "choix2" : None, "choix3" : None},  
                                                    "perdu_fin_du_tour" : False,     
                                                    "anim_static_image" : vitesse_animation*2}     
                    #remise à 0 des dé lancé
                    des.liste_des_lance = [] 
                    #remise à 0 des 3 association possible (on a ici que le 4 dés, exemple "possibilité_1" : [3,5,1,6])
                    des.affichage_resultat = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []} 
                    #remise à 0 des 3 association possible (ici, on les 2 possible colonnes enregistré dans les listes)
                    des.colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}
                elif bouton["type_bouton"] == "goto_menu" :
                    joueur_jaune1.reinitialisation()
                    joueur_rouge2.reinitialisation()
                    des.reinitialisation()
                    boutons.destruction_tout_les_boutons()
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//6, "Jouer en J vs J", "jouer_jcj", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//50, "Jouer en J vs IA", "jouer_jcai", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4+hauteur_ecran//8, "Quitter", "quitter", None)
                    message_fin_jeu = None
                    game_loop = False
                    menu_loop = True



        #affichage des dés
        if len(des.liste_des_lance) != 0 : #on test s'il y a des dés lancé. Si oui, on peut les afficher
            possibilite = 1
            couple = 0
            for y in range(2*hauteur_ecran//11, hauteur_ecran-3*hauteur_ecran//11, 3*hauteur_ecran//11) :
                for x in range(5*largeur_ecran//8, largeur_ecran-largeur_ecran//8, largeur_ecran//8) :
                    window.blit(des.affichage_resultat[f"possibilité_{possibilite}"][couple]["image"], (x-des.taille_des[0]//2, y-des.taille_des[1]//2))
                    window.blit(des.affichage_resultat[f"possibilité_{possibilite}"][couple+1]["image"], (x+des.taille_des[0]//2, y-des.taille_des[1]//2))
                    couple = 2
                possibilite+=1
                couple = 0
        
        #affichage des textes "choix impossible"
        for y in des.choix_impossible["choix"].values() :
            if y != None :
                text_surf = font1.render(f"choix impossible", True, (255,255,255))
                window.blit(text_surf, text_surf.get_rect(center = (5*largeur_ecran//8+3*largeur_ecran//32, y)))
        
        #"animation" quand le joueur n'as aucun choix possible pour laisser afficher cet écran pendant 2 secondes
        if des.choix_impossible["perdu_fin_du_tour"] :
            des.choix_impossible["anim_static_image"]-=1
            if des.choix_impossible["anim_static_image"] == 0 :
                #on enlève les colonnes ateint par les tours mais finalement pas bloqué par un pion avec le bouton stop. Cet progression est donc supprimé
                for col in joueur_actuel.colonne_fini_residu :
                    joueur_actuel.colonne_fini.pop(joueur_actuel.colonne_fini.index(col))
                joueur_actuel.colonne_fini_residu = []

                #remise à 0 de la progression des tours du joueur actuel (sans aucune sauvegarde)
                joueur_actuel.progression_tour = {"colonne" : [None, None, None], "hauteur" : [None, None, None]}
                joueur_actuel.coords_tour = {
                    "coords_tour1" : [largeur_ecran//38.4, hauteur_ecran//21.6],
                    "coords_tour2" : [largeur_ecran//11.29, hauteur_ecran//21.6], 
                    "coords_tour3" : [largeur_ecran//38.4, hauteur_ecran//6.35]
                }

                #remise à 0 des textes des choix
                des.choix_impossible = {"choix" : {"choix1" : None, "choix2" : None, "choix3" : None},  
                                                "perdu_fin_du_tour" : False,     
                                                "anim_static_image" : vitesse_animation*2}     
                #remise à 0 des dé lancé
                des.liste_des_lance = [] 
                #remise à 0 des 3 association possible (on a ici que le 4 dés, exemple "possibilité_1" : [3,5,1,6])
                des.affichage_resultat = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []} 
                #remise à 0 des 3 association possible (ici, on les 2 possible colonnes enregistré dans les listes)
                des.colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}
                #changement du joueur avec la fonction changement_joueur (qui est dans le fichier fonction_auxiliere.py)
                text_joueur_actuel = changement_joueur(text_joueur_actuel)
                if text_joueur_actuel == 1 :
                    joueur_actuel = joueur_jaune1 #variable qui contiendra la class du joueur actuel (utile pour simplifier le code)
                else :
                    joueur_actuel = joueur_rouge2
                #on recréé le bouton lancer les dés pour le prochain joueur
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Lancer les dés", "lancer_des", None)


        #affichage des pré_position affiche le nombre de pion qu'un joueur à amené au sommet. (affiche les pions restant à monter en pointillet) il y a 3 pions d'affiché
        for pre_pion in range(3) :
            #affichage joueur jaune 
            if len([joueur_jaune1.colonne_fini[k] for k in range(len(joueur_jaune1.colonne_fini)) if joueur_jaune1.colonne_fini[k] not in joueur_jaune1.colonne_fini_residu]) > pre_pion :
                window.blit(joueur_jaune1.pion, (conv_sizex(75*(pre_pion+1), largeur_ecran), conv_sizey(955, hauteur_ecran)))
            else :
                window.blit(joueur_jaune1.pre_position, (conv_sizex(75*(pre_pion+1), largeur_ecran), conv_sizey(955, hauteur_ecran)))
            #affichage joueur rouge
            if len([joueur_rouge2.colonne_fini[k] for k in range(len(joueur_rouge2.colonne_fini)) if joueur_rouge2.colonne_fini[k] not in joueur_rouge2.colonne_fini_residu]) > pre_pion :
                window.blit(joueur_rouge2.pion, (conv_sizex(820, largeur_ecran)+conv_sizex(75*pre_pion, largeur_ecran), conv_sizey(955, hauteur_ecran)))
            else :
                window.blit(joueur_rouge2.pre_position, (conv_sizex(750, largeur_ecran)+conv_sizex(75*(pre_pion+1), largeur_ecran), conv_sizey(955, hauteur_ecran)))

        #affichage des pions        
        for pion in range(2,13) :
            window.blit(joueur_jaune1.pion, (joueur_jaune1.coords_pion[f"coords_pion{pion}"][0]-joueur_jaune1.taille_tour[0]//2, joueur_jaune1.coords_pion[f"coords_pion{pion}"][1]-joueur_jaune1.taille_tour[1]//2))
            if joueur_jaune1.pion_placement[pion] == joueur_rouge2.pion_placement[pion]: #si les coordonnés des 2 pions sont les même (les pion sont au même endrois sur le plateau), on décale un peu le pion rouge pour pouvoir le voir dessous
                window.blit(joueur_rouge2.pion, (joueur_rouge2.coords_pion[f"coords_pion{pion}"][0]-joueur_rouge2.taille_tour[0]//4, joueur_rouge2.coords_pion[f"coords_pion{pion}"][1]-joueur_rouge2.taille_tour[1]//4))
            else :
                window.blit(joueur_rouge2.pion, (joueur_rouge2.coords_pion[f"coords_pion{pion}"][0]-joueur_rouge2.taille_tour[0]//2, joueur_rouge2.coords_pion[f"coords_pion{pion}"][1]-joueur_rouge2.taille_tour[1]//2))
        #affichage des tours        
        for tour in range(1,4) :
            window.blit(joueur_actuel.tour, (joueur_actuel.coords_tour[f"coords_tour{tour}"][0]-joueur_actuel.taille_tour[0]//2, joueur_actuel.coords_tour[f"coords_tour{tour}"][1]-joueur_actuel.taille_tour[1]//2))

        #animation des tours
        anim_tour_fini = False
        for anim in joueur_actuel.animation_tour :
            joueur_actuel.coords_tour[f"coords_tour{anim['ind_tour']}"][0] += anim["pas_X"]
            joueur_actuel.coords_tour[f"coords_tour{anim['ind_tour']}"][1] += anim["pas_Y"]
            anim["images_par_restante"]-=1
            if anim["images_par_restante"] == 0 : #quand l'animation est fini
                anim_tour_fini = True

        if joueur_actuel.animation_en_cours and anim_tour_fini : #on a fini toutes les animations
                joueur_actuel.animation_tour = []
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2-hauteur_ecran//12, "Lancer les dés", "lancer_des", None) #puis on affiche la suite du jeu avec les boutons lancer les dés et arrêter
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32,hauteur_ecran//2+hauteur_ecran//12, "Stop", "stop", None)
                joueur_actuel.animation_en_cours = False

        #animation des pions
        anim_pion_fini = False
        for anim in joueur_actuel.animation_pion :
            joueur_actuel.coords_pion[f"coords_pion{anim['colonne']}"][0] += anim["pas_X"]
            joueur_actuel.coords_pion[f"coords_pion{anim['colonne']}"][1] += anim["pas_Y"]
            anim["images_par_restante"]-=1
            if anim["images_par_restante"] == 0 : #quand l'animation est fini
                anim_pion_fini = True

        if joueur_actuel.animation_en_cours and anim_pion_fini : #on a fini toutes les animations
                joueur_actuel.animation_pion = []
                joueur_actuel.animation_en_cours = False
                #asignation de la nouvelle hauteur pour chaque pion en fonction de la hauteur des tours
                for ind_tour in range(3) :
                    if joueur_actuel.progression_tour["colonne"][ind_tour] != None :
                        joueur_actuel.pion_placement[joueur_actuel.progression_tour["colonne"][ind_tour]] = joueur_actuel.progression_tour["hauteur"][ind_tour]
                #réinitialisation des positions des tours
                joueur_actuel.coords_tour = {
                    "coords_tour1" : [joueur_actuel.largeur_ecran//38.4, joueur_actuel.hauteur_ecran//21.6],
                    "coords_tour2" : [joueur_actuel.largeur_ecran//11.29, joueur_actuel.hauteur_ecran//21.6], 
                    "coords_tour3" : [joueur_actuel.largeur_ecran//38.4, joueur_actuel.hauteur_ecran//6.35]
                }
                #réinitialisation des tours
                joueur_actuel.progression_tour = {"colonne" : [None, None, None], "hauteur" : [None, None, None]}
                
                if joueur_actuel.test_si_gagnant() :
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Retour au menu", "goto_menu", None)
                    message_fin_jeu = f"Le joueur {text_joueur_actuel} gagne la partie"
                else :
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2-hauteur_ecran//6, "Lancer les dés", "lancer_des", None) #puis on affiche la suite du jeu avec les boutons lancer les dés et arrêter
                    #chagement de joueur
                    text_joueur_actuel = changement_joueur(text_joueur_actuel)
                    if text_joueur_actuel == 1 :
                        joueur_actuel = joueur_jaune1 #variable qui contiendra la class du joueur actuel (utile pour simplifier le code)
                    else :
                        joueur_actuel = joueur_rouge2





        pygame.display.flip() #rafraichissement de l'écran
    
os._exit(1) #ferme le programme

