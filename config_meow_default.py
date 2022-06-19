
config = """
#
# Default config for the meow kattis client
# This should be place at $HOME/.meow.yaml
#
# Additionally, make sure to download and place kattis config at $HOME/.kattisrc
#   (see https://open.kattis.com/help/submit)
#

# IMPORTANT: ADJUST THESE TO FIT YOUR ENVIRONMENT

problem_directory: '/home/<yourname>/somewhere'

editor: 'vim'

default_extension: 'cpp'

default_template: 'cpp'
templates:
    cpp: '/home/<yourname>/Kattis/templates/template.cpp'


# These will never really need configuring unless you're customizing
language_guesses:
    .c: 'C'
    .c++: 'C++'
    .cc: 'C++'
    .c#: 'C#'
    .cpp: 'C++'
    .cs: 'C#'
    .cxx: 'C++'
    .cbl: 'COBOL'
    .cob: 'COBOL'
    .cpy: 'COBOL'
    .fs: 'F#'
    .go: 'Go'
    .h: 'C++'
    .hs: 'Haskell'
    .java: 'Java'
    .js: 'JavaScript'
    .kt: 'Kotlin'
    .lisp: 'Common Lisp'
    .cl: 'Common Lisp'
    .m: 'Objective-C'
    .ml: 'OCaml'
    .pas: 'Pascal'
    .php: 'PHP'
    .pl: 'Prolog'
    .py: 'Python 3'
    .rb: 'Ruby'
    .rs: 'Rust'
    .scala: 'Scala'

mainfile_languages:
  - 'Python2'
  - 'Python3'
  - 'PHP'
  - 'Rust'
  - 'Pascal'

mainclass_languages:
  - 'Java'
  - 'Scala'
  - 'Kotlin'
"""
