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


def skoori_näitamine(x_telg, y_telg):
    skoor = font.render("Skoor: " + str(round(skoori_value)), True, "Black")
    mänguekraan.blit(skoor, (x_telg, y_telg))


ring = u"\u2022"
tekst = f"{ring} Alustamiseks vajuta tühikut \n{ring} Liigu paremale parema nooleklahviga \n\
{ring} Liigu vasakule vasaku nooleklahviga \n{ring} Hüppamiseks kasuta tühikut \n{ring} Väljumiseks vajuta ESC klahvi"
teksti_pos = 60, 100


def mängu_avaleht():
    if avaleht:
        mänguekraan.fill("Pink")

        kogu_tekst = [sõna.split(' ') for sõna in tekst.splitlines()]
        vahe = font.size(' ')[0]
        x, y = teksti_pos
        for read in kogu_tekst:
            for sõnad in read:
                sõna_pind = font.render(sõnad, True, "Black")
                sõna_laius, sõna_kõrgus = sõna_pind.get_size()
                if x + sõna_laius >= LAIUS:
                    x = teksti_pos[0]
                    y += sõna_kõrgus
                mänguekraan.blit(sõna_pind, (x, y))
                x += sõna_laius + vahe
            x = teksti_pos[0]
            y += sõna_kõrgus

        # alguse_tekst = font.render("Alustamiseks vajuta tühikut", True, "Black")
        # alguse_tekst_rect = alguse_tekst.get_rect(center=(LAIUS / 2, 50))
        # mänguekraan.blit(alguse_tekst, alguse_tekst_rect)
        pg.display.update()


def mängu_kiirus():
    if skoori_value <= 20:
        kell.tick(60)
    if skoori_value > 20 and skoori_value <= 40:
        kell.tick(70)
    if skoori_value > 40 and skoori_value <= 60:
        kell.tick(80)
    if skoori_value > 60 and skoori_value <= 80:
        kell.tick(90)
    if skoori_value > 80 and skoori_value <= 100:
        kell.tick(100)
    if skoori_value > 100 and skoori_value <= 120:
        kell.tick(110)
    if skoori_value > 120 and skoori_value <= 140:
        kell.tick(120)
    if skoori_value > 140 and skoori_value <= 160:
        kell.tick(130)
    if skoori_value > 160:
        kell.tick(140)


pg.init()

# loome mänguekraani, lisame mänguekraani aknale pealkirja ja ikooni, kella, fondi tüübi ja suuruse

mänguekraan = pg.display.set_mode((LAIUS, KÕRGUS))
mänguekraan_rect = mänguekraan.get_rect()
pg.display.set_caption("Pablo seiklus")
mänguekraani_ikoon = pg.image.load("pildid/black-dog.png")
pg.display.set_icon(mänguekraani_ikoon)
kell = pg.time.Clock()
font = pg.font.Font("ZenDots-Regular.ttf", 30)

# salvestame pildid, mida kasutame tausta jaoks

maapind = pg.image.load("pildid/pind2.png")
linn = pg.image.load("pildid/lumine-taust-1.jpeg")

# salvestame teksti, mida visualiseerime mängu lõppedes

tekst_mäng_läbi = font.render("MÄNG LÄBI - kaotasid", False, "Black")
tekst_mäng_läbi_rect = tekst_mäng_läbi.get_rect(center=(LAIUS / 2, KÕRGUS / 2))

# laeme peategelase, kassi ja linnu pildid sisse, loeme need muutujatesse
# koera puhul ka määrame asukoha x- ja y-teljel, gravitatsiooni algpositsiooni ja ristküliku muutuse

koer = pg.image.load("pildid/dog_right.png")
koer_rect = koer.get_rect(midbottom=(80, MAAPIND_KÕRGUS + 5))
koer_gravitatsioon = 0
koer_rect_muutus = 0

kass = pg.image.load("pildid/cat_left.png")
lind = pg.image.load("pildid/dove-of-peace.png")

# loome vastaste jaoks järjendi, timeri ja määrame, mis aja möödudes uus vastane ilmub

vastased_rect_nimekiri = []
vastased_timer = pg.USEREVENT + 1
pg.time.set_timer(vastased_timer, 1600)

koera_heli = pg.mixer.Sound("helid/dog.wav")
mäng_läbi_heli = pg.mixer.Sound("helid/GameOver.wav")

# taustaheli, kasutame mixer.music.load, sest tahame, et see mängiks lõputult

tausta_heli = pg.mixer.music.load("helid/ambience.ogg")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)

# skoori muutujad

skoori_tekst_X = 10
skoori_tekst_Y = 10
skoori_value = 0

# ekraani liikumise muutuja

ekraan = 0

# mäng algab avalehe kuvamisega

avaleht = True
mäng_aktiivne = False

mängu_avaleht()

while avaleht:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            avaleht = False
            mäng_aktiivne = True

while True:
    # nupuvajutused
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
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
                    vastased_rect_nimekiri.append(
                        kass.get_rect(midbottom=(random.randint(900, 1100), MAAPIND_KÕRGUS + 2)))
                else:
                    vastased_rect_nimekiri.append(
                        lind.get_rect(midbottom=(random.randint(900, 1100), MAAPIND_KÕRGUS - 70)))
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                mäng_aktiivne = True
                skoori_value = 0

    # joonistame mänguekraanile linna, maapinna, teksti pinnad
    # joonistame kõik tegelased välja
    # uuendame kõike, mida tahame mänguekraanile kuvad

    if mäng_aktiivne:
        mänguekraan.blit(linn, (ekraan, 0))
        mänguekraan.blit(linn, (LAIUS + ekraan, 0))
        if (ekraan == -LAIUS):
            mänguekraan.blit(linn, (LAIUS + ekraan, 0))
            ekraan = 0
        ekraan -= 1
        mänguekraan.blit(maapind, (ekraan, MAAPIND_KÕRGUS))
        mänguekraan.blit(maapind, (LAIUS + ekraan, MAAPIND_KÕRGUS))
        if (ekraan == -LAIUS):
            mänguekraan.blit(maapind, (LAIUS + ekraan, MAAPIND_KÕRGUS))
            ekraan = 0
        ekraan -= 1

        # KOER
        koer_gravitatsioon += 1
        koer_rect.y += koer_gravitatsioon
        koer_rect.x += koer_rect_muutus

        # kontrollime, et koera ümbritsev ristkülik ei asuks allpool maapinna kõrgust, seame piiri

        if koer_rect.bottom >= MAAPIND_KÕRGUS + 5:
            koer_rect.bottom = MAAPIND_KÕRGUS + 5
        koer_rect.clamp_ip(mänguekraan_rect)
        mänguekraan.blit(koer, koer_rect)

        # joonistame koera(pinna) täpselt sinna asukohta, kus
        # koera ümber tõmmatud ristkülik asub

        # vaenlaste liikumine

        vastased_rect_nimekiri = vastaste_liikumine(vastased_rect_nimekiri)

        # kokkupõrge

        mäng_aktiivne = kokkupõrked(koer_rect, vastased_rect_nimekiri)

        # skoori lugemine
        if kokkupõrked(koer_rect, vastased_rect_nimekiri) == True:
            skoori_value += 0.01

        skoori_näitamine(skoori_tekst_X, skoori_tekst_Y)

        mängu_kiirus()

    # lõpuekraan
    else:
        mänguekraan.fill("Pink")
        mänguekraan.blit(tekst_mäng_läbi, tekst_mäng_läbi_rect)
        vastased_rect_nimekiri.clear()
        skoori_näitamine(skoori_tekst_X, skoori_tekst_Y)
        koer_rect = koer.get_rect(midbottom=(80, MAAPIND_KÕRGUS + 5))

    pg.display.update()

pg.quit()
