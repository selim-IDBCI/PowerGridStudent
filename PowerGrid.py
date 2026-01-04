
from Terrain import Terrain
from Reseau import Reseau

from StrategieReseau import StrategieReseauManuelle

if __name__ == "__main__":

    reseau = Reseau()

    terrain = Terrain()
    terrain.charger("terrains/t3.txt")
    print("Terrain chargé :")
    terrain.afficher()

    print("======= Configuration Automatique")
    reseau.configurer(terrain)
    if reseau.valider_reseau() and reseau.valider_distribution(terrain):
        print("Configuration valide simple trouvée")
        print("Cout : {}M€".format(reseau.calculer_cout(terrain)))
        reseau.afficher_avec_terrain(terrain)
    else:
        print("Pas de configuration valide trouvée. ")

    print("======= Configuration Manuelle")
    print(f"L'entrée du terrain se situe aux coordonnées {terrain.get_entree()}")
    reseau.set_strategie(StrategieReseauManuelle())
    reseau.configurer(terrain)
    if reseau.valider_reseau() and reseau.valider_distribution(terrain):
        print("Configuration valide optimale trouvée")
        print("Cout : {}M€".format(reseau.calculer_cout(terrain)))
        reseau.afficher_avec_terrain(terrain)
    else:
        print("Pas de configuration valide optimale trouvée.")
