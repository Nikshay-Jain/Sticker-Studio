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

- Grafana-Prometheus health tracker

- Wandb

- Dockerfile -> Docker compose -> Airflow

- Status tracker for frontend

- airflow, wandb expose on frontend

- feedback loop for text to image improvements

- test cases

- user manuals, reports

- demo video

Bonus:
- REST API and Streamlit - maybe
- data drift ???
- AI Agent to send the sticker to self in WhatsApp