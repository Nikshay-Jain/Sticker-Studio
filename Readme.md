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
- Integrate feature for text to ghibli generation:
to_ghibli, main.py, app.py to be updated for 2 options

- Add tags on bottom of sticker

- REST API and Streamlit

- Grafana-Prometheus health tracker

Bonus:
- AI Agent to send the sticker to self in WhatsApp