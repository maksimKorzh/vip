#!/bin/python3
import curses, json, sys, os, time
from copy import deepcopy
def main(stdscr):
  s = curses.initscr(); s.nodelay(1)
  curses.noecho(); curses.raw(); mod = 'n'; b = []; bf = []
  src = 'noname.txt'; d = 0; sch = ''; rst = []; si = 0 
  R, C = s.getmaxyx(); R -= 1; x, y, r, c = [0] * 4
  if len(sys.argv) == 2:
    src = sys.argv[1]
    with open(sys.argv[1]) as f:
      cont = f.read().split('\n'); cont = cont[:-1] if len(cont) > 1 else cont
      for rw in cont: b.append([ord(c) for c in rw])
  while(True):
    s.move(0, 0)
    if r < y: y = r
    if r >= y + R: y = r - R+1
    if c < x: x = c
    if c >= x + C: x = c - C+1
    for rw in range(R):
      brw = rw + y
      for cl in range(C): 
        bcl = cl + x
        try: s.addch(rw, cl, b[brw][bcl])
        except: pass 
      s.clrtoeol()
      try: s.addch('\n')
      except: pass
    curses.curs_set(0);
    s.move(r - y, c - x)
    curses.curs_set(1); s.refresh(); ch = -1
    while (ch == -1): ch = s.getch(); d += 1
    if ch == curses.KEY_RESIZE: R, C = s.getmaxyx(); R -= 1; s.refresh(); y = 0
    if mod == 'n':
      if ch == ord('i'): mod = 'i'
      elif ch == ord('a'): c += 1; mod = 'i'
      elif ch == ord('A'): c = len(b[r]); mod = 'i'
      elif ch == ord('o'): b.insert(r+1, []); r += 1; mod = 'i'
      elif ch == ord('O'): b.insert(r, []); mod = 'i'
      elif ch == ord('r'): mod = 'r'
      elif ch == ord('R'): mod = 'R'
      elif ch == ord('0'): c = 0
      elif ch == ord('$'): c = len(b[r])-1
      elif ch == ord('x') and len(b[r]): del b[r][c]

      elif ch == ord('h'): c -= 1 if c else 0 
      elif ch == ord('l'): c += 1 if c < len(b[r])-1 else 0 
      elif ch == ord('k'): r -= 1 if r else 0
      elif ch == ord('j'): r += 1 if r < len(b)-1 else 0
      rw = b[r] if r < len(b) else None
      lrw = len(rw) if rw is not None else 0
      if c > lrw-1: c = lrw-1 if lrw else lrw
    elif mod == 'i':
      if ch == 27: mod = 'n'; c -= 1 if c else 0
      elif ch != ((ch) & 0x1f) and ch < 128: b[r].insert(c, ch); c += 1;
      elif ch == ord('\n'): l = b[r][c:]; b[r] = b[r][:c]; r += 1; c = 0; b.insert(r, [] + l)
      elif ch == curses.KEY_BACKSPACE:
        if c: c -= 1; del b[r][c]
        elif r: l = b[r][c:]; del b[r]; r -= 1; c = len(b[r]); b[r] += l
    elif mod == 'r': b[r][c] = ch; mod = 'n'
    elif mod == 'R':
      if ch == 27: mod = 'n'; c -= 1 if c else 0
      elif ch != ((ch) & 0x1f) and ch < 128: b[r][c] = ch; c += 1;
      elif ch == curses.KEY_BACKSPACE: c -= 1 if c else 0
  
    if ch == (ord('q') & 0x1f): sys.exit()
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)
