import unittest
import xmlrunner
from Reseau import Reseau
from Terrain import Terrain, Case


class TestReseau(unittest.TestCase):

    def test_definition_entree(self):
        r = Reseau()
        r.ajouter_noeud(0, (0, 0))
        r.definir_entree(0)
        self.assertEqual(r.noeud_entree, 0)

    def test_ajout_noeud(self):
        # TODO
        r = Reseau()
        noeuds_t = {
            0: (0, 0),
            1: (1, 2),
            2: (3, 4),
            3: (5, 5),
        }
        for indx, coords in noeuds_t.items():
            r.ajouter_noeud(indx, coords)

        self.assertTrue(len(r.noeuds) == len(noeuds_t))

    def test_ajout_arc(self):
        r = Reseau()
        r.ajouter_noeud(0, (0, 0))
        r.ajouter_noeud(1, (1, 1))
        r.ajouter_arc(0, 1)
        self.assertIn((0, 1), r.arcs)

    def test_validation_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        self.assertTrue(r.valider_reseau())

    def test_validation_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)

        self.assertFalse(r.valider_reseau())

    def test_distribution_correcte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
            [Case.ENTREE, Case.VIDE, Case.VIDE],
            [Case.CLIENT, Case.VIDE, Case.CLIENT],
        ]

        self.assertTrue(r.valider_distribution(t))

    def test_distribution_incorrecte(self):
        r = Reseau()
        r.noeuds[0] = (0, 0)
        r.noeud_entree = 0

        r.noeuds[1] = (1, 0)
        r.arcs.append((0, 1))

        r.noeuds[2] = (0, 1)
        r.arcs.append((0, 2))

        r.noeuds[3] = (0, 2)
        r.arcs.append((2, 3))

        r.noeuds[4] = (1, 2)
        r.arcs.append((3, 4))

        t = Terrain()
        t.cases = [
            [Case.ENTREE, Case.VIDE, Case.VIDE],
            [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]

        self.assertFalse(r.valider_distribution(t))


if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
