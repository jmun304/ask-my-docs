# Capstone 2026 Project

# Ask My Docs: _A full-stack AI document Q&A system_
## Getting Started 
### Prerequisites 
* Python 3.10+
* Git

### Steps
1. Clone the repository:
`git clone https://github.com/jmun304/ask-my-docs.git`
2. Go into `ask-my-docs`:
`cd ask-my-docs`

**Set up backend Environment**

3. Go into backend folder: `cd backend`
4. Activate virtual envirionment: `python -m venv venv`
5. Activate Virtual Environment: 

_**Windows**_: `venv\Scripts\activate`

_**Mac/Linux**_: `source venv/bin/activate`

6. Install dependencies: `pip install -r requirements.txt`
7. Run backend server: `uvicorn app.main:app --reload`
8. Open: http://127.0.0.1:8000/docs

## Contribution Guidelines
### 1. Pick an issue to work on that is assigned to you

### 2. Create a feature branch
Make sure you are in root: `cd ask-my-docs`

`git checkout main`

`git pull origin main`

`git checkout -b [feature/<issue-name>]`

### 3. Work on feature
Repeat commits as needed.

Make sure you are in root: `cd ask-my-docs`
`git add .`

`git commit -m "commit message"`

### 4. Push your branch
`git push origin [feature/<issue-name>]`

### 5. Create a Pull Request (PR)
* Open PR from your branch → main

In PR description: **#ISSUE_NUMBER: (pick your issue)** and provide description for your PR.

### 6. Code Review

### 7. Ready to merge: REBASE BEFORE MERGING
`git checkout main`

`git pull origin main`

`git checkout [feature/<issue-name>]`

`git rebase main`

### 8. Squash Merge
Once approved, use "Squash and merge" on GitHub (ensures only 1 commit merged)

### 9. After merge - Clean up
1. Delete your branch locally:

`git branch -d [feature/<issue-name>]`

2. Delete remote branch:

`git push origin --delete [feature/<issue-name>]`
