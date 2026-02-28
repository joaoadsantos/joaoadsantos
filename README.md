# IQ Signal App (MVP)

Aplicativo desktop em Python para capturar uma região da tela com gráfico da IQ Option, calcular sinais heurísticos (EMA3/5/7, SMA21 e zona estilo YURI) e alertar quando a probabilidade estimada ultrapassa um threshold configurável.

## Executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Funcionalidades MVP
- Captura contínua da ROI da tela.
- Extração aproximada de candles a partir da imagem.
- Cálculo de sinal CALL/PUT com probabilidade.
- Alerta com bip + popup modal.
- Clique em OK minimiza o app.
- Log em CSV para calibração (`iq_signal_app/data/events.csv`).

## Configuração
Edite `config.yaml` para:
- ROI (`x`, `y`, `width`, `height`)
- intervalos de captura
- threshold
- cooldown
