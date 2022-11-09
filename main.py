import pygame as pg
from sys import exit
import random

def kokkupõrked(koer,vastased):
    if vastased:
        for vastane_rect in vastased:
            if koer.colliderect(vastane_rect):
                return False
    return True

def vastaste_liikumine(vastaste_nimekiri):
    if vastaste_nimekiri:
        for vastane_rect in vastaste_nimekiri:
            vastane_rect.x -= 5
            if vastane_rect.bottom == 352:
                ekraan.blit(kass,vastane_rect)
            else:
                ekraan.blit(lind,vastane_rect)

        # kustutame need vaenlased, kes on ekraanilt väljas
        vastaste_nimekiri = [vastane for vastane in vastaste_nimekiri if vastane.x > -50]
        return vastaste_nimekiri
    else:
        return []

pg.init()
ekraan = pg.display.set_mode((800, 400))
pg.display.set_caption("Pablo seiklused")
pablo_ikoon = pg.image.load("black-dog.png")
mäng_aktiivne = True
pg.display.set_icon(pablo_ikoon)
kell = pg.time.Clock()
font = pg.font.Font("Pixeltype.ttf", 55)

maapind = pg.image.load("pind2.png")
linn = pg.image.load("lumine-taust-1.jpeg")
tekst = font.render("Pablo seiklus", False, "Orange")
tekst_rect = tekst.get_rect(center=(400, 50))
tekst2 = font.render("GAME OVER", False, "Black")
tekst2_rect = tekst2.get_rect(center=(400,400))

# pinna asukoht on võrdne selle pinna vasaku ülemise nurga asukohaga
koer = pg.image.load("dog_right.png")
# joonistame koera pikki ümber ristküliku
# ristküliku puhul saame viitepunkti valida, midbottom, midleft, etc
koer_rect = koer.get_rect(midbottom=(80, 355))
koer_gravitatsioon = 0

kass = pg.image.load("cat_left.png")
kass_x_telg = 600
kass_rect = kass.get_rect(midbottom=(600,352))

vastased_rect_nimekiri = []
vastased_timer = pg.USEREVENT + 1
pg.time.set_timer(vastased_timer, 1000)

lind = pg.image.load("dove-of-peace.png")
while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()  # quit on init-i vastand
            exit()
        if mäng_aktiivne:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and koer_rect.bottom >= 350:
                    koer_gravitatsioon = -20
            if event.type == vastased_timer:
                if random.randint(0, 2):
                    vastased_rect_nimekiri.append(kass.get_rect(midbottom=(random.randint(900, 1100), 352)))
                else:
                    vastased_rect_nimekiri.append(lind.get_rect(midbottom=(random.randint(900, 1100), 300)))
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                mäng_aktiivne = True
    # joonistame ekraanile linna, maapinna, teksti pinnad
    # joonistame kõik tegelased välja
    # uuendame kõike

    if mäng_aktiivne:
        ekraan.blit(linn, (0, 0))
        ekraan.blit(maapind, (0, 350))
        ekraan.blit(tekst, tekst_rect)

        # KASS
        # kass_rect.x -= 3
        # if kass_rect.right <= 0:
        #     kass_rect.left = 800
        # ekraan.blit(kass, kass_rect)

        # KOER
        koer_gravitatsioon += 1
        koer_rect.y += koer_gravitatsioon
        if koer_rect.bottom >= 355:
            koer_rect.bottom = 355
        ekraan.blit(koer, koer_rect)
        # joonistame koera(pinna) täpselt sinna asukohta, kus
        # koera ümber tõmmatud ristkülik asub

        # vaenlaste liikumine
        vastased_rect_nimekiri = vastaste_liikumine(vastased_rect_nimekiri)

        # kokkupõrge
        mäng_aktiivne = kokkupõrked(koer_rect,vastased_rect_nimekiri)


    else:
        ekraan.fill("Pink")
        ekraan.blit(tekst2,tekst_rect)

    pg.display.update()
    kell.tick(60)  # max kaadrite arv sekundis
