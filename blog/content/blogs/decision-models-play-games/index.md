---
author: "Jim Bennett"
date: 2026-10-19
publishDate: 2026-10-19
description: "Decision models can now read images, so can they play games? I ran six decision models and two LLMs through Tic-tac-toe, Minesweeper and Flappy Bird from screenshots and from text, against deterministic baselines. The LLMs played well, the decision models mostly didn't, and reasoning explains a lot of the gap."
draft: true
slug: "decision-models-play-games"
title: "Can decision models play games from screenshots?"
tags: ["ai", "llm", "decision-models", "benchmarks", "evals", "multimodal", "games"]

images:
  - /blogs/decision-models-play-games/banner.png
featured_image: banner.png
---

Decision models are built to answer one kind of question quickly. You give the model a prompt and a fixed list of options, and it returns a probability for each option. That makes them a good fit for a step inside an agent: pick a tool, pick a route, decide whether to stop. I [recently benchmarked a number of these models](https://arize.com/blog/decision-model-benchmark/) and found them fast and effective.

Several of them now accept images too. Cloudflare's Clef Flash, Liquid's d1 models and OpenAI's Decisions route all handle images, and [TypeSafe's Jev 1.14](https://typesafe.ai/blog/jev-1-14) added experimental image support.

So I asked a fun question:

> If a decision model can read an image and use that to make a decision, can it play a game?

Games are a clean test. The screen gives you the information you need, the rules are fixed, the legal moves are known, and the score can tell you exactly how well the model did. The eval here is reduced to "did the model win?" or "what score did the model get?", a deterministic check.

I built a small browser arcade with three games and ran eight models through it. I mixed decision models with LLMs, and compared how well they did with images to how well they did with raw text. Then I put them up against a deterministic game engine as a comparison.

How did they do? OK, but not great, depending on the game. I'm a terrible gamer and I was able to score way better than most of the AIs. I'll walk through the models, the games, and the scores.

## Meet the games

![Tic-tac-toe in the arcade, with two Xs on the top row and Os in the centre and bottom right](/blogs/decision-models-play-games/game-in-play-tictactoe.png)

**Tic-tac-toe.** The classic three-in-a-row game on a 3 × 3 grid. The model plays against a perfect opponent, so the best it can do is a draw. Spaces are lettered A-I so the models know which spaces are empty and can respond with the letter of the space to play.

![Minesweeper in the arcade, with the left and centre of the board uncovered](/blogs/decision-models-play-games/game-in-play-minesweeper.png)

**Minesweeper.** An 8 × 8 board hides 10 mines. Every opened tile shows how many mines touch it, and the aim is to open all the safe tiles without hitting a mine. If you open a cell with a mine, you lose. The rows are numbered and the columns are lettered so the model can indicate which tile to open. To avoid losing on the first square, there is always a safe square that the model can play to start.

![Flappy Bird in the arcade, with the bird approaching the first pair of pipes](/blogs/decision-models-play-games/game-in-play-flappy.png)

**Flappy Bird.** A bird flies forward on its own through gaps between green pipes. The only choice is when to flap, and gravity does the rest. The bird falls under gravity, unless you flap, which raises the bird up a little before gravity brings it back down. If you hit a pipe, the top of the screen, or the ground, you lose.

## Meet the contestants

| Model | Cloud vs Local |
|---|---|
| [Jev 1.14](https://typesafe.ai/blog/jev-1-14) | Cloud |
| [GPT-6 Luna Decisions](https://developers.openai.com/api/docs/guides/decisions) | Cloud |
| [Clef Flash](https://blog.cloudflare.com/clef-decision-models/) | Cloud |
| [Liquid d1](https://docs.liquid.ai/lfm/models/decision-models) | Cloud |
| [Liquid d1-3B](https://huggingface.co/LiquidAI/d1-3B) | Local |
| [Liquid d1-omni-600M](https://huggingface.co/LiquidAI/d1-omni-600M) | Local |
| [GPT-6 Astra Responses](https://developers.openai.com/api/docs/models/gpt-6-astra) | Cloud |
| [GPT-6 Luna Responses](https://developers.openai.com/api/docs/models/gpt-6-luna) | Cloud |

This model set contains six decision models, a mix of local and cloud. The remaining two are LLMs, added as a comparison. GPT-6 Luna Responses and GPT-6 Luna Decisions are the same underlying model, one version is the normal LLM, the other is OpenAI's version that is tuned for decisions.

For each game the models were scored against a baseline using a deterministic game engine, a short piece of code written into the arcade itself, built on a standard technique:

- **Tic-tac-toe: minimax.** [Minimax](https://en.wikipedia.org/wiki/Minimax) searches every possible continuation of the game and picks the move that's best assuming the opponent also plays perfectly. Tic-tac-toe is small enough to search completely, and it's a [solved game](https://en.wikipedia.org/wiki/Solved_game). With perfect play on both sides, every game is a draw. The same minimax player is also the models' opponent.
- **Minesweeper: a constraint solver.** It treats every revealed number as a [constraint](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem) on the covered tiles around it. If a clue's mines are all accounted for, its other covered neighbours are safe. If a clue has exactly as many covered neighbours as missing mines, they're all mines. It also compares pairs of overlapping clues. It reads only the visible board, as the models do, and if nothing is provably safe it falls back to the lowest-risk guess.
- **Flappy Bird: a gap-centering rule.** A one-line autopilot: flap if the bird is falling and more than 18 pixels below the centre of the next gap, otherwise wait. Unlike the models, it reads the exact bird and pipe positions from the game rather than the pixels.

The baselines aren't competitors on equal terms as they have programmatic access to the game state. What they show is what a good score looks like.

As a comparison, I also did a text only version, where the models received a prompt with a description of the game state. This was to allow me to compare how the images worked against a pure text input.

TypeSafe recently released an image capable version of Jev, and was upfront that images are a work in progress. The [launch post](https://typesafe.ai/blog/jev-1-14) warns that *"all models (Jev included) perform worse on multimodality over pure text."* These tests allow me to verify this claim.

## Tic-tac-toe

### How I tested it

**Score:** 1 for a win, 0.5 for a draw, 0 for a loss, against the perfect minimax opponent. You can't beat perfect minimax, so 0.5 per game (a draw) is the best possible result. Each model plays 10 games per input type, five as O and five as X.

Each move for the model player is a single request sent to the model. The one exception is the last move. When only one empty square is left there's nothing to decide, so the arcade plays that square itself without calling the model, as decision models generally reject a single decision prompt.

The prompt is very explicit about the logic and describes how to play, how to win, and how to decide on the next move. If you can win, do so. If you need to block the opponent from winning, do so. Otherwise choose a square that helps you win.

#### Image input

When playing using images, the arcade sends a screen shot of the current board, a fixed prompt and the list of empty squares as the decision choices. There is no conversation history, just the image to give the model a view on the current game state. It gets back one choice, and plays it.

This is a typical image of a game where the model is O. The minimax game engine has played square F, and the board image is sent to the model.

![The Tic-tac-toe image sent to the model: a grid with X in square F and grey letters on the empty squares](/blogs/decision-models-play-games/input-image-tictactoe.jpg)

This is the prompt that goes with it. It explains the game rules, what side the model is playing, the instruction, and gives the choices based on the remaining squares.

```text
Prompt:
Use the image as the source of the current tic-tac-toe board. X and O show occupied squares; letters label empty squares. You are playing O. Choose a legal square that wins immediately if possible, otherwise block an immediate opponent win, otherwise choose a move that preserves a draw against perfect play. Return one offered action.

Image:
[the 512 × 512 board above]

Choices:
A: Place O in square A.
B: Place O in square B.
C: Place O in square C.
D: Place O in square D.
E: Place O in square E.
G: Place O in square G.
H: Place O in square H.
I: Place O in square I.
```

#### Text input

The text games used the same positions with no image at all. The board state is sent as a list of rows with the Xs and Os. This is the full request for the same first decision:

```text
Prompt:
Use the textual board state as the complete tic-tac-toe board. Rows are listed top to bottom; square letters A-I run left to right, then top to bottom. Each square is marked with X, O, or empty. A player wins by placing three of their marks in a horizontal, vertical, or diagonal line; filling the board without a line is a draw. You are playing O. Choose a legal square that wins immediately if possible, otherwise block an immediate opponent win, otherwise choose a move that preserves a draw against perfect play. Return one offered action.

State:
Row 1: A=empty | B=empty | C=empty
Row 2: D=empty | E=empty | F=X
Row 3: G=empty | H=empty | I=empty

Choices:
A: Place O in square A.
B: Place O in square B.
C: Place O in square C.
D: Place O in square D.
E: Place O in square E.
G: Place O in square G.
H: Place O in square H.
I: Place O in square I.
```

### Results

![Tic-tac-toe draws per model, image and text](/blogs/decision-models-play-games/fig-05-tictactoe-results.png)

**The decision models.** Jev 1.14 is the strongest of the decision models here. From images it drew nine of 10, losing only one game as X. From text it drew four of 10, all as O, and lost all five games as X. An interesting result that contradicts Jev's claim that image handling is not as good as text.

After Jev it falls away quickly. Liquid d1 drew four games per input, GPT-6 Luna Decisions drew one from images and three from text, Liquid d1-3B drew one from images, and Clef Flash and Liquid d1-omni-600M drew none. Across all six decision models that's 26 draws in 120 games.

**The LLMs.** GPT-6 Astra Responses is the clear winner. It drew all 20 games, 10 from images and 10 from text. That's the best result anyone can get against minimax. GPT-6 Luna Responses drew 19 of 20: nine from images and all 10 from text, with one image loss as O. Between them, the two LLMs drew 39 of 40 games. The LLMs far outperformed the decision models.

### How the decision models lose

![Clef Flash missing a block in Tic-tac-toe, with the probabilities it returned](/blogs/decision-models-play-games/fig-06-tictactoe-missed-block.png)

The losing pattern is nearly always the same: the opponent has two in a row and the model doesn't block. In this image of minimax vs Clef Flash, the threat is about as visible as it gets. Clef Flash's probabilities are close to flat, between 0.12 and 0.21, so the model isn't confident about anything. It just happens to rank D highest. In my replay of every image-mode game, Clef Flash and Liquid d1-omni-600M missed a forced block in all 10 of their games. This isn't a gap in the prompt, the prompt explicitly states:

> Choose a legal square that wins immediately if possible, otherwise block an immediate opponent win

Text input showed a stranger habit: picking the first square in the list. Clef Flash chose the first offered square on all 26 of its text decisions, so its games as X always opened A, then B, then D. Liquid d1-3B and Liquid d1-omni-600M did the same on all 15 of their text decisions as X. Here's one of those moves:

```text
Row 1: A=X | B=X | C=O
Row 2: D=empty | E=O | F=empty
Row 3: G=empty | H=empty | I=empty
choices: D, F, G, H, I
returned: D 0.31, G 0.25, F 0.19, H 0.14, I 0.12
```

O threatens C, E, G on the diagonal, so G was the only move that saved the game. The model put D first, which also happens to be first in the list, and minimax played G and won. In image mode the same models usually opened in the centre instead. So the input type does change *how* they play, even when it doesn't change the score.

### Prompt wording didn't rescue it

Before freezing the prompts, I ran some prompt experiments on a different set of games. A five-prompt sweep across four decision models found a "strategy" prompt that drew 7 of 24 games. In a paired check on 10 games that gap shrank to 14 draws out of 80 against 9 out of 80 for the existing prompt. Adding the explicit win-condition sentence to the text prompt left the total unchanged at 23 of 80 across all eight models. Prompt wording moved things a little. It didn't turn a decision model into one that blocks reliably.

## Minesweeper

### How I tested it

**Score:** safe tiles revealed, out of 54. The board is 8 × 8 with 10 mines. Every game starts with the same guaranteed-safe opening at D4 so that models don't lose immediately to random chance, and the score includes tiles the model got for free. A game ends at the first mine, or when the board is cleared. Each model played the same 10 boards with image input and again with text input, one request per move and the same fixed prompt every time.

On these 10 boards, the free opening of D4 alone reveals between 23 and 48 safe tiles before the model makes a single move. So the benchmark also reports **gain over the opening**: the score minus what D4 gave away on that board.

#### Image input

![The Minesweeper image sent to the model after the D4 opening, with a coordinate printed on every covered tile](/blogs/decision-models-play-games/input-image-minesweeper.jpg)

The image prints each covered tile's coordinate on the tile itself, so the model doesn't have to count rows and columns. This is the full request that went with it:

```text
Prompt:
Inspect the Minesweeper board image. There are 10 mines in total. White opened tiles show clue numbers: each number is the count of mines in the eight surrounding cells, including diagonals. A blank white tile has no mines in those surrounding cells. Blue tiles are covered. Use the visible clues and the total mine count to choose one covered tile that you judge safe to open. Do not choose a tile you believe contains a mine. If the image does not establish a safe tile, choose the covered tile that appears least risky. Return exactly one offered OPEN action.

Image:
[the 500 × 500 board above]

Choices (41, shuffled; each described as "Open covered tile <tile>."):
OPEN_H1, OPEN_E1, OPEN_H7, OPEN_G2, OPEN_A1, OPEN_D1, OPEN_A8
OPEN_G3, OPEN_E8, OPEN_B7, OPEN_F5, OPEN_H8, OPEN_H2, OPEN_H6
OPEN_F8, OPEN_C2, OPEN_H4, OPEN_B1, OPEN_F7, OPEN_C8, OPEN_E2
OPEN_C1, OPEN_G7, OPEN_A6, OPEN_H3, OPEN_H5, OPEN_G1, OPEN_F2
OPEN_B8, OPEN_D2, OPEN_F4, OPEN_F6, OPEN_A7, OPEN_G4, OPEN_G6
OPEN_F3, OPEN_B6, OPEN_F1, OPEN_G8, OPEN_G5, OPEN_D8
```

The choices are shuffled on every turn so list position can't hint at anything.

#### Text input

In text mode the same board arrived as a grid with a legend. This is the full request for the same first decision:

```text
Prompt:
Read the textual Minesweeper board state. There are 10 mines in total. The grid legend describes covered, flagged, blank, and numbered tiles. A clue number is the count of mines in the eight surrounding tiles, including diagonals. Use the visible clues and total mine count to choose one covered tile that you judge safe to open. Do not choose a tile you believe contains a mine. If the clues do not establish a safe tile, choose the covered tile that appears least risky. Return exactly one offered OPEN action.

State:
Columns are A through H; each line is the row with that number. Symbols: ? = covered tile, F = flagged tile, . = opened blank with zero neighboring mines, and a digit = opened clue showing that many mines in the eight surrounding tiles.
    A B C D E F G H
1: ? ? ? ? ? ? ? ?
2: 1 2 ? ? ? ? ? ?
3: . 1 1 1 1 ? ? ?
4: . . . . 1 ? ? ?
5: 1 1 1 . 2 ? ? ?
6: ? ? 1 . 1 ? ? ?
7: ? ? 2 1 3 ? ? ?
8: ? ? ? ? ? ? ? ?

Choices (41, shuffled; each described as "Open covered tile <tile>."):
OPEN_H1, OPEN_E1, OPEN_H7, OPEN_G2, OPEN_A1, OPEN_D1, OPEN_A8
OPEN_G3, OPEN_E8, OPEN_B7, OPEN_F5, OPEN_H8, OPEN_H2, OPEN_H6
OPEN_F8, OPEN_C2, OPEN_H4, OPEN_B1, OPEN_F7, OPEN_C8, OPEN_E2
OPEN_C1, OPEN_G7, OPEN_A6, OPEN_H3, OPEN_H5, OPEN_G1, OPEN_F2
OPEN_B8, OPEN_D2, OPEN_F4, OPEN_F6, OPEN_A7, OPEN_G4, OPEN_G6
OPEN_F3, OPEN_B6, OPEN_F1, OPEN_G8, OPEN_G5, OPEN_D8
```

### Results

![Minesweeper safe tiles per model, split into the free opening and the model's gain](/blogs/decision-models-play-games/fig-07-minesweeper-results.png)

**The decision models.** None of the six cleared a single board, and every one of their 120 games ended on a mine. Jev 1.14 and Clef Flash did best, both averaging 38.3 from images, which is a gain of 5.5 tiles. Liquid d1-omni-600M gained 4.7 from images and 3.4 from text. The rest gained less than three tiles from either input, so most of their score was the free opening.

**The LLMs.** GPT-6 Astra Responses cleared all 10 boards from images and all 10 from text. That took about 14 requests per board, at roughly 6 seconds per request. I checked every one of its 279 decisions against an exact solver. Each time it opened a tile that was provably safe given the visible clues and the mine count. It never had to guess, and it never did.

![Four frames from Astra clearing a Minesweeper board](/blogs/decision-models-play-games/fig-09-minesweeper-astra-sequence.png)

GPT-6 Luna Responses comes next: 44.4 from images (+11.6, one board cleared) and 41.5 from text (+8.7).

The best decision model gained about a quarter of what GPT-6 Astra Responses did, and less than half of GPT-6 Luna Responses' gain. They were fast, though: under 0.8 seconds per decision, against 6 to 8 seconds for the LLMs. Fast, but wrong.

### Most fatal clicks were on provable mines

![A Minesweeper frame where the model clicked a provable mine while ten tiles were provably safe](/blogs/decision-models-play-games/fig-08-minesweeper-fatal-click.png)

Every decision model hit a mine in every game, and GPT-6 Luna Responses hit one in all but one. My replay of every game found that no mine hit was forced. At the moment of every fatal click, at least one tile was provably safe. Most fatal clicks were on tiles that were *provably mines*. In the frame above, B3 shows a 1 with only one covered neighbour, C2, so C2 has to be a mine. The model opened it anyway.

This is the same failure as the missed block in Tic-tac-toe. The model can see the board, but it doesn't make the small check the board requires. The tile labels make it easy to name the right tile, but nothing makes the model look at a tile's neighbours first.

## Flappy Bird

### How I tested it

**Score:** pipes passed. The bird moves forward on its own. FLAP gives it an upward kick, and WAIT lets gravity pull it down. Each model played the same 10 courses from images and the same 10 from text, with the same fixed prompt for each input every time. A game ends when the bird hits a pipe, the top of the screen or the ground, or after 10 minutes of real time.

Flappy Bird is the one game here that runs in real time, so I had to change the way the models are called. A single image doesn't truly reflect the game state, you need multiple frames captured over a period of time that shows the bird's trajectory.

Being real time also means the game cannot wait for a response from the model. In the time the game waits for a response, the bird is crashing into the ground. Instead the game is paused whilst the model makes a decision, then resumed to handle the chosen action.

![The Flappy Bird decision loop: physics pauses, the model gets four frames and one request, returns FLAP or WAIT, then physics resumes for 0.24 simulated seconds](/blogs/decision-models-play-games/fig-01-flappy-loop.png)

I iterated over the number of frames to capture and the time between frames to get the best result. The final setting after testing for the most effective combination sends four frames, about 0.06 simulated seconds apart, so the model makes a decision every 0.24 simulated seconds.

The game also runs at a fifth of normal speed for the models, and as in the other games there's no conversation history and no retry. Latency costs nothing inside the game, because the game waits. That makes this an easier version of Flappy Bird than a human plays.

#### Image input

This is a typical set of frames. The bird has reached the first pair of pipes and is dropping towards the lower one.

![The four Flappy Bird frames sent to the model, about 0.06 simulated seconds apart, showing the bird falling towards the lower pipe of the first pair](/blogs/decision-models-play-games/fig-04-image-input-flappy.png)

The frames are unlabelled, and there are four so the model can tell whether the bird is rising or falling, and how fast, by looking at the order of the images as they are passed in chronological order. This is the full request that went with them:

```text
Prompt:
You are playing Flappy Bird. The yellow bird moves forward automatically. Keep it alive by avoiding the top of the screen, the ground, and the solid green pipes; pass through the open vertical gap between each top-and-bottom pipe pair. The images are ordered from earlier to current; compare them to infer whether the bird is rising or falling, and use the latest image for its position relative to the next gap. FLAP applies one upward impulse. From level motion, one flap carries the bird to a peak about 11% of screen height above its starting point before gravity pulls it back down; the actual rise depends on its motion when it flaps. WAIT applies no impulse; gravity and forward motion continue. Choose the single action that keeps the bird clear of hazards and on a path through the next gap. Do not describe the images.

Image:
[the four frames above, oldest first]

Context:
Last applied action: WAIT, about 1.3 real seconds ago.

Choices:
FLAP: Give the bird one upward flap impulse.
WAIT: Do not flap on this turn; gravity continues.
```

#### Text input

In text mode there's no image. The model gets four text observations, 0.06 simulated seconds apart, oldest first. Each one gives the bird's height and vertical speed, the last action, the distance to the next three pipes with the top, bottom and centre of each opening, and the score. That's exact pixel coordinates, so it's much closer to what the gap-centering rule reads than a screenshot is:

```text
Prompt:
You are playing Flappy Bird. The bird moves forward automatically. Keep it alive by avoiding the top of the screen, the ground, and the solid pipes; pass through the open vertical gap in each top-and-bottom pipe pair. Use the textual observations in time order to judge whether the bird is rising or falling and where it is relative to the next opening. Vertical positions are measured from the top of the playfield; larger y values are lower. FLAP applies one upward impulse. From level motion, one flap carries the bird to a peak about 11% of screen height above its starting point before gravity pulls it back down; the actual rise depends on its motion when it flaps. WAIT applies no impulse; gravity and forward motion continue. Choose the single action that avoids the hazards and keeps the bird on a path through the next opening. Return one offered action.

State:
Observations in time order, oldest first; each is spaced 0.06 simulated seconds apart:

Observation 1
Bird: y=333 px from the top; vertical speed 205 px/s (falling).
Last applied action: WAIT, 0.1 simulated seconds ago.
Upcoming pipes, nearest first: Pipe 1: 18 px ahead; opening from y=240 to y=408 px (center y=324 px). Pipe 2: 253 px ahead; opening from y=279 to y=447 px (center y=363 px). Pipe 3: 488 px ahead; opening from y=227 to y=395 px (center y=311 px)
Playfield: top of the screen y=0 px; ground y=570 px. Score: 0 pipes passed.

Observation 2
Bird: y=348 px from the top; vertical speed 271 px/s (falling).
Last applied action: WAIT, 0.1 simulated seconds ago.
Upcoming pipes, nearest first: Pipe 1: 9 px ahead; opening from y=240 to y=408 px (center y=324 px). Pipe 2: 244 px ahead; opening from y=279 to y=447 px (center y=363 px). Pipe 3: 479 px ahead; opening from y=227 to y=395 px (center y=311 px)
Playfield: top of the screen y=0 px; ground y=570 px. Score: 0 pipes passed.

Observation 3
Bird: y=368 px from the top; vertical speed 338 px/s (falling).
Last applied action: WAIT, 0.2 simulated seconds ago.
Upcoming pipes, nearest first: Pipe 1: -1 px ahead; opening from y=240 to y=408 px (center y=324 px). Pipe 2: 234 px ahead; opening from y=279 to y=447 px (center y=363 px). Pipe 3: 469 px ahead; opening from y=227 to y=395 px (center y=311 px)
Playfield: top of the screen y=0 px; ground y=570 px. Score: 0 pipes passed.

Observation 4 (current)
Bird: y=391 px from the top; vertical speed 404 px/s (falling).
Last applied action: WAIT, 0.3 simulated seconds ago.
Upcoming pipes, nearest first: Pipe 1: -10 px ahead; opening from y=240 to y=408 px (center y=324 px). Pipe 2: 225 px ahead; opening from y=279 to y=447 px (center y=363 px). Pipe 3: 460 px ahead; opening from y=227 to y=395 px (center y=311 px)
Playfield: top of the screen y=0 px; ground y=570 px. Score: 0 pipes passed.

Context:
Last applied action: WAIT, about 1.3 real seconds ago.

Choices:
FLAP: Give the bird one upward flap impulse.
WAIT: Do not flap on this turn; gravity continues.
```

### Results

![Pipes passed per game for the gap-centering baseline and every model, image and text input](/blogs/decision-models-play-games/fig-10-flappy-results.png)

The gap-centering rule, my deterministic code based player, averaged **19.3 pipes**, with a best of 39 and a worst of one.

**The decision models.** They barely flew at all. Liquid d1 averaged 0.5 pipes from images, with a best of two. Jev 1.14, GPT-6 Luna Decisions, Clef Flash, Liquid d1-3B and Liquid d1-omni-600M didn't pass a single pipe from images, and no decision model passed a pipe from text.

**The LLMs.** GPT-6 Astra Responses is the only model that really flew. It averaged **8.4 pipes** from images. Its best game never crashed: it was still flying when it hit the 10-minute limit, after 140 decisions at roughly 3 seconds each, and the last frame it was sent shows 20 pipes passed, so I count it as 20. Its best game that did end in a crash passed 16.

Text didn't help. GPT-6 Astra Responses averaged **3.9 pipes** from text, with a best of 17, so it did worse with exact coordinates than with screenshots. All 10 of its text games ended in a crash, eight of them on the upper pipe. GPT-6 Luna Responses barely flew from either input: 0.5 pipes from images, with a best of two, and zero from text.

### How the models crash

![FLAP and WAIT sequences for every model on one course](/blogs/decision-models-play-games/fig-11-flappy-actions.png)

Most of the decision models aren't steering at all. They play the same, or nearly the same, sequence on every course, whatever the frames show:

- **Jev 1.14** played FLAP on every decision in every game. The bird hit the top of the screen in all 10, after five decisions.
- **Clef Flash** played FLAP, WAIT, FLAP, WAIT on every course, identical each time, and also hit the top of the screen in all 10. GPT-6 Luna Decisions mostly alternated too, with the odd extra FLAP, and hit the top of the screen in all 10.
- **Liquid d1-3B** played WAIT on every decision and fell to the ground in all 10 games, after three decisions.
- **Liquid d1-omni-600M** usually played FLAP twice and then waited, and hit the ground in eight of 10.

Flapping every other decision is too much lift at this pace and never flapping is too little, so none of these patterns is a decision about the bird. From text the decision models were even more uniform, and most of them alternated FLAP and WAIT straight into the top of the screen. The two LLMs reacted to the course, but only GPT-6 Astra Responses changed its sequence enough to steer.

## So, can decision models play games?

Not well. The two LLMs were far better suited to these games than the six decision models.

### The LLMs played well

GPT-6 Astra Responses drew every Tic-tac-toe game against perfect play and cleared every Minesweeper board, from screenshots and from text alike. GPT-6 Luna Responses was close behind, with 19 draws in 20 and the only other cleared board. Astra was also the only model that really flew in Flappy Bird. Both were slow, though: 6 to 8 seconds per Minesweeper decision.

### The decision models struggled

Across the six of them: 26 draws in 120 Tic-tac-toe games, against 39 in 40 for the LLMs. No Minesweeper board cleared, and a best gain of 5.5 tiles against Astra's 21.2. In Flappy Bird, five of the six never passed a pipe. They missed blocks that were plainly visible, clicked tiles the board proved were mines, defaulted to the first option in text mode, and repeated one fixed FLAP and WAIT pattern whatever the course looked like. The near-flat probabilities they returned on lost positions suggest they often weren't really choosing at all. Jev 1.14 is the one exception: nine of 10 Tic-tac-toe draws from images, the only decision model near the ceiling in any game. But even Jev cleared no Minesweeper boards and passed no pipes.

That isn't a verdict on decision models for the job they're built for. They answered in well under a second, and in my [earlier benchmark](https://arize.com/blog/decision-model-benchmark/) that speed made them a good fit for routing steps inside an agent. Games are a different kind of decision.

### Is it the reasoning?

GPT-6 Luna is the cleanest comparison in this benchmark, because it's the same model on two routes. Through the Responses route it drew 19 of 20 Tic-tac-toe games and gained 11.6 Minesweeper tiles from images. Through the Decisions route it drew four of 20 and gained 1.8. The obvious difference between the routes is that Responses reasons before it answers and Decisions doesn't. So I tested that directly.

#### The test

Every LLM row in this post ran with the API's reasoning effort set to low, the server default. For this test I ran GPT-6 Luna Responses again with the effort set to none. Every call came back with zero reasoning tokens, so reasoning really was off.

Everything else stayed the same: the same 10 Tic-tac-toe games and the same 10 Minesweeper boards, from images and from text, against the same minimax and after the same opening.

#### The scores

| | Luna Responses, reasoning on | Luna Responses, reasoning off | Luna Decisions |
|---|---|---|---|
| Tic-tac-toe draws, image | 9 of 10 | 7 of 10 | 1 of 10 |
| Tic-tac-toe draws, text | 10 of 10 | 4 of 10 | 3 of 10 |
| Minesweeper tiles gained, image | +11.6 | +5.5 | +1.8 |
| Minesweeper tiles gained, text | +8.7 | +2.3 | +1.5 |
| Minesweeper boards cleared | 1 | 0 | 0 |
| Seconds per decision | 3 to 8 | 1.2 to 1.7 | 0.2 to 0.5 |

With reasoning off, Luna fell from 19 Tic-tac-toe draws to 11, and its Minesweeper games got much shorter: about two moves per game before it hit a mine, against 5.6 with reasoning on.

#### What it shows

Reasoning helps, and it's the biggest single factor. Turning it off cost Luna eight of its 19 Tic-tac-toe draws and at least half of its Minesweeper gain from either input.

Splitting by input shows where the rest comes from. From text, Luna with reasoning off played about as badly as Luna Decisions: four draws against three, and +2.3 tiles against +1.5. From images, it kept a clear lead: seven draws against one, and +5.5 tiles against +1.8. Same model, no reasoning on either route, and the Responses route still did much better with a screenshot. So the way each route handles the image makes a difference too. Part of that could be how the answer is picked: the Responses route returns one choice, while the Decisions route returns a probability for every option and the arcade plays the highest. This test can't separate the two.

Three cautions. It's 10 games per input, so none of these gaps is statistically significant. Reasoning off isn't quite the same as a single fast pass either, because Luna still took 1.2 to 1.7 seconds per decision against well under a second through Decisions. And I left Flappy Bird out, because the reasoning-off games ran at an older frame setting and can't be compared with the Flappy Bird results above.

### Real time is hard for everyone

Even with the game paused for every decision, GPT-6 Astra Responses averaged 8.4 pipes from images and 3.9 from text, against the gap-centering rule's 19.3. Astra also needed about 2.6 seconds per decision, so this only worked because the game waited. Real-time control is still a job for code in the inner loop, with a model setting the plan around it.

### Images held up against text

![Image vs text for every model across the three games](/blogs/decision-models-play-games/fig-12-image-vs-text.png)

For both kinds of model, put the three games side by side and there's no consistent text advantage.

For the LLMs, the input barely mattered in the turn-based games. GPT-6 Astra Responses was at the ceiling with both, and GPT-6 Luna Responses drew nine against 10 and gained 11.6 tiles against 8.7. In Flappy Bird, Astra did better from images (8.4 pipes) than from text (3.9).

For the decision models, images were if anything slightly better. The six of them drew 15 Tic-tac-toe games from images and 11 from text, and five of the six gained more Minesweeper tiles from images. Jev drew nine against four and gained 5.5 tiles against 1.8, and Clef Flash gained 5.5 against 0.3. GPT-6 Luna Decisions went the other way in Tic-tac-toe, one draw against three. In Flappy Bird they scored zero or close to it from either input.

Two cautions. First, with 10 games per cell the confidence intervals overlap almost everywhere, so none of these differences are statistically significant and I'm not claiming they are. Second, the text inputs aren't a clean "same information, no pixels" control. They spell out coordinates and symbols the model would otherwise have to read off pixels, so they're more explicit than the images. My benchmark protocol says so: *"The model image and text conditions compare visual input with an explicit state serialization; they do not isolate an image encoder independently of text detail."* So the fair reading is narrow. On these three games, reading a screenshot was not the bottleneck. A model that played well did so from either input, and a model that didn't, didn't.

That's a little at odds with TypeSafe's warning that models do worse with images than with text. I don't think it contradicts it. My boards are simple, high-contrast and labelled, and the games are small. A busier image, or a task where reading the picture really is the hard part, could easily flip the result.

### The baselines draw the lines

Minimax and the constraint solver both hit the ceiling, which shows these games are fully solvable from the visible board. The free Minesweeper opening shows that a raw score of 33 to 38 is mostly free tiles. And the Flappy Bird baseline shows what's possible: 19.3 pipes for a one-line rule that reads the game state on every frame.

If you're choosing between a decision model and an LLM for a step in your agent, the principle that carries over is to measure each one against the floor as well as the ceiling. A score means very little until you know what you'd get for free and what perfect play gets. Those two numbers told me more about these models than the scores did, and they made the gap between the LLMs and the decision models impossible to miss.
