
#
# The MIT License (MIT)
#
# Copyright (c) 2006-2015 Kattis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import re
import json
from requests import get, post
from requests.models import *
from config_kattis import *
from dataclasses import dataclass


_config = load_kattis_config()

ERROR = 8
WRONG = 14
SUCCESS = 16

@dataclass
class SubmissionTracker:
  status: int
  index: int
  message: str
  answers: List[bool]

  def is_done(self): return self.status > 5


def _login_args():
  login_args = {'user': _config.username, 'script': 'true'}
  if _config.password is not None: 
    login_args['password'] = _config.password
  if _config.token is not None: 
    login_args['token'] = _config.token
  return login_args


def _login():
  response = post(
    _config.loginurl,
    data=_login_args(), 
    headers={'User-Agent': 'kattis-cli-submit'}
  )

  if response.status_code == 200:
    return response.cookies
  if response.status_code == 403:
    raise HTTPError(f'Incorrect username or password/token for {_config.loginurl}')
  if response.status_code == 404:
    raise HTTPError(f'Incorrect login url: {_config.loginurl}')
  else:
    raise HTTPError(f'{response.status_code}\n{response.content}')


# Credit for this goes to of https://github.com/Kattis/kattis-cli/blob/master/submit.py
def _concat_files(files):
  sub_files = []
  for f in files:
      with open(f) as sub_file:
          sub_files.append(('sub_file[]',
                            (os.path.basename(f),
                            sub_file.read(),
                            'application/octet-stream')))
  return sub_files


def _status(status_url, cookies, tracker) -> SubmissionTracker:
  response = post(status_url, cookies=cookies, headers={'User-Agent': 'kattis-cli-submit'})
  content = json.loads(response.content.decode('utf-8'))
  status_id = int(content['status_id'])
  test_index = int(content['testcase_index'])

  tracker.status = status_id
  tracker.index = test_index

  if status_id == SUCCESS:
    tracker.message = "\nSubmission Accepted!"
    feedback = content['row_html']
    p = re.compile(r'cpu">(?P<time>.+?)<')
    m = p.search(feedback)
    if m is not None:
        tracker.message = f'{tracker.message}\nCPU Time: {m.group("time").replace("&nbsp;","")}'

    #fixme: do this more elegantly when time pls
    if test_index > 0:
        pat = re.compile(r'Test case (?P<i>\d+)\/(?P<n>\d+): (?P<ans>\w+)\"')
        matches = pat.finditer(content['row_html'])
        cases = list(matches)

        if len(cases) > 0: 
          n = min(int(cases[0].group('n')), len(cases))
          tracker.answers = [False] * n
          for i in range(n):
              test_case = cases[i]
              if 'accepted' == test_case.group('ans').strip().lower():
                tracker.answers[i] = True
              else:
                tracker.answers[i] = False

  elif status_id == ERROR:
    feedback = content['feedback_html']
    p = re.compile(r"<h3.*>(?P<title>.*)<\/h3>.*<pre.*>(?P<body>(.|\n)*)<\/pre>")
    m = p.search(feedback)
    tracker.message = f"""
ERROR: {m.group('title')}

{m.group('body')}
    """

  elif status_id == WRONG:
      tracker.message = "\nWrong Answer! [testcase {info['testcase_index]}]\n"

  elif test_index > 0:
    pat = re.compile(r'Test case (?P<i>\d+)\/(?P<n>\d+): (?P<ans>\w+)\"')
    matches = pat.finditer(content['row_html'])
    cases = list(matches)

    if len(cases) > 0: 
      n = min(int(cases[0].group('n')), len(cases))
      tracker.answers = [False] * n
      for i in range(n):
          test_case = cases[i]
          if 'accepted' == test_case.group('ans').strip().lower():
            tracker.answers[i] = True
          else:
            tracker.answers[i] = False
  
  else:
    tracker.message = content['feedback_html']


  return tracker


def submit(problem: str, language: str, mainclass: str, files: List[str]):

  data = {
    'submit': 'true', 
    'submit_ctr': 2, 
    'script': 'true',
    'language': language,
    'mainclass': mainclass,
    'problem': problem 
  }

  cookies = _login()
  url = _config.submissionurl
  file_data = _concat_files(files)

  response = post(f'{url}?json', data=data, files=file_data, cookies=cookies, headers={'User-Agent': 'kattis-cli-submit'})
  content = response.content.decode('utf-8').replace('<br />', '\n')

  if response.status_code != 200:
    raise HTTPError(f'{response.status_code}\n{response.content}')


  submission_id = re.search(r'Submission ID: (\d+)', content).group(1)
  new_cookies = _login() # why do we need?!?!?!?!
  status_url = f'{_config.submissionsurl}/{submission_id}?json'

  tracker = SubmissionTracker(0,0,0,[])
  def check_status():
    return _status(status_url, cookies=new_cookies, tracker=tracker)

  return check_status


if __name__ == '__main__':
  #testurl = f'https://{config.hostname}/problems/hello/statistics'
  #res = requests.gt(testurl, headers={'User-Agent': 'kattis-cli-submit'})
  print(_login().content)
