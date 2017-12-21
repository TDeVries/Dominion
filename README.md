# Dominion
Game engine for the board game Dominion (base set v1). WIP

Class Descriptions:

| File        | Description           |
| :-------------: |-------------|
|    cards.py      | Contains information about all of the cards, including cost, value and any special effects that the card may have |
|    player.py     | Contains player, hand and deck information      |
|     game.py      | Contains general game information such as supply pile setup and player management      |
|    play_game.py  |   Currently a debugging script, however this will manage the main game loop |


Features to add:

- [ ] Special abilities for cards
- [x] Main game loop
- [ ] Implement basic AI
- [ ] Implement more advanced AI

Decisions to make:
- Interface type (GUI, website, cmd, slack, etc.)
- Interaction type (application client/server, web client/server, etc)
