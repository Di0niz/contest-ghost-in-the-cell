# -*- coding: utf-8 -*-

import sys
import math

# раздел описания структуры программы

# действия, которые могут быть выполнен


# Описание используемых предметов

DEBUG = True


class EntityType:
    FACTORY = "FACTORY"
    TROOP = "TROOP"


class Entity:
    def __init__(self):
        self.player = 0
        self.entity_id = 0
    
    def __str__(self):
        return "%d" % self.entity_id

    def __repr__(self):
        return "%d" % self.entity_id

class FactoryEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.num_cyborg = 0
        self.production = 0
    def __str__(self):
        return "F%d" % self.entity_id

    def __repr__(self):
        return "F%d" % self.entity_id
class TroopEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.factory_from = 0
        self.factory_to = 0
        self.num_cyborg = 0
        self.time_remain = 0
    def __str__(self):
        return "T%d" % self.entity_id

    def __repr__(self):
        return "T%d" % self.entity_id

class World:
    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.troops = []
        self.factories = {}
        self.links = []
        self.num_factory = 0

    def init(self):
        """ инициализируем состояние игры """
        self.num_factory = int(raw_input())  # the number of factories
        link_count = int(raw_input())  # the number of links between factories

        # создаем пустой массив
        self.factories = map(lambda x: None, xrange(self.num_factory))


        # отображение вложенных данных
        if DEBUG:
            print >> sys.stderr, self.num_factory
            print >> sys.stderr, link_count

        self.create_links(self.num_factory)
        for i in xrange(link_count):
            raw = raw_input()
            if DEBUG:
                print >> sys.stderr, raw
            factory_1, factory_2, distance = [int(j) for j in raw.split()]

            # определение данных для отображение
            self.links[factory_1][factory_2] = distance
            self.links[factory_2][factory_1] = distance

    def update(self):
        """Обновление статуса текущего мира"""
        entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)
        if DEBUG:
            print >> sys.stderr, entity_count

        self.troops = []

        for i in xrange(entity_count):
            raw = raw_input()
            if DEBUG:
                print >> sys.stderr, raw
            entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = raw.split()
            entity_id = int(entity_id)
            arg_1 = int(arg_1)
            arg_2 = int(arg_2)
            arg_3 = int(arg_3)
            arg_4 = int(arg_4)
            arg_5 = int(arg_5)

            if entity_type == EntityType.FACTORY:
                factory = self.factories[entity_id]
                # инициализируем фабрику
                if factory is None:
                    factory = FactoryEntity()
                    self.factories[entity_id] = factory
                factory.entity_id = entity_id
                factory.player, factory.num_cyborg, factory.production = arg_1, arg_2, arg_3


            elif entity_type == EntityType.TROOP:
                troop = TroopEntity()
                troop.player, troop.factory_from, troop.factory_to = arg_1, arg_2, arg_3
                troop.num_cyborg, troop.time_remain = arg_4, arg_5
                troop.entity_id = entity_id

                self.troops.append(troop)

    def uniform_cost_search(self, start, goals):
        """ За основу взят алгоритм с wiki
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        node = start
        frontier = [node]
        explored = []

        # определение оптимальных вершин
        vertex = {node:(0, None)}

        # пока есть что обходить
        while not (node == None or len(frontier)==0):

            node = frontier.pop()

            explored.append(node)

            distance = vertex[node][0]

            next_node = None

            for n in self.get_nodes(node):
                if n not in explored:

                    # определяем вес связи 
                    next_distance = distance + self.links[node.entity_id][n.entity_id]

                    # помечаем текущую вершину
                    if n not in vertex or next_distance <= vertex[n][0]:
                        vertex[n] = (next_distance, node)

                    if not (n in frontier or n in goals):
                        frontier.append(n)
        return vertex


    def find_shortest(self, start, goals):
        vertex = self.uniform_cost_search(start, goals)

        # востанавливаем цепочку
        goal = goals[0]
        for n in goals:
            if vertex[n][0] < vertex[goal][0]:
                goal = n

        node = vertex[goal][1]
        solution = [goal]
        while node is not None:
            solution.insert(0,node)
            node = vertex[node][1]

        return solution

    
    def get_nodes(self, node):

        i = node.entity_id

        nodes = []
        for j in xrange(self.num_factory):
            newnode = self.factories[j]
            if self.links[i][j] > 0 and i != j and newnode not in nodes:
                nodes.append(newnode)

        return nodes

    def calc_amount_path(self, path):
        """Расчитываем стоимость пути между точками"""
        amount = 0
        for i in xrange(len(path) - 1):
            amount = amount + self.links[path[i].entity_id][path[i+1].entity_id]
        return amount

    def create_links(self, size):
        """Определяем создание новых элементов"""
        for i in xrange(size):
            l = []
            for j in xrange(size):
                l.append(0)
            self.links.append(l)
        return l


# Описание стратегии для принятия решения о базе

class ActionType:
    """ Определяем список возможных действий """
    PROBLEM_MOVE = "PROBLEM_MOVE"
    MOVE = "MOVE"

class Action:
    """Определение действия выполняемого для объекта """
    def __init__(self, action_from, action_to, action_method):
        self.action_from = action_from
        self.action_to = action_to
        self.method = action_method

    def run_method(self, kwargs):
        result = False
        method_result = None

        if method_result is None:
            result = False
        else: 
            result = True

class DummyStrategy:

    def __init__(self, world):
        self.world = world

    def get_actions(self):
        f = self.world.factories

        actions = []
        for base in filter(lambda x: x.num_cyborg > 0 and x.player == 1, f):

            attack = None
            entities_dict = filter(lambda x: x.player == 0 and x.production > 0, f) 

            if len(entities_dict) > 0:
                path = self.world.find_shortest(base, entities_dict)
                attack = path[1]

            if attack is None:
                entities_dict = filter(lambda x: x.player == -1, f)
                if len(entities_dict) > 0:
                    path = self.world.find_shortest(base, entities_dict)
                    attack = path[1]

            if attack is None:
                entities_dict = filter(lambda x: x.player == 0, f)

                if len(entities_dict) > 0:
                    path = self.world.find_shortest(base, entities_dict)
                    attack = path[1]


            if not (attack is None):
                actions.append( "MOVE %d %d %d" % (base.entity_id, attack.entity_id, base.num_cyborg))
        
        if len(actions) == 0:
            actions.append("WAIT")
        return ";".join(actions)

class Strategy:
    """ Применяемая стратегия """
    def __init__(self, world):
        self.world = world

        """Определяем перечень доступных евристик для стратегии"""
        self.states = [
            Action(ActionType.PROBLEM_MOVE, ActionType.MOVE, self.find_near_empty)
        ]

    def find_problem(self, factory):
        """ ищу проблему которую пытаемся решить. По умолчанию это будет движение"""

        problem = ActionType.MOVE

        return problem

    def find_near_empty(self, agrs):
        return False


    def find_command(self):
        return "WAIT"


    def find_action(self, state, for_wizard, prev_action=None):
        """Определяем правило, которое работало по набору состояний"""
        prev_state = None
        current_rule = None

        rules = self.get_rules(for_wizard, prev_action)

        filter_lambda = lambda x: x[0] == state and (x[2] is None or\
            (isinstance(x[3], list) and x[2](*x[3])) or\
            (not isinstance(x[3], list) and x[2](x[3]))\
        )

        level = ""
        rules_comment = ""
        while state != prev_state:
            prev_state = state

            try:
                filter_rules = filter(filter_lambda, rules)
            except Exception:
                print "Current state: %s\n%s" % (Strategy.desc(state), rules_comment)    
                raise NotImplementedError        

            for rule in filter_rules:
                state = rule[1]
                current_rule = rule
                break


            if prev_state != state:
                rules_comment += "%s%s\n" % (level, Strategy.desc(state))
                level = "%s " % level

        if (current_rule[3] == None):
            print rules_comment

        return current_rule[1], current_rule[3]



    def get_player_command(self):
        return "WAIT"


# основная часть программы

world = World()

world.init()

strategy = DummyStrategy(world)

while True:

    world.update()

    #strategy.find_command()

    #print strategy.get_player_command()

    #print world.links


    print strategy.get_actions()

    break