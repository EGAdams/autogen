copy files from unit test to live pi directory.

make a menu for the tennis tools



moved the files.

make test 6 for matrix

Find the live test directory.

Go to the Mode1Score directory

find the test file

need to modify test-game.cpp


This is is beginning to be a problem.  the code is messy.


test #6
===============================================================================
test global setup

score player 1 two sets until match win

perform the match win somehow.

Pi not booting.

restored power.  503pm


////////////////////////////////////////////////
Take a deep breath and explain it step by step.

explain in detail your reasoning for choosing in
a step by step way

use gpt-3.5-turbo-0613 for better data eveloping.

periodic git fetch?

todo: menus always need to be working, so check them periodically.

////////////////////////////////////////////////

===
# Sunday 10/15/2023
===

---
4:25 PM 10/15/2023
---
## The Detrot tampa game starts

no kickoff yet...

My train.

---
**5:10 PM 10/15/2023**
---

Right now I have tried to run the generic assistant and it seems like it starts going into circles whene the Java PATH is needing modification.  After it goes into circles, the token limit is reached.

---
**5:45 PM 10/15/2023**
---

## wheels spin... oh no..



# Research
5:16 PM 10/15/2023
===
## Think about the agent(s) that we will need to make test 6 from test 5.

### How would I break down `Make test 6 from test 5` into separate tasks?
#### Get to know the unit test that we need to convert.
- Open the file Mode1ScoreTest.cpp and copy the `Unit Test` Test_Two_Set_Win_Scenario
  - Remember that we need test 5 in hand so that the bot knows how to convert the working test to the new one.
- This piece of text needs to be minimized and go into the section: `** Working Unit Test #5 source code ** -- block`

#### Get the code that works on the matrix, but needs conversion
- Open Test #5 in `tennis-game.cpp` in the `rgb repo` because we know that it works
- Copy the `Test #5` method from `tennis-game.cpp` and put it into the `#Your Task` section of the translation prompt.






===
# The Matrix Project
# Make test 6 from test 5.
12:00 PM 10/16/2023
# Thought Process that AI entities may be using

- [x] Open the `rgb` directory
- [x] Change directory to the tennis game
- [x] Make sure test 6 is there and run it with the matrix disabled
## match win is shown
- [x] Find out where in the matrix to write the "Match Win" text
  - we will need to drill this down
    - ## Which classes are associated with `writing the new code` to handle the `"Match Win"` text writing?
      - ### ScoreBoard
            - This should be the only one right?  Remember that part about not having any dependencies?
            How could we have written "Match Win" directions above to minimize dependencies?
            Now I see `(writing the new code)`.  Writing new code huh?  Where?  ...the ScoreBoard object?
            Not this week.  We are NOT adding a new method to the ScoreBoard object. There is only one dependency(more on that later) what is a dependency.  now im not sure anymore.. but dam it's long and complicated.  `The ScoreBoard Object need to be split up into smaller sections.  adding a Match Win object will be the last straw.`   Let me check, maybe there is one?
            I would not advise one adding a new method here.

            - The ScoreBoard update() method is called here.  After that we draw the "Match Win" text.  Find the method that writes into the same place as the points go.

      - ### Mode1Score
      - calls ScoreBoard::Update
## change of plan found match win sequence already coded in.

    ### 


- [ ] Write the "Match Win" text in any old font
- [ ] Attach it to the game 












