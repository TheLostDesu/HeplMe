from car import car
from constansts import acceleration_opponent_max, acceleration_opponent_min, opponent_rotation_rate, can_go_ai
from geometry import Point, Ray
from variables import road
import variables
import pygame
import math

import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

agent = None

class QNetwork(nn.Module):
    def __init__(self, lr, input_dims, n_actions, fc1_dims = 256, fc2_dims=256, ):
        super(QNetwork, self).__init__()
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions
        self.fc1 = nn.Linear(*input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, n_actions)
        self.optimizer = optim.Adam(self.parameters(), lr = lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cpu')
        self.to(self.device)
    
    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        action = self.fc3(x)
        return action


class Deciser():
    def __init__(self, gamma, epsilon, lr, input_dims, n_actions, batch_size, max_mem_size = 1000,
                 epsilon_end=0.01, epsilon_dec = 0.001):
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_end = epsilon_end
        self.lr = lr
        self.input_dims = input_dims
        self.n_actions = n_actions
        self.actions = [i for i in range(n_actions)]
        self.max_mem_size = max_mem_size
        self.batch_size = batch_size
        self.Q = QNetwork(lr = self.lr, input_dims = input_dims, n_actions = self.n_actions)

        self.state_memory = np.zeros((self.max_mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.max_mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.max_mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.max_mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.max_mem_size, dtype=np.bool)
        self.mem_cntrl = 0
    

    def store_transition(self, state, action, reward, next_state, done):
        index = self.mem_cntrl % self.max_mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = next_state
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = done

        self.mem_cntrl += 1
    

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = T.tensor([observation]).to(self.Q.device)
            actions = self.Q.forward(state)
            action = T.argmax(actions).item()
        else:
            action = np.random.choice(self.actions)
        return action
    
    def learn(self):
        if self.mem_cntrl < self.batch_size:
            return
        
        self.Q.optimizer.zero_grad()
        max_mem = min(self.mem_cntrl, self.max_mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        state_batch = T.tensor(self.state_memory[batch]).to(self.Q.device)
        new_state_batch = T.tensor(self.new_state_memory[batch]).to(self.Q.device)
        reward_batch = T.tensor(self.reward_memory[batch]).to(self.Q.device)
        terminal_batch = T.tensor(self.terminal_memory[batch]).to(self.Q.device)
        action_batch = self.action_memory[batch]

        q = self.Q.forward(state_batch)[batch_index, action_batch]
        q_next = self.Q.forward(new_state_batch)
        q_next[terminal_batch] = 0.0
        k = (self.gamma * (T.max(q_next, dim=1)[0]))
        q_target = reward_batch + k

        loss = self.Q.loss(q_target, q).to(self.Q.device)
        loss.backward()
        self.Q.optimizer.step()
        
        self.epsilon = max(self.epsilon - self.epsilon_dec, self.epsilon_end)
        
score = 0

def agent_define():
    global agent, score
    score = 0
    agent = Deciser(0.99, 1.0, 0.001, [5], 8, 64)

def new_car():
    global score 
    score = 0



class AI_car(car):
    '''
    Класс отвечающий за машину оппонента
    '''
    def __init__(self):
        super().__init__(500, 100, angle = math.pi, max_acceleration = acceleration_opponent_max, min_acceleration = acceleration_opponent_min)
    

    def get_observation(self) -> list:
        '''
        Функция получения наблюдения за средой
        '''
        rct = self.car_rect
        point1 = rct.point1 % rct.point2
        angle = self.angle
        point2 = point1 + Point(math.cos(angle), -math.sin(angle))
        point3 = point1 + Point(math.cos(angle + math.pi/6), -math.sin(angle + math.pi/6))
        point4 = point1 + Point(math.cos(angle + math.pi/4), -math.sin(angle + math.pi/4))
        point5 = point1 + Point(-math.cos(angle + math.pi/6), math.sin(angle + math.pi/6))
        point6 = point1 + Point(-math.cos(angle + math.pi/4), math.sin(angle + math.pi/4))

        rays = [Ray(point1, point2),
                Ray(point1, point3),
                Ray(point1, point4),
                Ray(point1, point5),
                Ray(point1, point6)]
        obs = []

        for ray in rays:
            point_ans = None
            if road is not None:
                for segment in road.inner_poly:
                    pnt2 = ray.intersect_with_segment(segment)
                    if point_ans is None or (pnt2 is not None and pnt2.dist2(point1) < point_ans.dist2(point1)):
                        point_ans = pnt2
                
                for segment in road.outer_poly:
                    pnt2 = ray.intersect_with_segment(segment)
                    if point_ans is None or (pnt2 is not None and pnt2.dist2(point1) < point_ans.dist2(point1)):
                        point_ans = pnt2
            if point_ans is None:
                obs.append(1000.0)
            else:
                obs.append(point1.dist2(point_ans) ** 0.5)
        return obs



    def get_reward(self)->int:
        '''
        Функция выдачи награды
        '''
        if self.check_crash():
            return -10
        
        k = 0
        for i in variables.checkpoints:
            if not i.is_used and len(self.car_rect ^ i.checkpnt_rect):
                k += 1
                i.use()

        return k

    def next_frame(self):
        '''
        Функция проверки того, что было сделанно на кадре.
        Возвращает True, если машина все еще жива, иначе False
        '''
        if self.check_crash():
            return False

        global score

        obs = self.get_observation()

        decision_ = agent.choose_action(obs)
        if decision_ == 8:
            decision = ' '
        else:
            decision = can_go_ai[decision_]

        if 'w' in decision:
            self.accelerate()
        if 's' in decision:
            self.slow_down()
        if 'a' in decision:
            self.turn(opponent_rotation_rate * self.get_speed() / 5000)
        if 'd' in decision:
            self.turn(-opponent_rotation_rate * self.get_speed() / 5000)
        elif 'brk' in decision:
            self.break_()
        self.slow_down_by_drift()
        self.go()


        obs_ = self.get_observation()
        reward = self.get_reward()
        score += reward
        agent.store_transition(obs, decision_, reward, obs_, self.check_crash())
        agent.learn()
        obs = obs_

        return True

    def draw(self, surface):
        '''
        Функция рисующаяя машину на surface
        '''
        pygame.draw.polygon(surface, (255, 0, 0), self.car_rect.get_points())

        