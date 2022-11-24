import pygame as pg
from sys import exit
import random
pg.mixer.init()

LAIUS, KÕRGUS = 800, 400
MAAPIND_KÕRGUS = 350
KIIRUS = 3

def kokkupõrked(koer, vastased):
    if vastased:
        for vastane_rect in vastased:
            if koer.colliderect(vastane_rect):
                mäng_läbi_heli.play()
                return False
    return True

def vastaste_liikumine(vastaste_nimekiri):
    if vastaste_nimekiri:
        for vastane_rect in vastaste_nimekiri:
            vastane_rect.x -= KIIRUS
            if vastane_rect.bottom == MAAPIND_KÕRGUS + 2:
                mänguekraan.blit(kass, vastane_rect)
            else:
                mänguekraan.blit(lind, vastane_rect)

        # kustutame need vaenlased, kes on ekraanilt väljas, sp vaatame, kas vastase x telg > -50

        vastaste_nimekiri = [vastane for vastane in vastaste_nimekiri if vastane.x > -50]
        return vastaste_nimekiri
    else:
        return []
    
def skoori_näitamine(x, y):
    skoor = font.render("Skoor: " + str(round(skoori_value)),True, "Black")
    mänguekraan.blit(skoor, (x, y))


pg.init()

# loome mänguekraani, lisame mänguekraani aknale pealkirja ja ikooni, kella, fondi tüübi ja suuruse

mänguekraan = pg.display.set_mode((LAIUS, KÕRGUS))
pg.display.set_caption("Pablo seiklused")
mänguekraani_ikoon = pg.image.load("pildid/black-dog.png")
pg.display.set_icon(mänguekraani_ikoon)
kell = pg.time.Clock()
font = pg.font.Font("Pixeltype.ttf", 55)
mäng_aktiivne = True

# salvestame pildid, mida kasutame tausta jaoks

maapind = pg.image.load("pildid/pind2.png")
linn = pg.image.load("pildid/lumine-taust-1.jpeg")

# salvestame teksti, mida tahame visualiseerida mängu ajal

tekst_mängu_ajal = font.render("Pablo seiklus", False, "Orange")
tekst_mängu_ajal_rect = tekst_mängu_ajal.get_rect(center=(LAIUS / 2, 50))

# ja teksti, mida visualiseerime mängu lõppedes

tekst_mäng_läbi = font.render("GAME OVER", False, "Black")
tekst_mäng_läbi_rect = tekst_mäng_läbi.get_rect(center=(LAIUS / 2, KÕRGUS / 2))

# laeme peategelase, kassi ja linnu pildid sisse, loeme need muutujatesse
# koera puhul ka määrame asukoha x- ja y-teljel, gravitatsiooni algpositsiooni ja ristküliku muutuse

koer = pg.image.load("pildid/dog_right.png")
koer_rect = koer.get_rect(midbottom=(80, MAAPIND_KÕRGUS + 5))
koer_gravitatsioon = 0
koer_rect_muutus = 0

kass = pg.image.load("pildid/cat_left.png")
lind = pg.image.load("pildid/dove-of-peace.png")

# loome vastaste jaoks järjendi, timeri ja määrame, mis aja möödudes uus vastane ilmub (?)

vastased_rect_nimekiri = []
vastased_timer = pg.USEREVENT + 1
pg.time.set_timer(vastased_timer, 1600)

koera_heli = pg.mixer.Sound("helid/dog.wav")
mäng_läbi_heli = pg.mixer.Sound("helid/GameOver.wav")

# taustaheli, kasutame mixer.music.load, sest tahame, et see mängiks lõputult

tausta_heli = pg.mixer.music.load("helid/ambience.ogg")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)

#skoor

skoori_tekst_X = 10
skoori_tekst_Y = 10
skoori_value = 0

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()  # quit on init-i vastand, lõpetame mängu
            exit()
        if mäng_aktiivne:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and koer_rect.bottom >= MAAPIND_KÕRGUS:
                    koer_gravitatsioon = -22
                elif event.key == pg.K_RIGHT:
                    koera_heli.play()
                    koera_heli.set_volume(0.4)
                    koer_rect_muutus = KIIRUS
                elif event.key == pg.K_LEFT:
                    koer_rect_muutus = -KIIRUS
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    koer_rect_muutus = 0
            if event.type == vastased_timer:

                # siin määratakse juhuslikult, kas vastaste järjendisse lisatakse kass või lind ning määrame ka
                # kassi ja linnu asukoha x- ja y-teljel (koeral määrasime ülevalpool, vastastel aga siin)

                if random.randint(0, 2):
                    vastased_rect_nimekiri.append(kass.get_rect(midbottom=(random.randint(900, 1100), MAAPIND_KÕRGUS + 2)))
                else:
                    vastased_rect_nimekiri.append(lind.get_rect(midbottom=(random.randint(900, 1100), MAAPIND_KÕRGUS - 70)))
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                mäng_aktiivne = True


    # joonistame mänguekraanile linna, maapinna, teksti pinnad
    # joonistame kõik tegelased välja
    # uuendame kõike, mida tahame mänguekraanile kuvad

    if mäng_aktiivne:
        mänguekraan.blit(linn, (0, 0))
        mänguekraan.blit(maapind, (0, MAAPIND_KÕRGUS))
        mänguekraan.blit(tekst_mängu_ajal, tekst_mängu_ajal_rect)

        # KOER
        koer_gravitatsioon += 1
        koer_rect.y += koer_gravitatsioon
        koer_rect.x += koer_rect_muutus

        # kontrollime, et koera ümbritsev ristkülik ei asuks allpool maapinna kõrgust, seame piiri

        if koer_rect.bottom >= MAAPIND_KÕRGUS + 5:
            koer_rect.bottom = MAAPIND_KÕRGUS + 5
        mänguekraan.blit(koer, koer_rect)
        # joonistame koera(pinna) täpselt sinna asukohta, kus
        # koera ümber tõmmatud ristkülik asub

        # vaenlaste liikumine

        vastased_rect_nimekiri = vastaste_liikumine(vastased_rect_nimekiri)

        # skoori lugemine
        if kokkupõrked(koer_rect, vastased_rect_nimekiri) == True:
            skoori_value += 0.01
        mäng_aktiivne = kokkupõrked(koer_rect, vastased_rect_nimekiri)
        
        skoori_näitamine(skoori_tekst_X, skoori_tekst_Y)

    else:
        mänguekraan.fill("Pink")
        mänguekraan.blit(tekst_mäng_läbi, tekst_mäng_läbi_rect)
        vastased_rect_nimekiri.clear()
        skoori_näitamine(skoori_tekst_X, skoori_tekst_Y)

    pg.display.update()
    kell.tick(60)  # max kaadrite arv sekundis