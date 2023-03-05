

clic = None

#conv_sizex et y serv à convertir les taille en fonction de la taille de l'écran car le jeu a été créé pour une résolution de 1920*1080. 
#avec ces deux fonction, la taille des objets, image... s'adapte à la taille de l'écran qui lance le jeu
def conv_sizex(x, largeur_ecran):
    return int(largeur_ecran*x/1920)
def conv_sizey(y, hauteur_ecran):
    return int(hauteur_ecran*y/1080)


def changement_joueur(joueur_actuel) : #permet de changer de joueur (1 passe à 2 et inversement)
    if joueur_actuel == 1 :
        return 2
    else :
        return 1
    
def test_end_colonne(hauteur, colonne) : #permet de tester si une avec la hauteur en argument a atteint le sommet de la colonne en argument
    if hauteur == None :
        return False
    elif colonne <= 7 and colonne+(colonne-1) <= hauteur : #test si on atteint au prochain tour (d'où le +1 à la toute fin) le sommet d'une colonne du côté gauche du plateau (de 2 à 7 compris)
        return True
    elif colonne > 7 and (7-abs(7-colonne))+(13-colonne) <= hauteur : #test si on atteint au prochain tour le sommet d'une colonne du côté droit du plateau (de 8 à 12 compris)
        return True
    return False


def randomiseur_joueur_commence(j1, j2, ia_joue, randint) : #permet de randomiser le joueur qui commence à jouer
    rand = randint(1,2)
    if rand == 1 :
        return j1, rand, None
    else :
        if ia_joue : #si l'IA commence à jouer, on change le texte que qui joue par "Tour de l'IA"
            return j2, rand, "Tour de l'IA"
        return j2, rand, None
        
