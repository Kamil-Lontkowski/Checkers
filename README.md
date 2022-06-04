# Checkers

Game of checkers based on [this tutorial](https://youtu.be/vnd3RfeG3NM) made by [Tech With Tim](https://www.youtube.com/c/TechWithTim)

Only the portion of drawing and selecting pieces are taken from tutorial.
Whole menu system, getting valid moves and AI algorithms were rewritten.

Also, the rules are different.

This game follows Polish version of checkers.
The rules are as follows:
- The game is between two players
- The board consists of 64 fields
- Pieces move only on the dark fields
- Pieces move only ahead, and only one field
- You can't move not in your turn
- You can't skip your turn
- When the piece reaches opposite side of the board it becomes king
- Kings move in every direction on the diagonal by as many fields as they wish
- If player can jump enemy piece he has to
- You can jump enemy piece forward or backward
- If by jumping, piece reaches opposite side of the board, it does not become king
- The game end when player has no pieces or can't make a valid move
- If you can jump multiple pieces you have to choose the moves that jumps most pieces

### You have multiple options to choose
![Menu screen](screenshots/menu.png)

**You can:**
- Choose difficulty (depth of algorithm)
- Chose mode
  - Player vs Player
  - Player vs AI
  - AI vs AI 
  - AI vs random
- Choose algorithm used by specific side

In mode AI vs player AI always plays black side.

----
### The game supports multiple jumps, forward or backward as the rule states.
![](screenshots/game.png)

![](screenshots/multiple_jumps.png)
### As a king you can attack first enemy piece from distance.
![](screenshots/king_attack.png)

### At the end screen you can click whereever you want to go back to menu
![](screenshots/end_screen.png)

## Installation
If you have python installed you can:

### For windows
Clone this repository

`cd Checkers`

`py -m venv env`  

`.\env\Scripts\activate`

`py -m pip install -r requirements`

`py main.py`

Or you can download zip file from releases

Just extract files and run main.exe

I will try to add packages for linux

You can also try to create your own. After cloning this repo and installing requirements install pyinstaller

`pip3 install pyinstaller`

and type this command: `pyinstaller --noconsole --add-data "checkers/assets/crown.png;./checkers/assets" main.py
` 

dist folder will appear and in this folder you will find main folder and there will be main.exe


