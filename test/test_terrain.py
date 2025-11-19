import unittest
import xmlrunner

from Terrain import Terrain, Case

class TestTerrain(unittest.TestCase):

    def test_chargement(self):
        t = Terrain("../terrains/t1.txt")

        # Vérifier que l’entrée est bien trouvée
        self.assertEqual(t.source, (0, 0))

        # Vérifier que les clients sont bien trouvés
        self.assertIn((1, 0), t.clients)
        self.assertIn((1, 2), t.clients)
        self.assertIn((2, 1), t.clients)

        # Vérifier qu’un obstacle est bien trouvé
        self.assertIn((1, 1), t.obstacles)

        # Vérifier que la grille est bien remplie
        self.assertEqual(t.grid[0][0], "E")
        self.assertEqual(t.grid[1][1], "X")

    def test_accesseur(self):
        t = Terrain.__new__(Terrain)  # créer un objet sans appeler __init__
        t.cases = [
            [Case.ENTREE, Case.VIDE, Case.VIDE],
            [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t[0][0], Case.ENTREE)
        self.assertEqual(t[0][1], Case.VIDE)
        self.assertEqual(t[1][2], Case.CLIENT)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
