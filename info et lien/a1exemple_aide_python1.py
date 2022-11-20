#exemple aide en pyhon

#afficher un truc
print("hello world")
#-------------------------------------------------------------------------------#
#entrer un truc un input (demande à l'utilisateur une info)
var_input = input("entrer du text") #renvoi une chaine de caractère
#-------------------------------------------------------------------------------#
#passer de int to str
a = 1
b = "5"
print(str(a), int(b))
#-------------------------------------------------------------------------------#
#incrémenter 
i = 0
i+=1 #similaire à i++
i-=1 #similaire à i--
#-------------------------------------------------------------------------------#
#variable

a = 1
b = "test"
c = (1+1)/2
print("a : ", a, "b : ", b, "c : ", c)
#-------------------------------------------------------------------------------#
#lableau, n'existe pas vraiment


#lists
#liste vide
liste = []
#liste avec éléments (on peut y mettre nimporte quel element (int, str, class...))
list = [1, "test2", a, b, c]
#ajouter un élément (on peut ajouter nimporte quoi)
list.append(1)
#supprimer un element
list.pop() #supprime le dernier élément
list.pop(2) #supprime l'élément à l'indice 2
#-------------------------------------------------------------------------------#
#if, elif, else

if a == b :
    print(a)
elif a == c :
    print(b)
else :
    print(c)

#-------------------------------------------------------------------------------#
#boucle for
for k in range(10) : #boucle passant d'indice 0 à 9
    pass #permet de passer 
for k in range(5,10) : #boucle passant d'indice 5 à 9
    pass #permet de passer 
for k in range(5,10, 3) : #boucle passant d'indice 5 à 9 avec un pas de 3
    pass #permet de passer 

 #boucle while 
i = 10
while i>0 : 
    print(i)

#break permet aussi de sortir d'une boucle

#-------------------------------------------------------------------------------#
#définition d'une liste plus complet
liste = [k for k in range(5)] #créé une liste [0,1,2,3,4]

test_here = ["123", 1]
liste = [test_here[0] for k in range(3)] #va créé une liste ["123", "123", "123"]

#choper l'indice d'un élément connu d'une liste 
liste = [1,2,3,4,5]
print(liste.index(3)) #si l'élément dans index n'existe pas, une erreur est retourné

#slice (découpe) d'une liste
new_list = liste[1:2] #créé une nouvelle liste avec les éléments de liste de l'indice 1 à 2 compris
#ici new_list renvoi [2,3] (normalement)

#-------------------------------------------------------------------------------#
#importer une bibliotèue ou une classe d'un autre fichier (exemple avec random)
from random import randint
print(randint(1,5)) #donne un nombre aléatoire entre 1 et 5 compris

#-------------------------------------------------------------------------------#
#fonction
def nom_fonction(ag1, ag2) : #pas de definition  du type retourner. On retourne ce qu'on veux
    #do somthing
    return ag1, ag1-ag2
#appelle d'une fonction

print(nom_fonction(1,2))

#-------------------------------------------------------------------------------#
#essai/lever une exception
try :
    1/0
except :
    print("on peux pas diviser par 0")

#-------------------------------------------------------------------------------#
#avoir le max ou le min
print(max([1,2,3,4]))
list_t = [8,2,3,5,98]
print(min(list_t))

#-------------------------------------------------------------------------------#
#classe
class Nom_class :
    def __init__(self, arg1): #truc obligatoire (constructeur) qui initialise par défaut 
        self.a = 2
        self.text = "hello"
        self.arg = arg1
    
    def getA(self) : #self comme this en java mais obligatoire partout
        return self.a
    def setText(self, new_text) :
        self.text = new_text
    
cln = Nom_class(2) #création de la classe
print(cln.getA()) #similaire à cln.a
print(cln.a) #similaire à cln.getA()

cln.setText("new_text hello")
