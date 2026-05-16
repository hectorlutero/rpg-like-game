import pygame
from src.ui.scenes import Scene
from src.ui.combat_ui import CombatUI
from src.models.world import Position
from src.models.interaction import SelectionManager
from src.core.juice import JuiceService
from src.core.particles import ParticleManager

class CombatScene(Scene):
    def __init__(self, manager, combat_manager, enemy_world_pos):
        self.manager = manager
        self.context = manager.context
        self.combat_manager = combat_manager
        self.enemy_world_pos = enemy_world_pos 
        self.ui = CombatUI(self.manager.context.screen if hasattr(self.manager.context, 'screen') else None)
        self.particles = ParticleManager()
        self.juice = JuiceService(self.particles, settings_manager=self.context.settings)
        
        # Gerenciador de Navegação do Combate
        self.main_options = ["Attack", "Skill", "Magic", "Item", "Wait", "Flee"]
        self.selector = SelectionManager(self.main_options)
        
        # Estados: MAIN, SKILL_SELECT, MAGIC_SELECT
        self.state = "MAIN"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.combat_manager.is_waiting_for_input:
                return

            inputs = self.context.inputs
            if inputs.is_action_just_pressed(inputs.InputAction.CANCEL, event):
                if self.state != "MAIN":
                    self.state = "MAIN"
                    self.selector.set_options(self.main_options)
                return

            if inputs.is_action_just_pressed(inputs.InputAction.LEFT, event): 
                self.selector.prev()
            elif inputs.is_action_just_pressed(inputs.InputAction.RIGHT, event): 
                self.selector.next()
            elif inputs.is_action_just_pressed(inputs.InputAction.CONFIRM, event):
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
        attacker = self.combat_manager.active_entity
        target = self.combat_manager.enemies[0] # Simplificação: sempre ataca o primeiro inimigo
        
        # Determine position of target for particles
        if target in self.combat_manager.enemies:
            idx = self.combat_manager.enemies.index(target)
            tx, ty = 150, 150 + (idx * 100)
        else:
            idx = self.combat_manager.party.index(target)
            tx, ty = 600, 150 + (idx * 100)

        result = self.combat_manager.execute_action(
            attacker, 
            action_type, 
            target,
            ability_name=ability_name
        )
        
        # Trigger visual impact if it was an attack/skill and successful
        if action_type in ["Attack", "Skill", "Magic"] and result.get("success"):
            self.juice.impact(tx, ty)

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
            from src.ui.game_over_scene import GameOverScene
            self.manager.change_scene(GameOverScene(self.manager))
            return # Don't pop, we changed the whole stack

        # Volta para o mapa
        self.manager.pop()

    def update(self, dt):
        if self.combat_manager.is_over:
            return

        self.juice.update(dt)
        self.particles.update(dt)

        ready_entity = self.combat_manager.update(dt)
        
        if ready_entity and ready_entity in self.combat_manager.enemies:
            # Determine target (always party[0] for now in AI)
            target = self.combat_manager.party[0]
            idx = self.combat_manager.party.index(target)
            tx, ty = 600, 150 + (idx * 100)
            
            # Domain handles AI and paralysis check
            self.combat_manager.handle_enemy_turn(ready_entity)
            
            # Trigger impact for enemy attack
            self.juice.impact(tx, ty)
            
            # Check if enemy action ended the battle (Player death)
            if self.combat_manager.is_over:
                self._handle_battle_end()

    def draw(self, screen):
        # Limpa a tela antes de desenhar o combate para não sobrepor o mapa
        screen.fill((20, 20, 20))
        
        # Apply camera shake from juice
        shake_x, shake_y = self.juice.camera_offset
        
        # Create a surface for combat content to apply shake
        combat_surface = pygame.Surface(screen.get_size())
        combat_surface.fill((20, 20, 20))
        
        # Atualiza a tela na UI se necessário
        self.ui.screen = combat_surface
        self.ui.draw_combat_scene(self.combat_manager.party, self.combat_manager.enemies, self.combat_manager)
        self.particles.draw(combat_surface)
        self.ui.draw_battle_log(self.combat_manager.battle_log)
        if self.combat_manager.is_waiting_for_input:
            menu_title = "Menu Principal"
            if self.state == "SKILL_SELECT": menu_title = "Selecionar Skill"
            elif self.state == "MAGIC_SELECT": menu_title = "Selecionar Magia"
            
            self.ui.draw_action_menu(self.selector.options, self.selector.index, title=menu_title)

        # Draw combat surface with shake
        screen.blit(combat_surface, (int(shake_x), int(shake_y)))
        
        # Draw flash overlay
        if self.juice.flash_alpha > 0:
            flash_surf = pygame.Surface(screen.get_size())
            flash_surf.set_alpha(self.juice.flash_alpha)
            flash_surf.fill(self.juice.flash_color)
            screen.blit(flash_surf, (0, 0))
