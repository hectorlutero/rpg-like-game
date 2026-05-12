import pygame
from src.ui.scenes import Scene
from src.ui.combat_ui import CombatUI
from src.models.world import Position
from src.models.interaction import SelectionManager

class CombatScene(Scene):
    def __init__(self, manager, combat_manager, enemy_world_pos):
        self.manager = manager
        self.context = manager.context
        self.combat_manager = combat_manager
        self.enemy_world_pos = enemy_world_pos 
        self.ui = CombatUI(self.manager.context.screen if hasattr(self.manager.context, 'screen') else None)
        
        # Gerenciador de Navegação do Combate
        self.main_options = ["Attack", "Skill", "Magic", "Item", "Flee"]
        self.selector = SelectionManager(self.main_options)
        
        # Estados: MAIN, SKILL_SELECT, MAGIC_SELECT
        self.state = "MAIN"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.combat_manager.is_waiting_for_input:
                return

            if event.key == pygame.K_ESCAPE:
                if self.state != "MAIN":
                    self.state = "MAIN"
                    self.selector.set_options(self.main_options)
                return

            if event.key == pygame.K_LEFT: 
                self.selector.prev()
            elif event.key == pygame.K_RIGHT: 
                self.selector.next()
            elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self._confirm_selection()

    def _confirm_selection(self):
        selection = self.selector.current_item
        attacker = self.combat_manager.active_entity
        from src.models.skills import ABILITY_DATA

        if self.state == "MAIN":
            if selection == "Attack":
                self._execute_combat_action("Attack")
            elif selection == "Skill":
                # Entra no submenu de Skills Físicas
                skills = [name for name, abi in ABILITY_DATA.items() 
                         if abi.category == "Skill" and name in attacker.skills]
                if skills:
                    self.state = "SKILL_SELECT"
                    self.selector.set_options(skills)
                else:
                    self.combat_manager.battle_log.append(f"{attacker.name} não conhece Skills!")
            elif selection == "Magic":
                # Entra no submenu de Magias
                magics = [name for name, abi in ABILITY_DATA.items() 
                         if abi.category == "Spell" and name in attacker.skills]
                if magics:
                    self.state = "MAGIC_SELECT"
                    self.selector.set_options(magics)
                else:
                    self.combat_manager.battle_log.append(f"{attacker.name} não conhece Magias!")
            elif selection == "Flee":
                self._execute_combat_action("Flee")
            elif selection == "Item":
                self.combat_manager.battle_log.append("Inventário ainda não implementado!")

        elif self.state == "SKILL_SELECT":
            self._execute_combat_action("Skill", selection)
            self.state = "MAIN"
            self.selector.set_options(self.main_options)

        elif self.state == "MAGIC_SELECT":
            self._execute_combat_action("Magic", selection)
            self.state = "MAIN"
            self.selector.set_options(self.main_options)

    def _execute_combat_action(self, action_type, ability_name=None):
        result = self.combat_manager.execute_action(
            self.combat_manager.active_entity, 
            action_type, 
            self.combat_manager.enemies[0],
            ability_name=ability_name
        )
        
        if result.get("fled"):
            self.manager.pop()
            self.context.player.position.x -= 40
            self.context.player.position.y -= 40
        
        # Check for victory
        if all(e.hp <= 0 for e in self.combat_manager.enemies):
            # Adiciona recompensas
            msg = f"VITÓRIA! Ganhou {self.combat_manager.xp_reward} XP"
            if self.combat_manager.gold_reward > 0:
                msg += f" e {self.combat_manager.gold_reward} G"
            self.combat_manager.battle_log.append(msg)
            
            for hero in self.context.party:
                hero.gain_xp(self.combat_manager.xp_reward)
                hero.gold += self.combat_manager.gold_reward

            # Delay antes de fechar para o jogador ler o log (opcional, por enquanto fecha)
            self.manager.pop()
            tx = int(self.enemy_world_pos.x // self.context.world.tile_size)
            ty = int(self.enemy_world_pos.y // self.context.world.tile_size)
            self.context.world.remove_interactable(tx, ty)
            self.enemy_world_pos.x, self.enemy_world_pos.y = -100, -100

    def update(self, dt):
        ready_entity = self.combat_manager.update(dt)
        if ready_entity and ready_entity in self.combat_manager.enemies:
            # Enemy AI
            self.combat_manager.execute_action(ready_entity, "Attack", self.context.player)
            if self.context.player.hp <= 0:
                print("Game Over!")
                # Reset simple logic
                self.context.player.hp = self.context.player.max_hp
                self.context.player.position.x, self.context.player.position.y = 64, 64
                self.manager.pop()

    def draw(self, screen):
        # Limpa a tela antes de desenhar o combate para não sobrepor o mapa
        screen.fill((20, 20, 20))
        
        # Atualiza a tela na UI se necessário
        self.ui.screen = screen
        self.ui.draw_combat_scene(self.combat_manager.party, self.combat_manager.enemies, self.combat_manager)
        self.ui.draw_battle_log(self.combat_manager.battle_log)
        if self.combat_manager.is_waiting_for_input:
            menu_title = "Menu Principal"
            if self.state == "SKILL_SELECT": menu_title = "Selecionar Skill"
            elif self.state == "MAGIC_SELECT": menu_title = "Selecionar Magia"
            
            self.ui.draw_action_menu(self.selector.options, self.selector.index, title=menu_title)
