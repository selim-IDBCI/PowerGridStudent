
from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}
        self.arcs = []

        self.noeud_entree = -1

    def definir_entree(self, n: int) -> None:
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        if n >= 0:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
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

    def valider_reseau(self) -> bool:
        if not self.noeuds:
            return False
        if self.noeud_entree is None or self.noeud_entree not in self.noeuds:
            return False
        adj = self._adjacence()
        if not adj:
            return False
        a_visiter = [self.noeud_entree]
        visites = set()

        while a_visiter:
            n = a_visiter.pop()
            if n in visites:
                continue
            visites.add(n)
            a_visiter.extend(adj[n] - visites)
        return len(visites) == len(self.noeuds)

        

    def valider_distribution(self, t: Terrain) -> bool:
       if not self.valider_reseau():
            return False
       adj = self._adjacence()
       a_visiter = [self.noeud_entree]
       atteignables = set()
       while a_visiter:
            n = a_visiter.pop()
            if n in atteignables:
                continue
            atteignables.add(n)
            a_visiter.extend(adj[n] - atteignables)
       coord_to_nodes = {}
       for ident, coord in self.noeuds.items():
            coord_to_nodes.setdefault(coord, set()).add(ident)
       for lig, ligne in enumerate(t.cases):
            for col, case in enumerate(ligne):
                if case is Case.CLIENT:
                    coord = (lig, col)
                    ids = coord_to_nodes.get(coord, set())
                    if not ids or not (ids & atteignables):
                        return False

       return True



        

    def configurer(self, t: Terrain):
        self.noeud_entree, self.noeuds, self.arcs  = self.strat.configurer(t)

    def afficher(self) -> None:
        print("Réseau électrique ")
        print(f"Noeud d'entrée : {self.noeud_entree}")
        print("Noeuds (id -> (ligne, colonne)) :")
        for ident, coord in sorted(self.noeuds.items()):
            print(f"  {ident} -> {coord}")

        print("Arcs :")
        for n1, n2 in self.arcs:
            print(f"  {n1} <-> {n2}")
    
        pass

    def afficher_avec_terrain(self, t: Terrain) -> None:
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

