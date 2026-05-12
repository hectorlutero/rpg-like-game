import unittest

# Vamos criar esta classe a seguir
from src.models.interaction import SelectionManager

class TestNavigation(unittest.TestCase):
    def setUp(self):
        self.options = ["Attack", "Skill", "Item", "Flee"]
        self.selector = SelectionManager(self.options)

    def test_initial_selection(self):
        self.assertEqual(self.selector.index, 0)
        self.assertEqual(self.selector.current_item, "Attack")

    def test_navigate_forward(self):
        self.selector.next()
        self.assertEqual(self.selector.index, 1)
        self.assertEqual(self.selector.current_item, "Skill")

    def test_wrap_forward(self):
        # Vai até o fim e volta pro zero
        for _ in range(4):
            self.selector.next()
        self.assertEqual(self.selector.index, 0)

    def test_navigate_backward(self):
        # De 0 volta para o último (Flee)
        self.selector.prev()
        self.assertEqual(self.selector.index, 3)
        self.assertEqual(self.selector.current_item, "Flee")

    def test_update_options(self):
        # Se os itens mudarem (ex: abrir submenu de magias)
        new_options = ["Fire", "Ice"]
        self.selector.set_options(new_options)
        self.assertEqual(self.selector.index, 0)
        self.assertEqual(self.selector.current_item, "Fire")

if __name__ == "__main__":
    unittest.main()
