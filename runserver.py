# -*- coding: utf-8 -*-

import sys

# раздел описания структуры программы

# действия, которые могут быть выполнен


# Описание используемых предметов

DEBUG = True


class EntityType(object):
    """Описание внутриигровых объектов"""
    FACTORY = "FACTORY"
    TROOP = "TROOP"
    BOMB = "BOMB"


class Entity(object):
    """Определение базового класса внутриигровых объектов"""
    def __init__(self):
        self.player = 0
        self.entity_id = 0

    def to_str(self):
        return "%d" % self.entity_id

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()

class FactoryEntity(Entity):
    """Описание фабрики"""
    def __init__(self):
        Entity.__init__(self)
        self.num_cyborg = 0
        self.production = 0
    def to_str(self):
        return "F%d" % self.entity_id

class TroopEntity(Entity):
    """Описание пехоты"""
    def __init__(self):
        Entity.__init__(self)
        self.factory_from = 0
        self.factory_to = 0
        self.num_cyborg = 0
        self.time_remain = 0

    def to_str(self):
        return "T%d" % self.entity_id
class BombEntity(Entity):
    """Описание пехоты"""
    def __init__(self):
        Entity.__init__(self)
        self.factory_from = 0
        self.factory_to = 0
        self.time_remain = 0

    def to_str(self):
        return "T%d" % self.entity_id
# описание ламбда
LAMBDA_EMPTY_PRODUCTION = lambda x: x.player == 0 and x.production > 0
LAMBDA_PRODUCTION_3 = lambda x: x.player == 0 and x.production == 3
LAMBDA_PRODUCTION_2 = lambda x: x.player == 0 and x.production == 2
LAMBDA_PRODUCTION_1 = lambda x: x.player == 0 and x.production == 1
LAMBDA_OTHERS = lambda x: x.player < 1 and x.production == 0
LAMBDA_MY_ARMY = lambda x: x.player == 1 and x.num_cyborg > 0
LAMBDA_MY_ARMY_ALL = lambda x: x.player == 1
LAMBDA_ENEMY_ARMY = lambda x: x.player == -1 and x.num_cyborg > 0
LAMBDA_ENEMY_ARMY_ALL = lambda x: x.player == -1
LAMBDA_ENEMY_ARMY_PRODUCTION = lambda x: x.player == -1 and x.num_cyborg > 0 and x.production > 2
LAMBDA_EMPTY = lambda x: None
LAMBDA_ZERO = lambda x: 0



class World(object):
    """Описание игрового мира"""


    def __init__(self):
        """ Определяем список объектов доступных для класса """
        self.troops = []
        self.factories = {}
        self.links = []
        self.num_factory = 0
        self.bombs = []
        self.num_bombs = 2

    def init(self):
        """ инициализируем состояние игры """
        self.num_factory = int(raw_input())  # the number of factories
        link_count = int(raw_input())  # the number of links between factories

        # создаем пустой массив
        self.factories = map(LAMBDA_EMPTY, xrange(self.num_factory))


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

            elif entity_type == EntityType.BOMB:
                bomb = BombEntity()
                bomb.player, bomb.factory_from, bomb.factory_to = arg_1, arg_2, arg_3
                bomb.time_remain = arg_4
                bomb.entity_id = entity_id

                self.bombs.append(bomb)                

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
        while not (node is None or len(frontier) == 0):

            node = frontier.pop()

            explored.append(node)

            distance = vertex[node][0]

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
        """Описание алгоритма поиска кратчайшего пути"""
        vertex = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку
        goal = goals[0]
        for n in goals:
            if vertex[n][0] < vertex[goal][0]:
                goal = n
            elif vertex[n][0] == vertex[goal][0] and n.production < goal.production:
                goal = n

        node = vertex[goal][1]
        solution = [goal]
        while node is not None:
            solution.insert(0, node)
            node = vertex[node][1]

        return solution


    def get_nodes(self, node):
        """Определение списка соседних вершин"""

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
            zero_list = map(LAMBDA_ZERO, xrange(size))
            self.links.append(zero_list)



# Описание стратегии для принятия решения о базе

class ActionType:
    """ Определяем список возможных действий """
    PROBLEM_MOVE = "PROBLEM_MOVE"
    MOVE = "MOVE"
    ATTACK_EMPTY_BASE = "ATTACK_EMPTY_BASE"

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





# описание продвинутой стратегии 
class SmartStrategy:
    """ Применяемая стратегия """
    def __init__(self, world):
        self.world = world

        self.targets = world.factories

        self.actions = []

        """Определяем перечень доступных евристик для стратегии"""
        self.moves = {}
        self.grow = []
        self.bombs = {}

    def move_troop(self, base, next_point, attack, num_cyborg):
        """Осуществляем передвижения киборгов"""
        if base.num_cyborg >= num_cyborg:
            base.num_cyborg = base.num_cyborg - num_cyborg
        else:
            base.num_cyborg = 0

        if attack.num_cyborg >= num_cyborg:
            attack.num_cyborg = attack.num_cyborg - num_cyborg
        else:
            attack.num_cyborg = 0

        key = (base, next_point)

        if key not in self.moves:
            self.moves[key] = num_cyborg
        else:
            self.moves[key] = self.moves[key] + num_cyborg

    def parse_commands(self):
        """Преобразуем список команд в действия"""
        actions = []
        for command in self.moves:
            base, next_point = command
            action = "MOVE %d %d %d" % (base.entity_id, next_point.entity_id, self.moves[command])
            actions.append(action)

        for base in self.grow:
            action = "INC %d" % base.entity_id
            actions.append(action)

        for enemy in self.bombs:
            action = "BOMB %d %d" % (self.bombs[enemy].entity_id, enemy.entity_id)
            actions.append(action)   

        return actions

    def attack_targets(self, targets):
        """Определяем направление по цели"""

        if len(targets) == 0:
            return False

        for base in filter(LAMBDA_MY_ARMY, self.targets):

            dist_targets = targets

            # удаляем базы расстояние до которых больше 5
            for target in dist_targets:
                if self.world.calc_amount_path([base,target])>3:
                    dist_targets = [item for item in dist_targets if item not in [target]]

            do_while = base.num_cyborg > 0 and len(dist_targets) > 0

            while do_while:
                path = self.world.find_shortest(base, dist_targets)

                near, target = path[1], path[-1]

                self.move_troop(base, near, target, min(target.num_cyborg + 1, base.num_cyborg))

                if (target.num_cyborg == 0):
                    dist_targets = [item for item in dist_targets if item not in [target]]
                    targets = [item for item in targets if item not in [target]]

                do_while = base.num_cyborg > 0 and len(dist_targets) > 0
        return True # (ActionType.ATTACK_ENEMY, args)

    def factory_grow (self):
        """Фабрика растет, когда общее количество больше 30 и на одной точке больше 10"""

        factories = filter(LAMBDA_MY_ARMY, self.targets)
        sum_lambda = lambda x,y: x + y.num_cyborg
        all_cyborgs = reduce(sum_lambda, factories, 0)

        if all_cyborgs > 30:
            for base in factories:
                if (base.num_cyborg > 10):
                    base.num_cyborg = base.num_cyborg - 10
                    self.grow.append(base)

    def boombs_attack(self):
        """Бросаем бомбу только в случае, 
        если длина хода меньше 1, армия противника больше нас,
        если это промышленно значимый объект
        """

        if self.world.num_bombs == 0:
            return

        # потенциальная бага, если если только мои войска
        if len(filter(LAMBDA_MY_ARMY_ALL, self.world.bombs)) > 0:
            return

        factories = filter(LAMBDA_MY_ARMY_ALL, self.targets)

        enemies = filter(LAMBDA_ENEMY_ARMY_PRODUCTION, self.targets)

        for base in factories:
            for enemy in enemies:
                if self.world.calc_amount_path([base, enemy]) == 1\
                and base.num_cyborg <= base.num_cyborg:
                    self.world.num_bombs = self.world.num_bombs - 1
                    # исключаем из списка целей
                    self.targets = [item for item in self.targets if item not in [enemy]]
                    self.bombs[enemy] = base

                    # за один ход кидаем одну бомбу
                    return
                    
    def last_targets(self):
        factories = filter(LAMBDA_MY_ARMY, self.targets)

        targets = filter(LAMBDA_ENEMY_ARMY_ALL, self.targets)

        if len(targets) == 0:
            return

        for base in factories:       
            
            path = self.world.find_shortest(base, targets)
            near, target = path[1], path[-1]
            
            self.move_troop(base, near, target, base.num_cyborg)


    def get_actions(self):
        """получаем цепочку действий"""
        self.factory_grow()
        self.boombs_attack()
        self.attack_targets(filter(LAMBDA_PRODUCTION_3, self.targets))
        self.attack_targets(filter(LAMBDA_PRODUCTION_2, self.targets))
        self.attack_targets(filter(LAMBDA_PRODUCTION_1, self.targets))
        self.attack_targets(filter(LAMBDA_ENEMY_ARMY, self.targets))
        self.attack_targets(filter(LAMBDA_OTHERS, self.targets))

        self.last_targets()


        actions = self.parse_commands()

        if len(actions) == 0:
            actions = ["WAIT"]

        return ";".join(actions)

class DummyStrategy:
    """Простая стратегия для отладки отдельных элементов"""
    def __init__(self, world):
        self.world = world

    def get_actions(self):
        f = self.world.factories

        primary_target = filter(lambda x: x.player != 1 and x.production > 0, f) 
        else_target = filter(lambda x: x.player != 1 and x.production == 0, f)
        vertex = {}
        attacks = {}

        last_target = None

        facilities = filter(lambda x: x.num_cyborg > 0 and x.player == 1, f)

        for base in facilities:

            attack, target, path = None, None, None

            # определяем количество доступных ботов
            num_cyborg = base.num_cyborg

            while num_cyborg >  0 and len(primary_target) + len(primary_target) > 0:

                if len(primary_target) > 0:
                    path = self.world.find_shortest(base, primary_target)

                elif len(else_target) > 0:
                    path = self.world.find_shortest(base, else_target)

                if path is not None:

                    attack, target = path[1], path[-1]

                    if target not in vertex:
                        vertex[target] = target.num_cyborg + 1

                    cur_cyborg = min(vertex[target], num_cyborg)

                    num_cyborg = num_cyborg - cur_cyborg
                    vertex[target] = vertex[target] - cur_cyborg


                    if vertex[target] == 0:
                        primary_target = [item for item in primary_target if item not in [target]]
                        else_target = [item for item in else_target if item not in [target]]


                    if attack not in attacks:
                        attacks[attack] = {}

                    if base not in attacks[attack]:
                        attacks[attack][base] = cur_cyborg

                else:
                    if not (attack is None or base is None):
                        # на последнюю базу отправляем оставшихся
                        attacks[attack][base] = attacks[attack][base] + num_cyborg
                    num_cyborg = 0
                    
        actions = []
        if len(attacks) == 0:
            actions.append("WAIT")
        else:
            for attack in attacks.keys():
                for base in attacks[attack].keys():
                    command = "MOVE %d %d %d" % (base.entity_id, attack.entity_id, attacks[attack][base])
                    if DEBUG:
                        print >> sys.stderr, command, base.num_cyborg
                    actions.append(command)

        return ";".join(actions)


# основная часть программы

world = World()

world.init()


while True:

    world.update()

    strategy = SmartStrategy(world)
    print strategy.get_actions()

    break
