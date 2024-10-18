# CAT 🐈
### Chess Algorithmic Training 

## What does it contain of?
1. **Chess game**
   - **fully written by myself** - even en passant
   - **playable** - you can just play it with your friend
   - **tested** - processed 1 milion games from database.lichess.org
2. **Chess engine**
   - work in progess

## How to play?
1. Install requirements
2. Run play_offline.py script
3. Enter correct moves (Algebraic chess notation) by typing, confirm by enter
   - **warning** - if you enter invalid notation (like "fdsljjdla" game would crash)
   <br>why don't I change it? Don't think that pro-chess players make mistakes?
   <br> **but if** move is invalid from its nature (chess rules), it is detected
   - if you are struggling, see this notation on Wikipedia, chess.com or see 
   <br> "print_move_description(...)" function in "notation_translator"

## Problems that would be fixed soon
1. Game doesn't end on itself when checkmate is there
2. Game doesn't detect draws:
   - stalemate
   - dead position (also insufficient mating material)
   - Threefold Repetition
   - 50 move rule
3. invalid notation inputs
   - hey come on boss, is it really a problem?