# Sticker-Studio

Pipeline:
- streamlit run scripts/app.py
- Upload images to uploads/ and rest data in variables
- Segment image via model.py
- Change theme via convertor.py
- Add captions and convert to sticker via generator.py
- Refers font.py to get desired fonts via fonts/
- Saved in stickers/
- Logs at every step in logs/