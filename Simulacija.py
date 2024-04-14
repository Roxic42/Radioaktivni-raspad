import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#importamo sve što nam treba za simulaciju

#klasa za materijal koji će se raspadati
class RadioaktivniMaterijal:
    def __init__(self, pocetni_N, vrijeme, pol_raspad=None, konst_radraspad=None):
        #liste služe za crtanje grafova
        self.pocetni_N = pocetni_N #broj atoma na početku simulacije
        self.preostali_N = pocetni_N #broja atoma koji ostane nakon simulacije
        self.preostali_lista = [pocetni_N]
        self.raspadnuti_N = 0 #broj atoma koji se raspao
        self.raspadnuti_lista = [self.raspadnuti_N]
        self.vrijeme = vrijeme #vrijeme, tj. broj koraka po kojima će se raspadat
        self.pol_raspad = pol_raspad #poluraspad atoma
        self.konst_radraspad = konst_radraspad #konstanta radioaktivnog raspada
        self.aktivnost_lista = []
        self.provjera() #provjera se vrti kada se inicira element
        self.x_os = 0 #ovo je lista koraka koja služi za x-os na grafu

    # provjera se vrti da se vidi je li korisnik upisao vrijeme poluraspada ili konstantu radioaktivnog raspada i pretvara jedno u drugo
    def provjera(self):
        if self.pol_raspad != None:
            self.konst_radraspad = math.log(2) / self.pol_raspad
        elif self.konst_radraspad != None:
            self.pol_raspad = math.log(2) / self.konst_radraspad
        
    #stavljaju se informacije na graf    
    def update(self,frame):
        #line1 je za funkciju preostalih atoma
        self.line1.set_xdata(self.x_os[:frame])
        self.line1.set_ydata(self.preostali_lista[:frame])
        #line1 je za funkciju raspadnutih atoma 
        self.line2.set_xdata(self.x_os[:frame])
        self.line2.set_ydata(self.raspadnuti_lista[:frame])
        #line1 je za funkciju aktivnosti atoma
        self.line3.set_xdata(self.x_os[:frame])
        self.line3.set_ydata(self.aktivnost_lista[:frame])
        return (self.line1, self.line2, self.line3)

    #funkcija koja raspada materijal
    def raspadni(self):
        for t in range(self.vrijeme): #za svaki korak se provjerava svaki atom
            aktivnost = 0 
            for atom in range(self.preostali_N): #za svaki atom se gleda hoće li se raspast ili ne
                if random.random() < 1 - math.exp(-self.konst_radraspad):
                    aktivnost += 1 #ako se raspao atom, aktivnost se u tom koraku povećava
            self.preostali_N -= aktivnost #za svaki korak se miče iz preostalih atoma onoliko koliko ih se raspalo (aktivnost)
            self.raspadnuti_N += aktivnost #za svaki korak se dodaje u raspadnute atome onoliko koliko ih se raspalo (aktivnost)
            #nadopune se liste za taj korak koje će kasnije poslužit za točke na grafovima (y-osi)
            self.preostali_lista.append(self.preostali_N)
            self.raspadnuti_lista.append(self.raspadnuti_N)
            self.aktivnost_lista.append(aktivnost)
            self.x_os = list(range(self.vrijeme)) #tu se zapravo kreira lista za x_os prema tome koliko koraka imamo

        #sve za crtanje grafova
        fig1, ax = plt.subplots()

        self.line1 = ax.plot(self.x_os[0], self.preostali_lista[0], label=f"Broj preostalih jezgara")[0]
        self.line2 = ax.plot(self.x_os[0], self.raspadnuti_lista[0], label=f"Broj raspadnutih jezgara")[0]
        self.line3 = ax.plot(self.x_os[0], self.aktivnost_lista[0], label=f"Aktivnost - [Bq]")[0]

        ax.set(xlim=[0, self.vrijeme], ylim=[0, self.pocetni_N], xlabel='Broj koraka', ylabel='broj jezgara')
        plt.title("Simulacija radioaktivnog raspada")
        ax.legend()
        ani = animation.FuncAnimation(fig=fig1, func=self.update, frames=self.vrijeme, interval=30, repeat=False)
        #plt.show()
        ani.save("graf.gif")


        



