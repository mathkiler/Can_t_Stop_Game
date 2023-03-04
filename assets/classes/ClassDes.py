

from random import randint
from pygame.locals import *
import pygame

from assets.classes.variable_global import *
from assets.classes.fonction_auxiliere import *


class Des :

    def __init__(self, largeur_ecran, hauteur_ecran, get_chemin) :
        self.hauteur_ecran = hauteur_ecran
        self.largeur_ecran = largeur_ecran
        self.taille_des = (conv_sizex(100, largeur_ecran), conv_sizey(100, hauteur_ecran))
        self.image_des = [] #liste des images des 6 face du dés
        for face in range(1,7) :
            self.image_des.append(pygame.transform.scale(pygame.image.load(get_chemin(f"./assets/images/des/image_des{face}.png")).convert_alpha(), (self.taille_des[0], self.taille_des[1])))
        self.liste_des_lance = [] #liste qui contient les 4 dés lancé avec 2 paramètre "face" et "image" dans la fonction lancer_des
        #affichage_resultat liste qui contient les résultat des dés. Cette liste ser à afficher les bonnes images des dés
        self.affichage_resultat = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []} #les associations des dés seront compris dans l'ordre : dés 1 va avec dé 2 et dés 3 avec le 4 (on a une liste arrangé)
        #liste des associations (on a l'adition des couples de dés)
        self.colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}
        self.choix_impossible = {"choix" : {"choix1" : None, "choix2" : None, "choix3" : None},   #si un choix est None, c'est que ce choix est possible et qu'il y a un boutton associé
                                 "perdu_fin_du_tour" : False,     #"perdu_fin_du_tour" est mis en True si aucun choix n'est possible.
                                 "anim_static_image" : vitesse_animation*2}     #"anim_static_image" ets le nombre d'image (en image par secondes) qu'il reste pour que l'image avec le s3 choix impossible reste affiché pendant 2 secondes (sachant qu'on a 30 images par secondes)
                     

    def lancer_des(self) : #fonction qui lance les 4 dés
        for k in range(4) : #on lance dés
            face = randint(1,6)
            self.liste_des_lance.append({"face" : face, "image" : self.image_des[face-1]})
    
    def init_affichage(self, boutons, joueur) : #fonction qui calcule quels choix sont possible ou pas
        #répartition des dés dans les listes d'association
        liste_association = [[1,2,3,4], [1,3,2,4], [1,4,2,3]]
        for ind in liste_association[0] :
            self.affichage_resultat["possibilité_1"].append(self.liste_des_lance[ind-1]) #on applique un "-1" pour passer en mode indice (0 étant le début de la liste)
        self.colonne_association["possibilité_1"].append(self.affichage_resultat["possibilité_1"][0]["face"]+self.affichage_resultat["possibilité_1"][1]["face"])
        self.colonne_association["possibilité_1"].append(self.affichage_resultat["possibilité_1"][2]["face"]+self.affichage_resultat["possibilité_1"][3]["face"])
        for ind in liste_association[1] :
            self.affichage_resultat["possibilité_2"].append(self.liste_des_lance[ind-1])
        self.colonne_association["possibilité_2"].append(self.affichage_resultat["possibilité_2"][0]["face"]+self.affichage_resultat["possibilité_2"][1]["face"])
        self.colonne_association["possibilité_2"].append(self.affichage_resultat["possibilité_2"][2]["face"]+self.affichage_resultat["possibilité_2"][3]["face"])
        for ind in liste_association[2] :
            self.affichage_resultat["possibilité_3"].append(self.liste_des_lance[ind-1])
        self.colonne_association["possibilité_3"].append(self.affichage_resultat["possibilité_3"][0]["face"]+self.affichage_resultat["possibilité_3"][1]["face"])
        self.colonne_association["possibilité_3"].append(self.affichage_resultat["possibilité_3"][2]["face"]+self.affichage_resultat["possibilité_3"][3]["face"])
        
        
        
        #analyse et affichage des boutons
        y = 3*self.hauteur_ecran//11
        indice = 1
        for possibilite in self.colonne_association.values() :
            #choix où les deux déplacement sont possible
            cas_figure = -1 #var qui indiue le cas de figure des dés comme par exemple cas 0, la progression sur les 2 combinaison est possible
            if joueur.progression_tour["colonne"].count(None) >= 2 :
                if possibilite[0] not in joueur.colonne_fini and possibilite[1] not in joueur.colonne_fini :
                    cas_figure = 0
                elif possibilite[0] in joueur.colonne_fini :
                    cas_figure = 2
                elif possibilite[1] in joueur.colonne_fini :
                    cas_figure = 1
            elif joueur.progression_tour["colonne"].count(None) == 1 :
                if (possibilite[0] not in joueur.colonne_fini and possibilite[1] not in joueur.colonne_fini) and (possibilite[0] in joueur.progression_tour["colonne"] or possibilite[1] in joueur.progression_tour["colonne"]):
                    cas_figure = 0
                elif possibilite[0] not in joueur.progression_tour["colonne"] and possibilite[1] not in joueur.progression_tour["colonne"] :
                    if possibilite[0] in joueur.colonne_fini :
                        cas_figure = 2
                    elif possibilite[1] in joueur.colonne_fini :
                        cas_figure = 1
                    else :
                        cas_figure = 3
            elif joueur.progression_tour["colonne"].count(None) == 0 :
                if (possibilite[0] not in joueur.colonne_fini and possibilite[1] not in joueur.colonne_fini) and possibilite[0] in joueur.progression_tour["colonne"] and possibilite[1] in joueur.progression_tour["colonne"] :
                    if possibilite[0] in joueur.colonne_fini :
                        cas_figure = 2
                    if possibilite[1] in joueur.colonne_fini :
                        cas_figure = 1
                if possibilite[0] in joueur.progression_tour["colonne"] and possibilite[0] not in joueur.colonne_fini :
                    cas_figure = 1
                if possibilite[1] in joueur.progression_tour["colonne"] and possibilite[1] not in joueur.colonne_fini :
                    cas_figure = 2

            #test pour éviter de faire un double alors que le sommet n'es que à une seul case. Si ce cas se présente, on force l'affichage et le choix d'une seul possibilité (on remplace par exemple un "Progresser sur 7 et 7" par un "Progresser sur 7")
            for ind_tour in range(3) :
                if joueur.progression_tour["hauteur"][ind_tour] == None and joueur.pion_placement[possibilite[0]] != None:
                    tamp = joueur.pion_placement[possibilite[0]]+1
                elif joueur.progression_tour["hauteur"][ind_tour] != None:
                    tamp = joueur.progression_tour["hauteur"][ind_tour]
                else :
                    tamp = None
                if cas_figure == 0 and possibilite[0] == possibilite[1] and test_end_colonne(tamp, possibilite[0]) :
                    cas_figure = 1

                    
                
                
            #affichage des bouton(s) ou non en fonction du cas de figure
            if cas_figure == 0 :
                texte_bouton = f"Progresser sur {possibilite[0]} et {possibilite[1]}"
                boutons.creation_bouton(5*self.largeur_ecran//8+3*self.largeur_ecran//32, y, texte_bouton, "progression", [possibilite[0], possibilite[1]])
            elif cas_figure == 1 :
                texte_bouton = f"Progresser sur {possibilite[0]}"
                boutons.creation_bouton(5*self.largeur_ecran//8+3*self.largeur_ecran//32, y, texte_bouton, "progression", [possibilite[0], None])                
            elif cas_figure == 2 :
                texte_bouton = f"Progresser sur {possibilite[1]}"
                boutons.creation_bouton(5*self.largeur_ecran//8+3*self.largeur_ecran//32, y, texte_bouton, "progression", [possibilite[1], None])
            elif cas_figure == 3 :
                texte_bouton = f"Progresser sur {possibilite[0]}"
                boutons.creation_bouton(5*self.largeur_ecran//8+3*self.largeur_ecran//32, y, texte_bouton, "progression", [possibilite[0], None])                  
                texte_bouton = f"Progresser sur {possibilite[1]}"
                boutons.creation_bouton(5*self.largeur_ecran//8+3*self.largeur_ecran//32, y+self.hauteur_ecran//11, texte_bouton, "progression", [possibilite[1], None])
            else :
                self.choix_impossible["choix"][f"choix{indice}"] = y
            y+=3*self.hauteur_ecran//11
            indice+=1
        if self.choix_impossible["choix"]["choix1"] != None and self.choix_impossible["choix"]["choix2"] != None and self.choix_impossible["choix"]["choix3"] != None : #True si aucun choix n'est possible
            self.choix_impossible["perdu_fin_du_tour"] = True



    def reinitialisation(self) :
        self.liste_des_lance = [] #liste qui contient les 4 dés lancé avec 2 paramètre "face" et "image" dans la fonction lancer_des
        self.affichage_resultat = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []} #les associations des dés seront compris dans l'ordre : dés 1 va avec dé 2 et dés 3 avec le 4 (on a une liste arrangé)
        self.colonne_association = {"possibilité_1" : [],"possibilité_2" : [],"possibilité_3" : []}
        self.choix_impossible = {"choix" : {"choix1" : None, "choix2" : None, "choix3" : None},   #si un choix est None, c'est que ce choix est possible et qu'il y a un boutton associé
                                 "perdu_fin_du_tour" : False,     #"perdu_fin_du_tour" est mis en True si aucun choix n'est possible.
                                 "anim_static_image" : vitesse_animation*2}     #"anim_static_image" ets le nombre d'image (en image par secondes) qu'il reste pour que l'image avec le s3 choix impossible reste affiché pendant 2 secondes (sachant qu'on a 30 images par secondes)




