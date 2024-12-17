import pygame
import time
import random

from pygame.sprite import Sprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0 , 0 , 0)
TEXT_COLOR = pygame.Color(255 , 0 , 0)


# 定义一个基类
class BaseItem(Sprite) :
    def __init__(self , color , width , height) :
        pygame.sprite.Sprite.__init__(self)


class MainGame(object) :
    window = None
    my_tank = None
    # 存储敌方坦克的列表
    enemyTankList = []
    enemyTankCount = 5
    # 存储我方子弹的列表
    myBulletList = []
    # 存储敌方子弹的列表
    enemyBulletList = []
    # 存储爆炸效果的列表
    explodeList = []
    # 存储墙壁的列表
    wallList = []

    def __init__(self) :
        pass

    # 开始游戏
    def start_game(self) :
        # 加载主窗口
        # 初始化窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH , SCREEN_HEIGHT])
        # 初始化我坦克
        # MainGame.my_tank = Tank(350,250)
        self.createMyTank()
        # 初始化敌方坦克
        self.creatEnemyTank()
        # 初始化墙壁
        self.createWall()
        # 设置窗口标题
        pygame.display.set_caption("TankGame V1.0")
        while True :
            # 是坦克移动的速度慢一点
            time.sleep(0.02)
            # 给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            self.get_event()
            # 绘制文字
            MainGame.window.blit(self.get_text_surface('敌方坦克剩余数量 %d' % len(MainGame.enemyTankList)) , (10 , 10))
            # 展示我方坦克
            # 判断我方坦克是否存活
            if MainGame.my_tank and MainGame.my_tank.live :
                MainGame.my_tank.show_tank()
            else :
                del MainGame.my_tank
                MainGame.my_tank = None
            # 坦克移动
            if MainGame.my_tank and MainGame.my_tank.live :
                if not MainGame.my_tank.stop :
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall()
            # 展示敌方坦克
            self.blitEnemyTank()
            # 循环遍历显示我方坦克子弹
            self.blitMyBullet()
            # 循环遍历显示敌方坦克子弹
            self.blitEnemyBullet()
            # 循环遍历爆炸列表
            self.blitExplode()
            # 循环遍历墙壁列表
            self.blitWall()
            # 更新窗口
            pygame.display.update()

    def createWall(self) :
        # 初始化墙壁
        for i in range(6) :
            wall = Wall(i * 140 , 220)
            MainGame.wallList.append(wall)

    def createMyTank(self) :
        MainGame.my_tank = Tank(350 , 300)
        # 创建music对象
        music = Music('img/start.wav')
        music.play()

    def creatEnemyTank(self) :
        top = 100
        for i in range(MainGame.enemyTankCount) :
            left = random.randint(0 , SCREEN_WIDTH - 100)
            speed = random.randint(1 , 3)
            enemy = EnemyTank(left , top , speed)
            MainGame.enemyTankList.append(enemy)

    def blitEnemyTank(self) :
        for enemy in MainGame.enemyTankList :
            if enemy.live :
                enemy.show_tank()
                enemy.move()
                enemy.hitWall()
                # 发射子弹
                enemyBullet = enemy.shot()
                # 敌方子弹是否为 None
                if enemyBullet :
                    # 将敌方子弹存储到列表中
                    MainGame.enemyBulletList.append(enemyBullet)
            else :
                MainGame.enemyTankList.remove(enemy)

    def blitMyBullet(self) :
        for myBullet in MainGame.myBulletList :
            if myBullet.live :
                myBullet.show_bullet()
                myBullet.move_bullet()
                myBullet.myBullet_hit_enemyTank()
                myBullet.hitWall()
            else :
                MainGame.myBulletList.remove(myBullet)

    def blitEnemyBullet(self) :
        for bullet in MainGame.enemyBulletList :
            if bullet.live :
                bullet.show_bullet()
                bullet.move_bullet()
                bullet.enemyBullet_hit_myTank()
                bullet.hitWall()
            else :
                MainGame.enemyBulletList.remove(bullet)

    def blitExplode(self) :
        for explode in MainGame.explodeList :
            explode.show_explode()
            if explode.live :
                explode.show_explode()
            else :
                MainGame.explodeList.remove(explode)

    def blitWall(self) :
        for wall in MainGame.wallList :
            if wall.live :
                wall.show_wall()
            else :
                MainGame.wallList.remove(wall)

    # 结束游戏
    def end_game(self) :
        print('感谢使用，欢迎下次光临')
        exit()

    # 左上角文字的绘制
    def get_text_surface(self , text) :
        # 初始化字体模块
        pygame.font.init()
        # 查看所有字体
        # print(pygame.font.get_fonts())
        # 获取字体Font对象
        font = pygame.font.SysFont('kaiti' , 18)
        # 绘制文字信息
        text_surface = font.render(text , True , TEXT_COLOR)
        return text_surface

    # 获取事件
    def get_event(self) :
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList :
            # 判断按下的键的类型
            if event.type == pygame.QUIT :
                # 退出，关闭窗口
                self.end_game()
            if event.type == pygame.KEYDOWN :
                if MainGame.my_tank and MainGame.my_tank.live :
                    # 键盘按下
                    if event.key == pygame.K_LEFT :
                        # 坦克切换方向
                        MainGame.my_tank.direction = 'L'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下左键，坦克向左移动')
                    elif event.key == pygame.K_RIGHT :
                        # 坦克切换方向
                        MainGame.my_tank.direction = 'R'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下右键，坦克向右移动')
                    elif event.key == pygame.K_UP :
                        # 坦克切换方向
                        MainGame.my_tank.direction = 'U'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下上键，坦克向上移动')
                    elif event.key == pygame.K_DOWN :
                        # 坦克切换方向
                        MainGame.my_tank.direction = 'D'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下下键，坦克向下移动')
                    elif event.key == pygame.K_SPACE :
                        # 创建我方坦克的子弹,并限制大小
                        if len(MainGame.myBulletList) < 3 :
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                            music = Music('img/hit.wav')
                            music.play()
                            print('发射子弹')
                    elif event.key == pygame.K_ESCAPE :
                        self.end_game()
                else :
                    if event.key == pygame.K_RETURN :
                        self.createMyTank()
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN or \
                        event.key == pygame.K_LEFT or \
                        event.key == pygame.K_RIGHT :
                    if MainGame.my_tank and MainGame.my_tank.live :
                        MainGame.my_tank.stop = True


class Tank(BaseItem) :
    def __init__(self , left , top) :
        # 保存加载的图片
        self.images = {'U' : pygame.image.load('img/p1tankU.gif') ,
                       'D' : pygame.image.load('img/p1tankD.gif') ,
                       'L' : pygame.image.load('img/p1tankL.gif') ,
                       'R' : pygame.image.load('img/p1tankR.gif')}
        # 方向
        self.direction = 'U'
        # 根据当前图片的方向获取图片 surface
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = left , top
        # 速度
        self.speed = 5
        # 坦克移动开关
        self.stop = True
        # 是否活着
        self.live = True
        # 旧坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 移动
    def move(self) :
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的方向并进行移动
        if self.direction == 'U' :
            if self.rect.top < self.speed :
                self.rect.top = 0
            else :
                self.rect.top -= self.speed
        elif self.direction == 'D' :
            if self.rect.top + self.rect.height + self.speed > SCREEN_HEIGHT :
                self.rect.top = SCREEN_HEIGHT - self.rect.height
            else :
                self.rect.top += self.speed
        elif self.direction == 'L' :
            if self.rect.left - self.speed < 0 :
                self.rect.left = 0
            else :
                self.rect.left -= self.speed
        elif self.direction == 'R' :
            if self.rect.left + self.rect.width + self.speed > SCREEN_WIDTH :
                self.rect.left = SCREEN_WIDTH - self.rect.width
            else :
                self.rect.left += self.speed

    # 射击
    def shot(self) :
        return Bullet(self)

    def stay(self) :
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 检测坦克是否与墙壁发生碰撞
    def hitWall(self) :
        for wall in MainGame.wallList :
            if pygame.sprite.collide_rect(self , wall) :
                self.stay()

    # 展示坦克
    def show_tank(self) :
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image , self.rect)


# 我方坦克
class MyTank(Tank) :
    def __init__(self) :
        pass


# 敌方坦克
class EnemyTank(Tank) :
    def __init__(self , left , top , speed) :
        # 调用父类的初始化方法
        super(EnemyTank , self).__init__(left , top)
        # 保存加载的图片
        self.images = {'U' : pygame.image.load('img/enemy1U.gif') ,
                       'D' : pygame.image.load('img/enemy1D.gif') ,
                       'L' : pygame.image.load('img/enemy1L.gif') ,
                       'R' : pygame.image.load('img/enemy1R.gif')}
        # 方向
        self.direction = self.randDirection()
        # 根据当前图片的方向获取图片 surface
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = left , top
        # 速度
        self.speed = speed
        # 坦克移动开关
        self.flag = True
        # 增加一个步数变量
        self.step = 30

    # 随机生成敌方坦克方向
    def randDirection(self) :
        num = random.randint(1 , 4)
        if num == 1 :
            return 'U'
        elif num == 2 :
            return 'D'
        elif num == 3 :
            return 'L'
        elif num == 4 :
            return 'R'

    def move(self) :
        super().move()
        if self.step <= 0 :
            self.step = 30
            self.direction = self.randDirection()
        self.step -= 1

    # 重写shot
    def shot(self) :
        num = random.randint(1 , 100)
        if num < 10 :
            return Bullet(self)


# 子弹类
class Bullet(BaseItem) :
    def __init__(self , tank) :
        self.images = pygame.image.load('img/enemymissile.gif')
        # 坦克方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.images.get_rect()
        # 子弹的left 和 top 与方向有关
        if self.direction == 'U' :
            self.rect.left = tank.rect.left + tank.rect.width // 2 - self.rect.width // 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D' :
            self.rect.left = tank.rect.left + tank.rect.width // 2 - self.rect.width // 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L' :
            self.rect.left = tank.rect.left - self.rect.width // 2 - self.rect.width // 2
            self.rect.top = tank.rect.top + tank.rect.width // 2 - self.rect.width // 2
        elif self.direction == 'R' :
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width // 2 - self.rect.width // 2

        # 子弹的速度
        self.speed = 6
        # 子弹的状态,是否碰到墙壁
        self.live = True

    # 移动子弹的方法
    def move_bullet(self) :
        if self.direction == 'U' :
            if self.rect.top - self.speed < 0 :
                self.rect.top = 0
                self.live = False
            else :
                self.rect.top -= self.speed
        elif self.direction == 'D' :
            if self.rect.top + self.rect.height + self.speed > SCREEN_HEIGHT :
                self.rect.top = SCREEN_HEIGHT - self.rect.height
                self.live = False
            else :
                self.rect.top += self.speed
        elif self.direction == 'L' :
            if self.rect.left - self.speed < 0 :
                self.rect.left = 0
                self.live = False
            else :
                self.rect.left -= self.speed
        elif self.direction == 'R' :
            if self.rect.left + self.rect.width + self.speed > SCREEN_WIDTH :
                self.rect.left = SCREEN_WIDTH - self.rect.width
                self.live = False
            else :
                self.rect.left += self.speed

    # 展示子弹的方法
    def show_bullet(self) :
        # 将图片加载到窗口
        MainGame.window.blit(self.images , self.rect)

    # 子弹是否碰撞墙壁
    def hitWall(self) :
        for wall in MainGame.wallList :
            if pygame.sprite.collide_rect(self , wall) :
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0 :
                    wall.live = False

    # 我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self) :
        # 循环遍历敌方坦克列表，并进行判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList :
            if pygame.sprite.collide_rect(enemyTank , self) :
                # 修改敌方坦克状态和我方子弹状态
                enemyTank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                MainGame.explodeList.append(explode)

    # 敌方子弹与我方坦克的碰撞
    def enemyBullet_hit_myTank(self) :
        if MainGame.my_tank and MainGame.my_tank.live :
            if pygame.sprite.collide_rect(MainGame.my_tank , self) :
                # 修改敌方坦克状态和我方子弹状态
                MainGame.my_tank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(MainGame.my_tank)
                MainGame.explodeList.append(explode)


class Wall(object) :
    def __init__(self , left , top) :
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 10

    # 展示墙壁的方法
    def show_wall(self) :
        MainGame.window.blit(self.image , self.rect)


class Explode(object) :
    def __init__(self , tank) :
        # 爆炸的位置
        self.rect = tank.rect
        self.images = [
            pygame.image.load('img/blast0.gif') ,
            pygame.image.load('img/blast1.gif') ,
            pygame.image.load('img/blast2.gif') ,
            pygame.image.load('img/blast3.gif') ,
            pygame.image.load('img/blast4.gif')
        ]
        self.step = 0
        self.image = self.images[self.step]
        # 是否活着
        self.live = True

    # 展示爆炸效果的方法
    def show_explode(self) :
        if self.step < len(self.images) :
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image , self.rect)
        else :
            self.live = False
            self.step = 0


class Music(object) :
    def __init__(self , filename) :
        self.filename = filename
        pygame.mixer.init()
        pygame.mixer.music.load(self.filename)

    # 播放背景音乐的方法
    def play(self) :
        pygame.mixer.music.play()


if __name__ == '__main__' :
    MainGame().start_game()
