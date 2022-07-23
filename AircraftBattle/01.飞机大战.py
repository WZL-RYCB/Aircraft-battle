import time as t
import pygame as p
from pygame import *
def main():
    """完成整个程序的控制"""
    #1创建一个窗口
    screen = p.display.set_mode((480,700),0,32)
    #2创建一个图片，当做背景
    background = p.image.load("./images/background.png")
    #2创建一个图片，当做背景
    player = p.image.load("./images/me1.png")

    x = 480 / 2 - 100 / 2
    y = 550
    #飞机速度
    speed = 10
    while True:
        # 3将背景图片贴到窗口处
        screen.blit(background, (0, 0))
        # 3将背景图片贴到窗口处
        screen.blit(player, (x, y))
        #获取事件
        for event in p.event.get():
            #判断事件类型
            if event.type == QUIT:
                #执行pygame退出
                p.quit()
                #python程序退出
                exit()
        #监听键盘事件
        key_pressed = p.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            print("上")
            y -= speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print("下")
            y += speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            print("左")
            x -= speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("右")
            x += speed
        if key_pressed[K_SPACE]:
            print("空格")
        #4显示窗口中的内容
        p.display.update()
        t.sleep(0.01)

if __name__ == '__main__':
    main()