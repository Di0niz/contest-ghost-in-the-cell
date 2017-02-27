# -*- coding: utf-8 -*-

import sys
import math

# раздел описания структуры программы

# действия, которые могут быть выполнен

class Action:
    def command(self):
        pass


# Описание используемых предметов

class EntityType:
    FACTORY = 1
    TROOP = 2


class Entity:
    pass

class FactoryEntity(Entity):
    pass

class TroopEntity(Entity):
    pass

class World:
    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.troops = []
        self.factories = []
        self.links = []

    def init(self):
        """ инициализируем состояние игры """
        factory_count = int(raw_input())  # the number of factories
        link_count = int(raw_input())  # the number of links between factories

        # отображение вложенных данных
        print >> sys.stderr, factory_count
        print >> sys.stderr, link_count

        self.create_links(factory_count)
        for i in xrange(link_count):
            raw = raw_input()
            print >> sys.stderr, raw
            factory_1, factory_2, distance = [int(j) for j in raw.split()]

            # определение данных для отображение
            w.links[factory_1][factory_2] = distance



    def create_links(self, size):
        """Определяем создание новых элементов"""
        for i in xrange(size):
            l = []
            for j in xrange(size):
                l.append(0)
                self.links.append(l)
        return l


# Описание стратегии для принятия решения о базе

class Strategy:
    
    def __init__(self, world):        
        self.world = world
        
    
    def get_player_command():
        return "WAIT"


# Описание генератора мира для определения заданных объектов 

class WorldGenerator:

    @staticmethod
    def get_world():
        
        w = World()

        factory_count = int(raw_input())  # the number of factories
        link_count = int(raw_input())  # the number of links between factories

        # отображение вложенных данных
        print >> sys.stderr, factory_count
        print >> sys.stderr, link_count

        w.create_links(factory_count)
        for i in xrange(link_count):
            raw = raw_input()
            print >> sys.stderr, raw
            factory_1, factory_2, distance = [int(j) for j in raw.split()]

            # определение данных для отображение
            w.links[factory_1][factory_2] = distance

        return w

    @staticmethod
    def read_entities():
        entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)

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
                pass
            elif entity_type == EntityType.TROOP:
                pass    
            pass

    @staticmethod
    def get_factory(entity_id, entity_type, arg_1, arg_2, arg_3):
        return None

    @staticmethod
    def get_troop(entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5):
        return None
        

# основная часть программы

w = World()

w.init()

while True:

    w.update()