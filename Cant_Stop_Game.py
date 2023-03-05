





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













#import des modules
#pygame est le module pour l'interface graphique. Pygame utilise un système par rafraichissement : on passe dans boucle principale, pour calculer, et afficher les objets/images. Puis on fait un "pygame.display.flip()" pour rafraichir l'écran
from random import randint
from pygame.locals import *
import pygame
import sys
import os

#import des classes
from assets.classes.ClassPlateau import Plateau
from assets.classes.ClassJoueur import Joueur
from assets.classes.ClassBoutons import Boutons
from assets.classes.ClassDes import Des
from assets.classes.ClassIA import IA

#import des fonction et variables global
from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *




#utile pour le passage en .exe (les fichiers seront dans une dossier local au .exe)
def get_chemin(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)







#initialisation pygame (interface graphique) 
pygame.init()
pygame.display.set_caption("Can't Stop Game") #changement du titre de la fenêtre

#Ouverture de la fenêtre Pygame
window = pygame.display.set_mode((0,0)) #création d'une fenêtre en plein écran
clock = pygame.time.Clock() #clock utile pour bloquer la boucle du jeu et limiter la vitesse de la boucle (même principe que sleep du module time)
largeur_ecran, hauteur_ecran = pygame.display.get_surface().get_size()
#on utilise la taille de l'écran pour adapter la tailles des images en conséquence. Grâce à cela, peut import la taille de l'écran qui run le jeu, il s'adaptera à la taille de l'écran
#à chaque fois qu'il y a des coordonnées, elle seront en fonction de la taille de l'écran. Tout les nombre comme (largeur_ecran/40) on été calculé pour un écran 1920x1080 puis reporté en fonction de la taille de l'écran actuel


#fonts (police) pour les textes
font1 = pygame.font.SysFont("comicsansms", int(largeur_ecran/40))
font_menu = pygame.font.SysFont("comicsansms", int(largeur_ecran/27))



#chargement des sprites de l'animation du chargement lorsque l'IA joue
sprite_chargement_IA = [pygame.transform.scale(pygame.image.load(get_chemin(f"./assets/images/animation_chargement_sprite/windows-xp-loading-gif_{k}.gif")).convert_alpha(), (conv_sizex(200, largeur_ecran), conv_sizey(26, hauteur_ecran))) for k in range(19)]





#initialisation du jeu
plateau = Plateau(largeur_ecran, hauteur_ecran, get_chemin) #ces trois paramètres étant utile pour l'importation et redimensionner les images
#création de 2 instances pour les 2 joueurs (quand l'IA joue, elle prend la place du joueur rouge)
joueur_jaune1 = Joueur(1, largeur_ecran, hauteur_ecran, get_chemin)
joueur_rouge2 = Joueur(2, largeur_ecran, hauteur_ecran, get_chemin)
#classe qui va gérer les boutons
boutons = Boutons(largeur_ecran, hauteur_ecran, get_chemin)
#création des boutons du menu (Jouer en J vs J (Joueur versus Joueur), Joueur en J vs IA (Joueur versus IA) et Quitter)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//6, "Jouer en J vs J", "jouer_jcj", None)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//50, "Jouer en J vs IA", "jouer_jcia", None)
boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4+hauteur_ecran//8, "Quitter", "quitter", None)
des = Des(largeur_ecran, hauteur_ecran, get_chemin)



#Boucle Main principal
while main_loop:
    while menu_loop : #boucle du menu
		#Limitation de vitesse de la boucle
        clock.tick(fps_menu) 

        keys = pygame.key.get_pressed() #on récupère tout les touches du clavier (keys[] = True si la touche est préssé)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si on ferme le jeu, on sort des 2 boucles (principal et menu) ce qui ferme le jeu
                main_loop = False
                menu_loop = False
            if event.type == MOUSEBUTTONDOWN and clic == None: #si on détecte un clic de la sourie (DOWN signifie appui)
                clic = event.button #clic gauche renvoi 1, clic droit renvoi 3 clic molette 2
            else :
                clic = None #sinon, on met clic à None pour indiqué qu'il n'y a pas de clic
        #rotation_bg_menu() permet d'effectuer la rotation de l'image du background du menu (voir la classe plateau pour plus de détail)
        image = plateau.rotation_bg_menu()
        #affichage du background et foreground du mennu
        window.blit(image, (largeur_ecran//2-image.get_width()//2,hauteur_ecran//2-image.get_height()//2))
        window.blit(plateau.menu_fg, (0, 0))

        #affichage du Titre du jeu. Sont mouvement (qui n'est pas linéaire) est effectué grâce à deplacement_text_menu() de la classe plateau
        text_surf = font_menu.render("Can't Stop Game", True, (1, 236, 164)) #(1, 236, 164) est la couleur en (R,V,B)
        #on utilise get_rect pour pouvoir center le text avce "center = "
        window.blit(text_surf, text_surf.get_rect(center = (largeur_ecran//2, hauteur_ecran//2-conv_sizey(200, hauteur_ecran)+plateau.deplacement_text_menu())))

        #affichage des boutons
        pos_sourie_X, pos_sourie_Y = pygame.mouse.get_pos() #on récupère la position en X et Y de la sourie
        boutons.test_survole(pos_sourie_X, pos_sourie_Y, clic, None, False) #fonction qui test si on survole ou clic sur bouton. D'où le clic en argument. Ici, None et False sotn des argument utile pour que l'IA clic sur les boutons (dans le menu, il n'ya a pas d'IA)
        clic = None #après avoir tester les clic sur les boutons, on remet clic à None 
        #on parcours tout les boutons dans la liste des boutons de la classe boutons
        for bouton in boutons.liste_bouton :
            if bouton["survol"] == False: #test si la sourie n'est pas par dessus le bouton pour l'afficher différemment
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
                elif bouton["type_bouton"] == "jouer_jcj" : #boutons joueur versus joueur
                    #lancement d'une nouvelle partie (on passe dans la boucle game_loop)
                    boutons.destruction_tout_les_boutons()
                    #on randomise le joueur qui commence à jouer
                    joueur_actuel, text_joueur_actuel, message_change_en_jeu = randomiseur_joueur_commence(joueur_jaune1, joueur_rouge2, IA_joue, randint)
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Lancer les dés", "lancer_des", None)
                    boutons.creation_bouton(conv_sizex(1943, largeur_ecran), 0, "", "retour_menu", None)
                    #on change de boucle
                    menu_loop = False
                    game_loop = True
                elif bouton["type_bouton"] == "jouer_jcia" : #boutons joueur versus IA
                    #lancement d'une nouvelle partie (on passe dans la boucle game_loop)
                    boutons.destruction_tout_les_boutons()
                    IA_joue = True
                    joueur_actuel, text_joueur_actuel, message_change_en_jeu = randomiseur_joueur_commence(joueur_jaune1, joueur_rouge2, IA_joue, randint)
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Lancer les dés", "lancer_des", None)
                    boutons.creation_bouton(conv_sizex(1943, largeur_ecran), 0, "", "retour_menu", None)
                    menu_loop = False
                    game_loop = True
                    #si l'IA commence à jouer (IA est le joueur rouge (2)), on lance directement sont script qui va choisir quel est le meilleur bouton à appuyer
                    if text_joueur_actuel == 2 :
                        animation_IA_en_cours = True
                        #on utilise un thread car l'IA peut mettre plusieurs secondes pour calculer sont choix. Avec un thread, on ne bloque pas l'affichage du jeu
                        IAthread = IA(boutons.liste_bouton, joueur_jaune1, joueur_rouge2)
                        IAthread.start()                    
        #Rafraîchissement de l'écran
        pygame.display.flip()



    while game_loop : #boucle du jeu
		#Limitation de vitesse de la boucle
        clock.tick(fps) 
        #évents clavier
        keys = pygame.key.get_pressed() #on récupère tout les touches du clavier (keys[] = True si la touche est pressé)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                game_loop = False
            if event.type == MOUSEBUTTONDOWN and clic == None: #si on détecte un clic de la sourie (DOWN signifie appui)
                clic = event.button #clic gauche renvoi 1, clic doit renvoi 3 clic molette 2
                
            else :
                clic = None #sinon, on met clic à None pour indiqué qu'il n'y a pas de clic
        #défilement() permet d'effectuer le défilement de l'image du background du menu (voir la classe plateau pour plus de détail)
        plateau.defilement()
        #---affichage des images/textes
        #plateau/background
        window.blit(plateau.image_bg1, (0, plateau.position_image_bg1))
        window.blit(plateau.image_bg2, (0, plateau.position_image_bg2))
        window.blit(plateau.image_plateau, (0, 0))
        #texte de qui doit jouer
        if message_change_en_jeu == None : #message_change_en_jeu est utiliser pour changer le message au dessus (utiliser pour afficher "Tour de l'IA" et "le joueur 1 gagne la partie")
            msg = f"Tour du joueur {text_joueur_actuel}"
        else :
            msg = message_change_en_jeu
        text_surf = font1.render(msg, True, couleur_joueur[text_joueur_actuel])
        window.blit(text_surf, text_surf.get_rect(center = (5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//11)))

        #affichage des boutons
        pos_sourie_X, pos_sourie_Y = pygame.mouse.get_pos() #on récupère la position en X et Y de la sourie
        boutons.test_survole(pos_sourie_X, pos_sourie_Y, clic, text_joueur_actuel, IA_joue)  #fonction qui test si on survole ou clic sur bouton. D'où le clic en argument. text_joueur_actuel, IA_joue permettent de savoir si c'est l'IA qui joue. Auquel cas, on empêche le joeuur de pouvoir clicker à la place de l'IA sur les boutons
        clic = None#après avoir tester les clic sur les boutons, on remet clic à None 
        #on parcours tout les boutons dans la liste des boutons de la classe boutons
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
                    #init_affichage() permet de calculer les choix possible et de créé les boutons adéquat
                    des.init_affichage(boutons, joueur_actuel)
                    #si l'IA commence à jouer (IA est le joueur rouge (2)), on lance directement sont script qui va choisir quel est le meilleur bouton à appuyer
                    if IA_joue and text_joueur_actuel == 2:
                        animation_IA_en_cours = True
                        # if len(boutons.liste_bouton) == 0 :
                        #     print("1111111111111111111")
                        #     while len(boutons.liste_bouton) == 0 and des.choix_impossible["perdu_fin_du_tour"] == False: #utile pour régler un bug qui démarre l'IA alors que les choix n'on pas encore été calculé. On attend donc que ces calcules soit terminé
                        #         pass
                        #on utilise un thread car l'IA peut mettre plusieurs secondes pour calculer sont choix. Avec un thread, on ne bloque pas l'affichage du jeu
                        IAthread = IA(boutons.liste_bouton, joueur_jaune1, joueur_rouge2)
                        IAthread.start()                

                elif bouton["type_bouton"] == "progression" :
                    #déplacement des tours (uniquement l'initialisation). L'animation et fin d'animation se fait plus bas dans les animations
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
                    joueur_actuel.colonne_fini_residu = [] #vide la liste des résidus (voir la classe joueur pour comprendre sont utilité)
                    #déplacement des pions (uniquement l'initialisation). L'animation et fin d'animation se fait plus bas dans les animations
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
                elif bouton["type_bouton"] == "goto_menu" : #si un joueur a gagné, on affiche un bouton pour revenir au menu (avec un "type_bouton" qui ramène ici)
                    #on réinitialise tout puis on reviens dans la boucle du menu
                    joueur_jaune1.reinitialisation()
                    joueur_rouge2.reinitialisation()
                    des.reinitialisation()
                    boutons.destruction_tout_les_boutons()
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//6, "Jouer en J vs J", "jouer_jcj", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//50, "Jouer en J vs IA", "jouer_jcia", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4+hauteur_ecran//8, "Quitter", "quitter", None)
                    message_change_en_jeu = None
                    game_loop = False
                    menu_loop = True
                    IA_joue = False
                
        #affichage du bouton retour au menu
        if boutons.bouton_retour_menu != None :
            if boutons.bouton_retour_menu["survol"] :
                window.blit(boutons.image_bouton_croix_survol, (conv_sizex(1560, largeur_ecran), 0))
            else :
                window.blit(boutons.image_bouton_croix, (conv_sizex(1843, largeur_ecran), 0))
            if boutons.bouton_retour_menu["clic"] :
                    boutons.bouton_retour_menu = None
                    #on réinitialise tout puis on reviens dans la boucle du menu
                    joueur_jaune1.reinitialisation()
                    joueur_rouge2.reinitialisation()
                    des.reinitialisation()
                    boutons.destruction_tout_les_boutons()
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//6, "Jouer en J vs J", "jouer_jcj", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4-hauteur_ecran//50, "Jouer en J vs IA", "jouer_jcia", None)
                    boutons.creation_bouton(largeur_ecran//2, 3*hauteur_ecran//4+hauteur_ecran//8, "Quitter", "quitter", None)
                    message_change_en_jeu = None
                    game_loop = False
                    menu_loop = True
                    IA_joue = False



        #affichage des dés
        if len(des.liste_des_lance) != 0 : #on test s'il y a des dés lancé. Si oui, on peut les afficher
            possibilite = 1 #il y a 3 possibilité car 3 combinaison des 4 dés. Cette variable parcours les possibilité
            couple = 0 #utile pour avoir les couples de dés. Pour chaque possibilité, les couples sont 0 avec 1 et 2 avec 3
            for y in range(2*hauteur_ecran//11, hauteur_ecran-3*hauteur_ecran//11, 3*hauteur_ecran//11) :
                for x in range(5*largeur_ecran//8, largeur_ecran-largeur_ecran//8, largeur_ecran//8) :
                    window.blit(des.affichage_resultat[f"possibilité_{possibilite}"][couple]["image"], (x-des.taille_des[0]//2, y-des.taille_des[1]//2))
                    window.blit(des.affichage_resultat[f"possibilité_{possibilite}"][couple+1]["image"], (x+des.taille_des[0]//2, y-des.taille_des[1]//2))
                    couple = 2
                possibilite+=1
                couple = 0
        
        #affichage des textes "choix impossible"
        for y in des.choix_impossible["choix"].values() : #on parcours les valeurs (qui sont des coordonnées y des position des textes "choix impossible")
            if y != None : #si le choix en question est bien impossible (None équivaut à un choix possible)
                text_surf = font1.render(f"choix impossible", True, (255,255,255))
                window.blit(text_surf, text_surf.get_rect(center = (5*largeur_ecran//8+3*largeur_ecran//32, y)))
        
        #"animation" quand le joueur n'as aucun choix possible pour laisser afficher cet écran pendant 2 secondes
        if des.choix_impossible["perdu_fin_du_tour"] : #si on a bien eu 3 choix impossible, cette variable se met à True dans la classe Des
            des.choix_impossible["anim_static_image"]-=1 #pour une vitesse normal, cette variable est par défaut à 60. ce qui fait attendre 2 seconde sachant qu'on a 30 images par secondes
            if des.choix_impossible["anim_static_image"] == 0 : #fin de l'attente
                #on enlève les colonnes atteint par les tours mais finalement pas bloqué par un pion avec le bouton stop. Cet progression est donc supprimé
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
                #on recréé le bouton lancer les dés pour le prochain joueur
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Lancer les dés", "lancer_des", None)
                #changement du joueur avec la fonction changement_joueur (qui est dans le fichier fonction_auxiliere.py)
                text_joueur_actuel = changement_joueur(text_joueur_actuel)
                if text_joueur_actuel == 1 :
                    animation_IA_en_cours = False
                    message_change_en_jeu = None
                    joueur_actuel = joueur_jaune1 #variable qui contiendra la class du joueur actuel (utile pour simplifier le code)
                else :
                    #si l'IA commence à jouer (IA est le joueur rouge (2)), on lance directement sont script qui va choisir quel est le meilleur bouton à appuyer
                    if IA_joue and text_joueur_actuel == 2:
                        animation_IA_en_cours = True
                        message_change_en_jeu = "Tour de l'IA"
                        #on utilise un thread car l'IA peut mettre plusieurs secondes pour calculer sont choix. Avec un thread, on ne bloque pas l'affichage du jeu
                        IAthread = IA(boutons.liste_bouton, joueur_jaune1, joueur_rouge2)
                        IAthread.start()
                    joueur_actuel = joueur_rouge2


        #affichage des pré_position affiche le nombre de pion qu'un joueur à amené au sommet. (affiche les pions restant à monter en pointillé) il y a 3 pions d'affiché
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
        for pion in range(2,13) : #il ne peut y avoir au maximum qu'un pion par colonne
            window.blit(joueur_jaune1.pion, (joueur_jaune1.coords_pion[f"coords_pion{pion}"][0]-joueur_jaune1.taille_tour[0]//2, joueur_jaune1.coords_pion[f"coords_pion{pion}"][1]-joueur_jaune1.taille_tour[1]//2))
            if joueur_jaune1.pion_placement[pion] == joueur_rouge2.pion_placement[pion]: #si les coordonnés des 2 pions sont les même (les pion sont au même endroit sur le plateau), on décale un peu le pion rouge pour pouvoir le voir dessous
                window.blit(joueur_rouge2.pion, (joueur_rouge2.coords_pion[f"coords_pion{pion}"][0]-joueur_rouge2.taille_tour[0]//4, joueur_rouge2.coords_pion[f"coords_pion{pion}"][1]-joueur_rouge2.taille_tour[1]//4))
            else :
                window.blit(joueur_rouge2.pion, (joueur_rouge2.coords_pion[f"coords_pion{pion}"][0]-joueur_rouge2.taille_tour[0]//2, joueur_rouge2.coords_pion[f"coords_pion{pion}"][1]-joueur_rouge2.taille_tour[1]//2))
        #affichage des tours        
        for tour in range(1,4) :
            window.blit(joueur_actuel.tour, (joueur_actuel.coords_tour[f"coords_tour{tour}"][0]-joueur_actuel.taille_tour[0]//2, joueur_actuel.coords_tour[f"coords_tour{tour}"][1]-joueur_actuel.taille_tour[1]//2))

        #affichage animation du chargement lorsque l'IA joue (cela indique que l'IA est en train de calculer)
        if animation_IA_en_cours :
            window.blit(sprite_chargement_IA[animation_IA_sprite_indice], (largeur_ecran//1.16, hauteur_ecran//12.41))
            animation_IA_sprite_indice+=1 #on se déplace de sprite en sprite (frame)
            if animation_IA_sprite_indice == 19 :
                animation_IA_sprite_indice = 0


        #animation des tours
        anim_tour_fini = False
        for anim in joueur_actuel.animation_tour : #on regarde toutes les animations
            joueur_actuel.coords_tour[f"coords_tour{anim['ind_tour']}"][0] += anim["pas_X"] #déplacement en X
            joueur_actuel.coords_tour[f"coords_tour{anim['ind_tour']}"][1] += anim["pas_Y"] #déplacement en Y
            anim["images_par_restante"]-=1 #nombre de déplacement restant -1 (à vitesse normal, on a une animation de 1 seconde donc cette variable est à 30 par default)
            if anim["images_par_restante"] == 0 : #quand l'animation est fini
                anim_tour_fini = True

        if joueur_actuel.animation_en_cours and anim_tour_fini : #on a fini toutes les animations
                joueur_actuel.animation_tour = [] #on vide la liste des animations
                #on continue le jeu en proposant lancer les dés ou Stop
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2-hauteur_ecran//12, "Lancer les dés", "lancer_des", None) #puis on affiche la suite du jeu avec les boutons lancer les dés et arrêter
                boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32,hauteur_ecran//2+hauteur_ecran//12, "Stop", "stop", None)
                joueur_actuel.animation_en_cours = False
                #si l'IA commence à jouer (IA est le joueur rouge (2)), on lance directement sont script qui va choisir quel est le meilleur bouton à appuyer
                if IA_joue and text_joueur_actuel == 2:
                    animation_IA_en_cours = True
                    #on utilise un thread car l'IA peut mettre plusieurs secondes pour calculer sont choix. Avec un thread, on ne bloque pas l'affichage du jeu
                    IAthread = IA(boutons.liste_bouton, joueur_jaune1, joueur_rouge2)
                    IAthread.start()


        #animation des pions
        anim_pion_fini = False
        for anim in joueur_actuel.animation_pion : #on regarde toutes les animations
            joueur_actuel.coords_pion[f"coords_pion{anim['colonne']}"][0] += anim["pas_X"] #déplacement en X
            joueur_actuel.coords_pion[f"coords_pion{anim['colonne']}"][1] += anim["pas_Y"] #déplacement en Y
            anim["images_par_restante"]-=1 #nombre de déplacement restant -1 (à vitesse normal, on a une animation de 1 seconde donc cette variable est à 30 par default)
            if anim["images_par_restante"] == 0 : #quand l'animation est fini
                anim_pion_fini = True

        if joueur_actuel.animation_en_cours and anim_pion_fini : #on a fini toutes les animations
                joueur_actuel.animation_pion = [] #on vide la liste des animations
                joueur_actuel.animation_en_cours = False
                #assignation de la nouvelle hauteur pour chaque pion en fonction de la hauteur des tours
                for ind_tour in range(3) : #on regarde chaque tour pour changer la valeur de hauteur des pions
                    if joueur_actuel.progression_tour["colonne"][ind_tour] != None : #si la tour a bien été placé sur le plateau
                        joueur_actuel.pion_placement[joueur_actuel.progression_tour["colonne"][ind_tour]] = joueur_actuel.progression_tour["hauteur"][ind_tour]
                #réinitialisation des positions des tours
                joueur_actuel.coords_tour = {
                    "coords_tour1" : [joueur_actuel.largeur_ecran//38.4, joueur_actuel.hauteur_ecran//21.6],
                    "coords_tour2" : [joueur_actuel.largeur_ecran//11.29, joueur_actuel.hauteur_ecran//21.6], 
                    "coords_tour3" : [joueur_actuel.largeur_ecran//38.4, joueur_actuel.hauteur_ecran//6.35]
                }
                #réinitialisation des tours
                joueur_actuel.progression_tour = {"colonne" : [None, None, None], "hauteur" : [None, None, None]}
                
                if joueur_actuel.test_si_gagnant() : #test si il y a un gagnant (il suffit de tester si le joueur à 3 pions qui on atteint le sommet)
                    if text_joueur_actuel == 2 and IA_joue : #si l'IA a gagné, on change text_joueur_actuel pour autoriser le clic sur un bouton (sinon, le jeu autorise uniquement l'IA d'appuyer sur les boutons lors de son tour)
                        text_joueur_actuel = 1
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2, "Retour au menu", "goto_menu", None)
                    message_change_en_jeu = f"Le joueur {text_joueur_actuel} gagne la partie"
                    boutons.bouton_retour_menu = None
                else : #sinon, on continue le jeu en changeant de joueur
                    boutons.creation_bouton(5*largeur_ecran//8+3*largeur_ecran//32, hauteur_ecran//2-hauteur_ecran//6, "Lancer les dés", "lancer_des", None) #puis on affiche la suite du jeu avec les boutons lancer les dés et arrêter
                    #changement de joueur
                    text_joueur_actuel = changement_joueur(text_joueur_actuel)
                    if text_joueur_actuel == 1 :
                        animation_IA_en_cours = False
                        message_change_en_jeu = None
                        joueur_actuel = joueur_jaune1 #variable qui contiendra la class du joueur actuel (utile pour simplifier le code)
                    else :
                        #si l'IA commence à jouer (IA est le joueur rouge (2)), on lance directement sont scipt qui va choisir quel est le meilleur bouton à appuyer
                        if IA_joue and text_joueur_actuel == 2:
                            animation_IA_en_cours = True
                            message_change_en_jeu = "Tour de l'IA"
                            #on utilise un thread car l'IA peut mettre plusieurs secondes pour calculer sont choix. Avec un thread, on ne bloque pas l'affichage du jeu
                            IAthread = IA(boutons.liste_bouton, joueur_jaune1, joueur_rouge2)
                            IAthread.start()
                        joueur_actuel = joueur_rouge2





        pygame.display.flip() #rafraichissement de l'écran
    
os._exit(1) #ferme le programme

