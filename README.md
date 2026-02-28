# IQ Signal App (MVP)

Aplicativo desktop em Python para capturar automaticamente o monitor onde está o gráfico da IQ Option, calcular sinais heurísticos (EMA3/5/7, SMA21 e zona estilo YURI) e alertar em tempo real com **PUT** ou **CALL**.

## Modo de uso (2 monitores)
- Deixe o gráfico da IQ Option no **monitor 1**.
- Abra o programa Python no **monitor 2**.
- O app captura automaticamente o monitor configurado em `chart_monitor_index`.
- O app aplica **auto-ROI central** (`center_crop_ratio`) para reduzir ruído visual.

## Executar no Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Configuração (`config.yaml`)
- `chart_monitor_index`: monitor do gráfico (1 = monitor principal no `mss`).
- `center_crop_ratio`: recorte central automático (0.65–0.75 recomendado).
- `threshold`: nível mínimo de probabilidade para disparar alerta (sugestão inicial: 0.78).
- `confirm_ticks`: confirmações consecutivas do mesmo sinal (sugestão: 2).
- `min_score_alert`: score mínimo para alertar (escala 0–100, sugestão 24–26).
- `min_frame_delta`: variação mínima entre frames (sugestão 0.45–0.60).
- `cooldown_seconds`: tempo mínimo entre alertas (20–30s).
- `capture_interval_ms`: intervalo entre capturas.

## Funcionalidades MVP
- Captura automática da tela do monitor selecionado (sem ROI manual).
- Auto-ROI central para reduzir ruído de menus e elementos externos ao gráfico.
- Processamento em tempo real dos candles da imagem.
- Cálculo de sinal com saída simplificada: **PUT** ou **CALL**.
- Filtros de sensibilidade com confirmação + score mínimo + delta mínimo.
- Alerta sonoro + destaque do sinal em label dentro da janela (sem popup e sem minimizar).
- Log em CSV para calibração (`iq_signal_app/data/events.csv`).
