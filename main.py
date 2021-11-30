#!/usr/bin/env python3

import new
import submit
import sys
import webbrowser
import config_kattis

def _print_commands():
  print('usage: meow <command>\n\ncommands:')
  print('\tnew')
  print('\tsubmit')
  print('\tbrowser')

def open_browser():
    config = config_kattis.load_kattis_config()
    webbrowser.open(f'https://{config.hostname}')


def main():
    if len(sys.argv) == 1:
      _print_commands()
      sys.exit(1)

    command = sys.argv[1]

    if command == 'new':
      new.new_problem()
    elif command == 'browser':
      open_browser()
    elif command == 'submit':
      submit.submit_problem()
    else:
      _print_commands()
      sys.exit(1)

if __name__ == '__main__': main()

