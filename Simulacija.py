import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

#klasa za materijal koji će se raspadati
class RadioaktivniMaterijal:
    def __init__(self, pocetni_N, vrijeme, pol_raspad=None, konst_radraspad=None):
        #liste služe za crtanje grafova
        self.pocetni_N = pocetni_N
        self.preostali_N = pocetni_N
        self.preostali_lista = [pocetni_N]
        self.raspadnuti_N = 0
        self.vrijeme = vrijeme
        self.pol_raspad = pol_raspad
        self.konst_radraspad = konst_radraspad
        self.aktivnost_lista = []
        self.provjera()
        self.x_os = 0

    # provjera se vrti da se vidi je li korisnik upisao vrijeme poluraspada ili konstantu radioaktivnog raspada
    def provjera(self):
        if self.pol_raspad != None:
            self.konst_radraspad = math.log(2) / self.pol_raspad
        elif self.konst_radraspad != None:
            self.pol_raspad = math.log(2) / self.konst_radraspad
        
        
    def update(self,frame):
        self.line.set_xdata(self.x_os[:frame])
        self.line.set_ydata(self.preostali_lista[:frame])
        return (self.line)

    #funkcija koja raspada materijal
    def raspadni(self):
        for t in range(self.vrijeme):
            aktivnost = 0
            for atom in range(self.preostali_N):
                if random.random() < 1 - math.exp(-self.konst_radraspad):
                    aktivnost += 1
            self.preostali_N -= aktivnost
            self.raspadnuti_N += aktivnost
            self.preostali_lista.append(self.preostali_N)
            self.aktivnost_lista.append(aktivnost)
            self.x_os = list(range(self.vrijeme))
        fig, ax = plt.subplots()
        self.line = ax.plot(self.x_os[0], self.preostali_lista[0], label=f"Broj preostalih jezgara")[0]
        ax.set(xlim=[0, self.vrijeme], ylim=[0, self.pocetni_N], xlabel='Vrijeme [s]', ylabel='broj jezgara')
        ax.legend()
        ani = animation.FuncAnimation(fig=fig, func=self.update, frames=self.vrijeme, interval=30, repeat=False)
        #plt.show()
        ani.save("graf.gif")


        



