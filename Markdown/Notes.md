# Pac-Man

## Concepts

### Github

A `Repository` is a core unit in *GitHub*. It's a git folder that contains your source code, all
the files (including project files), and their full version history (commits, pushes...). This 
is the shared space where you can collaborate with other developers through branches, commits,
pull requests, and discussions.

The `Project` is a planning and tracking tool. You can organize issues and pull requests in a
**Kanban-Style** workflow. It adds automation, visual and dashboards.

#### Issues
`Issues` can track bug reports, new features and ideas (Also anything else that you need to 
write down or discuss with your team). Additionally, you can create sub-issues and easily 
browse the full hierarchy to be done.

You can add `sub-issues` to quickly break down larger pieces of work into smaller issues.

#### Pull Requests
`Pull requests` are proposals to merge code changes into a project. A pull request is GitHub's
key collaboration feature, letting developers discuss and review changes before merging them.

A pull request is organized in different tabs:
- **The Conversation tab** shows the description, timeline, comments, and reviews.
- **The Commits tab** shows how the pull request branch changed over time.
- **The Checks tab** shows automated tests, builds, and other validations.
- **The Files changed tab** shows the diff that reviewers use to understand the proposed changes.
- **The Findings tab** shows automated code review results, such as code scanning alerts, for the proposed changes.

#### Branching Name Practices
To keep branches organized and easy to comprehend the branch propose a common technique is using
prefixes. Some common purposes are:

1. **feature/:** For new features or functionalities.
2. **bugfix/:** For fixing bugs in the code.
3. **hotfix/:** For urgent patches, usually applied to production.
4. **design/:** For user interface or user experience updates.
5. **refactor/:** For improving code structure without changing functionality.
6. **test/:** For writing or improving automated tests.
7. **doc/:** For documentation updates.

These prefixes should be followed with a short descriptive name. These names should be concise
yet informative. This are some tips:
- Use *hyphens (-)* to separate words for better readability.
- *Avoid generic terms* like update, changes, or stuff.
- Focus on the *primary task* or issue the branch addresses.

#### Actions

Action is an integration platform that allows you to automate your build, test and deployment
pipeline. You can create workflows that run tests whenever you push a change to your repository
or that deploy pull requests to production.

**How it works**
- A workflow is a `.yml` file in `.github/workflows/` (root of the repo).
- GitHub finds every file in that folder and runs it on its own server (`runs-on: ubuntu-latest`), not on your machine.
- Structure: **event** (`on:`) triggers a **job**, which runs **steps** in order on one fresh machine.
- `uses:` = a prebuilt step (`owner/repo@version`). `run:` = a shell command.

**Our CI: flake8 + mypy on every pull request**

`.github/workflows/ci.yml`:

```yaml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --locked
      - name: Lint
        run: |
          if [ -n "$(git ls-files '*.py')" ]; then
            uv run flake8 .
            uv run mypy .
          else
            echo "No Python files, skipping"
          fi
```

- `actions/checkout`: downloads the repo code onto the runner (without it the machine is empty).
- `astral-sh/setup-uv`: installs `uv`.
- `uv sync --locked`: installs dependencies from `uv.lock`, fails if the lock is out of date.
- `uv run`: runs the tool inside the project environment.
- The `if` skips linting when the repo has no `.py` files, so the job stays green.
- Config lives in the repo: `[tool.mypy] strict = true` in `pyproject.toml` and `.flake8` (`exclude = .venv`).

**Read the results**
```sh
gh pr checks --watch        # live status of the PR
gh run list --limit 5       # recent runs
gh run view --log-failed    # why it failed
```
- Green = passed, red = failed. Every new push to the PR branch re-runs it.
- A run with no duration usually means the YAML is invalid (it never started). Check the Actions tab for the error line.

**Block merging when checks fail (ruleset on `main`)**

Settings → Rules → Rulesets → New branch ruleset:
- Name: `protect-main`, Enforcement status: **Active**
- Bypass list: empty (nobody skips it, you included)
- Target: default branch (`main`)
- Tick: Restrict deletions, Block force pushes
- Tick: **Require a pull request before merging**
- Tick: **Require status checks to pass** → add `lint`, and tick "Require branches to be up to date before merging"

Result: pushing to `main` is rejected (`GH013: Repository rule violations`) and the merge button is disabled until `lint` is green.

**Common mistakes**
- Folder named `.github/workflow/` (missing `s`): the workflow never runs.
- `- run:` written as a separate list item after `- name:`: invalid, they must be the same step (aligned keys).
- Required check name not matching the job name (`lint`): the PR waits forever on "expected".
- Committed on local `main` by accident and the push is rejected: move the commit to a branch, then reset `main`:
  ```sh
  git switch -c <branch>
  git switch main
  git reset --hard origin/main
  ```
- Forgetting to commit `uv.lock`: CI and local environments drift apart.

#### GitHub CLI (commands && workflow)

>Rule: **NEVER COMMIT TO MAIN**. Every change → 1 issue → 1 branch → 1 PR.

0. Setup GitHub CLI

Install `GitHub CLI` in the website [Download](https://cli.github.com/).

>For Codam, install the .tar.gz folder unpack it and move `gh` file to `~/local/bin`

Login to gh with you're GitHub and once logged in open the repo and gh will detect the 
repository and link it.

```sh
gh auth login
```

1. Create an issue

To create an issue you use `gh issue create` or `new` its an alias. You can use the interactive
menu or use some flags to add **name**, **type** or **assignee**.

```sh
gh issue create --title "Creating makefile" --assignee "Martin"
```

To create `sub-issues` use the flag **--parent** with the father **ID-Number**

```sh
gh issue create --title "Creating makefile" --assignee "Martin" --parent 5
```
>Use `gh issue create --help` for more information

To see a list of *active issues* use:

```sh
gh issue list
gh issue view <num> # For specific info in one issue use their number id
```

2. Create a branch linked to the issue

Before creating a new branch to start working on an issue *you MUST be on main branch* and pull
any changes so main always remains clean and stable.

```sh
git switch main
git pull origin main
```

Then you will create the branch from the issue and use the flag `-c` to move directly to
that new branch and the flag `-n` to give a name to the branch:
>If `\n` this is not provided it will give a default name derived from the issue name. Check
> [Branching naming](#branching-name-practices)

```sh
gh issue develop <num> -c -n "feature/3-Creating-Makefile
```

3. Work on the branch

Work normally in that branch, `git add .`, `git commit -m "..."`, `git push <branch>`

>Note: Be clear with commit messages to easily track the development of the project.

4. Pull request

Once an issue is ready to merge with main, you need to create a pull request.

```sh
gh pr create --base main --title Added Makefile --body "Closes #<issue-num>"
```

>This closes the issue with that number automatically `--body "Closes #<issue-num>"`

Once a **pr** is created, within the github website `pull request` panel oyu can see pending
pull requests. An automatic check can be run such as (mypy or flake8) if a *ci.yml* file is
located in the repo root under `.github/workflows`. In rulesets you can add a rule that if
lint fails you wont be able to merge with main.

To check if a `pr` has passed you can run the following commands:

```sh
gh run view --log-failed # Will show the exact errors on a specific pull request
```

>Very useful command to see all branches throughout the life-cycle of the project. You can also
>install `git graph` extension on **VS Code** to see it on the source control panel.

```sh
git log --oneline --graph --decorate --all
git branch -a -vv
```

If you want to check in the CLI a `pull request` and merge it without touching GitHub website
run the following commands:

```sh
gh pr checks <num> # Checks the state of a specific pr

# If no errors found you can merge
gh pr merge <num> <strategy> --delete-branch --auto

# Available strats:
#   --squash -> All branch commits collapse into a single commit on main. Best option for simplicity
#   --merge -> Keeps A, B, C exactly as written, plus one extra merge commit X.
#   --rebasae -> Each commit is replayed one by one on main. No merge commit, linear history.
# --auto -> Merges automatically the moment the rules pass
```

### Pygame

#### 1. Mental model

- Pygame draws pixels onto **Surfaces** (2D arrays of pixels in RAM).
- The **display surface** is the window. Nothing appears until `pygame.display.flip()`.
- A game is a loop: **events -> update -> draw -> flip -> tick**.
- Coordinates: `(0, 0)` is top-left, x grows right, **y grows down**.

#### 2. Init and window

```python
import pygame

pygame.init()                                   # init all modules
screen = pygame.display.set_mode((672, 864))    # returns the display Surface
pygame.display.set_caption("Pac-Man")
...
pygame.quit()                                   # always on exit
```

| Flag | Effect |
|---|---|
| `pygame.RESIZABLE` | user can resize (emits `VIDEORESIZE`) |
| `pygame.FULLSCREEN` | fullscreen |
| `pygame.SCALED` | fixed logical size, auto-scaled by pygame |

`set_mode((0, 0))` uses the current desktop size.

#### 3. Main loop

```python
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():            # 1. events
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000                  # 2. cap FPS, dt in seconds
    update(dt)                                  # 3. logic

    screen.fill((0, 0, 0))                      # 4. draw
    draw(screen)
    pygame.display.flip()                       # 5. show
pygame.quit()
```

- `clock.tick(60)` sleeps to cap at 60 FPS and returns ms since the last call.
- **Use `dt`** for movement: `x += speed * dt` (speed in pixels/second). Never move "N pixels per frame" if speed must be consistent.
- `pygame.event.get()` empties the queue. Call it **once per frame**; two calls steal events from each other.

#### 4. Events and input

Two ways to read the keyboard:

| Method | Use for | Fires |
|---|---|---|
| `event.type == KEYDOWN` / `KEYUP` | one-shot actions (pause, menu select, "next direction") | once per press |
| `pygame.key.get_pressed()` | continuous state (is a key held now?) | every call |

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: ...
        if event.key == pygame.K_LEFT: ...

keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]: ...
```

Mouse: `MOUSEBUTTONDOWN` (`event.pos`, `event.button`), `MOUSEMOTION`, or `pygame.mouse.get_pos()`.

Common events: `QUIT`, `KEYDOWN`, `KEYUP`, `MOUSEBUTTONDOWN`, `MOUSEBUTTONUP`, `MOUSEMOTION`, `VIDEORESIZE`.

#### 5. Surface and blit

```python
surf = pygame.Surface((w, h))             # opaque
surf = pygame.Surface((w, h), pygame.SRCALPHA)  # per-pixel alpha
surf.fill((r, g, b))                      # or (r, g, b, a) with SRCALPHA
target.blit(surf, (x, y))                 # copy surf onto target at (x, y)
```

- `blit(source, dest, area=None)`: `area` is a `Rect` of the source to copy (this is how you draw one tile of a sprite sheet).
- Order of blits = draw order (last one on top).
- `surf.get_size()`, `get_width()`, `get_height()`, `get_rect()`.
- `surf.subsurface(rect)` returns a **view** sharing pixels with `surf` (no copy).
- `surf.copy()` returns a real copy.

#### 6. Rect

`pygame.Rect(x, y, w, h)` holds integers. Handy attributes (assignable):
`x y w h`, `top bottom left right`, `center centerx centery`, `topleft bottomright size`.

```python
r = surf.get_rect(center=(100, 100))     # position a surface by its center
r.colliderect(other)                     # overlap test
r.collidepoint(pos)                      # mouse over button?
r.move(dx, dy)                           # returns new Rect
r.move_ip(dx, dy)                        # in place
```

**Pitfall:** Rects store ints. `rect.x += 0.4` is truncated, so slow movement stops. Keep a float position `pos` and copy it to `rect.topleft` each frame.

#### 7. Drawing primitives

```python
pygame.draw.rect(surf, color, rect, width=0, border_radius=0)   # width 0 = filled
pygame.draw.circle(surf, color, center, radius, width=0)
pygame.draw.line(surf, color, start, end, width=1)
pygame.draw.polygon(surf, color, points, width=0)
pygame.draw.arc(...)
```

Colors: `(r, g, b)` or `(r, g, b, a)`, 0..255. Or `pygame.Color("yellow")`.

#### 8. Images and sprite sheets

```python
img = pygame.image.load("assets/tiles.png").convert_alpha()
```

- `.convert()` (opaque) or `.convert_alpha()` (transparency): **do it once after load**, it makes blitting much faster. It needs `set_mode` to have been called first.
- Load images once at startup, not every frame.

Slicing a grid sheet (16x16 tiles, 4 per row):

```python
TILE = 16
def get_tile(sheet, v):
    x = (v % 4) * TILE
    y = (v // 4) * TILE
    return sheet.subsurface(pygame.Rect(x, y, TILE, TILE))
```

#### 9. Scaling

```python
pygame.transform.scale(surf, (w, h))        # nearest neighbour: sharp, use for pixel art
pygame.transform.smoothscale(surf, (w, h))  # smooth: blurs pixel art
pygame.transform.rotate(surf, angle)
pygame.transform.flip(surf, flip_x, flip_y)
```

**Pattern for fixed-resolution games:** draw everything on a fixed logical surface (e.g. 672x864), then scale that one surface to the window once per frame and blit it centered. Mouse positions must then be converted from window coords to logical coords:

```python
lx = (mouse_x - offset_x) / scale
ly = (mouse_y - offset_y) / scale
```

Compute scale as `min(win_w / W, win_h / H)` to keep the aspect ratio.

#### 10. Text

```python
font = pygame.font.Font("assets/font.ttf", 24)   # or pygame.font.SysFont("arial", 24)
text = font.render("SCORE 100", True, (255, 255, 255))   # True = antialiasing
screen.blit(text, (10, 10))
```

`render` is slow-ish: create fonts once, and re-render text only when it changes.

#### 11. Sound

```python
pygame.mixer.init()                      # done by pygame.init()
sfx = pygame.mixer.Sound("assets/eat.wav")
sfx.play()
pygame.mixer.music.load("assets/theme.ogg")
pygame.mixer.music.play(-1)              # -1 = loop forever
```

Sounds are short effects loaded in memory; music is streamed.

#### 12. Timing

- `pygame.time.get_ticks()`: ms since `init`.
- `pygame.time.set_timer(EVENT_ID, ms)`: posts a custom event every `ms`.
- Custom events: `MY_EVENT = pygame.USEREVENT + 1`.
- For timed states (power pellet lasts 6 s), store a deadline and compare, or count down with `dt`.

#### 13. Screens / game states

A clean structure for menus + game:

```python
class Screen:
    def handle_event(self, event) -> Action: ...   # input
    def update(self, dt) -> None: ...              # logic
    def draw(self, surface) -> None: ...           # drawing only
```

- The app holds `current_screen` and calls the same three methods every frame.
- A screen **returns an action** to request a change (`START_GAME`, `BACK`, `QUIT`) instead of importing other screens. That avoids circular imports.
- `draw` must not change game state; `update` must not draw.

#### 14. Common mistakes

- Calling `convert_alpha()` or loading images **every frame**.
- Forgetting `display.flip()` (black window) or `fill()` (ghost trails).
- Moving by fixed pixels per frame instead of `speed * dt`.
- Using `Rect` for positions that need decimals.
- Calling `event.get()` twice per frame.
- Using `smoothscale` on pixel art.
- Not handling `QUIT` (window can't be closed).
- Getting mouse position without converting to logical coordinates after scaling.
- Doing blocking work (`time.sleep`, long loops) inside the main loop: the window freezes.
- Forgetting `pygame.quit()`.

#### 15. Grid-based movement (Pac-Man style)

- Keep the **grid position** (`col`, `row`) and a **pixel offset** between cells.
- Store the player's **requested direction**; apply it only when centered on a cell and the next cell is open (check the wall bit).
- Cell value is a bitmask: bit 0 N, 1 E, 2 S, 3 W; `1` = closed.
  `can_go_north = not (cell & 1)`, `can_go_east = not (cell & 2)`, etc.
- Pixel position = `col * TILE`, `row * TILE` (plus the maze offset on the arcade surface).

#### 16. Quick reference

| Task | Call |
|---|---|
| Init / quit | `pygame.init()` / `pygame.quit()` |
| Window | `pygame.display.set_mode(size, flags)` |
| Show frame | `pygame.display.flip()` |
| Clear | `surf.fill(color)` |
| Draw image | `target.blit(surf, pos)` |
| Load image | `pygame.image.load(p).convert_alpha()` |
| Events | `pygame.event.get()` |
| Held keys | `pygame.key.get_pressed()` |
| Mouse | `pygame.mouse.get_pos()` |
| FPS / dt | `clock.tick(fps)` |
| Scale | `pygame.transform.scale(...)` |
| Collision | `rect.colliderect(other)` |