##var/lists global
fps_menu = 20
fps = 30 #fréquence de rafraîchissement de l'écran (en image par seconde)
#on admet que joueur 1 = pions jaune et joueur 2 = pions rouge
text_joueur_actuel = None #choix aléatoire du joueur qui commence à jouer (variable utilisé pour de texte "au tour de joueur 1/2") (on initialisera cette variable au moment de lancer le jeu en joueur contre joueur)
joueur_actuel = None #variable qui va contenir la class du joueur qui est en train de jouer (initialiser au moment de lancer une partie)
couleur_joueur = {1 : (204,208,76), 2 : (244,52,76)}
vitesse_animation = 1 #vitesse des animations sachant que vitess_animation = 1 équivaut à animation normal et 0 à très rapide (1*fps = 30 = 30 images par secondes = 1 seconde)
vitesse_animation = int(fps*vitesse_animation) #variable utile surtout pour effectuer des tests plus rapidement
message_change_en_jeu = None #message = Joueur X a gagné ! quand un joueur gagne. Sinon il affiche Tour de joueur X. Ce message pourra être aussi utilisé pour afficher "Tour de l'IA"
#On admet quand l'IA joue, L'IA sera toujours le joueurs rouge et le joueur sera le jaune (le joueur qui commence est tout de même randomisé)
IA_joue = False

#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
game_loop = False #boucle du jeu
menu_loop = True #boucle du jeu
