from random import randint


from assets.classes.DesClass import Des
# from assets.classes.AlpinisteClass import Alpiniste
# from assets.classes.CampClass import Camp 
# from assets.classes.JoueurClass import Joueur 
# from assets.classes.PlateauJeuClass import PlateauJeu 



de1 = Des()
print(de1.valeur)
de1.lance_des(["im1", "im2", "im3", "im4", "im5", "im6"], randint)
print(de1.valeur)