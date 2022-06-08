import random


class Graph(object):
    def __init__(self, cost_matrix: list, rank: int):
        """
        :param cost_matrix:
        :param rank: maliyet matrisi sıralaması
        :param rank: rank of the cost matrix

        """

        self.matrix = cost_matrix
        self.rank = rank
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, rho: float, q: int,
                 strategy: int):
        """
        :param ant_count: Modeldeki karınca sayısı
        :param generations: Modelin generasyon  sayısı
        :param alpha: feromon seviyesinin formüle etkisi ##relative importance of pheromone
        :param beta: maliyetin formüle etkisi ## relative importance of heuristic information
        :param rho (p): feromon buharlaşma oranı ## pheromone residual coefficient
        :param q: feromon yoğunluğu ## pheromone intensity
        :param strategy: Feromon güncelleme stratejisi. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        ## pheromone update strategy.
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy


    def _update_pheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]


    def solve(self, graph: Graph):
        """
        :param graph:
        """
        best_cost = float('inf')
        best_solution = []
        for gen in range(self.generations): #Jenerasyon sayısı kadar işlem yapılacak

            ants = [_Ant(self, graph) for i in range(self.ant_count)]
           
            #her bir karınca için işlem yapılacak
            ##action will be taken for each ant
            for ant in ants:
                for i in range(graph.rank - 1):
                    ant._select_next() #karınca bir yol seçecek ##the ant will choose a path
                ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]] #Yolunu tamamlayan karıncanın gittiği yol tutuluyor ##The path taken by the ant that completes its path is kept.
                
                if ant.total_cost < best_cost: #karıcanın yolu yeni en iyi yol olabilir, karşılaştırma yapılıyor ##The ant's path may be the new best path. making a comparison
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tabu
               
                # feromon güncellemesi    ## update pheromone
                ant._update_pheromone_delta()
            self._update_pheromone(graph, ants)
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # tabu list
        self.pheromone_delta = []  # yerel feromon artışı ## the local increase of pheromone
        self.allowed = [i for i in range(graph.rank)]  # sonraki seçim için izin verilen düğümler  ## nodes which are allowed for the next selection
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in
                    range(graph.rank)]  # buluşsal bilgi ## heuristic information
        start = random.randint(0, graph.rank - 1)  # herhangi bir düğümden başla  ## start from any node
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _select_next(self):
        #feromon seviyesi ve maliyetin formüle etksi = dominator
        denominator = 0
        #olasılık hesaplama formülü payka kısmı hesaplanıyor
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta

        probabilities = [0 for i in range(self.graph.rank)] #Bir sonraki adımda düğümlere geçme olasılığı ## probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                #Gidilebilecek her yol için olasılık hesaplaması 
                self.allowed.index(i) 
                #olasılık hesaplama formülü
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                    self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass  # do nothing
       
        #Rulet yöntemi ile bir sonraki düğüm seçilecek ## select next node by probability roulette
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected


    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]

        ##Feromon güncellemesi 
        #Yeni Feromon Seviyesi = Eski Feromon Seviyesi + ( 1 / iki nokta arası maliyet   )
        self.pheromone_delta[i][j] = self.colony.Q +  (1/ self.graph.matrix[i][j])

