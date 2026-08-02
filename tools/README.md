# Taller del visor de tango

El `index.html` de la raíz **se genera** desde acá — no editarlo a mano:

```bash
python3 tools/build.py     # regenera ../index.html
git add index.html && git commit && git push   # redeploya GitHub Pages
```

## Archivos

- `template.html` — la interfaz completa (HTML/CSS/JS) con dos placeholders:
  `__DATA__` (catálogo de videos) y `__TRAILS__` (estelas de pies).
- `data/data_es.json` — catálogo final: 5 secciones → subsecciones → items
  `{c: código, t: título en español, e: título original si difiere, y: ID de YouTube}`.
- `data/data.json` — catálogo con títulos originales en inglés.
- `data/videos.json` — mapeo código → ID de YouTube scrapeado de cada subpágina.
- `data/structure.json` — estructura scrapeada de libraryofdance.org/dances/tango/.
- `translate.py` — diccionarios de traducción (secciones, subsecciones y títulos
  por código); lee `data.json` y escribe `data_es.json`.
- `pose/pose_<código>.json` — detección cruda de tobillos por frame
  (YOLOv8m-pose con tracking, `vid_stride=2`, coordenadas normalizadas).
- `pose/trails_<código>.json` — estelas suavizadas por pie:
  `{lead_la|lead_ra|follow_la|follow_ra: [[t, x, y], ...]}`.

## Para anotar un video nuevo

1. Bajarlo: `yt-dlp -f 'bv*[height<=480]+ba/b[height<=480]' -o CODE.webm <url>`
2. Correr pose (ver historial: YOLO `model.track(...)` → `pose_CODE.json`).
3. Generar `trails_CODE.json` (fusionar IDs fragmentados del bailarín ocluido;
   quien mira a cámara trackea estable).
4. Agregar la entrada en `ANNO` dentro de `template.html` (textos, flechas,
   arcos y `{type:'trail'}`).
5. `python3 tools/build.py` y commit.

Las anotaciones usan coordenadas normalizadas (0–1) sobre el cuadro del video.
