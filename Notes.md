# Fly-in

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

To check if a `pr` has passed you can run the following commands:

```sh
gh run view --log-failed # Will show the exact errors on a specific pull request