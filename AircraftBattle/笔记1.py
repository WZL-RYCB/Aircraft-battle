import time as t
import pygame as p
from pygame import *
import random as r


class HeroPlane(p.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        p.sprite.Sprite.__init__(self)

        # 4创建一个图片，当做飞机
        self.player = p.image.load("./images/me1.png")
        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()  # rect矩形
        self.rect.topleft = [480 / 2 - 100 / 2, 600]
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = p.sprite.Group()

    def key_control(self):
        # 监听键盘事件
        key_pressed = p.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)
            # 把子弹放到列表里
            self.bullets.add(bullet)

    def update(self):
        self.key_control()
        self.display()

    def display(self):
        # 5将背景图片贴到窗口处
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)


class EnemyPlane(p.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        p.sprite.Sprite.__init__(self)
        # 4创建一个图片，当做飞机
        self.player = p.image.load("./images/enemy1.png")
        # 根据图片image获取矩形对象
        self.rect = self.image.get_rect()  # rect矩形
        self.rect.topleft = [0, 0]
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = p.sprite.Group()
        # 敌机移动方向
        self.direction = "right"

    def display(self):
        # 5将背景图片贴到窗口处
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def auto_move(self):
        if self.direction == "right":
            self.rect.right += self.speed
        elif self.direction == "left":
            self.rect.right -= self.speed
        if self.rect.right > 480 - 51:
            self.direction = "left"
        elif self.rect.right < 0:
            self.direction = "right"

    def auto_fire(self):
        """自动开火 创建子弹对象 添加进列表"""
        random_num = r.randint(1, 10)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)

#子弹类
#属性
class Bullet(p.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 精灵类初始化
        p.sprite.Sprite.__init__(self)

        # 创建图片
        self.image  = p.image.load("./images/bullet2.png")

        # 获取矩形对象
        self.rect= self.image.get_rect()
        self.rect.topleft = [x + 100/2 - 2/2, y - 11]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

#敌方子弹类
#属性
class EnemyBullet(p.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 精灵类初始化
        p.sprite.Sprite.__init__(self)
        # 创建图片
        self.image = p.image.load("./images/bullet1.png")
        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 58/2 - 4/2, y + 43]
        #窗口
        self.screen = screen
        #速度
        self.speed = 10
    def update(self):
        #  修改子弹坐标
        self.rect.top += self.speed
        #  如果子弹移出屏幕上方 则销毁子弹对象
        if self.rect.top > 852:
            self.kill()


class GameSound(object):
    def __init__(self):
        p.mixer.init()  # 音乐模块初始化
        p.mixer.music.load("./sound/game_music.ogg")
        p.mixer.music.set_volume(0.5)  # 声音大小

    def playBackgroundMusic(self):
        p.mixer.music.play(-1)  # 开始播放音乐

def main():
    """完成整个程序的控制"""
    sound = GameSound()
    sound.playBackgroundMusic()
    # 1创建一个窗口,用来显示内容
    screen = p.display.set_mode((480, 700), 0, 32)
    # 2创建一个图片，当做背景
    background = p.image.load("./images/background.png")

    player = HeroPlane(screen)
    enemyplane = EnemyPlane(screen)
    while True:
        # 5将背景图片贴到窗口处
        screen.blit(background, (0, 0))
        # 获取事件
        for event in p.event.get():
            # 判断事件类型
            if event.type == QUIT:
                # 执行pygame退出
                p.quit()
                # python程序退出
                exit()
        # 执行飞机的按键监听
        player.key_control()
        # 飞机的显示
        player.display()
        # 敌方飞机的显示
        enemyplane.display()
        # 敌机自动移动
        enemyplane.auto_move()
        # 敌机自动开火
        enemyplane.auto_fire()
        # 4显示窗口中的内容
        p.display.update()
        t.sleep(0.01)


if __name__ == '__main__':
    main()