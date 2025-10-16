from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter('IDLE')

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event): #event가 space key input -> 확인 T/F
                self.next_state = self.rules[self.cur_state][check_event] #IDLE
                self.cur_state.exit(state_event)
                self.next_state.enter(state_event)
                #현재 상태가 어떤 이벤트에 의해서 다음 상태로 바꼈는지 보여주는 디버깅 메시지
                print(f'State Change: {self.cur_state.__class__.__name__}  by {event_to_string(state_event) } -> {self.next_state.__class__.__name__}')
                self.cur_state = self.next_state
                print(f'Unhandled Event: {self.cur_state.__class__.__name__}  by {event_to_string(state_event)}')
                return


