import unittest
import xmlrunner

from Terrain import Terrain, Case

class TestTerrain(unittest.TestCase):

    def test_chargement(self):
        # TODO
        t = Terrain()
        # On crée un fichier temporaire de description de terrain
        nom_fichier = "terrain_test.txt"
        contenu = "E~~\nCCC\n"
        with open(nom_fichier, "w") as f:
            f.write(contenu)

        # Chargement du fichier
        t.charger(nom_fichier)

        attendu = [
            [Case.ENTREE, Case.VIDE, Case.VIDE],
            [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t.cases, attendu)

    def test_accesseur(self):
        t = Terrain()
        t.cases = [
                [Case.ENTREE, Case.VIDE, Case.VIDE],
                [Case.CLIENT, Case.CLIENT, Case.CLIENT],
        ]
        self.assertEqual(t[0][0], Case.ENTREE)
        self.assertEqual(t[0][1], Case.VIDE)
        self.assertEqual(t[1][2], Case.CLIENT)

if __name__ == "__main__":
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output="test-reports"))
