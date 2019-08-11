#!/usr/bin/python3
# author: Mats Nilsson

import pigpio
import time
import sys
from collections import Counter

pi = pigpio.pi()

T = 255
t0 = 0
t1 = 0
tx_gpio = 17
rx_gpio = 27

pi.set_mode(rx_gpio, pigpio.INPUT) # set GPIO 15 as an input
pi.set_mode(tx_gpio, pigpio.OUTPUT) # set GPIO 14 as an output

msg = []
msg_start = False
msg_list = []

# SYNC
sync_wf = []
sync_wf.append(pigpio.pulse(1<<tx_gpio, 0, T))
sync_wf.append(pigpio.pulse(0, 1<<tx_gpio, 10*T))
# 1
one_wf = []
one_wf.append(pigpio.pulse(1<<tx_gpio, 0, T))
one_wf.append(pigpio.pulse(0, 1<<tx_gpio, 1*T))
# 0
zero_wf = []
zero_wf.append(pigpio.pulse(1<<tx_gpio, 0, T))
zero_wf.append(pigpio.pulse(0, 1<<tx_gpio, 5*T))
# P
pause_wf = []
pause_wf.append(pigpio.pulse(1<<tx_gpio, 0, T))
pause_wf.append(pigpio.pulse(0, 1<<tx_gpio, 40*T))

def decode(pulselength):
  if pulselength == 2:
    return "1"
  elif pulselength == 6:
    return "0"
  elif pulselength == 11 or pulselength == 12:
    return "S"
  elif pulselength >= 41 and pulselength <= 43:
    return "P"
  else:
    return "X"

def rx_callback(gpio, level, tick):
  global t0, t1, msg, msg_start
  t1 = tick
  pulse = abs((t1 - t0)) / T
  c = decode(round(pulse))
  if c == "S":
    msg_start = True
  if c == "P":
    msg.append(c)
    tmp_msg = "".join(msg)
    if len(tmp_msg) > 5:
      msg_list.append(tmp_msg)
      print(msg_list[-1])
    msg_start = False
    msg = []
  if msg_start:
    msg.append(c)
  t0 = t1

def tx(word):
  global sync_wf, one_wf, zero_wf, pause_wf
  wf = []
  for c in word:
    if c == "S":
      wf.extend(sync_wf)
    elif c == "1":
      wf.extend(one_wf)
    elif c == "0":
      wf.extend(zero_wf)
    elif c == "P":
      wf.extend(pause_wf)
    else:
      print("this is bad")

  pi.wave_add_generic(wf)
  wave = pi.wave_create()

  for x in range(1,6):
    print("Sending wave {0}...".format(x))
    pi.wave_send_once(wave)
    time.sleep(0.1)

if len(sys.argv) > 1:
  tx(sys.argv[1])
else:
  cb1 = pi.callback(rx_gpio, pigpio.RISING_EDGE, rx_callback)
  time.sleep(15)

  print("Most likely string:")
  c = Counter(msg_list)
  print(c.most_common(1))
