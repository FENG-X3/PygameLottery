# coding:utf-8
import pygame, sys, random, time, easygui
from pygame.locals import *

# 初始化pygame环境
pygame.init()
pygame.mixer.init()
# 创建一个长宽分别为480/650窗口
screen = pygame.display.set_mode((960, 720))
screen.fill((255, 255, 255))
# 设置窗口标题
pygame.display.set_caption("幸运抽奖")
background_image = pygame.image.load("项目素材/背景.jpeg")
pygame.mixer.music.load('项目素材/好运来.mp3')
pygame.mixer.music.play()


def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if Game.state == '选择阶段':
                Game.state = '开始滚动'
            elif Game.state == '结果1' or Game.state == '结果2':
                Game.state = '开始滚动'


def render_text(text, position, size, color):
    font = pygame.font.Font("项目素材/fonts/simhei.ttf", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


class Participant:
    def __init__(self, number, name, x, y):
        self.number = number
        self.name = name
        self.x = x
        self.y = y
        self.result_name = ''

    def draw(self):
        render_text(f"第{self.number}位幸运观众: {self.name}", (self.x, self.y), 30, (255, 255, 255))

    def show_result(self):
        render_text(f"第{self.number}位幸运观众: {self.result_name}", (self.x, self.y), 30, (255, 255, 255))


def check_time(last_time, interval):
    if last_time == 0:
        Game.last_time = time.time()
        return False
    current_time = time.time()
    return current_time - last_time >= interval


class Game:
    music_playing = True
    state = '选择阶段'
    flash_intensity = 0
    flash_increasing = True
    participants = [
        Participant('一', '', 50, 50),
        Participant('二', '', 500, 50),
        Participant('三', '', 50, 250),
        Participant('四', '', 500, 250),
        Participant('五', '', 50, 450),
        Participant('六', '', 500, 450)
    ]
    selected_numbers = [0, 0, 0, 0, 0, 0]
    last_time = 0

    participant_names = ['用户01', '用户02', '用户03', '用户04', '用户05', '用户06', '用户07', '用户08', '用户09', '用户10',
                         '用户11', '用户12', '用户13', '用户14', '用户15', '用户16', '用户17', '用户18', '用户19', '用户20',
                         '用户21', '用户22', '用户23', '用户24']
    available_numbers = list(range(0, len(participant_names)))
    original_available_numbers = list(range(0, len(participant_names)))


def flash_text(text):
    render_text(text, (170, 650), 30,
                (150 + Game.flash_intensity, 150 + Game.flash_intensity, 150 + Game.flash_intensity))
    if Game.flash_increasing:
        Game.flash_intensity += 2
        if Game.flash_intensity >= 100:
            Game.flash_increasing = False
    else:
        Game.flash_intensity -= 3
        if Game.flash_intensity <= 10:
            Game.flash_increasing = True


def search(list, number):
    for i in range(len(list)):
        if list[i] == number:
            return i


def choose():
    num = 0
    Game.selected_numbers[0] = random.randint(0, len(Game.available_numbers) - 1)
    Game.available_numbers.remove(Game.selected_numbers[0])
    for i in Game.selected_numbers:
        if num != 0:
            k = random.randint(0, len(Game.available_numbers) - 1)
            Game.selected_numbers[num] = Game.available_numbers[k]
            Game.available_numbers.remove(Game.selected_numbers[num])
        num += 1
    Game.available_numbers = list(range(0, len(Game.participant_names)))


def rolling():
    if Game.state == '开始滚动':
        s = 0
        screen.blit(background_image, (0, 0))
        choose()
        for participant in Game.participants:
            participant.name = Game.participant_names[Game.selected_numbers[search(Game.participants, participant)]]
            participant.draw()
        if not check_time(Game.last_time, 5):
            return
        Game.last_time = 0
        Game.state = '结果1'
        for participant in Game.participants:
            participant.result_name = Game.participant_names[
                Game.selected_numbers[search(Game.participants, participant)]]
        pygame.mixer.music.stop()

    if Game.state == '滚动结束1':
        screen.blit(background_image, (0, 0))
        choose()
        for participant in Game.participants:
            participant.name = Game.participant_names[Game.selected_numbers[search(Game.participants, participant)]]
            participant.draw()
        if not check_time(Game.last_time, 5):
            return
        Game.last_time = time.time()
        Game.state = '结果2'

        for participant in Game.participants:
            participant.result_name = Game.participant_names[
                Game.selected_numbers[search(Game.participants, participant)]]


def show_result():
    if Game.state == '结果1':
        for participant in Game.participants:
            participant.show_result()
        flash_text('——————按下空格键以继续——————')
    if Game.state == '结果2':
        for participant in Game.participants:
            participant.show_result()
        flash_text('——————按下空格键以继续——————')


def check_game_state():
    screen.blit(background_image, (0, 0))
    if Game.state == '选择阶段' or Game.state == '选择阶段2':
        for participant in Game.participants:
            participant.draw()
        flash_text('——————按下空格键以抽取——————')
    rolling()
    show_result()


while True:
    handle_event()
    check_game_state()
    pygame.display.update()
    pygame.time.delay(10)
