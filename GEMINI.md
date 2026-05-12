# Diretrizes do Projeto: RPG Classic

## Mandatos Absolutos
- **Testes Obrigatórios**: Toda e qualquer implementação, modificação ou refatoração no código DEVE ser seguida pela execução da suíte de testes (`pytest tests/`).
- **Commits Obrigatórios**: Após a implementação de uma funcionalidade e a verificação bem-sucedida dos testes, o código DEVE ser comitado imediatamente para garantir o histórico de progresso.
- **Validação Antecipada**: Se uma nova funcionalidade for adicionada, um novo teste unitário ou de integração deve ser criado ANTES ou DURANTE a implementação (TDD).
- **Integridade de Regressão**: Nunca considerar uma tarefa concluída sem confirmar que o contador de testes passou 100% com as novas mudanças.

## Convenções de Código
- Seguir a arquitetura de Cenas (Scene-based).
- Priorizar a composição sobre a herança.
- Manter o `GameContext` como a única fonte de verdade para o estado global.
