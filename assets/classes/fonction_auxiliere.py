

clic = False

#conv_sizex et y serv à convertir les taille en fonction de la taille de l'écran car le jeu a été créé pour une résolution de 1920*1080. 
#avec ces deux fonction, la taille des objets, image... s'adapte à la taille de l'écran qui lance le jeu

def conv_sizex(x, largeur_ecran):
    return int(largeur_ecran*x/1920)
def conv_sizey(y, hauteur_ecran):
    return int(hauteur_ecran*y/1080)


def changement_joueur(joueur_actuel) :
    if joueur_actuel == 1 :
        return 2
    else :
        return 1
    
def test_end_colonne(hauteur, colonne) :
    print(f"{hauteur=} {colonne=}")
    if hauteur == None :
        return False
    elif colonne <= 7 and colonne+(colonne-1) <= hauteur : #test si on atteint au prochain tour (d'où le +1 à la toute fin) le sommet d'une colonne du côté gauche du plateau (de 2 à 7 compris)
        print("true -7 colonne")
        return True
    elif colonne > 7 and (7-abs(7-colonne))+(13-colonne) <= hauteur : #test si on attein au prochain tour le sommet d'une colonne du côté droit du plateau (de 8 à 12 compris)
        print("true+7 colonne")
        return True
    return False

            