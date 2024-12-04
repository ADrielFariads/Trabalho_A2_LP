# Cosmic Survivor
by Adriel Dias, Gabriel Schuenker, Kauan Kevin, João Vitor Resende

<br>
<p >
  <img src="https://github.com/user-attachments/assets/bc188eaa-3f02-4345-ab7f-d07e38ad7466">
</p>
<br>

## About the project
Welcome to Cosmic Survivor, an action-packed survival game developed with Pygame! In this adventure, you take control of a hero stranded on an alien planet, fighting against waves of monstrous creatures to survive as long as possible and achieve the highest score. Choose your hero wisely, as each has unique abilities that can turn the tide in your favor!

### Heroes
- Cyborg: A versatile and balanced fighter available from the start. Perfect for beginners.
- Machinegun: A ranged powerhouse with rapid-fire attacks. Requires unlocking through achievements.
- Blade Master: A melee expert with devastating close-range abilities. Also unlockable by progressing in the game.
<br>
<p >
  <img src="https://github.com/user-attachments/assets/1c00dcad-97ae-4dcd-829e-5521da538829">
</p>
<br>

### Enemies
Face relentless waves of alien monsters, including:

- Goblin: Quick and numerous, they test your reflexes.
- Andromaluis: Strong and durable, posing a significant challenge.
- Slime: Slippery and unpredictable, capable of surprising attacks.
- AlienBat: Flying foes that keep you on your toes.
<br>
<p>
  <img src="https://github.com/user-attachments/assets/c5f1b960-6136-4e89-8e30-b33b3ced3571">
</p>
<br>

### Gameplay
Survive for as long as possible while eliminating waves of enemies. Your performance depends on your hero's skills and your strategy. The game features three difficulty levels:

- Low: Ideal for practice or casual play.
- Medium: A balanced challenge for most players.
- High: Only for the brave! Enemies are relentless and unforgiving.
<br>
<p>
  <img src="https://github.com/user-attachments/assets/525b5704-054d-4783-ae6e-653169cfc4c3">
</p>
<br>
Unlock new heroes by achieving milestones and climbing the leaderboard. Can you become the ultimate survivor?

## Project directories

* **assest**: Contains the sprites of characters/objects, images and audios used in the game.

* **src**: The source directory, contains most of the project functions.

* **tests**: Test directory, used to test the functions of **src**.

 ## Installing this project

 First of all, you can clone the repository: 

 ```bash

   git clone https://github.com/ADrielFariads/Trabalho_A2_LP.git

```

 And be sure you have installed compatible versions of the libraries used. The versions we used are available in `requirements.txt`


 ```python

    pip install -r requirements.txt

```

After that, you have all the necessary things to run the game. So, to do it, run:

```shell
$ python main.py
```

## Using the project

In the menu there is an option to view the controllers:

<br>
<p>
  <img src="https://github.com/user-attachments/assets/c511d183-e117-4227-819c-f46842331d87">
</p>
<br>

In the interface game when you hover the mouse over the skills we get information about them:

<br>
<p>
  <img src="https://github.com/user-attachments/assets/6eca1233-18ae-4c59-adce-9f73a18981f9">
</p>
<br>

Now just click play and have fun!!

## Tests

You can run the files in `tests` folders to test the modules in `src`.

```bash

python -m unittest discover -s tests -p "*.py"

```
