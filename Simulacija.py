import random
import math
import matplotlib.pyplot as plt

#klasa za materijal koji će se raspadati
class RadioaktivniMaterijal:
    def __init__(self, pocetni_N, vrijeme, pol_raspad=None, konst_radraspad=None):
        #liste služe za crtanje grafova
        self.pocenti_N = pocetni_N
        self.preostali_N = pocetni_N
        self.preostali_lista = [pocetni_N]
        self.raspadnuti_N = 0
        self.vrijeme = vrijeme
        self.pol_raspad = pol_raspad
        self.konst_radraspad = konst_radraspad
        self.aktivnost_lista = []
        self.provjera()

    # provjera se vrti da se vidi je li korisnik upisao vrijeme poluraspada ili konstantu radioaktivnog raspada
    def provjera(self):
        if self.pol_raspad is not None:
            self.konst_radraspad = math.log(2) / self.pol_raspad
        elif self.konst_radraspad is not None:
            self.pol_raspad = math.log(2) / self.konst_radraspad

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
        x_os = list(range(len(self.preostali_lista)))
        plt.grid(True)
        plt.plot(x_os, self.preostali_lista)
        plt.xlim(0, None)
        plt.ylim(0, None) 
        plt.tight_layout()
        plt.show()

Mipi = RadioaktivniMaterijal(1600, 100, pol_raspad=20)
Mipi.raspadni()

        



