from os import wait
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto


class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int):
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int):
        if n1 > n2:
            tmp = n2
            n2 = n1
            n1 = tmp
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    def parcourir_reseau(self):
        noeuds = self.noeuds
        entry_id = self.noeud_entree
        if self.noeud_entree not in self.noeuds or self.noeud_entree == -1:
            return set()
        # id de noeud_entree
        graph = {n: [] for n in noeuds.keys()}
        for n1, n2 in self.arcs:
            graph[n1].append(n2)
            graph[n2].append(n1)

        # Application de l'algorithme BFS :
        visited = set()
        queue = [entry_id]
        while queue:
            front = queue.pop(0)
            if front not in visited:
                visited.add(front)
                for neighbor in graph[front]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return visited

    def valider_reseau(self) -> bool:
        # TOVERIFY
        visited = self.parcourir_reseau()
        if len(self.noeuds) == len(visited):
            return True
        return False

    def valider_distribution(self, t: Terrain) -> bool:
        # TOVERIFY
        visited = self.parcourir_reseau()
        noeuds = self.noeuds

        possible_coord = {noeuds[v] for v in visited}
        clients = t.get_clients()
        for client in clients:
            if client not in possible_coord:
                return False
        return True

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs = self.strat.configurer(t)

    def afficher(self):
        # TODO
        pass

    def afficher_avec_terrain(self, t: Terrain):
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("~", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    if c == Case.CLIENT:
                        print("C", end="")
                    if c == Case.VIDE:
                        print("+", end="")
                    if c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
            print()

    def calculer_cout(self, t: Terrain) -> float:
        cout = 0
        for _ in self.arcs:
            cout += 1.5
        for n in self.noeuds.values():
            if t[n[0]][n[1]] == Case.OBSTACLE:
                cout += 2
            else:
                cout += 1
        return cout
