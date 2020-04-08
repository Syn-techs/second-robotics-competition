# Author: TuNaPRo1234
# Bu oyunun amacı bir robotik yarışma simülasyonu değil, driverların yeteneklerini geliştirmek, ve üzerine yapay zeka yapmak
# Eğer oyunu geliştirmek isteyen olursa diye aralara yorum koyacağım
# Robotların ileri gitmesi için önce self.cur_speed değişkeni ayarlanıyor daha sonra bu değişkene ve self.angle'a bakarak x_change ve y_change hesaplanıyor,
# x, y ve change değerleri göz önünde bulundurularak sınırlara değip değmediği hesaplanıyor (migField ve ekranın kendisi, Robot classının update, isOnBound
# ve controlBound fonksiyonları yardımıyla) change değerleri x ve yye ekleniyor (Robot.update)

# Images klasörün içindeki fotoğrafları "freepik" diye bir siteden aldım (test için) sonra kendi tasarımlarımı ekleyeceğim
# Robotun classı Robots.py'de, robotlar da orada tanımlanıp players diye bir arrayin içine ekliyorum ve for döngüsüyle karakterler tek tek işleniyor


# import tensorflow as tf
from settings import *
from Robots import *
from Field import *
import pygame
import timeit
import random
import numpy
import math
import time
import sys
import os


def gameInit():  # Oyun başladığında bir kere çalışan fonksiyon
    global screen
    global title

    pygame.display.set_caption(title)


def runTime():  # Oyun süresince dönen fonksiyon
    global players  # Robotlar
    global colors
    global height
    global width
    global defaults

    screen.fill(defaults["backgroundColor"])

    for i in range(len(players)):
        # direkt olarak i yerine bunu verebilirdim ama işime yarayabilir diye böyle yaptım
        curPlayer = players[i]
        # Nedenini bilmiyorum ama bütün pozisyonları tupple olarak yazdım. Ve bu da bunun gibi bir sürü satırla uğraştırıyor beni
        (x, y) = curPlayer.pos
        # aslında nedeni pygamein de böyle kullanıyor olması
        for event in pygame.event.get():  # pygame event kontrol şeysi
            if event.type == pygame.QUIT:  # Çıkma tuşu şeysi
                return 0    # bu fonksiyonun döndürdüğü değer ana fonksiyonda isRunning değişkenine atanıyor
                # o değişken de while döngüsünde yazılı filan aşağı bakın
            # TUSLARLA OYNAMA
            if curPlayer.type == "player":  # Driver geliştirme olayını gerçekleştirmek istiyorsan bu kısmı pygame event kontrol şeysinin üstüne alıp sağ solları değiştir
                # tuşlar BASILINCA (Hayatımda gördüğüm en sinir bozucu özelliklerden)
                if event.type == pygame.KEYDOWN:
                    # if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and curPlayer.y_change == 0:
                    if event.key == pygame.K_LEFT:  # Sol tuş
                        curPlayer.turn(-curPlayer.max_speed)  # sola dön

                    if event.key == pygame.K_RIGHT:  # sağ tuş
                        curPlayer.turn(curPlayer.max_speed)  # sağa dön

                    # elif event.key in [pygame.K_DOWN, pygame.K_UP] and curPlayer.a_change == 0:
                    if event.key == pygame.K_UP:  # yukarı tuş
                        curPlayer.cur_speed = 1  # yönümüz ileri

                    if event.key == pygame.K_DOWN:  # aşağı tuş
                        curPlayer.cur_speed = -1  # yönümüz geri

                if event.type == pygame.KEYUP:  # tuşlara BASILMAYI BIRAKINCA
                    # sağ veya sol tuşa basılma olayı biterse
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        curPlayer.a_change = 0  # açı değişimini durdur

                    # yukarı veya aşağı tuşa basılma olayı biterse
                    elif event.key in [pygame.K_DOWN, pygame.K_UP]:
                        # change değişkenlerini ve speedi sıfırla
                        curPlayer.y_change, curPlayer.x_change, curPlayer.cur_speed = 0, 0, 0

        #################################################################################################################
        # DÜŞMAN OYUNCUNUN BEYNİİİ
        # if False:
        if curPlayer.type == "enemy":
            targetPlayer = None

            for i in range(len(players)):
                if players[i].type == "player":
                    targetPlayer = players[i]
                    break

            if targetPlayer is None:
                raise Exception("Güzel kardeşim lütfen oyuncuları geri ekle.")

            # uUUUuUUUuuuUuUUuuU
            if targetPlayer.pos != curPlayer.pos:

                # Şimdi burada çok saçma ve sinir bozucu bir olay var. İki oyuncu arasındaki açıyı kullanmak için
                # bulduğum fonksiyonları nasıl düzenlemem gerektiğini bilmiyorum çünkü matematik dehası değilim
                # ve bu fonksiyonların döndürdüğü değerler 0 ile 180 arasında oluyor (sağda da solda da). O yüzden
                # önce 1 derece sola dönüyorum, daha sonra açının değişimine göre hedefin sağda ya da solda olduğunu hesaplıyorum

                oldAng = curPlayer.findAngleVec(targetPlayer.pos)
                curPlayer.angle += 1
                newAng = curPlayer.findAngleVec(targetPlayer.pos)
                curPlayer.angle -= 1

                if oldAng < newAng and oldAng < 175:  # hedefe doğru (sola) dön
                    # eğer çok solda değilse dönerek ilerle
                    if oldAng > defaults["enemygatta"]:
                        # Enemy "Go and Turn" Tolerance Angle ;-)
                        curPlayer.turn(-1)
                        curPlayer.cur_speed = 1

                    else:  # eğer çok soldaysa ileri gitmeden dön
                        curPlayer.turn(-1)
                        curPlayer.cur_speed = 0

                # hedefe doğru (sağa) dön
                elif oldAng >= newAng and oldAng < 175:
                    # eğer çok sağda değilse dönerek ilerle
                    if oldAng > defaults["enemygatta"]:
                        curPlayer.turn(1)
                        curPlayer.cur_speed = 1

                    else:  # eğer çok sağdaysa ileri gitmeden dön
                        curPlayer.turn(1)
                        curPlayer.cur_speed = 0

                else:
                    curPlayer.turn(0)  # Ortadaysa dönmeyi durdur

        #################################################################################################################

        curPlayer.draw()

    migField.draw()

    pygame.display.update()

    return True


def configFps(configFunc, runtimeFunc):  # Ana fonksiyon
    global stabilization  # temel amacım bütün fps stabilizasyon olaylarını kendim yazmaktı
    global FPS  # yazdım da
    isRunning = True  # ama beklediğim kadar stabil olmadı ve hafif bir kayması vardı
    configFunc()  # ben de clock kullanma kararı aldım
    if stabilization:  # neyse
        while isRunning:  # eğer fps çok düşük geliyorsa settings.py dosyasından değiştirebilirsin
            # ama önermiyorum çünkü her şey arttırdığın kadar hızlanır
            clock.tick(FPS)
            isRunning = runtimeFunc()  # runtimeFunc() birkaç satır aşağıda runTime olarak giriliyor
        pygame.quit()  # runtimeFunc içinde çıkmak için return 0 yapmıştık o while döngüsünü bitiriyor sonra buraya
    else:
        while isRunning:  # Aynısı ama fpssiz
            isRunning = runtimeFunc()  # Neden stabilizasyonu kapatırsın ki
        pygame.quit()


if __name__ == "__main__":
    configFps(gameInit, runTime)
