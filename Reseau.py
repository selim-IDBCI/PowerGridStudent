from Terrain import Terrain, Case
from StrategieReseau import StrategieReseau, StrategieReseauAuto

class Reseau:
    def __init__(self):
        self.strat = StrategieReseauAuto()
        self.noeuds = {}          # {id_noeud: (ligne, colonne)}
        self.arcs = []            # [(n1, n2)]
        self.noeud_entree = -1    # identifiant du noeud d’entrée

    def definir_entree(self, n: int) -> None:
        """Définit le noeud d’entrée du réseau si l’id existe."""
        if n in self.noeuds.keys():
            self.noeud_entree = n
        else:
            self.noeud_entree = -1

    def ajouter_noeud(self, n: int, coords: tuple[int, int]):
        """Ajoute un noeud au réseau avec ses coordonnées."""
        if n >= 0 and isinstance(coords, tuple) and len(coords) == 2:
            self.noeuds[n] = coords

    def ajouter_arc(self, n1: int, n2: int) -> None:
        """Ajoute un arc entre deux noeuds existants s’il n’existe pas déjà."""
        if n1 > n2:
            n1, n2 = n2, n1
        if n1 not in self.noeuds.keys() or n2 not in self.noeuds.keys():
            return
        if (n1, n2) not in self.arcs:
            self.arcs.append((n1, n2))

    def set_strategie(self, strat: StrategieReseau):
        self.strat = strat

    # --------------------------------------------------------------------
    # TODO 1 : Validation du réseau
    # --------------------------------------------------------------------
    def valider_reseau(self) -> bool:
        """
        Vérifie que :
        - Un noeud d’entrée est défini
        - Tous les arcs relient des noeuds existants
        - Aucun doublon d’arcs
        - Le réseau est connexe à partir du noeud d’entrée
        """
        if self.noeud_entree == -1 or self.noeud_entree not in self.noeuds:
            return False

        # Vérifie que tous les arcs sont valides
        for (n1, n2) in self.arcs:
            if n1 not in self.noeuds or n2 not in self.noeuds:
                return False

        # Vérifie la connectivité du réseau (BFS ou DFS)
        visited = set()
        a_visiter = [self.noeud_entree]
        while a_visiter:
            n = a_visiter.pop()
            if n not in visited:
                visited.add(n)
                voisins = [b for (a, b) in self.arcs if a == n] + [a for (a, b) in self.arcs if b == n]
                a_visiter.extend(voisins)

        return len(visited) == len(self.noeuds)

    # --------------------------------------------------------------------
    # TODO 2 : Validation de la distribution sur un terrain
    # --------------------------------------------------------------------
    def valider_distribution(self, t: Terrain) -> bool:
        """
        Vérifie que tous les clients du terrain sont couverts par un noeud du réseau.
        Un client est considéré couvert si un noeud se trouve sur sa case.
        """
        for i, ligne in enumerate(t.cases):
            for j, case in enumerate(ligne):
                if case == Case.CLIENT:
                    if (i, j) not in self.noeuds.values():
                        return False
        return True

    def configurer(self, t: Terrain):
        """Configure le réseau selon la stratégie définie."""
        self.noeud_entree, self.noeuds, self.arcs = self.strat.configurer(t)

    # --------------------------------------------------------------------
    # TODO 3 : Affichage simple du réseau
    # --------------------------------------------------------------------
    def afficher(self) -> None:
        """Affiche les noeuds et arcs dans le terminal."""
        print("=== Réseau ===")
        if not self.noeuds:
            print("Aucun noeud défini.")
            return
        print(f"Noeud d’entrée : {self.noeud_entree}")
        print("Noeuds :")
        for n, coords in self.noeuds.items():
            print(f"  - {n} : {coords}")
        print("Arcs :")
        for a in self.arcs:
            print(f"  - {a[0]} <-> {a[1]}")
        print("================")

    def afficher_avec_terrain(self, t: Terrain) -> None:
        for ligne, l in enumerate(t.cases):
            for colonne, c in enumerate(l):
                if (ligne, colonne) not in self.noeuds.values():
                    if c == Case.OBSTACLE:
                        print("X", end="")
                    elif c == Case.CLIENT:
                        print("C", end="")
                    elif c == Case.VIDE:
                        print("~", end="")
                    elif c == Case.ENTREE:
                        print("E", end="")
                    else:
                        print(" ", end="")
                else:
                    if c == Case.OBSTACLE:
                        print("T", end="")
                    elif c == Case.CLIENT:
                        print("C", end="")
                    elif c == Case.VIDE:
                        print("+", end="")
                    elif c == Case.ENTREE:
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
