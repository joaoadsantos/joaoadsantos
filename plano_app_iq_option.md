# Plano de Desenvolvimento — App Python de Leitura de Gráfico em Tempo Real (IQ Option)

## 1) Objetivo funcional (MVP)
Construir um aplicativo desktop em Python que:
- Capture em tempo real uma região da tela onde está o gráfico da IQ Option.
- Extraia candles e sinais visuais suficientes para calcular EMA 3/5/7, SMA 21 e lógica inspirada no indicador YURI SNIPE OB.
- Gere um score convertido em probabilidade para **CALL** (comprar) ou **PUT** (vender).
- Quando a probabilidade for **>= 75%**:
  - toque um bip,
  - exiba popup modal com ação sugerida e percentual,
  - aguarde o usuário clicar **OK**,
  - minimize automaticamente o app para facilitar a execução manual da ordem.
- Registre cada evento em log para posterior calibração.

---

## 2) Requisitos funcionais detalhados
1. Selecionar e salvar ROI (região de interesse) do gráfico.
2. Capturar frames continuamente (150–250 ms por ciclo).
3. Detectar/estimar candles recentes e sua direção.
4. Calcular EMA3, EMA5, EMA7 e SMA21 sobre série reconstruída.
5. Traduzir a lógica YURI para Python (normalização/zona/extremos).
6. Combinar sinais em um score de decisão.
7. Converter score em probabilidade (0 a 1).
8. Aplicar threshold configurável (inicial 0.75).
9. Aplicar cooldown para evitar alertas repetidos (30–60s).
10. Emitir alerta sonoro + popup com:
    - `Ação sugerida: CALL/PUT`
    - `Probabilidade: XX%`
11. Ao clicar OK, minimizar janela principal.
12. Persistir logs com timestamp, features, score e decisão.

---

## 3) Requisitos não-funcionais
- Baixa latência (resposta perceptível em < 1s após o setup do candle/sinal).
- Robustez visual a pequenas mudanças de tema/cor do gráfico.
- Configuração sem recompilar (YAML).
- Logs auditáveis para revisão e melhoria.
- Operação local (sem depender de API da corretora).

---

## 4) Arquitetura proposta
```text
iq_signal_app/
  main.py
  config.yaml
  capture/
    screen.py
  vision/
    preprocess.py
    candles.py
  indicators/
    ma.py
    yuri.py
  engine/
    scoring.py
    probability.py
    cooldown.py
  alerts/
    sound.py
    popup.py
  ui/
    main_window.py
    roi_selector.py
  logs/
    repository.py
  data/
    events.csv
```

### Responsabilidade dos módulos
- **capture/**: captura da ROI e controle de taxa de atualização.
- **vision/**: limpeza de imagem, detecção de candles e extração de série.
- **indicators/**: EMA/SMA + versão Python da lógica YURI.
- **engine/**: cálculo de score, probabilidade e regra de disparo.
- **alerts/**: bip + popup + handshake de confirmação.
- **ui/**: monitoramento, botões de controle, seleção de ROI, minimização.
- **logs/**: persistência e exportação para análise.

---

## 5) Stack técnica recomendada
- **Captura de tela**: `mss`
- **Visão computacional**: `opencv-python`, `numpy`
- **UI**: `PySide6` (ou `tkinter` para MVP ultra-rápido)
- **Som (Windows)**: `winsound` (fallback cross-platform opcional)
- **Configuração**: `pydantic` + `pyyaml`
- **Logs**: `logging` padrão (ou `loguru`)
- **Opcional OCR**: `pytesseract` (somente se realmente necessário)

---

## 6) Modelo de sinal (fase 1 — heurístico)

### Regras-base
1. **Tendência curta**
   - EMA3 > EMA5 > EMA7 → favorece CALL
   - EMA3 < EMA5 < EMA7 → favorece PUT
2. **Filtro de tendência base**
   - Preço acima da SMA21 reforça CALL
   - Preço abaixo da SMA21 reforça PUT
3. **Zonas YURI**
   - Próximo de `extBot/sigBot` + candle de reversão → peso para CALL
   - Próximo de `extTop/sigTop` + candle de reversão → peso para PUT
4. **Confirmação de candle**
   - 2–3 candles recentes validando direção aumentam confiança.

### Exemplo de score ponderado
- Tendência curta: 35%
- Filtro SMA21: 20%
- Zona YURI: 30%
- Confirmação candle: 15%

`score_final` em [-1, +1] (negativo: PUT, positivo: CALL).

### Conversão para probabilidade
- `p_call = sigmoid(k * score_final)`
- `p_put = 1 - p_call`
- Sinal final = maior probabilidade.
- Dispara alerta apenas se `max(p_call, p_put) >= 0.75`.

> Observação: inicialmente isso é uma **confiança do modelo heurístico**, não probabilidade estatística calibrada.

---

## 7) Pipeline em tempo real
1. Captura frame.
2. Preprocessa imagem (contraste, limiar, remoção de ruído).
3. Atualiza série de candles (janela deslizante N candles).
4. Recalcula EMA/SMA + variáveis da lógica YURI.
5. Gera score e probabilidade.
6. Verifica threshold + cooldown.
7. Se válido: toca bip + popup modal.
8. Usuário clica OK.
9. App minimiza.
10. Evento registrado no log.

---

## 8) Roadmap por etapas

### Etapa A — Base (1–2 dias)
- Projeto inicial, config, logging.
- Captura da ROI estável + preview.
- Controle start/stop.

**Entregável:** app captura em loop com FPS aceitável (4–8+ FPS).

### Etapa B — Leitura do gráfico (2–4 dias)
- Preprocessamento robusto.
- Detecção de corpo/pavio (ou aproximação).
- Série OHLC aproximada por candle.

**Entregável:** reconstrução consistente visualmente.

### Etapa C — Indicadores (2–3 dias)
- EMA 3/5/7 e SMA 21.
- Implementação Python da lógica YURI SNIPE OB adaptada.
- Testes unitários com séries sintéticas.

**Entregável:** indicadores batendo com expectativa teórica.

### Etapa D — Engine de probabilidade (2–3 dias)
- Score inicial ponderado.
- Sigmoid/calibração inicial.
- Cooldown, debounce e bloqueio de alertas duplicados.

**Entregável:** geração de CALL/PUT + probabilidade.

### Etapa E — Alertas e UX (1–2 dias)
- Bip customizável.
- Popup modal com ação/probabilidade.
- Botão OK minimiza app automaticamente.

**Entregável:** fluxo completo de execução manual.

### Etapa F — Calibração contínua (contínuo)
- Registrar resultado real pós-sinal (win/loss manual).
- Reestimar pesos/threshold periodicamente.
- Medir precisão por período e ativo.

**Entregável:** melhoria progressiva de assertividade.

---

## 9) Formato de logs recomendado
Campos mínimos por evento:
- `timestamp`
- `asset` (se disponível)
- `timeframe`
- `ema3`, `ema5`, `ema7`, `sma21`
- `yuri_zone_state`
- `score`
- `prob_call`, `prob_put`
- `signal` (CALL/PUT/NONE)
- `triggered` (bool)
- `cooldown_active` (bool)
- `user_ack_time`
- `manual_result` (win/loss/skip)

Isso habilita backtest aproximado e calibração futura.

---

## 10) Riscos e mitigação
1. **Ruído visual / mudanças de layout**
   - Mitigar com ROI fixa e calibração de cor/tema.
2. **Detecção imperfeita de candles**
   - Começar com abordagem aproximada + validação visual.
3. **Falso “75%” sem base estatística**
   - Tratar como score inicial e calibrar com dados reais.
4. **Excesso de alertas**
   - Cooldown + confirmação por múltiplas regras.

---

## 11) Critérios de aceite do MVP
- App consegue capturar ROI continuamente sem travar.
- Consegue calcular EMA3/5/7 + SMA21 em tempo real.
- Gera sugestão CALL/PUT com probabilidade.
- Só alerta quando >= threshold definido.
- Popup + OK + minimização funcionando.
- Log completo salvo por evento.

---

## 12) Próximos passos imediatos (execução prática)
1. Criar esqueleto do projeto e `config.yaml`.
2. Implementar `capture/screen.py` + seletor de ROI.
3. Implementar pipeline mínimo de candles (mesmo aproximado).
4. Subir módulo de indicadores (EMA/SMA).
5. Integrar regra heurística inicial e popup de alerta.
6. Rodar em conta demo e iniciar coleta de logs para calibração.

---

## 13) Nota de responsabilidade
Este app deve ser usado como **ferramenta de suporte à decisão**, não garantia de resultado.
A probabilidade inicial é um indicador técnico modelado e precisa de validação contínua em ambiente controlado (demo/paper) antes de uso financeiro real.
