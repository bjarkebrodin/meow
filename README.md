
# Meow

is a modification of the original kattis submission client,
with additional support for submitting such as timing feedback and some error messages.
Additionally, some file system convenience and templating functionality has been added.

Currently we can do stuff like this

```
meow new <problem> [-t TEMPLATE]
meow submit [-h] [-p PROBLEM] [-m MAINCLASS] [-l LANGUAGE] [-t TAG] <files ...>
```


<!--

kattis list
kattis status
kattis browser
kattis random <difficulty>
kattis queue <problem>
kattis poll

<difficulty> := trivial | easy | medium | hard
<problem> := kattis problem shortname

-->

## Dependencies

`python3`
`pyyaml`
`requests`

For your convenience: ensure `python3` and `pip3` are present then run
`pip3 install pyyaml requests`



## Example

```
❮ meow submit ratingproblems.cpp

Submitting ratingproblems
Language: C++


      /^--^\     /^--^\     /^--^\
      \____/     \____/     \____/
     /      \   /      \   /      \
    |        | |        | |        |
     \__  __/   \__  __/   \__  __/
|^|^|^|^\ \^|^|^|^/ /^|^|^|^|^\ \^|^|^|^|
| | | | |\ \| | |/ /| | | | | | \ \ | | |
| | | | / / | | |\ \| | | | | |/ /| | | |
| | | | \/| | | | \/| | | | | |\/ | | | |
#########################################

 ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓

Submission Accepted!
CPU Time: 0.00s
```



