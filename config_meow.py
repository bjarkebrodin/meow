
from dataclasses import dataclass
from typing import *
from yaml import safe_load
from config_meow_default import config as default_config
from nix_utils import *

CONFIG_PATH = f'{HOME}/.meow.yaml'
_meow_config = None

class MeowConfigInvalidException(Exception): pass


@dataclass
class MeowConfig:
  problem_directory: str
  editor: str
  default_template: str
  templates: Dict[str, str]
  language_guesses: Dict[str, str]
  mainfile_languages: Dict[str, str]
  mainclass_languages: Dict[str, str]


def _parse_yaml(path: str) -> None:
  with open(path, "r") as stream: 
      return safe_load(stream)


def _ensure_config() -> None:
  try :
    _dump_config()
  except :
    pass


def _dump_config() -> None:

  if exists(CONFIG_PATH):
    raise FileExistsError(f'{CONFIG_PATH} already exists, aborting...')

  with open(CONFIG_PATH, "w") as stream:
    stream.write(default_config)


def load_meow_config() -> MeowConfig:
  global _meow_config

  if _meow_config is not None:
    return _meow_config

  _ensure_config()

  try :
    parsed = _parse_yaml(CONFIG_PATH)
    _meow_config = MeowConfig(
      problem_directory = parsed['problem_directory'],
      editor = parsed['editor'],
      default_template = parsed['default_template'],
      templates = parsed['templates'],
      language_guesses = parsed['language_guesses'],
      mainfile_languages = parsed['mainfile_languages'],
      mainclass_languages = parsed['mainclass_languages'],
    )
    return _meow_config

  except :
    raise MeowConfigInvalidException


if __name__ == '__main__':
  print('local config:\n')
  print(load_meow_config())
