
import os

def _expand(path):
  return os.path.abspath(
         os.path.expandvars(
         os.path.expanduser(path)))

def _expanded(g): 
  def f(*args, **kwargs):
    return g(_expand(*args, **kwargs))
  return f


HOME = os.path.expanduser('~')


def ext(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[1]


def pwd(): 
  return os.getcwd()


@_expanded
def exists(path):
  return os.path.exists(path)


@_expanded
def isfile(path):
  return os.path.isfile(path)


@_expanded  
def isdir(path):
  return os.path.isdir(path)


@_expanded
def islink(path):
  return os.path.islink(path)


@_expanded
def cd(path): 
  if os.path.isdir(path):
    os.chdir(path)
  else:
    raise NotADirectoryError(f'{path} is not a directory')


@_expanded
def touch(path):
  if not os.path.isdir(path):
    open(path, 'a').close()
  else:
    raise IsADirectoryError(f'{path} is a directory')


@_expanded
def mkdir(path):
  return os.mkdir(path)


def ls(path=None):
  def _ls_no_path(): return os.listdir()

  @_expanded 
  def _ls(path): return os.listdir(path)

  if path is None:
    return _ls_no_path()
  else:
    return _ls(path)


def rm(path, r=False): 

  @_expanded
  def _rm(_path):
    if isdir(path) and r == True:
      for child in ls(path): 
        rm(os.path.join(path, child), True)
  
    if isdir(path):
      os.rmdir(path)
    else:
      os.remove(path)

  return _rm(path)
