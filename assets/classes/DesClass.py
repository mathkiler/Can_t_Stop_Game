


class Des :
    def __init__(self):
        self.valeur = 0
        self.im_des = None

    def lance_des(self, all_im_des, randint) :
        self.valeur = randint(1,6)
        self.im_des = all_im_des[self.valeur-1]
