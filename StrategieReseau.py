from Terrain import Terrain, Case
from functools import reduce


class StrategieReseau:
    def configurer(
        self, t: Terrain
    ) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        return -1, {}, []


# implémentation de la fonction qui gère la configuration manuelle d'un réseau à partir d'un terrain. L'utilisateur doit avoir l'occasion
# d'entrer les informations de la nouvelle configuration. Vous pouvez, par exemple, implémenter une fonction qui, dans une boucle, affiche
# le réseau et le terrain puis demande à l'utilisateur d'ajouter un noeud à un endroit du terrain. L'utilisateur devrait alors spécifier
# quels liaisons seront générées entre ce nouveau noeud et les noeuds voisins existants
class StrategieReseauManuelle(StrategieReseau):
    def configurer(
        self, t: Terrain
    ) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:

        counter = 0
        nodes = {}
        arcs = []
        while True:
            print("Réseau actuel :")
            t.afficher()
            if counter == 0:
                entry = int(input("Entrez l'ID' de l'entrée : "))
                print(f"Entrée définie {entry})")
            else:
                cmd = input(
                    "Entrez une commande (1 : ajouter_noeud, 2 : ajouter_arc ou 3 : quitter) : "
                )
                if cmd == "1" or cmd == "ajouter_noeud":
                    n = int(input("Entrez l'ID du noeud : "))
                    x = int(input("Entrez la coordonnée x du noeud : "))
                    y = int(input("Entrez la coordonnée y du noeud : "))
                    nodes[n] = (x, y)
                    print(f"Noeud {n} ajouté en ({x}, {y})")
                elif cmd == "2" or cmd == "ajouter_arc":
                    n1 = int(input("Entrez l'ID du premier noeud : "))
                    n2 = int(input("Entrez l'ID du second noeud : "))
                    arcs.append((n1, n2))
                    print(f"Arc ajouté entre {n1} et {n2}")
                elif cmd == "3" or cmd == "quitter":
                    break
            counter += 1
        return entry, nodes, arcs


type ID = int

type Cable = tuple[ID, ID]
"The smallest ID must always be on the left of the tuple"

type Coords = tuple[int, int]
"row index then column index (y then x)"

class StrategieReseauAuto(StrategieReseau):
    def configurer(self, t: Terrain) -> tuple[int, dict[int, tuple[int, int]], list[tuple[int, int]]]:
        def coords_to_id(coords: Coords) -> ID:
            i, j = coords
            assert j < t.largeur, "Coordinates must remain within the bounds of the terrain"
            return i * t.largeur + j


        def id_to_coords(id: ID) -> Coords:
            assert id < t.largeur * t.hauteur, "IDs must remain within the bounds of the terrain"
            return divmod(id, t.largeur)


        def get_neighbours_ids(id: ID) -> set[ID]:
            ci, cj = id_to_coords(id)
            out: set[int] = set()

            for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                j = cj + dj
                i = ci + di

                if 0 <= j < t.largeur and 0 <= i < t.hauteur:
                    id = coords_to_id((i, j))

                    # Ignore if this is an obstacle
                    if t[i][j] != Case.OBSTACLE:
                        out.add(id)

            return out


        entry_id: int = coords_to_id(t.get_entree())


        def compute_cheapest_layout(previous_layout: set[Cable], client_id: ID) -> set[Cable]:
            """
            Computes the cheapest addition to the layout `previous_layout` needed to link the two
            clients with IDs `entry_id` and `client_id`.

            Uses Dijkstra's algorithm under the hood.
            """

            visited: dict[ID, tuple[ID | None, int]] = {entry_id: (None, 0)}
            "{id: (previous_id, cost)}"

            ids_to_visit: list[int] = [entry_id]

            while len(ids_to_visit) > 0:
                current_id = ids_to_visit.pop()
                neighbours_ids = get_neighbours_ids(current_id)
                for id in neighbours_ids:
                    if id not in visited:
                        ids_to_visit.insert(0, id)

                for neighbour_id in neighbours_ids:
                    cost: int = visited[current_id][1] + 1

                    # We prioritize cables that are already laid
                    l, r = sorted((current_id, neighbour_id))
                    if (l, r) in previous_layout:
                        cost -= 1

                    if neighbour_id not in visited or cost < visited[neighbour_id][1]:
                        visited[neighbour_id] = (current_id, cost)

            new_layout: set[Cable] = set()
            current_id = client_id
            while current_id != entry_id:
                previous_id = visited[current_id][0]
                assert previous_id != None, "Only the entry node should have no previous node"

                l, r = sorted((current_id, previous_id))
                new_layout.add((l, r))

                current_id = previous_id

            return new_layout.union(previous_layout)

        clients_to_link: set[ID] = set(map(coords_to_id, t.get_clients()))

        # The smaller id must always be on the left of the tuple
        final_layout: set[tuple[int, int]] = set()

        while len(clients_to_link) > 0:
            clients_iter = iter(clients_to_link)
            # This will always work because `clients_to_connect` isn't empty
            closest_client: ID = clients_iter.__next__()
            cheapest_layout: set[Cable] = compute_cheapest_layout(final_layout, closest_client)

            for client in clients_iter:
                current_path: set[Cable] = compute_cheapest_layout(final_layout, client)
                if len(current_path) < len(cheapest_layout):
                    closest_client = client
                    cheapest_layout = current_path

            clients_to_link.remove(closest_client)
            final_layout = cheapest_layout

        used_ids = set(id for cable in final_layout for id in cable)
        ids_mapping: dict[int, tuple[int, int]] = { id: id_to_coords(id) for id in used_ids }

        return entry_id, ids_mapping, list(final_layout)
