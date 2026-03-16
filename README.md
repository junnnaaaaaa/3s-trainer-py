# Python 3 style trainer 
A very simple 3 style trainer that allows you to store your algs and words such that they are assigned to the same letter pair. The idea is that when you use the timer, instead of recalling letter pair from word then alg from letter pair, you recall straight from word to alg 
## Dependencies
You need git, python3 and pyside6
## Usage
Clone the directory as such:
`git clone github.com/junnnaaaaaa/3s-trainer-py`
Then just run main.py:
`python3 source/main.py`
I'll consider packaging in future, but I'm also probably gonna turn it into a
svelte program if I plan to go ahead with that
## Features
- Storage of pairs and comms even after application has been closed and reopened
- Importing existing word and comm sheets as .csv's (please that the comms are very
  limited right now, as I have not been able to compensate for different different
  letterering systems or those with targets or tables that are not 25x25 with the
  first row and column being a label)
- A simple timer which shows a letter pair from a list which the user creates
  when started along with its associated word, as well as session mean and last
  time.
- Algorithm verification so that when a user enters an algorithm it tests if its
  a valid algorithm or not. It also accounts for common commutator notation
## Future Timeline
I will likely not bother to continue this project but if I do:
- Touch up the Timer, add features like more statistics and local storage of
  times across different sessions. Adding hints for comms as well.
- Verification that comms work when people enter them in. 
- Compensating for more formats of comm lists
- Allow for different lettering schemes and displaying things by target notation
  rather than just Speffz lettering scheme. (Also helps with comm verification
  in the future)
- Rewrite with Tauri
## Credits 
- Thanks to https://github.com/b-paul (aka bpaul) for letting me use their comm
  sheets to realise that my import algorithm will need a lot of work in future
- Thank to Amy Smith for letting me use her word sheet just for basic testing.
  You can find her on youtube @voidedhon
