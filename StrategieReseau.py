
from Terrain import Terrain, Case

class StrategieReseau:
    def configurer(
        self, t: Terrain
    ) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []


class StrategieReseauManuelle(StrategieReseau):
    def configurer(
        self, t: Terrain
    ) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
      
        
        from StrategieReseau import StrategieReseauAuto  

        auto = StrategieReseauAuto()
        noeud_entree, noeuds, arcs = auto.configurer(t)

        if not noeuds:
            print("Aucun noeud disponible sur ce terrain.")
            return -1, {}, []
        print("Configuration automatique de base créée.")
        print("Liste des noeuds disponibles :")
        for nid, (x, y) in noeuds.items():
            print(f"  {nid}: ({x}, {y})")

        while True:
            saisie = input(
                f"Entrez l'identifiant du noeud d'entrée "
                f"(laisser vide pour {noeud_entree}) : "
            ).strip()
            if saisie == "":
               
                break
            try:
                choix = int(saisie)
            except ValueError:
                print("Veuillez entrer un entier valide.")
                continue
            if choix not in noeuds:
                print("Identifiant de noeud inconnu, réessayez.")
                continue
            noeud_entree = choix
            break

     
        return noeud_entree, noeuds, arcs

       


class StrategieReseauAuto(StrategieReseau):
    def configurer(
        self, t: Terrain
    ) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        

        noeuds: Dict[int, Tuple[int, int]] = {}
        arcs: List[Tuple[int, int]] = []
        id_par_coord: Dict[Tuple[int, int], int] = {}

        
        if hasattr(t, "largeur") and hasattr(t, "hauteur") and hasattr(t, "get_case"):
            largeur = getattr(t, "largeur")
            hauteur = getattr(t, "hauteur")
            get_case = getattr(t, "get_case")

            for y in range(hauteur):
                for x in range(largeur):
                    case: Case = get_case(x, y)

                    constructible = True
                    if hasattr(case, "constructible"):
                        constructible = getattr(case, "constructible")
                    elif hasattr(case, "est_constructible"):
                        constructible = case.est_constructible()

                    if not constructible:
                        continue

                    node_id = len(noeuds)
                    coord = (x, y)
                    noeuds[node_id] = coord
                    id_par_coord[coord] = node_id

         
            voisins = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for (x, y), nid in id_par_coord.items():
                for dx, dy in voisins:
                    c2 = (x + dx, y + dy)
                    nid2 = id_par_coord.get(c2)
                    if nid2 is not None:
                        arcs.append((nid, nid2))

        else:
           
            for case in t:  # type: ignore
                x = getattr(case, "x", None)
                y = getattr(case, "y", None)
                if x is None or y is None:
                    continue

                constructible = True
                if hasattr(case, "constructible"):
                    constructible = getattr(case, "constructible")
                elif hasattr(case, "est_constructible"):
                    constructible = case.est_constructible()  

                if not constructible:
                    continue

                node_id = len(noeuds)
                coord = (int(x), int(y))
                noeuds[node_id] = coord
                id_par_coord[coord] = node_id


            ids = list(noeuds.items())
            for i in range(len(ids)):
                id1, (x1, y1) = ids[i]
                for j in range(i + 1, len(ids)):
                    id2, (x2, y2) = ids[j]
                    if abs(x1 - x2) + abs(y1 - y2) == 1:
                        arcs.append((id1, id2))

        if noeuds:
            noeud_entree = min(noeuds.keys())
        else:
            noeud_entree = -1

        return noeud_entree, noeuds, arcs

        return -1, {}, []  