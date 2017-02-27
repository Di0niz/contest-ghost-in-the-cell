# -*- coding: utf-8 -*-


# раздел описания структуры программы

# действия, которые могут быть выполнен

class Action:
    def command(self):
        pass


# Описание используемых предметов

class Entity:
    pass

class FactoryEntity(Entity):
    pass

class TroopEntity(Entity):
    pass

# Описание стратегии для принятия решения о базе


# Описание генератора мира для определения заданных объектов 

class Generator:

    @staticmethod
    def get_world():
        factory_count = int(raw_input())  # the number of factories
        link_count = int(raw_input())  # the number of links between factories
        for i in xrange(link_count):
            factory_1, factory_2, distance = [int(j) for j in raw_input().split()]

    @staticmethod
    def read_entities():
        entity_count = int(raw_input())  # the number of entities (e.g. factories and troops)
        for i in xrange(entity_count):
            entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = raw_input().split()
            entity_id = int(entity_id)
            arg_1 = int(arg_1)
            arg_2 = int(arg_2)
            arg_3 = int(arg_3)
            arg_4 = int(arg_4)
            arg_5 = int(arg_5)