import time
import time as t
import pygame
import random as r
from pygame.constants import *


class HeroPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)

        # 4创建一个图片，当做飞机
        self.player = pygame.image.load("./images/me1.png")
        # 根据图片image获取矩形对象
        self.rect = self.player.get_rect()  # rect矩形
        self.rect.topleft = [Manager.bg_size[0] / 2 - 100 / 2, 550]
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = pygame.sprite.Group()

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            t.sleep(10)
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.rect.left, self.rect.top, 1)
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


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)
        # 4创建一个图片，当做飞机
        self.player = pygame.image.load("./images/enemy1.png")
        # 根据图片image获取矩形对象
        self.rect = self.player.get_rect()  # rect矩形
        self.rect.topleft = [0, 0]
        # 飞机速度
        self.speed = 10
        self.screen = screen
        # 装子弹的列表
        self.bullets = pygame.sprite.Group()
        # 敌机移动方向
        self.direction = "right"

    def display(self):
        # 5将背景图片贴到窗口处
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()
        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

    def auto_move(self):
        if self.direction == "right":
            self.rect.right += self.speed
        elif self.direction == "left":
            self.rect.right -= self.speed
        if self.rect.right > Manager.bg_size[0] - 51:
            self.direction = "left"
        elif self.rect.right < 0:
            self.direction = "right"

    def auto_fire(self):
        """自动开火 创建子弹对象 添加进列表"""
        random_num = r.randint(1, 10)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)


# 子弹类
# 属性
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, speed):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)

        # 创建图片
        self.image = pygame.image.load("./images/bullet2.png")

        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 100 / 2 - 2 / 2, y - 11]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = speed

    def update(self):
        #  修改子弹坐标
        self.rect.top -= self.speed
        #  如果子弹移出屏幕上方 则销毁子弹对象
        if self.rect.top < -22:
            self.kill()


# 敌方子弹类
# 属性

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # 精灵类初始化
        pygame.sprite.Sprite.__init__(self)
        # 创建图片
        self.image = pygame.image.load("./images/bullet1.png")
        # 获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 58 / 2 - 4 / 2, y + 43]
        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

    def update(self):
        #  修改子弹坐标
        self.rect.top += self.speed
        #  如果子弹移出屏幕上方 则销毁子弹对象
        if self.rect.top > Manager.bg_size[1]:
            self.kill()


class GameSound(object):
    def __init__(self):
        pygame.mixer.init()  # 音乐模块初始化
        pygame.mixer.music.load("./sound/game_music.ogg")
        pygame.mixer.music.set_volume(0.5)  # 声音大小

        self.__bomb = pygame.mixer.Sound("./sound/get_bomb.wav")

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐
    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)


class Bomb(object):
    # 初始化碰撞
    def __init__(self, screen, type):
        self.screen = screen
        if type == "enemy":
           # 加载爆炸资源
           self.mImages = [
               pygame.image.load("./images/enemy1_down" + str(v) + ".png") for v in range(1, 5)]
        else:
            self.mImages = [
                pygame.image.load("./images/me_destroy_" + str(v) + ".png") for v in range(1, 5)]
        # 设置当前爆炸播放索引
        self.mIndex = 0
        # 保障设置
        self.mPos = [0, 0]
        # 是否可见
        self.mVisible = False

    def action(self, rect):
        # 触发爆炸方法draw
        # 爆炸坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 打开爆炸的开关
        self.mVisible = True



    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImages[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImages):
            # 如果下标已经到最后 代表爆炸结束
            # 下标重置 mVisible重置
            self.mIndex = 0
            self.mVisible = False

# 地图


class GameBackground(object):
    # 初始化地图
    def __init__(self, screen):
        self.mImage1 = pygame.image.load("./images/background.png")
        self.mImage2 = pygame.image.load("./images/background.png")
        # 窗口
        self.screen = screen
        # 辅助移动地图
        self.y1 = 0
        self.y2 = -Manager.bg_size[1]    # -700

     # 移动地图
    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 >= Manager.bg_size[1]:
            self.y1 = 0
        if self.y2 >= 0:
            self.y2 = -Manager.bg_size[1]

    # 绘制地图

    def draw(self):
        self.screen.blit(self.mImage1, (0, self.y1))
        self.screen.blit(self.mImage2, (0, self.y2))


class Manager(object):
    bg_size = (480, 700)

    def __init__(self):
        pygame.init()
        # 创建一个窗口
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 32)
        # 创建背景图片
        #self.background = pygame.image.load("./images/background.png")
        self.map = GameBackground(self.screen)
        # 初始化一个装玩家精灵的group
        self.players = pygame.sprite.Group()
        # 初始化一个装敌机精灵的group
        self.enemys = pygame.sprite.Group()
        # 初始化一个玩家爆炸的对象
        self.player_bomb = Bomb(self.screen, "player")
        # 初始化一个敌机爆炸的对象
        self.enemy_bomb = Bomb(self.screen, "enemy")
        # 初始化一个声音播放的对象
        self.sound = GameSound()

    def exit(self):
        print("退出")
        pygame.quit()
        exit()

    def new_player(self):
        # 创建飞机对象 添加到玩家的组
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        # 创建敌机对象 添加到敌机的组
        enemy = EnemyPlane(self.screen)
        self.enemys.add(enemy)
    # 绘制文字

    def drawText(self, text, x, y, textHeight=30, fontColor=(255, 0, 0), backgroundColor=None):
        # 通过字体文件获取字体对象
        font_obj = pygame.font.Font("./images/FZHuaSTHJW.TTF", textHeight)
        # 配置要显示的文字
        text_obj = font_obj.render(text, True, fontColor, backgroundColor)
        # 获取要显示的对象rect
        text_rect = text_obj.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = (x, y)
        # 绘制字到指定区域
        self.screen.blit(text_obj, text_rect)


    def main(self):
        # 播放背景音乐
        self.sound.playBackgroundMusic()
        # 创建一个玩家
        self.new_player()
        # 创建一个敌机
        self.new_enemy()
        while True:
            # 把背景图片贴到窗口
            #self.screen.blit(self.background, (0, 0))
            # 移动地图
            self.map.move()
            # 把地图贴到窗口上
            self.map.draw()
            # 绘制文字
            self.drawText("hp: 10000", 0, 0)
            # 遍历所有事件
            for event in pygame.event.get():
                # 判断事件类型如果python是退出
                if event.type == QUIT:
                    exit()
            # 调用爆炸的对象
            self.player_bomb.draw()
            self.enemy_bomb.draw()
            # 判断碰撞
            iscollide = pygame.sprite.groupcollide(self.players, self.enemys, True, True)
            if iscollide:
                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0]
                # 玩家爆炸图片
                self.player_bomb.action(x.rect)
                # 敌机爆炸图片
                self.enemy_bomb.action(y.rect)\
                # 爆炸的声音
                self.sound.playBombSound()
            # 玩家飞机和子弹的显示
            self.players.update()
            # 敌机和子弹的显示
            self.enemys.update()
            # 刷新窗口内容
            pygame.display.update()
            t.sleep(0.01)
if __name__ == "__main__":
    manager = Manager()
    manager.main()

