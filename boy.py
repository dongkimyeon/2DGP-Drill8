from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine

#이벤트 체크 함수
def space_down(event): # event가 space key input 인가를 확인 T/F
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE
def a_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_a

def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT
def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT
def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT
def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT

def time_out(event):
    return event[0] == 'TIME_OUT'

class AutoRun:
    def __init__(self, boy):
        self.boy = boy
        self.boy.running_start_time = get_time()
    def enter(self, event):
        print('AutoRun')

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.dir * 5
        if get_time() - self.boy.running_start_time > 5.0:
            self.boy.state_machine.handle_state_event(('TIME_OUT', 0))

    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        if right_down(event) or left_up(event) or a_down(event):
            self.boy.face_dir = 1
            self.boy.dir = 1
        elif left_down(event) or right_up(event):
            self.boy.face_dir = -1
            self.boy.dir = -1

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.dir * 5

    def draw(self):
        if self.boy.face_dir == 1:  # right
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:  # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)

class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        self.boy.dir = 0
        self.boy.wait_start_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if get_time() - self.boy.wait_start_time > 10.0:
            self.boy.state_machine.handle_state_event(('TIME_OUT', 0))


    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)

class Sleep:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, event):
        self.boy.dir = 0

    def exit(self, event):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2, '',self.boy.x, self.boy.y - 25, 100, 100)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, -3.141592/2, 'h',self.boy.x, self.boy.y - 25, 100, 100)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        self.AUTO_RUN = AutoRun(self)
        self.state_machine = StateMachine(
        self.IDLE, #초기 상태
        {
            self.SLEEP : {space_down : self.IDLE},
            self.IDLE : {right_down : self.RUN, left_down : self.RUN,  time_out : self.SLEEP , a_down : self.AUTO_RUN},
            self.RUN : {right_down : self.IDLE, left_down : self.IDLE, right_up : self.IDLE , left_up : self.IDLE },
            self.AUTO_RUN : {time_out : self.IDLE}
        })

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

