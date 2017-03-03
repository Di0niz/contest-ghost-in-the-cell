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
        # количество доступных киборгов для хода
        self.av_cyborg = 0
        # количество противников в следующие ходы
        # ограничиваем прогноз ходов следующими 5 ходами
        self.enemy_cyborgs = [0, 0, 0, 0, 0]
        # количество дополнительных солдат в следующие
        self.army_cyborgs = [0, 0, 0, 0, 0]
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
LAMBDA_PRODUCTION = lambda x: x.player == 0 and x.production > 0
LAMBDA_PRODUCTION_3 = lambda x: x.player == 0 and x.production == 3
LAMBDA_PRODUCTION_2 = lambda x: x.player == 0 and x.production == 2
LAMBDA_PRODUCTION_1 = lambda x: x.player == 0 and x.production == 1
LAMBDA_OTHERS = lambda x: x.player < 1 and x.production == 0
LAMBDA_OTHERS_ALL = lambda x: x.player < 1
LAMBDA_MY_ARMY = lambda x: x.player == 1 and x.num_cyborg > 0
LAMBDA_MY_ARMY_ALL = lambda x: x.player == 1
LAMBDA_MY_ARMY_PRODUCTION = lambda x: x.player == 1 and x.production > 0
LAMBDA_ENEMY_ARMY = lambda x: x.player == -1 and x.num_cyborg > 0
LAMBDA_ENEMY_ARMY_ALL = lambda x: x.player == -1
LAMBDA_ENEMY_ARMY_PRODUCTION = lambda x: x.player == -1 and x.num_cyborg > 0 and x.production > 2
LAMBDA_EMPTY = lambda x: None
LAMBDA_ZERO = lambda x: 0

REDUCE_PRODUCTION = lambda a, x: x if (a is None\
or a.production == 3\
or a.production == 3\
or a.production < x.production)\
and x.production < 3 else a

REDUCE_CYBORG_FOR_PRODUCTION = lambda a, x: x if (a is None \
or a.num_cyborg < x.num_cyborg)\
and x.production < 3 and a.production < 3 else a



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
                if factory.player == 1:
                    factory.av_cyborg = factory.num_cyborg
                else:
                    factory.av_cyborg = 0

                factory.enemy_cyborgs = [0, 0, 0, 0, 0]
                factory.army_cyborgs = [0, 0, 0, 0, 0]

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
                    if n not in vertex or next_distance < vertex[n][0]:
                        vertex[n] = (next_distance, node)

                    if not (n in frontier or n in goals):
                        frontier.append(n)

        return vertex


    def find_shortest(self, start, goals):
        """Описание алгоритма поиска кратчайшего пути"""
        vertex = self.uniform_cost_search(start, goals)
        # востанавливаем цепочку

        min_len = 10
        min_solution = []
        for goal in goals:
            solution = [goal]
            node = vertex[goal][1]
 
            while node is not None:
                solution.insert(0, node)
                node = vertex[node][1]

            if min_len > len(solution):
                min_solution = solution

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

# описание продвинутой стратегии
class SmartStrategy(object):
    """ Применяемая стратегия """
    def __init__(self, world):
        self.world = world

        self.targets = world.factories

        self.actions = []

        """Определяем перечень доступных евристик для стратегии"""
        self.moves = {}
        self.grow = []
        self.bombs = {}

        # используем для ведения ограничений магические константы


        # определяем доступные параметры
        # на чей стороне перевес?

        # определяем массив потребностей,
        # по умолчанию равен количеству противников, которые следует побороть
        self.factories_potential = map(LAMBDA_ZERO, xrange(world.num_factory))

        # определяем количество доступных очков для ходов
        self.cyborgs = map(LAMBDA_ZERO, xrange(world.num_factory))

        # для каждого игрока определяем его силу
        # начальное значение как 0
        self.player_production = {-1:0, 0:0, 1:0}

        # определяем мощность армии каждого игрока
        # начальное значение как 0
        self.player_cyborg = {-1:0, 0:0, 1:0}

    def calc_potential(self):
        """Расчитываем потребность в очках"""
        for factory in filter(LAMBDA_OTHERS_ALL, self.world.factories):
            self.factories_potential[factory.entity_id] = factory.num_cyborg

        
        # корректируем потенциал баз с учетом
        for troop in self.world.troops:
            # если враг приближает к моей фабрике
            if troop.time_remain < 2:

                factory_to = self.world.factories[troop.factory_to]

                # определяем направление удара
                direction = 1 if factory_to.player != troop.player else -1 

                entity_id = troop.factory_to
                delta_cyborg = troop.num_cyborg * direction

                self.factories_potential[entity_id] =\
                    self.factories_potential[entity_id] + delta_cyborg

    def calc_available_cyborgs(self):
        """Определяем возможное количество используемых ботов для каждой фабрики"""
        for base in filter(LAMBDA_MY_ARMY, self.world.factories):
            # расчитываем потребность
            need_cyborg = base.num_cyborg - max(self.factories_potential[base.entity_id],0)
            # потребность определяем не выше 0
            self.cyborgs[base.entity_id] = max(need_cyborg, 0)
    def calc_production(self):
        """Расчитываем мощность производства"""
        pp = self.player_production
        for factory in self.world.factories:
            pp[factory.player] = pp[factory.player] + factory.production
    def calc_cyborgs(self):
        """Расчитываем сумму всех войск в армии"""
        p_cyborg = self.player_cyborg

        for factory in self.world.factories + self.world.troops:
            p_cyborg[factory.player] = p_cyborg[factory.player] + factory.num_cyborg

    def move_troop(self, base, next_point, attack, num_cyborg):
        """Осуществляем передвижения киборгов"""

        # для своих баз уменьшаем количество доступных киборгов
        if self.cyborgs[base.entity_id] >= num_cyborg:
            self.cyborgs[base.entity_id] = self.cyborgs[base.entity_id] - num_cyborg
        else:
            self.cyborgs[base.entity_id] = 0

        # для чужых баз, уменьшаем потребность в киборгах
        # не меняем потребность для точки, до которой далеко
        if next_point == attack:
            if self.factories_potential[attack.entity_id] >= num_cyborg:

                self.factories_potential[attack.entity_id] =\
                self.factories_potential[attack.entity_id] - num_cyborg
            else:
                self.factories_potential[attack.entity_id] = 0

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
                if self.world.calc_amount_path([base, target]) > 3:
                    dist_targets = [item for item in dist_targets if item not in [target]]

            do_while = self.cyborgs[base.entity_id] > 0 and len(dist_targets) > 0

            # повторяем цикл
            while do_while:
                path = self.world.find_shortest(base, dist_targets)

                near, target = path[1], path[-1]
                # определяем потребность
                # учитываем что армия противника может рости
                if (target.player == -1):
                    cur_cyborg = self.factories_potential[target.entity_id] +\
                        target.production * self.world.calc_amount_path(path) + 1
                else:
                    cur_cyborg = self.factories_potential[target.entity_id] + 1

                need_cyborg = max(min(cur_cyborg, self.cyborgs[base.entity_id]),0)

                self.move_troop(base, near, target, need_cyborg)

                if self.factories_potential[target.entity_id] == 0:
                    dist_targets = [item for item in dist_targets if item not in [target]]
                    targets = [item for item in targets if item not in [target]]

                do_while = self.cyborgs[base.entity_id] > 0 and len(dist_targets) > 0 and cur_cyborg > 0

        return True # (ActionType.ATTACK_ENEMY, args)

    def factory_grow(self):
        """Фабрика растет, когда общее количество больше 30 и на одной точке больше 10"""

        factories = filter(LAMBDA_MY_ARMY, self.targets)
        sum_lambda = lambda x, y: x + y.num_cyborg
        all_cyborgs = reduce(sum_lambda, factories, 0)

        if all_cyborgs > 30:
            for base in factories:
                if self.cyborgs[base.entity_id] > 10:
                    self.cyborgs[base.entity_id] = self.cyborgs[base.entity_id] - 10
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

    def boombs_attack_myself(self):
        """Бросаем бомбу в самих себя, если наступает большая
        армия противника
        """

        if self.world.num_bombs == 0:
            return

        # потенциальная бага, если только мои войска
        if len(filter(LAMBDA_MY_ARMY_ALL, self.world.bombs)) > 0:
            return

        max_cyborg, potential_entity_id = 7, -1
        for entity_id in xrange(len(self.factories_potential)):
            num_cyborg = self.factories_potential[entity_id]
            if num_cyborg > max_cyborg:
                max_cyborg = num_cyborg
                potential_entity_id = entity_id

        # если нашли такаю базу
        if potential_entity_id >= 0:
            targets = filter(LAMBDA_MY_ARMY_ALL, self.targets)

            base = self.world.factories[potential_entity_id]
            targets = [item for item in targets if item not in [base]]
            path = self.world.find_shortest(base, targets)

            if path is not None and len(path) == 2:
                self.bombs[base] = path[1]

                # потенциальные требования уменьшаем
                self.factories_potential[base.entity_id] = 0
                # восстанавливаем количество киборгов для распределения
                if base.player == 1:
                    self.cyborgs[base.entity_id] = base.num_cyborg


    def last_targets(self):
        """Все доступные ресурсы направляем на последнюю цель"""
        factories = filter(LAMBDA_MY_ARMY, self.targets)

        targets = filter(LAMBDA_ENEMY_ARMY_ALL, self.targets)

        if len(targets) == 0:
            return

        for base in factories:

            path = self.world.find_shortest(base, targets)
            near, target = path[1], path[-1]

            self.move_troop(base, near, target, self.cyborgs[base.entity_id])

    
    def prepare(self):
        """Делаем первый проход стратегии"""
        self.calc_production()
        self.calc_cyborgs()
        self.calc_potential()
        self.calc_available_cyborgs()

    def update(self):
        """Обновляем полученные результаты"""
        pass

    def solve_find_empty_base(self):
        """решаем проблему не занятых баз"""

        if self.player_production[0] > 0:
            self.attack_targets(filter(LAMBDA_PRODUCTION_3, self.targets))
            self.attack_targets(filter(LAMBDA_PRODUCTION_2, self.targets))
            self.attack_targets(filter(LAMBDA_PRODUCTION_1, self.targets))

    def solve_grow_base(self):

        pp = self.player_production
        # однозначно когда нет возможности роста
        if pp[-1] >= pp[1] and pp[0] == 0:

            # определяем есть ли возможность вырасти сейчас
            factory = reduce(REDUCE_CYBORG_FOR_PRODUCTION,\
            map(LAMBDA_MY_ARMY_PRODUCTION, self.targets))

            if factory is not None and factory.num_cyborg > 10:
                self.grow.append(factory)


    def get_actions(self):
        """получаем цепочку действий"""

        # подготавливаем данные

        self.prepare()

        self.solve_find_empty_base()

        # пока блокируем рост, так как должно быть преимущество
        # над противником
        #self.factory_grow()
        #self.boombs_attack()
        #self.boombs_attack_myself()
        #self.attack_targets(filter(LAMBDA_PRODUCTION_3, self.targets))
        #self.attack_targets(filter(LAMBDA_PRODUCTION_2, self.targets))
        #self.attack_targets(filter(LAMBDA_PRODUCTION_1, self.targets))
        #self.attack_targets(filter(LAMBDA_ENEMY_ARMY, self.targets))
        #self.attack_targets(filter(LAMBDA_OTHERS, self.targets))
        #self.last_targets()


        actions = self.parse_commands()

        if len(actions) == 0:
            actions = ["WAIT"]

        return ";".join(actions)


# основная часть программы

WORLD = World()

WORLD.init()

while True:

    WORLD.update()

    STRATEGY = SmartStrategy(WORLD)
    print STRATEGY.get_actions()

    break
