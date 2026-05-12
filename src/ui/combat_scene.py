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
        self.main_options = ["Attack", "Skill", "Magic", "Item", "Wait", "Flee"]
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
        from src.models.status import StatusManager

        # Check for Paralysis restriction
        is_paralyzed = StatusManager.is_paralyzed(attacker)
        if is_paralyzed and selection not in ["Item", "Wait"]:
            self.combat_manager.battle_log.append(f"{attacker.name} está paralisado e só pode usar Itens ou Esperar!")
            return

        if self.state == "MAIN":
            if selection == "Attack":
                self._execute_combat_action("Attack")
            elif selection == "Wait":
                self._execute_combat_action("Wait")
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
            self._handle_flee()
        
        # Check if battle is over
        if self.combat_manager.is_over:
            self._handle_battle_end()

    def _handle_flee(self):
        self.manager.pop()
        
        # Recuar o jogador baseado na direção que ele estava olhando
        dx, dy = 0, 0
        if self.context.player.facing_direction == "N": dy = 40
        elif self.context.player.facing_direction == "S": dy = -40
        elif self.context.player.facing_direction == "W": dx = 40
        elif self.context.player.facing_direction == "E": dx = -40
        
        # Verifica colisão para o recuo
        new_x = self.context.player.position.x + dx
        new_y = self.context.player.position.y + dy
        if self.context.world.can_move_to(self.context.player, new_x, new_y):
            self.context.player.position.x = new_x
            self.context.player.position.y = new_y
        else:
            new_x = self.context.player.position.x + (dx // 2)
            new_y = self.context.player.position.y + (dy // 2)
            if self.context.world.can_move_to(self.context.player, new_x, new_y):
                self.context.player.position.x = new_x
                self.context.player.position.y = new_y

    def _handle_battle_end(self):
        if self.combat_manager.winner == "Party":
            # Obtém e exibe recompensas do domínio
            reward_msgs = self.combat_manager.resolve_rewards()
            self.combat_manager.battle_log.extend(reward_msgs)
            
            # Limpeza do mundo (O Inimigo morre)
            tx = int(self.enemy_world_pos.x // self.context.world.tile_size)
            ty = int(self.enemy_world_pos.y // self.context.world.tile_size)
            self.context.world.remove_interactable(tx, ty)
        
        elif self.combat_manager.winner == "Enemies":
            print("Game Over!")
            # Reset simples (Teleporte para o início e cura)
            self.context.player.hp = self.context.player.max_hp
            self.context.player.position.x, self.context.player.position.y = 64, 64

        # Volta para o mapa
        self.manager.pop()

    def update(self, dt):
        if self.combat_manager.is_over:
            return

        ready_entity = self.combat_manager.update(dt)
        
        if ready_entity and ready_entity in self.combat_manager.enemies:
            # Domain handles AI and paralysis check
            self.combat_manager.handle_enemy_turn(ready_entity)
            
            # Check if enemy action ended the battle (Player death)
            if self.combat_manager.is_over:
                self._handle_battle_end()

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
