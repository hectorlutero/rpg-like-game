## Problem Statement

Atualmente, o desenvolvimento de novos conteúdos (mapas, quests, assets visuais, áudio, itens e balanceamento) para o RPG Classic é um processo manual, descentralizado e altamente técnico. Exige a edição direta de dezenas de arquivos JSON complexos, dificultando a manutenção da direção de arte, do balanceamento do jogo e a velocidade de iteração.

## Solution

Criar o **The Forge**, uma suíte de desenvolvimento 'Twin-Engine' em Electron/React que atua como o estúdio oficial do jogo. O Forge será desenvolvido em duas grandes Fases (Phases). A **Phase 1 (Forge Core)** entregará ferramentas visuais robustas para todos os domínios da engine (Mapas, Narrativa, Áudio, Balanceamento, etc.), conectadas via Live-Sync (Hotlink) com o jogo. A **Phase 2 (Forge AI Orchestration)** transformará o estúdio em um orquestrador de inteligência artificial, utilizando a estrutura da Phase 1 como contexto para gerar prompts, exportar Agent Skills e integrar APIs para automação do desenvolvimento seguindo o fluxo natural de criação de um RPG.

## User Stories

### Phase 1: Forge Core (Ferramentas Manuais & Infraestrutura)

**Infraestrutura & Live-Sync**
1. Como desenvolvedor, quero que o Dash abra a Engine Pygame simultaneamente, para testar as mudanças em tempo real (Twin-Engine).
2. Como desenvolvedor, quero que a Engine Pygame detecte e aplique mudanças nos arquivos JSON instantaneamente (Hotlink), evitando reinicializações.

**Design de Mapas (The Architect)**
3. Como level designer, quero pintar texturas de chão em um grid, para definir a base do cenário visualmente.
4. Como level designer, quero 'carimbar' Props (árvores, móveis) sobre o mapa, configurando Y-Sorting e colisões com cliques, sem tocar no JSON.

**Narrativa & Quests (The Storyteller)**
5. Como escritor, quero criar Quests usando Grafos de Nós (Macro), para organizar ramificações e dependências da história.
6. Como escritor, quero detalhar cutscenes em uma Timeline (Micro), controlando movimentos, falas e esperas.

**Gestão de Áudio (The Maestro)**
7. Como sound designer, quero definir zonas de áudio em mapas, para que o jogo altere sons de fundo e aplique efeitos dinamicamente por contexto.
8. Como sound designer, quero vincular sons específicos a interações e materiais (ex: passos na grama), diretamente pela interface.

**Balanceamento & Sistemas (The Tactician & The Merchant)**
9. Como game designer, quero criar itens e equipamentos definindo seus efeitos (buffs temporários, restrições) através de uma interface de formulário.
10. Como game designer, quero gerenciar atributos de Classes, Personagens e Bestiário, e simular cenários de combate dentro do editor para testar o balanceamento.
11. Como desenvolvedor, quero um 'Theme Editor' para customizar o visual das interfaces do jogo (cores, fontes, bordas) centralizando a UI.

### Phase 2: Forge AI Orchestration (Automação & Agent Skills)

**Contexto Global & World Manifest**
12. Como diretor de arte/narrativa, quero definir o 'Tema', 'Tom' e 'História Base' do jogo em um World Manifest, para que ele sirva de contexto obrigatório para as IAs.

**Pipeline Híbrido (Manual e APIs)**
13. Como desenvolvedor, quero um 'Prompt Studio' que gere prompts otimizados baseados no World Manifest para uso manual em IAs externas (DALL-E, Midjourney, Claude).
14. Como desenvolvedor, quero fazer upload do resultado visual/JSON das IAs no Dash e ter o slicing/validação feitos automaticamente.
15. Como desenvolvedor, quero inserir chaves de API para que o Dash gere e injete assets e scripts diretamente no projeto (Full Integration).

**Agent Skills por Domínio**
16. Como desenvolvedor, quero que o Dash exporte 'Skills' específicas (DesignSkill, BeastSkill, QuestSkill) que herdam o contexto do projeto, para que eu possa usar agentes no terminal local focados em domínios específicos.

## Implementation Decisions

### Módulos Phase 1
- **Twin-Process Bridge:** Comunicação WebSockets/File Watcher entre React e Pygame.
- **Canvas Map Renderer:** Editor de mapas 2D visual compatível com Tile + Prop Y-Sorting.
- **Node/Timeline Editors:** Gerenciamento visual que serializa para os esquemas de json do diretor.
- **Form-based System Editors:** UIs tipadas para gerenciar Bestiário, Classes e Itens.

### Módulos Phase 2
- **World Manifest Context Store:** Repositório global de lore e design guidelines.
- **Prompt Generator Engine:** Sistema que combina metadados de domínio (ex: stats de um monstro) com o Manifest para gerar diretrizes de IA.
- **Skill Exporter:** Gerador de arquivos .md no padrão Matt Pocock/Gemini CLI para agentes externos.

## Testing Decisions
- **Data Integrity:** Validação rigorosa dos JSONs gerados pelo Dash contra os esquemas esperados pela Pygame Engine.
- **UX Tests:** Garantir que ferramentas core (Node Editor, Map Painter) sejam fluidas.
- **Live-Sync Tests:** Validar a resiliência da Engine ao receber atualizações dinâmicas massivas via WebSocket/Watcher.

## Out of Scope
- Renderização 3D.
- Execução de LLMs locais dentro do Electron (dependência de APIs externas ou prompts manuais).
- Multiplayer co-op de edição.

## Road Map de Milestones

### Phase 1: The Studio (Edição Visual)
- **Milestone 7: The Forge Foundation** (Infra Twin-Engine, Hotlink e Manifest Base).
- **Milestone 8: The Architect & Storyteller** (Mapas Visuais, Quest Nodes e Timeline JSON).
- **Milestone 9: The Maestro & Styler** (Áudio Contextual, Zonas de Som e Customização de UI).
- **Milestone 10: The Tactician & Merchant** (Classes, Bestiário, Itens e Simulador de Balanceamento).

### Phase 2: AI Orchestration (A Fábrica)
- **Milestone 11: The World Manifest & Prompts** (Integração do Lore/Design System com geradores de prompts).
- **Milestone 12: Skill Exporter & Agents** (Criação de Agent Skills focadas por domínio: BeastSkill, QuestSkill, etc).
- **Milestone 13: Native API Integration** (Geração de assets direta via providers conectados).