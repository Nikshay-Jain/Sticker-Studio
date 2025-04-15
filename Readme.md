# Ghibli-Sticker-Studio

## Pipeline:
- streamlit run scripts/app.py
- Upload ghibli images to uploads/ and rest data in variables else, change theme via convertor.py
- Segment image via model.py
- Add captions and convert to sticker via generator.py
- Refers font.py to get desired fonts via fonts/
- Saved in stickers/
- Logs at every step in logs/

## Need to do:
- Integrate feature for text to ghibli generation as option
- shift to check_conv_ghibli from hardcoded stuff and edit app.py accordingly

- REST API and frontend code from Streamlit

- Grafana-Prometheus health tracker

- AI Agent to send the sticker to self in WhatsApp