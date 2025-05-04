# Wolfenstein Game Coursework Report

## 1. Introduction

### 1.1 What is your application?
The Wolfenstein game is a Python-based first-person shooter that uses 2D raycasting to simulate a 3D environment. The game includes features such as player movement, enemy AI, weapon mechanics, and level rendering. It demonstrates object-oriented programming (OOP) principles and implements design patterns like the Factory Method.

### 1.2 How to run the program?
1. Install Python (version 3.10 or higher).
2. Install the required library:
   ```
   pip install pygame
   ```
3. Run the `main.py` file:
   ```
   python main.py
   ```

### 1.3 How to use the program?
- Use the arrow keys or `WASD` to move the player.
- Use space to shoot(stab).
- Press `ESC` to return to the main menu.
- Collect gold and ammo to increase your score and resources.

---

## 2. Body/Analysis

### 2.1 Functional Requirements Implementation
The program meets the functional requirements by implementing:
- **Player Movement**: The `Player` class handles movement and interaction with the environment.
- **Enemy AI**: The `NPC` class and its subclasses (`SoldierNPC`, `OfficerNPC`) implement enemy behavior.
- **Weapons**: The `Gunmanager` class manages weapon switching and shooting mechanics.
- **Level Rendering**: The `Raycaster` class handles raycasting for 3D-like rendering.

### 2.2 Code Examples

#### Polymorphism
Polymorphism is demonstrated in the `Gunmanager` class, where different weapons (e.g., `Knife`, `Gun`) share a common interface for updating and reloading:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\gun.py
class Gunmanager():
    def update(self, screen):
        current_weapon = self.weapons[self.current_weapon_index]
        current_weapon.update(screen)
```

#### Abstraction
The `weapon` abstract class defines a common interface for all weapon types:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\ammo.py
class weapon(ABC):
    @abstractmethod
    def dothing(self):
        pass
```

#### Inheritance
The `SoldierNPC` and `OfficerNPC` classes inherit from the `NPC` class:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\factory.py
class SoldierNPC(NPC):
    def __init__(self, player, raycaster, map, path, pos, scale=30, shift=0.01):
        super().__init__(player, raycaster, map, path, pos, scale, shift)
```

#### Encapsulation
The `Player` class encapsulates player attributes like health and ammo:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\player.py
class Player:
    def __init__(self, map):
        self._health = 100
        self._ammo = 10
```

#### Factory Method
The `NPCFactory` class creates NPC objects based on their type:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\factory.py
class NPCFactory:
    @staticmethod
    def create_npc(npc_type, player, raycaster, map, pos):
        if npc_type == "soldier":
            return SoldierNPC(player, raycaster, map, "path/to/soldier.png", pos)
```

#### Aggregation
The `ObjectHandler` class aggregates multiple sprites and NPCs:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\sprite_handler.py
class ObjectHandler:
    def __init__(self, player, raycaster, map):
        self.sprite_list = []
        self.npc_list = []
```

#### Saving to a Text File
Highscores are saved to a text file using the `write_highscore` function:
```python
# filepath: c:\Users\AK\Documents\bbb\python\wolfenstein\highscore.py
def write_highscore(score):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(f"{score}\n")
```

---

## 3. Results and Summary

### 3.1 Results
- Implemented a functional first-person shooter game with raycasting.
- Demonstrated OOP principles.
- 

### 3.2 Conclusions
- The coursework achieved a playable game that meets the functional requirements.
- The use of OOP principles improved code modularity and reusability.
- Some challenges I faced while working on this project were implementing doors, handling player collisions with sprites and walls.  

### 3.3 Future Prospects
- Rework the animated sprites class to improve animation, as the current animation speed is directly dependent on the frame rate.
- Implement advanced AI for enemies.
- Fix performance issues.
- Implement better UI.
- Make more levels.

