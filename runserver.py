# -*- coding: utf-8 -*-

import sys
import math

# раздел описания структуры программы

# действия, которые могут быть выполнен


# Описание используемых предметов

class EntityType:
    FACTORY = 1
    TROOP = 2


class Entity:
    def __init__(self):
        self.player = 0

class FactoryEntity(Entity):
    def __init__(self):
        super(FactoryEntity, self).__init__()
        self.num_cyborg = 0
        self.production = 0

class TroopEntity(Entity):
    def __init__(self):
        super(TroopEntity, self).__init__()
        self.factory_from = 0
        self.factory_to = 0
        self.num_cyborg = 0
        self.time_remain = 0

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

        self.factories = {a:None for a in xrange(self.num_factory)}


        # отображение вложенных данных
        print >> sys.stderr, self.num_factory
        print >> sys.stderr, link_count

        self.create_links(self.num_factory)
        for i in xrange(link_count):
            raw = raw_input()
            print >> sys.stderr, raw
            factory_1, factory_2, distance = [int(j) for j in raw.split()]

            # определение данных для отображение
            self.links[factory_1][factory_2] = distance

    def update(self):
        """Обновление статуса текущего мира"""
        entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)
        print >> sys.stderr, entity_count

        self.troops = []

        for i in xrange(entity_count):
            raw = raw_input()
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

                factory.player, factory.num_cyborg, factory.production = arg_1, arg_2, arg_3


            elif entity_type == EntityType.TROOP:
                troop = TroopEntity()
                troop.player, troop.factory_from, troop.factory_to, troop.num_cyborg,\
                troop.time_remain = arg_1, arg_2, arg_3, arg_4, arg_5
                self.troops.append(troop)



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
    def __init__(self, action_from, action_to, action_method, action_kwarg):
        # 
        self.action_type = None
        # 
        self.action_target = None
        # набор аргументов
        self.argv = None 

class Strategy:
    """ Применяемая стратегия """
    def __init__(self):
        self.world = world

        """Определяем перечень доступных евристик для стратегии"""
        states = [
            Action(ActionType.PROBLEM_MOVE, ActionType.MOVE, self.find_near_empty)
        ]
        return states

    def find_problem(self, factory):
        """ ищу проблему которую пытаемся решить. По умолчанию это будет движение"""
        problem = ActionType.MOVE

        return problem


    def find_command(self, world):
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

strategy = Strategy(world)

while True:

    world.update()

    strategy.find_command(world)

    print strategy.get_player_command()

    break
