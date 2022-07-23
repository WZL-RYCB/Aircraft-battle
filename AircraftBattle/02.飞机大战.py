import time as t
import pygame as p
from pygame import *
import random as r
class HeroPlane(object):
    def __init__ (self, screen):
        # 4创建一个图片，当做飞机
        self.player = p.image.load("./images/me1.png")

        self.x = 480 / 2 - 100 / 2
        self.y = 550
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = []
    def key_control(self):
        # 监听键盘事件
        key_pressed = p.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.y -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.y += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.x -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.x += self.speed
        if key_pressed[K_SPACE]:
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.x, self.y)
            # 把子弹放到列表里
            self.bullets.append(bullet)
    def display(self):
        # 5将背景图片贴到窗口处
        self.screen.blit(self.player, (self.x, self.y))
        # 遍历所有子弹
        for bullet in self.bullets:
            #让子弹飞 修改子弹y坐标
            bullet.auto_move()

            # 子弹显示在窗口
            bullet.display()

class EnemyPlane(object):
    def __init__ (self, screen):
        # 4创建一个图片，当做飞机
        self.player = p.image.load("./images/enemy1.png")   #57 43

        self.x = 0
        self.y = 0
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = []
        #敌机移动方向
        self.direction = "right"

    def display(self):
        # 5将背景图片贴到窗口处
        self.screen.blit(self.player, (self.x, self.y))
        # 遍历所有子弹
        for bullet in self.bullets:
            #让子弹飞 修改子弹y坐标
            bullet.auto_move()
            # 子弹显示在窗口
            bullet.display()
    def auto_move(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        if self.x > 480 - 51:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"
    def auto_fire(self):
        """自动开火 创建子弹对象 添加进列表"""
        bullet = EnemyBullet(self.screen, self.x, self.y)
        random_num = r.randint(1, 10)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.x, self.y)
            self.bullets.append(bullet)


#子弹类
#属性
class Bullet(object):
    def __init__(self, screen, x, y):
        #坐标
        self.x = x + 100/2 - 2/2
        self.y = y - 11
        #图片
        self.image = p.image.load("./images/bullet2.png")
        #窗口
        self.screen = screen
        #速度
        self.speed = 10

    def display(self):
        """显示子弹到窗口"""
        self.screen.blit(self.image, (self.x, self.y))
    def auto_move(self):
        """"让子弹飞 修改子弹y坐标"""
        self.y -= self.speed

#敌方子弹类
#属性
class EnemyBullet(object):
    def __init__(self, screen, x, y):
        #坐标
        self.x = x + 58/2 - 4/2
        self.y = y + 43
        #图片
        self.image = p.image.load("./images/bullet1.png")
        #窗口
        self.screen = screen
        #速度
        self.speed = 10

    def display(self):
        """显示子弹到窗口"""
        self.screen.blit(self.image, (self.x, self.y))
    def auto_move(self):
        """"让子弹飞 修改子弹y坐标"""
        self.y += self.speed
class GameSound(object):
    def __init__(self):
        p.mixer.init()  # 音乐模块初始化
        p.mixer.music.load("./sound/game_music.ogg")
        p.mixer.music.set_volume(0.5)  #声音大小

    def playBackgroundMusic(self):
        p.mixer.music.play(-1)  #开始播放音乐
def main():
    """完成整个程序的控制"""
    sound = GameSound()
    sound.playBackgroundMusic()
    #1创建一个窗口,用来显示内容
    screen = p.display.set_mode((480,700),0,32)
    #2创建一个图片，当做背景
    background = p.image.load("./images/background.png")
    #4创建一个图片，当做飞机
    player = p.image.load("./images/me1.png")


    x = 480 / 2 - 100 / 2
    y = 550
    #飞机速度
    speed = 10
    player = HeroPlane(screen)
    enemyplane = EnemyPlane(screen)
    while True:
        # 5将背景图片贴到窗口处
        screen.blit(background, (0, 0))

        #获取事件
        for event in p.event.get():
            #判断事件类型
            if event.type == QUIT:
                #执行pygame退出
                p.quit()
                #python程序退出
                exit()
        #执行飞机的按键监听
        player.key_control()
        #飞机的显示
        player.display()
        # 敌方飞机的显示
        enemyplane.display()
        #敌机自动移动
        enemyplane.auto_move()
        # 敌机自动开火
        enemyplane.auto_fire()
        #4显示窗口中的内容
        p.display.update()
        t.sleep(0.01)

if __name__ == '__main__':
    main()