# IQ Signal App (MVP)

Aplicativo desktop em Python para capturar automaticamente o monitor onde está o gráfico da IQ Option, calcular sinais heurísticos (EMA3/5/7, SMA21 e zona estilo YURI) e alertar em tempo real com **PUT** ou **CALL**.

## Modo de uso (2 monitores)
- Deixe o gráfico da IQ Option no **monitor 1**.
- Abra o programa Python no **monitor 2**.
- O app captura automaticamente o monitor configurado em `chart_monitor_index`.

## Executar no Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Configuração (`config.yaml`)
- `chart_monitor_index`: monitor do gráfico (1 = monitor principal no `mss`).
- `threshold`: nível mínimo de probabilidade para disparar alerta.
- `capture_interval_ms`: intervalo entre capturas.
- `cooldown_seconds`: tempo mínimo entre alertas.

## Funcionalidades MVP
- Captura automática da tela do monitor selecionado (sem ROI manual).
- Processamento em tempo real dos candles da imagem.
- Cálculo de sinal com saída simplificada: **PUT** ou **CALL**.
- Alerta sonoro + popup modal; ao clicar OK, o app minimiza.
- Log em CSV para calibração (`iq_signal_app/data/events.csv`).
