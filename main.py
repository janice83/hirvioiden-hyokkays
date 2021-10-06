# pelin tavoite on kerätä 50 kolikkoa ja samalla varoa hirviöitä jotka hyökkäävät. Sinä olet robotti joka liikkuu ylös ja alas nuolinäppäimillä.
import pygame
import random

class Hirvio:
    def __init__(self):
        self.monster=pygame.image.load("hirvio.png")
        self.x=random.randint(800, 2000)
        self.y=random.randint(0, 480-self.monster.get_height())

class Kolikko:
    def __init__(self):
        self.raha=pygame.image.load("kolikko.png")
        self.x=random.randint(800, 2000)
        self.y=random.randint(0, 480-self.raha.get_height())

class HirvioHyokkays:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hirviöiden Hyökkäys")
        self.kello = pygame.time.Clock()
        self.naytto = pygame.display.set_mode((800, 480))
        self.robo=pygame.image.load("robo.png")
        self.monster=pygame.image.load("hirvio.png")
        self.pisteet=0
        self.x=0  #robon sijainti pelin alussa
        self.y=240 
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.ylos=False
        self.alas=False
        self.tormays=0 # mikäli 0, pelaaja ei ole vielä törmännyt hirviöön ja peli jatkuu
        self.hirviot=self.luo_hirviot()
        self.kolikot=self.luo_kolikot()
        self.silmukka()

    def silmukka(self): #pelisilmukka
        while True:
            self.katso_tapahtumat()
            self.piirra_naytto()
            self.liiku()
            pygame.display.flip()
            self.kello.tick(60)
                        
    def katso_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_n:
                    HirvioHyokkays()
                if tapahtuma.key == pygame.K_DOWN: 
                    if self.y < 480-self.robo.get_height():
                        self.alas=True
                if tapahtuma.key == pygame.K_UP: 
                    if self.y > 0:
                        self.ylos=True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas=False
                if tapahtuma.key == pygame.K_UP:
                    self.ylos=False

            if tapahtuma.type == pygame.QUIT:
                exit()

    def piirra_naytto(self): #piirretään tausta eri värilla riippuen siitä montako pistettä on kerätty
        if self.tormays == 0:
            if self.pisteet < 10:
                self.naytto.fill((0, 200, 0))
                self.piirra_hahmot(-2, -1.5)
            elif self.pisteet < 20:
                self.naytto.fill((0, 0, 255))
                self.piirra_hahmot(-2.5, -1.5)
            elif self.pisteet < 30:
                self.naytto.fill((240, 0, 255))
                self.piirra_hahmot(-2.75, -2)
            elif self.pisteet < 40:
                self.naytto.fill((255, 255, 0))
                self.piirra_hahmot(-3, -2)
            elif self.pisteet < 50:
                self.naytto.fill((255, 100, 100))
                self.piirra_hahmot(-3.5, -2.5)
            elif self.pisteet == 50:
                self.peli_ohi()
        elif self.tormays > 0: # mikäli pelaaja on törmännyt hirviöön, peli on ohi
            self.peli_ohi()

    def piirra_hahmot(self, hirvio_vauhti, kolikko_vauhti): # hirviöiden ja kolikoiden vauhti riippuu myös pistemäärästä, enemmän pisteitä = nopeampi vauhti
        self.naytto.blit(self.robo, (self.x, self.y))
        teksti=self.fontti.render(f"Pisteet: {self.pisteet}", True, (255, 0, 0))
        self.naytto.blit(teksti, (550, 20))
        
        for hirvio in self.hirviot: #piirretään hirviöt listalta ja annetaan sille vauhti
            self.naytto.blit(hirvio.monster, (hirvio.x, hirvio.y))
            hirvio.x+=hirvio_vauhti
            if self.hirvio_ulkona(hirvio) == "ulkona":
                Hirvio.__init__(hirvio) #arvotaan hirviölle uusi sijainti 
            elif self.hirvio_ulkona(hirvio) == "tormays":
                self.tormays+=1
                
        for kolikko in self.kolikot: #piirretään kolikko listalta ja annetaan sille vauhti
            self.naytto.blit(kolikko.raha, (kolikko.x, kolikko.y))
            kolikko.x+=kolikko_vauhti
            if self.kolikko_ulkona(kolikko) == True:
                Kolikko.__init__(kolikko) #arvotaan kolikolle uusi sijainti 
        
    def liiku(self):
        if self.ylos == True and self.y > 0:
            self.y-=5
        if self.alas == True and self.y+self.robo.get_height() < 480:
            self.y+=5
   
    def luo_hirviot(self): #luodaan hirviot luokkaan Hirvio, arvotaan sijainti ja tallennetaan listaan
        lista=[]
        for h in range(7):
            h=Hirvio()
            lista.append(h)
        return lista

    def luo_kolikot(self): #luodaan kolikot luokkaan Kolikko, arvotaan sijainti ja tallennetaan listaan
        lista=[]
        for k in range(7):
            k=Kolikko()
            lista.append(k)
        return lista

    def hirvio_ulkona(self, hirvio): #katsotaan onko hirviö törmännyt robottiin...
        if hirvio.x in range(self.x, self.x+self.robo.get_width()):
            hirvio_keski=hirvio.y+hirvio.monster.get_height()/2
            robo_keski=self.y+self.robo.get_height()/2
            if abs(robo_keski-hirvio_keski) <= (self.robo.get_height()+hirvio.monster.get_height())/2:
                return "tormays" 
        elif hirvio.x+self.monster.get_width() <= 0: # ...vai poistunut ruudulta ilman törmäystä
            return "ulkona" 
        
    def kolikko_ulkona(self, kolikko): #katsotaan saako pelaaja pisteen jos kolikko osuu robon kohdalle...
        if kolikko.x in range(self.x, self.x+self.robo.get_width()):
            kolikko_keski=kolikko.y+kolikko.raha.get_height()/2
            robo_keski=self.y+self.robo.get_height()/2
            if abs(robo_keski-kolikko_keski) <= (self.robo.get_height()+kolikko.raha.get_height())/2:
                self.pisteet+=1
                return True
        elif kolikko.x+kolikko.raha.get_width() <= 0: #...vai pääsikö kolikko karkuun ruudun ulkopuolelle
            return True
        return False

    def peli_ohi(self):
        font2 = pygame.font.SysFont("Arial", 50)
        uusi_peli=self.fontti.render(f"N = uusi peli", True, (255, 0, 0)) # jos pelaaja painaa N = New game, peli alkaa alusta
        if self.pisteet >= 50: # ruutunäkymä jos pelaaja kerää 50 kolikkoa ja voittaa pelin
            self.naytto.fill((0, 0, 0))
            voitto=font2.render(f"Onneksi olkoon, voitit pelin!", True, (255, 0, 0))
            self.naytto.blit(voitto, (100, 100))
            self.naytto.blit(uusi_peli, (550, 20))
            pygame.display.flip()
            
        elif self.pisteet < 50: # näkymä jos pelaaja osuu hirviöön ja häviää pelin 
            self.naytto.fill((0, 0, 0))
            tappio=font2.render(f"Game Over, Hirviöt voittivat!", True, (255, 0, 0))
            self.naytto.blit(tappio, (150, 100))
            self.naytto.blit(uusi_peli, (550, 20))
            pygame.display.flip()
            
if __name__ == "__main__":
    HirvioHyokkays()
