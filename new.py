
from config_kattis import load_kattis_config
from config_meow import *
from typing import *
from nix_utils import *
from argparse import ArgumentParser, Namespace
from header import header
from sys import exit


def _parse_args() -> Namespace:
  parser = ArgumentParser(prog='meow', description='Start a new problem, language is derived from template')
  parser.add_argument('new')
  parser.add_argument('problem')
  parser.add_argument('-t', '--template')
  parser.add_argument('-e', '--editor')
  return parser.parse_args()


def _template_if_exists(config: MeowConfig, args: Namespace) -> str:
  template = config.templates[config.default_template]

  if args.template: 
    template = config.templates[args.template]
  if not exists(template): 
    raise FileNotFoundError(f'{template} does not exist')

  return template
    

def _ensure_problem_dir(config: MeowConfig) -> str:
  if not exists(config.problem_directory): 
    mkdir(config.problem_directory)

  return config.problem_directory


def _init_problem_or_old_file(config: MeowConfig, args: Namespace, template: str) -> str:
  _ensure_problem_dir(config)

  file_ext = ext(template)
  filedir = f'{config.problem_directory}/{args.problem}'
  if not exists(filedir): 
    mkdir(filedir)

  filename = f'{filedir}/{args.problem}{file_ext}'

  if not exists(filename):
    with open(filename, 'wb') as problem_stream:
        with open(template, 'rb') as template_stream:
            problem_stream.write(template_stream.read())
    return filename

  else:
    print(f'{filename} alread exists, not writing template..\n\n\t[e|E]xit\n\t[o|O]pen file in editor')
    ans = input()
    if ans.lower().startswith('o'): 
      return filename
    else: 
      exit(0)


def new_problem() -> None:
  config       =  load_meow_config()
  args         = _parse_args()
  editor       =  args.editor if args.editor else config.editor
  template     = _template_if_exists(config, args)
  problem_file = _init_problem_or_old_file(config, args, template)

  if editor.split(' ')[0].split('\\')[-1] in ['vim', 'nvim', 'nano', 'emacs', 'ne', 'tilde']:
    os.system(f'{editor} {problem_file}')
  else:
    os.system(f'{editor} {problem_file} &> /dev/null &')


if __name__ == '__main__':
  print(header)
  new_problem()
