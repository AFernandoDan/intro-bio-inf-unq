import unittest

from intro_biologia import Aminoacido, GrupoQuimico, Proteina


class TestGrupoQuimico(unittest.TestCase):
    def test_grupo_quimico_enum(self):
        self.assertEqual(GrupoQuimico.NO_POLAR.value, "No polar")
        self.assertEqual(GrupoQuimico.POLAR_NEUTRO.name, "POLAR_NEUTRO")
        self.assertIs(Aminoacido.glicina().grupo, GrupoQuimico.NO_POLAR)


class TestAminoacido(unittest.TestCase):
    def test_aminoacido_repr(self):
        self.assertEqual(repr(Aminoacido.glicina()), "Gli")
        self.assertEqual(repr(Aminoacido.acido_glutamico()), "Áci")


class TestProteina(unittest.TestCase):
    def test_proteina_mostrar_estructura_primaria(self):
        proteina = Proteina("Prueba", [
            Aminoacido.metionina(),
            Aminoacido.alanina(),
            Aminoacido.cisteina(),
            Aminoacido.lisina(),
        ])
        self.assertEqual(
            proteina.mostrar_estructura_primaria(),
            "NH2-Met-Ala-Cis-Lis-COOH",
        )

    def test_proteina_calcular_masa_total(self):
        proteina = Proteina("Prueba", [
            Aminoacido.glicina(),
            Aminoacido.alanina(),
            Aminoacido.valina(),
        ])
        masa_esperada = 75.07 + 89.09 + 117.15 - 2 * 18.01
        self.assertAlmostEqual(proteina.calcular_masa_total(), masa_esperada, places=6)

    def test_proteina_repr(self):
        proteina = Proteina("MiProteina", [Aminoacido.glicina()])
        self.assertEqual(repr(proteina), "Proteina(MiProteina, n=1, secuencia='G')")

    def test_proteina_sin_secuencia_levanta_error(self):
        with self.assertRaises(ValueError):
            Proteina("Vacía", [])


if __name__ == "__main__":
    unittest.main()
