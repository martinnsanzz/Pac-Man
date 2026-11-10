*This project has been created as part of the 42 curriculum by masanz-s and danmorei*

[Martin GitHub](https://github.com/martinnsanzz)
[Daniel Github](https://github.com/Danitell0)

# Pac-Man
*Ghosts! More ghosts!*

## 📂 Description


## 🔷 Instructions




## ➕ Additional requirements

In this section additional requirements mentioned on the `subject.pdf` will be added:

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

## 📖 Resources
This is a list of multiple resources use throughout the life-cycle of the project

### 🐍 Python
- [Python argparse: Syntax, Usage, and Examples](https://mimo.org/glossary/python/argparse)
- [How to Pass Command-Line Arguments in pytest](https://medium.com/@johnidouglasmarangon/how-to-pass-command-line-arguments-in-pytest-custom-addoptions-a706bae89d05)

#### Pygame
- [Pygame Docs](https://www.pygame.org/docs/)
- [How to load Custom Fonts](https://www.makeuseof.com/pygame-fonts-text-effects-how-load/)

### 😺 GitHub
- [GitHub Branching Name Best Practices](https://dev.to/jps27cse/github-branching-name-best-practices-49ei)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Repository vs Project](https://gitprotect.io/blog/github-repository-vs-project/)
- [CLI GitHub](https://cli.github.com/)

### 📋 Other Stuff
- [The Pac-Man Dossier by Jamey Pittman](https://pacman.holenet.info/)

## 🤖 AI Usage

**AI was NOT used to generate code.** All function implementations were written by Martin™ and
Daniel™.

**Where AI was used:**


**What AI was not used for**
