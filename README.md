# Tetris for the TI-84 Evo-T

A colour Tetris game for the **TI-84 Evo-T** graphing calculator, written in Python.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- 7 coloured pieces
- **Ghost piece**: a grey shadow shows where the piece will land
- **Next** piece preview
- Score, lines and levels: every 10 lines the pieces fall faster
- **High score** that stays saved after you quit
- Start screen, pause and "play again"
- No flicker

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`tetris.py`](tetris.py) from this repo

## Setup

1. Download [`tetris.py`](tetris.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `tetris.py` onto the page to send it to the calculator.
6. **Choose RAM, not Archive.**
   The Python app on the Evo-T does not show files that are in Archive.

> **Already sent it to Archive?** On the calculator press **2nd → mem → Mem Management**,
> find **TETRIS** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **TETRIS** and run it.
3. Press **enter** on the start screen.

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ | Move left / right |
| ▲ | Turn the piece |
| ▼ | Fall fast for a moment (tap again to keep going) |
| enter | Drop the piece to the bottom |
| 2nd or mode | Pause (2nd or enter to go on) |
| clear | Quit |

## Points

| Action | Points |
|---|---|
| ▼ fast fall | 1 per row |
| enter drop | 2 per row |
| 1 line | 100 × level |
| 2 lines | 300 × level |
| 3 lines | 700 × level |
| 4 lines | 1500 × level |

## High score

The best score is saved in a calculator list called **TETRS**, so it stays after you quit.

- To reset the high score, delete the list **TETRS** in **2nd → mem → Mem Management**.
- A calculator reset (RAM clear) also resets it.

## Good to know

- Files in RAM are deleted when the calculator resets. Keep `tetris.py` on your computer
  so you can send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
