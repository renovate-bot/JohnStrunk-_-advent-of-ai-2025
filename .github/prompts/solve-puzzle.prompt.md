---
description: Solve the daily puzzle
mode: agent
---

# Solving the Daily Puzzle

Ask the user to provide the following information:

- The day number of the puzzle they want to solve (e.g., 5).
- The part of the puzzle they want to solve (1 or 2).
- The text description of the puzzle.
- The main input data for the puzzle. (This is usually only required once per
  day, but you can ask for it again if needed.)

You should then follow these steps:

1. Create a new directory for that day's puzzle if it doesn't already exist,
   following the naming convention `dayXX` where `XX` is the zero-padded day
   number (e.g., `day05` for day 5).
2. Inside that directory, create a file named `puzzle-partY.txt` where `Y` is
   the part number (1 or 2), and populate it with the provided puzzle
   description.
3. Create another file named `input.txt` in the same directory and populate it
   with the provided input data.
4. Commit these new files to a new branch named `dayXX`.
5. Solve the puzzle according to the provided description and input data,
   following the conventions and requirements of this repository.
