import unittest
from src.models.character import Character
from src.models.classes import Warrior, Rogue
from src.models.atb import ATBEngine

class TestATBEngine(unittest.TestCase):
    def test_meter_fills_after_tick(self):
        hero = Character("Guerreiro", Warrior())
        engine = ATBEngine()
        engine.add_combatant(hero)
        self.assertEqual(engine.get_meter(hero), 0)
        engine.tick(delta_time=1.0)
        self.assertGreater(engine.get_meter(hero), 0)

    def test_rogue_fills_faster_than_warrior(self):
        warrior = Character("Warrior", Warrior())
        rogue = Character("Rogue", Rogue())
        engine = ATBEngine()
        engine.add_combatant(warrior)
        engine.add_combatant(rogue)
        engine.tick(delta_time=1.0)
        self.assertGreater(engine.get_meter(rogue), engine.get_meter(warrior))

    def test_ready_at_100(self):
        hero = Character("Speedy", Rogue())
        engine = ATBEngine()
        engine.add_combatant(hero)
        while engine.get_meter(hero) < 100:
            engine.tick(delta_time=1.0)
        self.assertTrue(engine.is_ready(hero))
        self.assertIn(hero, engine.get_ready_combatants())

    def test_reset_meter_after_action(self):
        hero = Character("ActionHero", Warrior())
        engine = ATBEngine()
        engine.add_combatant(hero)
        while not engine.is_ready(hero):
            engine.tick(1.0)
        engine.reset_meter(hero)
        self.assertEqual(engine.get_meter(hero), 0)
        self.assertFalse(engine.is_ready(hero))

if __name__ == '__main__':
    unittest.main()
