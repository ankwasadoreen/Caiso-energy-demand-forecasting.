# GitHub Upload Checklist

- [ ] Copy your working notebooks into `notebooks/`
- [ ] Copy processed CSVs into `data/processed/`
- [ ] Test `python -m streamlit run dashboard/app.py`
- [ ] Restart and run all notebooks from top to bottom
- [ ] Remove hard-coded local paths such as `C:\Users\...`
- [ ] Remove API keys, passwords, tokens, and `.env` files
- [ ] Check data licensing before uploading raw datasets
- [ ] Add screenshots to `docs/` if you want them in the README
- [ ] Run `pip freeze > requirements-lock.txt` from your working environment if exact reproducibility is needed
- [ ] Initialize Git and commit
