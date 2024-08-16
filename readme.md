# Pixel Dungeon 2

Make sure to read the [License](./LICENSE) File.

Install the [requirments](#requirements)


## Warns
- ! We are working on a Map Editor for this game, so the update will be delayed while I and others are working on these 2 projects simultaneously, please be patient.
- ! About the *In-Game*, the in-game system is f*cked, and i will need to fix this, but also i need to rework this, so i will erase all and rewrite all of the system, more delay on the next updates.

# Changes
**V1.0.2**
- Render Distance/Field Of View now are working, can help for low perfomance PCs;
- Draw Map changed;
- Fixed Sprites Backgrounds;
- Re-worked Barrier Sprite;
- Water & Barrier Animated;
- FPS Independant Animation;
- Gravity FPS Independant;
- Tips for some Widgets;
- Engine updated;

# How to edit maps?
is easy to edit maps, only follow this steps:
- 1. Find "Data" folder in your game directory;
- 2. Inside of "Data" find ["maps.json"](./data/maps.json);
- 3. Open ["maps.json"](./data/maps.json);
- 4. Actually the unique map used is "default-map", so, edit it using the ids of tiles;
- 5. is it, easy yeh?

# Credits
- [@MrJuaumBR](https://github.com/MrJuaumBR)
- [@akvendramin](https://github.com/akvendramin)

# Requirements
- maxpygame >= 0.1.7fix2
- pygame
- xlwt
- JPyDB >= 0.8.1
- Requests

Please install all items form [Requirements.txt](./requirements.txt)


```py
python -m pip install -r .\requirements.txt
```