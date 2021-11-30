
import re
import time
import header
import kattis_client as kattis

from nix_utils import *
from config_meow import *
from argparse import ArgumentParser, Namespace


# Credit for this goes to of https://github.com/Kattis/kattis-cli/blob/master/submit.py
def _parse_args() -> Namespace:
  parser = ArgumentParser(prog='meow', description='Submit a solution to Kattis')
  parser.add_argument('submit')
  parser.add_argument('-p', '--problem')
  parser.add_argument('-m', '--mainclass')
  parser.add_argument('-l', '--language')
  parser.add_argument('files', nargs='+')
  return parser.parse_args()


def _problem_name_or_guess(args: Namespace) -> str:
  if args.problem is not None: 
    return args.problem
  return args.files[0].split('.')[0]


def _language_or_guess(config: MeowConfig, args: Namespace) -> str:
  if args.language is not None:
    return args.language
  return config.language_guesses[ext(args.files[0])]


# Credit for this goes to of https://github.com/Kattis/kattis-cli/blob/master/submit.py
def _guess_mainfile(language: str, files: List[str]):
    for filename in files:
        if os.path.splitext(os.path.basename(filename))[0] in ['main', 'Main']:
            return filename
    for filename in files:
        try:
            with open(filename) as f:
                conts = f.read()
                if language in ['Java', 'Rust', 'Scala', 'Kotlin'] and re.search(r' main\s*\(', conts):
                    return filename
                if language == 'Pascal' and re.match(r'^\s*[Pp]rogram\b', conts):
                    return filename
        except IOError:
            pass
    return files[0]


# Credit for this goes to of https://github.com/Kattis/kattis-cli/blob/master/submit.py
def _guess_mainclass(config, language: str, files: List[str]):
    if language in config.mainfile_languages and len(files) > 1:
        return os.path.basename(_guess_mainfile(language, files))
    if language in config.mainclass_languages:
        mainfile = os.path.basename(_guess_mainfile(language, files))
        name = os.path.splitext(mainfile)[0]
        if language == 'Kotlin':
            return name[0].upper() + name[1:] + 'Kt'
        return name
    return None


def _adjust_file_paths(files: List[str], problem: str, config: MeowConfig):
  adjusted_files = []
  for file in files:
    if os.path.expanduser(file).startswith('/'):
      adjusted_files.append(file)
    else:
      adjusted_files.append(f'{config.problem_directory}/{problem}/{os.path.basename(file)}')
  return adjusted_files


def _track_status(get_status):
  finished = False
  latest = 0

  while(not finished):
    time.sleep(0.2)

    status: kattis.SubmissionTracker = get_status() 

    if len(status.answers) > 0:
      for i in range(latest, min(status.index, len(status.answers))):
        ans = status.answers[i]
        if ans: print(' \u2713', end='', flush=True)
        else  : print(' \u274C', end='', flush=True)
        if (i+1) % 19 == 0: print(flush=True)
      latest = status.index

    finished = status.is_done()
    if finished:
      print()
      print(status.message)


def submit_problem():

  config = load_meow_config()
  args = _parse_args()
  language = _language_or_guess(config, args)
  mainclass = _guess_mainclass(config, language, args.files)
  problem = _problem_name_or_guess(args)
  files = _adjust_file_paths(args.files, problem, config)

  print()
  print(f'Submitting {problem}') 
  print(f'Language: {language}\n') 
  print(header.header)

  # filestring = "\n\t".join(files)
  # print(f'Files submitted: \n\t{filestring}\n') 

  return _track_status(kattis.submit(problem, language, mainclass, files))


if __name__ == '__main__':
  submit_problem()
