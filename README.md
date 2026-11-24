# space-esc

Space Escape is an arcade shooter inspired by Galaga, made with Python and Pygame. Reach 1000 points to escape!

**Controls:** arrow keys or WASD to move, Space to shoot, Esc to return to the menu.

## Play in the browser

`web/` holds a Python 3 version of the game that runs in the browser with [pygbag](https://pypi.org/project/pygbag/).

```bash
pip install pygbag
python3 -m pygbag web            # test it at http://localhost:8000
python3 -m pygbag --build web    # output goes to web/build/web/
```

To embed the game in a website, copy everything in `web/build/web/` to the site and load its `index.html` in an `<iframe>`.

## Original desktop version

The files at the top of the repo are the original version. It needs **Python 2.7 and Pygame 1.9.1**. Download all the files and folders into one folder, then run `Space Escape.py`.

The `Coins/` images were never committed, so the desktop version crashes when a bonus coin appears. `web/Coins/` has placeholder frames you can copy over.
