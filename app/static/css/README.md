# CSS

*the compiled css is no longer tracked**

To get the production's css run this command :

```bash
sass app/static/scss/style.scss:app/static/css/style.css --style compressed
```

For development and live compilation, watch the scss folder :

```bash
sass --watch app/static/scss/:app/static/css/
```
