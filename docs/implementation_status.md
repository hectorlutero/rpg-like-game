# Status da Implementação - Maio de 2026

## 🟢 Concluído e Estável (Core Engine)

### 1. Sistema de Mundo e Transições
- **Portal & Portals**: Sistema bidirecional de mapas com *fades* e salvamento automático.
- **WorldOrchestrator**: Gerenciamento robusto de carregamento de JSON e posicionamento por tags.

### 2. Motor de Missões (Deep Quest Engine)
- **Estrutura**: Suporte a objetivos contáveis (ex: "Mate 5 Slimes") e baseados em eventos.
- **Ações**: Recompensas automáticas de XP, Ouro e Itens sem necessidade de scripts manuais.
- **Quest Log**: Aba integrada no menu principal para acompanhamento de progresso.

### 3. IA e Navegação
- **Pathfinding**: Implementação de A* funcional para busca de caminhos na grade.
- **Comportamentos**: *Wander* (aleatório), *Pursuit* (perseguição) e *Leashing* (limite de área).
- **LoS**: Sistema de linha de visão (*Raycasting*) para detecção de jogador.

### 4. Áudio e "Juice"
- **SoundManager**: Mixagem de BGM, SFX e Ambientes com mapeamento por ID.
- **JuiceService**: Screen shake baseado em trauma, flashes de impacto e *hit-stop*.

### 5. Economia e Equipamento
- **Loja**: Cenas de compra e venda com taxas configuráveis.
- **Equipamento**: Sistema de proficiência por classe e bônus de atributos complexos.

## 🟡 Em Desenvolvimento / Pendente (Conteúdo & Polimento)

### 1. Narrativa (Main Quest)
- [ ] Criar a sequência completa de quests da "Vila Inicial" até a "Caverna do Chefe".
- [ ] Implementar diálogos ramificados que afetam o estado global.

### 2. Assets Visuais
- [ ] Substituir formas geométricas por sprites/tilesets básicos de pixel art.
- [ ] Adicionar animações de partículas simples para magias e efeitos de status.

### 3. Balanceamento e Bosses
- [ ] Criar IA de Chefe com múltiplas fases de ataque.
- [ ] Refinar curvas de XP e preços da loja.
