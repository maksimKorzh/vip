#!/bin/python3
import curses, json, sys, os, time
from copy import deepcopy
def main(stdscr):
  s = curses.initscr(); s.nodelay(1)
  curses.noecho(); curses.raw(); mod = 'n'; b = []; bf = []
  src = 'noname.txt'; d = 0; sch = ''; rst = []; si = 0 
  R, C = s.getmaxyx(); R -= 1; x, y, r, c = [0] * 4; t = ''
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
    stat = mod + ' "' + src  + '" line ' + str(r+1) + ' of '
    stat += str(len(b)) + ' --' + str(int(((r+1)*100/(len(b)-1)))) + '%-- ' + 'col ' + str(c)
    s.addstr(stat); s.clrtoeol()
    curses.curs_set(0);
    s.move(r - y, c - x)
    curses.curs_set(1); s.refresh(); ch = -1
    while (ch == -1): ch = s.getch(); d += 1
    if ch == curses.KEY_RESIZE: R, C = s.getmaxyx(); R -= 1; s.refresh(); y = 0
    if chr(ch).isdigit() and chr(ch) != '0' and mod not in 'irR': t += chr(ch);
    elif mod == 'n':
      if ch == ord('i'): mod = 'i'
      elif ch == ord('a'): c += 1; mod = 'i'
      elif ch == ord('A'): c = len(b[r]); mod = 'i'
      elif ch == ord('o'): b.insert(r+1, []); r += 1; mod = 'i'
      elif ch == ord('O'): b.insert(r, []); mod = 'i'
      elif ch == ord('r'): mod = 'r'
      elif ch == ord('R'): mod = 'R'
      elif ch == ord('x') and len(b[r]): del b[r][c]
      elif ch == ord('G'): r = int(t) if len(t) and int(t) < len(b) else len(b)-1
      elif ch == ord('g'): mod = 'g'
      elif ch == ord('w'):
        if b[r][c] == ord(' '):
          while 1:
            c += 1
            if c >= len(b[r])-1:
              if r < len(b)-1: r += 1; c = 0
              break
            if b[r][c] != ord(' '): break
        else:
          while 1:
            c += 1
            if c >= len(b[r])-1:
              if r < len(b)-1: r += 1; c = 0
              break
            if not chr(b[r][c]).isalpha() or b[r][c] == ord(' '):
              while 1:
                c += 1
                if c >= len(b[r])-1:
                  if r < len(b)-1: r += 1; c = 0
                  break
                if chr(b[r][c]).isalpha(): break
              break
      elif ch == ord('e'):
        if b[r][c] == ord(' '):
          while 1:
            c += 1
            if c >= len(b[r])-1:
              if r < len(b)-1: r += 1; c = 0
              break
            if b[r][c] != ord(' '):
              while 1:
                c += 1
                if c >= len(b[r])-1:
                  if r < len(b)-1: r += 1; c = 0
                  break
                if not chr(b[r][c+1]).isalpha(): break
              break
        else:
          while 1:
            c += 1
            if c >= len(b[r])-1:
              if r < len(b)-1: r += 1; c = 0
              break
            if not chr(b[r][c+1]).isalpha(): break
      elif ch == ord('0'):
        if t == '': c = 0
        else: t += chr(ch)
      elif ch == ord('$'):
        if len(t): r = r + int(t)-1 if (r + int(t)-1) < len(b) else r
        c = len(b[r])-1

      elif ch == ord('h'): c -= 1 if c else 0 
      elif ch == ord('l'): c += 1 if c < len(b[r])-1 else 0 
      elif ch == ord('k'): r -= 1 if r else 0
      elif ch == ord('j'): r += 1 if r < len(b)-1 else 0
      rw = b[r] if r < len(b) else None
      lrw = len(rw) if rw is not None else 0
      if c > lrw-1: c = lrw-1 if lrw else lrw
      if ch == ord('A'): c = lrw
      if ch != ord('0'): t = ''
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
    elif mod == 'g': r = 0; col = 0; mod = 'n' 
    if ch == (ord('q') & 0x1f): sys.exit()
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)
