# Everyday Gym: public pages

Public web pages for the Everyday Gym Android app, served by GitHub Pages. The Play Store listing
links to the privacy policy here.

- English: `privacy/`
- Portuguese: `privacidade/`

The text comes from the app repository's `legal/` folder, which the app also shows on screen, so
the page and the app always say the same thing. Never edit the HTML by hand: change `legal/` in the
app repository, then regenerate and commit:

```bash
pip install markdown
python3 build.py ../Everyday-Gym/legal
```
