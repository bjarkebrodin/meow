
from dataclasses import dataclass
from typing import *
from nix_utils import *
from configparser import ConfigParser

KATTIS_RC_PATH = f'{HOME}/.kattisrc'

class KattisrcNotFoundException(Exception): pass
class KattisrcInvalidException(Exception): pass


_config_kattis = None


@dataclass
class KattisConfig:
  username: str
  hostname: str
  loginurl: str
  submissionurl: str
  submissionsurl: str
  token: str = None
  password: str = None


def load_kattis_config() -> KattisConfig :
  global _config_kattis

  if _config_kattis is not None:
    return _config_kattis

  try:
    parser = ConfigParser()
    parser.read(KATTIS_RC_PATH)
    _config_kattis = KattisConfig (
      username       = parser.get('user', 'username'),
      token          = parser.get('user', 'token'),
      hostname       = parser.get('kattis', 'hostname'),
      loginurl       = parser.get('kattis', 'loginurl'),
      submissionurl  = parser.get('kattis', 'submissionurl'),
      submissionsurl = parser.get('kattis', 'submissionsurl'),
    )
  except FileNotFoundError:
    raise KattisrcNotFoundException
  except:
    raise KattisrcInvalidException

  return _config_kattis


if __name__ == '__main__':
  print('Local Config:')
  _config = load_kattis_config()
  print(_config)
