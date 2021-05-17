
# OkeyCard
OkeyCard is a minigame from Metin2, the rules are simply: 

There are 24 cards, 3 colors(Red, Blue, Green), 8 cards each with numbers from 1 to 8. 
The goal of the game is to score at least 400 points, points can be earned by combining 3 cards:

100 points - One by one, cards of same colors (eg. 1R,2R,3R, R - red colour)

10 + 10 * the smallest card number - One by one, cards of different colors (eg. 1R,2B,3R = 20 points, R- red, B- blue)

10 + 10 * number of card - Three cards of the same number(eg. 8R, 8B, 8G = 90 poitns, R - red, B - blue, G- green)

## Goal
Creating a bot so that it plays faster and with better accuracy than the user
## Current results(will be updated as it progresses)
### How it looks in game(5 games, speed x4)

<p align="center">
  <img src="https://user-images.githubusercontent.com/81371889/116788400-9f13c500-aaa9-11eb-9a48-f3cf1c0b87b9.gif" alt="animated" />
</p>

### Results of BOT
#### General results:
| Games played  | Wins(>=400pkt) | Win ratio  | Average time for 1 game |
| :---: | :---: |:---: | :---:|
| 4410 | 1970  | 44.67%  |33.58s|
 
 
 **UPDATE, optimized version:**
| Games played  | Wins(>=400pkt) | Win ratio  | Average time for 1 game |
| :---: | :---: |:---: | :---:|
| 2932 |1340|45.70%|30.55s|

**UPDATE:** now BOT resign when game is unwinable(impossible to get 400 points), 

| Games played  | Wins(>=400pkt) | Win ratio  | Average time for 1 game |
| :---: | :---: |:---: | :---:|
| 2393 |1029|43.00|23.64s|

#### More detailed results:
<img src="https://user-images.githubusercontent.com/81371889/116786279-04fa4f80-aa9e-11eb-9317-f066b597a51d.png" width="50" height="200">


### Compare my game with the bot game

#### General results:

| | Games played  | Wins(>=400pkt) | Win ratio  | Average time for 1 game |
| :---: |:---:| :---:|:---: | :---: |
| **Me** |304 | 143 |47.03% |51.63s | 
| **BOT** | 304 | 150 |49.34%| 33.06s|

#### More detailed results:

<img src="https://user-images.githubusercontent.com/81371889/116787024-16455b00-aaa2-11eb-8640-587f74c23aea.png" width="150" height="200">

### Test yourself!
If you think I played the sets wrong, you can try to play the(first 50) sets yourself!

Download(only for Windows): https://drive.google.com/file/d/16xbowZ37K9XiXRZSl6io47qE3WJiB6GQ/view?usp=sharing

Scan: https://www.virustotal.com/gui/file/82a3777e04e4d11d8196b41ac9e4c5d57c1a0c3aada094b0e5a1761eb46c3ff6/detection

<p align="center">
  <img src="https://user-images.githubusercontent.com/81371889/115154223-11cc7b80-a07a-11eb-85ad-b6a3c58f8815.png" width="600" height="400">
</p>


## Future plan
Make the same bot, but using a Machine Learning model.
