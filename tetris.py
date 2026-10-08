# Tetris for the TI-84 Evo
# Keys: left/right = move, up = turn, hold down = fall fast,
#       enter = drop, 2nd or mode = pause, clear = quit
import random
from ti_draw import clear, set_color, fill_rect, draw_text
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
dirty = [False]                # something new was drawn

def paint(always=False):
    if paint_buffer and (always or dirty[0]):
        paint_buffer()
    dirty[0] = False
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 320, 240
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key

# On the Evo get_key wants one number. Find out once at the start,
# because an error on every key check makes the game slow.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    import gc
except:
    gc = None
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep

# Key numbers. The Evo uses the second number in each pair
# (down = 34 and enter = 105 are tested). The last key number
# shows on screen, so wrong ones are easy to fix.
LEFT = (2, 24)
RIGHT = (1, 26)
TURN = (3, 25)
DOWN = (4, 34)
DROP = (5, 105)
PAUSE = (21, 22)              # 2nd, mode
QUIT = (9, 45)
HOLD = 4                      # steps of fast fall per down press

W, H = 10, 20                 # board size in cells
C = (SH - 20) // H            # cell size in pixels
X0 = (SW - W * C) // 2 - 40   # board left edge
Y0 = (SH - H * C) // 2        # board top edge
TX = X0 + W * C + 12          # text column

# Pieces as 4 cells around (0, 0). y goes down.
PIECES = [
    [(-1, 0), (0, 0), (1, 0), (2, 0)],    # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],     # O
    [(-1, 0), (0, 0), (1, 0), (0, 1)],    # T
    [(0, 0), (1, 0), (-1, 1), (0, 1)],    # S
    [(-1, 0), (0, 0), (0, 1), (1, 1)],    # Z
    [(-1, 0), (0, 0), (1, 0), (1, 1)],    # J
    [(-1, 0), (0, 0), (1, 0), (-1, 1)]]   # L
COLORS = [(0, 0, 0), (0, 200, 220), (230, 200, 0), (160, 0, 200),
          (0, 190, 0), (220, 0, 0), (0, 60, 230), (240, 130, 0),
          (70, 70, 70)]
GHOST = 8                     # grey shadow where the piece will land
POINTS = [0, 100, 300, 700, 1500]    # for 1, 2, 3, 4 lines (x level)

board = [[0] * W for y in range(H)]

def cell(x, y, c):
    dirty[0] = True
    set_color(*COLORS[c])
    fill_rect(X0 + x * C, Y0 + y * C, C - 1, C - 1)

def fits(cells, px, py):
    for x, y in cells:
        x, y = x + px, y + py
        if x < 0 or x >= W or y >= H:
            return False
        if y >= 0 and board[y][x]:
            return False
    return True

def ghost_y(cells, px, py):
    while fits(cells, px, py + 1):
        py += 1
    return py

# Screen squares of a piece and its ghost: {(x, y): color}
def piece_map(cells, px, py, c):
    m = {}
    gy = ghost_y(cells, px, py)
    for x, y in cells:
        m[(x + px, y + gy)] = GHOST
    for x, y in cells:
        m[(x + px, y + py)] = c
    return m

# Only draw the squares that changed (much faster than drawing all)
def redraw(old, new):
    for xy in old:
        if xy not in new and xy[1] >= 0:
            cell(xy[0], xy[1], 0)
    for xy in new:
        if old.get(xy) != new[xy] and xy[1] >= 0:
            cell(xy[0], xy[1], new[xy])

def turn(cells, p):
    if p == 1:                 # O does not turn
        return cells
    return [(-y, x) for x, y in cells]

def text(row, s):
    dirty[0] = True
    set_color(0, 0, 0)
    fill_rect(TX, Y0 + row * 20, SW - TX, 18)
    set_color(255, 255, 255)
    draw_text(TX, Y0 + row * 20 + 14, s)

# Score panel: wipe the whole top of the side panel (up to the screen edge,
# so tall letters leave nothing behind), then write all 4 lines again
def stats(score, lines, level, best):
    dirty[0] = True
    set_color(0, 0, 0)
    fill_rect(TX, 0, SW - TX, Y0 + 80)
    set_color(255, 255, 255)
    rows = ["Score " + str(score), "Lines " + str(lines),
            "Level " + str(level), "Best " + str(best)]
    for i in range(4):
        draw_text(TX, Y0 + i * 20 + 14, rows[i])

def draw_all():
    for y in range(H):
        for x in range(W):
            cell(x, y, board[y][x])

def draw_next(p):
    set_color(0, 0, 0)
    fill_rect(TX, Y0 + 100, 5 * C, 3 * C)
    for x, y in PIECES[p]:
        set_color(*COLORS[p + 1])
        fill_rect(TX + (x + 1) * C, Y0 + 100 + y * C, C - 1, C - 1)

def clear_lines():
    full = [y for y in range(H) if 0 not in board[y]]
    for y in full:
        del board[y]
        board.insert(0, [0] * W)
    return len(full)

def wait_for(keys):
    paint(True)
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# High score lives in the calculator list TETRS, so it stays after quitting
def load_best():
    try:
        return int(recall_list("TETRS")[0])
    except:
        return 0

def save_best(n):
    try:
        store_list("TETRS", [n])
    except:
        pass

def start_screen(best):
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    x = SW // 2 - 70
    for i in range(6):                    # title in piece colors
        set_color(*COLORS[i + 1])
        draw_text(x + 30 + i * 14, 20, "TETRIS"[i])
    set_color(255, 255, 255)
    draw_text(x, 45, "Best " + str(best))
    help = ["LEFT RIGHT: move", "UP: turn", "DOWN: hold = fast",
            "ENTER: drop", "2ND: pause", "CLEAR: quit"]
    for i in range(len(help)):
        draw_text(x, 72 + i * 20, help[i])
    set_color(230, 200, 0)
    draw_text(x, 195, "ENTER: start")
    return wait_for(DROP + QUIT) in DROP

def main(best):
    for y in range(H):
        board[y] = [0] * W
    clear()
    set_color(0, 0, 0)
    fill_rect(0, 0, SW, SH)
    set_color(120, 120, 120)
    fill_rect(X0 - 2, Y0 - 2, W * C + 3, H * C + 3)
    draw_all()
    score, lines, level = 0, 0, 1
    stats(0, 0, 1, best)
    text(4, "Next:")
    nxt = random.randrange(7)
    while True:
        p, nxt = nxt, random.randrange(7)
        draw_next(nxt)
        cells, px, py = PIECES[p], 4, 0
        if not fits(cells, px, py):
            break                       # no room: game over
        if gc:
            gc.collect()                # tidy memory now, not mid-move
        now = piece_map(cells, px, py, p + 1)
        redraw({}, now)
        t, fast = 0, 0
        while True:
            k = key()
            if not k:
                pass                    # no key: skip all the checks
            elif k in QUIT:
                return score, lines, level, True
            elif k in PAUSE:
                text(7, "PAUSED")
                text(8, "2ND: go on")
                if wait_for(PAUSE + DROP + QUIT) in QUIT:
                    return score, lines, level, True
                text(7, "")
                text(8, "")
            elif k in DOWN:
                fast = HOLD                         # fall fast while held
            elif k in DROP:
                ny = ghost_y(cells, px, py)
                score += 2 * (ny - py)             # 2 points per row dropped
                py = ny
                new = piece_map(cells, px, py, p + 1)
                redraw(now, new)
                now = new
                t = 99
            else:
                nc, nx = cells, px
                if k in LEFT:
                    nx -= 1
                elif k in RIGHT:
                    nx += 1
                elif k in TURN:
                    nc = turn(cells, p)
                    for kick in (0, -1, 1, -2, 2):  # push off the wall
                        if fits(nc, px + kick, py):
                            nx = px + kick
                            break
                if fits(nc, nx, py):
                    cells, px = nc, nx
                    new = piece_map(cells, px, py, p + 1)
                    redraw(now, new)
                    now = new
            t += 1
            if fast or t >= max(1, 11 - level):    # time to fall
                t = 0
                if not fits(cells, px, py + 1):
                    break                           # landed
                if fast:
                    fast -= 1
                    score += 1                      # 1 point per fast row
                py += 1
                new = piece_map(cells, px, py, p + 1)
                redraw(now, new)
                now = new
            paint()
            sleep(0.03)
        for x, y in cells:
            if y + py >= 0:
                board[y + py][x + px] = p + 1
        n = clear_lines()
        if n:
            lines += n
            score += POINTS[n] * level
            level = 1 + lines // 10
            draw_all()
        stats(score, lines, level, best)
    return score, lines, level, False

best = load_best()
if start_screen(best):
    while True:
        score, lines, level, quit = main(best)
        if score > best:
            best = score
            save_best(best)
            stats(score, lines, level, best)
            text(7, "NEW BEST!")
        else:
            text(7, "GAME OVER")
        if quit:
            break
        text(8, "ENTER: again")
        text(9, "CLEAR: quit")
        if wait_for(DROP + QUIT) in QUIT:
            break
paint(True)                    # show the last screen before quitting
