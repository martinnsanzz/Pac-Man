# Pac-Man

## The Basics
The **Player** can move Pac-Man in 4 directions - `up, down, left and right`.
There's a total of `4 ghosts` that chase the player, trying to *capture and kill* him.

The **goal** is to clear the maze of `dots` while avoiding the ghosts.

### Rounds and lives
- Each round starts with the ghosts in the `monster pen` (center of the maze). They leave it one by one to chase Pac-Man.
- If a ghost catches Pac-Man: a life is lost, the ghosts return to the pen and Pac-Man goes back to the start position.
- No lives left when caught: **game over**.
- All dots eaten: the board resets and a new round starts.

### Dots
| Type | Amount | Points |
|---|---|---|
| Small dot | 240 | 10 |
| Energizer (big, flashing, in the corners) | 4 | 50 |
| **Total** | **244** | **2,600 per maze** |

All 244 dots must be eaten to advance.

### Extra points
**1. Eating ghosts (energizers)**
- Eating an energizer makes the ghosts **reverse direction** and turn **blue** for a short time.
- Blue ghosts can be eaten. Only their eyes return to the pen, where they respawn.
- Points double with each ghost from the same energizer: `200 → 400 → 800 → 1600`.
- All 4 ghosts on all 4 energizers: **+12,000** points.
- The blue time shrinks with each level. From level 19, ghosts no longer turn blue.

**2. Bonus fruit**
- Appears twice per round, below the monster pen: after `70` dots and after `170` dots eaten.
- Worth `100 to 5,000` points, depending on the level.
- Stays on screen between `9 and 10 seconds` (the exact time is random, not predictable).
- The last 6 completed levels plus the current one are shown along the bottom (fruit/level counter).

| Levels | Item | Points | Two per board |
|---|---|---|---|
| 1 | Cherry | 100 | 200 |
| 2 | Strawberry | 300 | 600 |
| 3 to 4 | Orange | 500 | 1,000 |
| 5 to 6 | Apple | 700 | 1,400 |
| 7 to 8 | Melon | 1,000 | 2,000 |
| 9 to 10 | Galaxian flagship | 2,000 | 4,000 |
| 11 to 12 | Bell | 3,000 | 6,000 |
| 13 and beyond | Key | 5,000 | 10,000 |

## Ghost behavior

### Modes
Ghosts are always in exactly one of three modes:

| Mode | Goal |
|---|---|
| **Chase** | Hunt Pac-Man down |
| **Scatter** | Give up the chase and head to their home corner |
| **Frightened** | Wander randomly after an energizer is eaten (dark blue, slower, flash white before ending) |

### Personalities (chase mode)
| Ghost | Color | Behavior |
|---|---|---|
| Blinky | Red | Aggressive, stays right behind you |
| Pinky | Pink | Gets in front of you and cuts you off |
| Inky | Light blue | Least predictable |
| Clyde | Orange | Does his own thing, stays out of the way |

### Direction rules
- Ghosts **can't reverse** on their own. At an intersection they continue forward or turn to a side.
- The system **forces a reversal** on these mode changes: chase→scatter, chase→frightened, scatter→chase, scatter→frightened.
- **No reversal** when frightened ends (frightened→chase/scatter).
- A reversal happens when the ghost enters its next tile, so ghosts don't all turn at the same instant.

### Scatter/chase timer
- Starts in **scatter** at the beginning of a level or after losing a life, and resets then.
- 4 scatter periods per level, then chase forever.
- The timer **pauses** during frightened mode, then resumes in the previous mode.

| Mode | Level 1 | Levels 2-4 | Levels 5+ |
|---|---|---|---|
| Scatter | 7 | 7 | 5 |
| Chase | 20 | 20 | 20 |
| Scatter | 7 | 7 | 5 |
| Chase | 20 | 20 | 20 |
| Scatter | 5 | 5 | 5 |
| Chase | 20 | 1033 | 1037 |
| Scatter | 5 | 1/60 | 1/60 |
| Chase | indefinite | indefinite | indefinite |

Values are in seconds. A 1/60 s scatter shows up as just a reversal.

### Frightened mode
- Triggered by one of the 4 energizers: ghosts reverse, turn dark blue and move slower.
- At each intersection a **pseudo-random** direction is tried first. If it is blocked by a wall or is the opposite direction, the next one is tried clockwise.
- The random generator resets with the same seed at each new level and after losing a life, so patterns are repeatable.
- Frightened time shrinks per level, until ghosts no longer turn blue (they still reverse).

### Speed
| Level | Pac-Man | Pac-Man eating dots | Ghost normal | Ghost frightened | Ghost tunnel |
|---|---|---|---|---|---|
| 1 | 80% | ~71% | 75% | 50% | 40% |
| 2-4 | 90% | ~79% | 85% | 55% | 45% |
| 5-20 | 100% | ~87% | 95% | 60% | 50% |
| 21+ | 90% | ~79% | 95% | - | 50% |

- Eating a small dot stops Pac-Man for **1 frame** (1/60 s), an energizer for **3 frames**.
- Pac-Man is a bit faster than the ghosts until level 21, then the ghosts are faster.
- Frightened Pac-Man speed (levels 1-4): 90%, 95%, then 100%.
- Ghosts in a side tunnel are almost halved in speed.