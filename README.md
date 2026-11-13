*This project has been created as part of the 42 curriculum by masanz-s and danmorei*

[Martin GitHub](https://github.com/martinnsanzz)
[Daniel Github](https://github.com/Danitell0)

# Pac-Man
*Ghosts! More ghosts!*

## 📂 Description


## 🔷 Instructions




## ➕ Additional requirements

In this section additional requirements mentioned on the `subject.pdf` will be added:

### ⚒️ Configuration 

The game is configured with a JSON file passed as the only command-line argument:

```bash
uv run python pac-man.py config.json
```

```json
{
    "highscore_filename": "highscore.json",
    "lives": 4,
    "total_pacgum": 42,
    "pacgum_points": 10,
    "super_pacgum_points": 50,
    "ghost_points": 200,
    "level_time_limit": 90
}
```

#### Parameters

| Key | Description | Default | Accepted values |
|---|---|---|---|
| `highscore_filename` | File used to store the high score | `highscore.json` | Name ending in `.json`, non-empty, no `/` or spaces |
| `lives` | Starting lives | `3` | Integer, 1 to 100 |
| `total_pacgum` | Total number of pac-gums | `42` | Integer, 1 to 10 |
| `pacgum_points` | Points per pac-gum | `10` | Integer, 1 to 100 |
| `super_pacgum_points` | Points per super pac-gum | `50` | Integer, 1 to 500 |
| `ghost_points` | Points per ghost | `200` | Integer, 1 to 2000 |
| `level_time_limit` | Time limit of a level | `90` | Integer, 1 to 1000 |
| `retro_shader` | Enables the retro shader | `on` | `"on"` or `"off"` |

#### File format

- The file must have the `.json` extension and be encoded in UTF-8.
- Full-line comments are allowed: `# ...`, `// ...` and `/* ... */`.
- Multi-line `/* ... */` blocks are allowed and must be closed.
- Blank lines are ignored.

#### Missing and unknown values

- Every key is optional. A key that is absent takes its default value from the table above, so a partial file (or `{}`) is valid.
- Defaults are not checked by the validators. Only values written in the file are.
- Unknown keys are ignored.

#### Validation and errors

The file is parsed and then validated against the `GameConfig` model (Pydantic). The program stops with a `PacManError` if:

- the file cannot be opened or read, is empty, is not UTF-8, or is not valid JSON;
- a `/* */` comment is left open;
- a value is outside its accepted range or has the wrong type, or `retro_shader` is not `"on"`/`"off"`, or `highscore_filename` is invalid.

Only the first invalid field is reported, with the reason.

#### Storage

The validated values are stored in a single typed `GameConfig` object, with each key as an attribute. It is built once at startup, after validation and after defaults are filled in.

### 🏆 Highscores
Highscores are saved in a JSON file. Its name is set by `highscore_filename` in the config file (default: `highscore.json`).
The file is created on the first save, in the folder the game is run from.

**Format:** a list of entries, sorted from highest to lowest score.

```json
[
    {"name": "PacMaster", "score": 1200},
    {"name": "MsPacMan", "score": 850}
]
```

**Rules:**
- Only the top 10 scores are kept
- Names: 1-10 characters, letters, digits and spaces only (can't start with a space)
- Scores: non-negative integers
- On a tie, the older score stays ranked above the new one

**Error handling:**
- Missing file -> the game starts with an empty table
- Corrupted or invalid file -> the table is emptied and a warning is printed in the terminal
- File can-t be written -> a warning is printed in the terminal and the game keeps running

### 🔋 Maze Generation

> Work in progress: the maze is currently generated once, when the game is entered, with fixed parameters.

### Generation

Mazes come from the `MazeGenerator` class of the `mazegen` package (the A-Maze-ing project), used by `MazeGen`:

```python
generator = MazeGenerator(19, 20, (0, 0), (1, 1), False)
generator.generate()
grid = generator.maze
```

- `width = 19` and `height = 20` are currently hardcoded.
- `generator.maze` is a 2D list of integers, indexed as `grid[row][col]`.
- Each integer describes one cell (see below). The grid is passed unchanged to `MazeRenderer`.

### Cell encoding

Each cell value is a 4-bit mask, one bit per direction:

| Bit | Value | Direction |
|---|---|---|
| 0 | 1 | N |
| 1 | 2 | E |
| 2 | 4 | S |
| 3 | 8 | W |

Binary is read as `W S E N` (bit 3 to bit 0). A set bit means there is a wall on that side of the cell. A value of `0` has no walls and `15` is closed on all four sides.

### Tilemap


`assets/tilemap/tilemap.png` is a 64x64 px image holding 16 tiles of 16x16 px, in a 4x4 grid. `AssetsLoader._load_tiles` slices it in reading order (left to right, top to bottom):

- `col = index % 4`, `row = index // 4`
- the tile at `index` is cut with `subsurface` and scaled x2 to 32x32 px
- `AssetsLoader.tiles[index]` is the tile for the cell value `index`

The cell value is therefore used directly as the tile index:

| Value | Binary (WSEN) | Walls | Tilemap (row, col) |
|---|---|---|---|
| 0 | 0000 | none | (0, 0) |
| 1 | 0001 | N | (0, 1) |
| 2 | 0010 | E | (0, 2) |
| 3 | 0011 | N, E | (0, 3) |
| 4 | 0100 | S | (1, 0) |
| 5 | 0101 | N, S | (1, 1) |
| 6 | 0110 | E, S | (1, 2) |
| 7 | 0111 | N, E, S | (1, 3) |
| 8 | 1000 | W | (2, 0) |
| 9 | 1001 | N, W | (2, 1) |
| 10 | 1010 | E, W | (2, 2) |
| 11 | 1011 | N, E, W | (2, 3) |
| 12 | 1100 | S, W | (3, 0) |
| 13 | 1101 | N, S, W | (3, 1) |
| 14 | 1110 | E, S, W | (3, 2) |
| 15 | 1111 | N, E, S, W | (3, 3) |

### Rendering

`MazeRenderer` draws the grid on a surface:

1. **Layout:** the maze is centered on the surface. `start_x` and `start_y` are computed from the surface size and the maze size in tiles (`tile_px` = 32).
2. **Tiles:** each cell is blitted at `start + (col, row) * tile_px`, using `tiles[value]`.
3. **Border:** a rectangle around the whole maze, inflated by one wall thickness on each side. The thickness is `wall_px = 2 * tile_px // 16` (4 px).
4. **Junctions:** the tiles do not draw the corners where four cells meet. For every interior corner, a `2 * wall_px` square in `WALL_COLOR` (`(43, 95, 255)`) is drawn if one of the four adjacent cells has a wall bit touching that corner:
   - top-left cell: `E` or `S`
   - top-right cell: `W` or `S`
   - bottom-left cell: `N` or `E`
   - bottom-right cell: `N` or `W`

## 📖 Resources
This is a list of multiple resources use throughout the life-cycle of the project

### 🐍 Python
- [Python argparse: Syntax, Usage, and Examples](https://mimo.org/glossary/python/argparse)
- [How to Pass Command-Line Arguments in pytest](https://medium.com/@johnidouglasmarangon/how-to-pass-command-line-arguments-in-pytest-custom-addoptions-a706bae89d05)

#### Pygame
- [Pygame Docs](https://www.pygame.org/docs/)
- [How to load Custom Fonts](https://www.makeuseof.com/pygame-fonts-text-effects-how-load/)
- [Pygame-ce Docs](https://pyga.me/docs/)

### 😺 GitHub
- [GitHub Branching Name Best Practices](https://dev.to/jps27cse/github-branching-name-best-practices-49ei)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Repository vs Project](https://gitprotect.io/blog/github-repository-vs-project/)
- [CLI GitHub](https://cli.github.com/)
- [Managing remote repositories](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories)
- [Push 2 different githubs](https://www.youtube.com/watch?v=mIH_heuc1Y0)

### 📋 Other Stuff
- [The Pac-Man Dossier by Jamey Pittman](https://pacman.holenet.info/)

## 🤖 AI Usage

**AI was NOT used to generate code.** All function implementations were written by Martin™ and
Daniel™.

**Where AI was used:**


**What AI was not used for**
