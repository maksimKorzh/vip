#!/bin/python3
import curses, json, sys, os, time
from copy import deepcopy
def main(stdscr):
  s = curses.initscr(); s.nodelay(1)
  curses.noecho(); curses.raw(); mod = 'n'; b = []; bf = []; bu = []
  src = 'noname.txt'; d = -1; sch = ''; rst = []; si = 0 
  R, C = s.getmaxyx(); R -= 1; x, y, r, c = [0] * 4; t = ''
  if len(sys.argv) == 2:
    src = sys.argv[1]
    with open(sys.argv[1]) as f:
      cont = f.read().split('\n'); cont = cont[:-1] if len(cont) > 1 else cont
      for rw in cont: b.append([ord(c) for c in rw])
  d += 1; bu.insert(d, [deepcopy(b), [r, c]])
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
    stat = mod + ' "' + src  + '" line ' + str(r+1)
    try: stat += ' of ' + str(len(b)) + ' --' + str(int(((r+1)*100/(len(b))))) + '%--'
    except: pass
    stat += ' col ' + str(c)
    s.addstr(stat); s.clrtoeol()
    curses.curs_set(0);
    s.move(r - y, c - x)
    curses.curs_set(1); s.refresh(); ch = -1
    while (ch == -1): ch = s.getch()
    if ch == curses.KEY_RESIZE: R, C = s.getmaxyx(); R -= 1; s.refresh(); y = 0
    if chr(ch).isdigit() and chr(ch) != '0' and mod not in 'irR': t += chr(ch);
    elif mod == 'n':
      if ch == ord('i'): mod = 'i'
      elif ch == ord('a'): c += 1; mod = 'i'
      elif ch == ord('A'): c = len(b[r]); mod = 'i'
      elif ch == ord('o'): b.insert(r+1, []); r += 1; mod = 'o'
      elif ch == ord('O'): b.insert(r, []); mod = 'O'
      elif ch == ord('r'): mod = 'r'
      elif ch == ord('R'): mod = 'R'
      elif ch == ord('x') and len(b[r]): del b[r][c]
      elif ch == ord('G'): r = int(t)-1 if len(t) and int(t)-1 < len(b) else len(b)-1
      elif ch == ord('g'): mod = 'g'
      elif ch == ord('0'):
        if t == '': c = 0
        else: t += chr(ch)
      elif ch == ord('$'):
        if len(t): r = r + int(t)-1 if (r + int(t)-1) < len(b) else r
        c = len(b[r])-1
      elif ch == ord('d'): mod = 'd'
      elif ch == ord('y'): mod = 'y'
      elif ch == ord('p'):
       for l in bf:
         if len(b) > 1: r += 1
         b.insert(r, deepcopy(l))
       d += 1; bu.insert(d, [deepcopy(b), [r, c]])
      elif ch == ord('u'):
        if d >= 1: d -= 1; b = deepcopy(bu[d][0]); r, c = bu[d][1]
      elif ch == (ord('r') & 0x1f):
        if d < len(bu)-1: d += 1; b = deepcopy(bu[d][0]); r, c = bu[d][1]
      elif ch == ord('h'): c -= 1 if c else 0 
      elif ch == ord('l'): c += 1 if c < len(b[r])-1 else 0 
      elif ch == ord('k'): r -= 1 if r else 0
      elif ch == ord('j'): r += 1 if r < len(b)-1 else 0
      rw = b[r] if r < len(b) else None
      lrw = len(rw) if rw is not None else 0
      if c > lrw-1: c = lrw-1 if lrw else lrw
      if ch == ord('A'): c = lrw
      if ch != ord('0') and mod not in 'dy': t = ''
    elif mod in 'ioO':
      if ch == 27: mod = 'n'; c -= 1 if c else 0
      elif ch != ((ch) & 0x1f) and ch < 128: b[r].insert(c, ch); c += 1;
      elif ch == ord('\n'): l = b[r][c:]; b[r] = b[r][:c]; r += 1; c = 0; b.insert(r, [] + l)
      elif ch == curses.KEY_BACKSPACE:
        if c: c -= 1; del b[r][c]
        elif r: l = b[r][c:]; del b[r]; r -= 1; c = len(b[r]); b[r] += l
    elif mod == 'r':
      try: b[r][c] = ch
      except: pass
      mod = 'n'
    elif mod == 'R':
      if ch == 27: mod = 'n'; c -= 1 if c else 0
      elif ch != ((ch) & 0x1f) and ch < 128: b[r][c] = ch; c += 1;
      elif ch == curses.KEY_BACKSPACE: c -= 1 if c else 0
    elif mod == 'g': r = 0; c = 0; mod = 'n' 
    elif mod == 'd':
      if ch == ord('d'):  
        bf = []; ln = 0
        num = int(t) if len(t) else 1
        for i in range(num):
          if len(b) == 1 and b[0] == []: break
          bf.append(b[r]); ln += 1
          if len(b) > 1: del b[r]
          elif len(b) == 1: b[r] = []
          if r and r == len(b): r -= 1; c = 0
      mod = 'n'; t = ''; s.move(R, 0)
    elif mod == 'y':
      if ch == ord('y'):  
        bf = []; ln = 0
        num = int(t) if len(t) else 1
        for i in range(num):
          if r+i >= len(b): break
          bf.append(b[r+i])
          ln += 1
      mod = 'n'; t = ''; s.move(R, 0)
    if (ch != 27 and mod in 'irRdoOyd'): d += 1; bu.insert(d, [deepcopy(b), [r, c]])
    if ch == (ord('q') & 0x1f): sys.exit();
os.environ.setdefault('ESCDELAY', '25')
curses.wrapper(main)
