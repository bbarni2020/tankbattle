import tkinter as tk
import time
import random


class postitions:
        occupied_positions = []

#%% Tank
class Tank:
    def __init__(self):
        self.name = "Unnamed Tank"
        self.health = 10
        self.fuel = 25
        self.bullets = 5
        self.rockets = 2
        self.score = 0
        self.position = (0, 0)  # (x, y)
        self.live = True
        self.grid_size = 12
        self.recharge_place = (0, 0)
        self.color = "green"
        self.recharge_num = 3
        self.tired = 35
        self.way = False
        self.dupolicate = True

    def distance_to(self, target):
        if isinstance(target, Tank):  # If the target is a tank, get its position
            target = target.position
        return abs(self.position[0] - target[0]) + abs(self.position[1] - target[1])

    def can_shoot(self, bot):
        return self.distance_to(bot) == 1 and self.bullets > 0

    def can_rocket(self, bot):
        return self.distance_to(bot) <= 3 and self.rockets > 0

    def shoot(self, bot):
        if self.tired <= 0:
            self.live = False
            return
        self.tired -= 1
        if self.can_shoot(bot):
            bot.health -= 1
            self.bullets -= 1
            print("Shot at tank", bot.name, "with", self.name)
            if bot.health <= 0:
                bot.live = False
                self.score += 1
                print("Destroyed tank", bot.name, "with", self.name)
                TankVisualizer.bot_sprites = []

    def rocket(self, bot):
        if self.tired <= 0:
            self.live = False
            return
        self.tired -= 2
        if self.can_rocket(bot):
            bot.health -= 2
            self.rockets -= 1
            print("Rocketed at tank", bot.name, "with", self.name)
            if bot.health <= 0:
                bot.live = False
                self.score += 1
                print("Destroyed tank", bot.name, "with", self.name)
                TankVisualizer.bot_sprites = []

    def recharge(self):
        if self.position == self.recharge_place and self.recharge_num > 0:
            self.fuel = 25
            self.bullets = 10
            self.rockets = 2
            self.health = 10
            self.tired = 35
            print("Recharged in tank", self.name)
            self.recharge_num -= 1
            print("Recharge remaining:", self.recharge_num)

    def move(self, target):
        if self.fuel <= 0:
            self.live = False
            return
        if self.tired <= 0:
            self.live = False
            return
        self.tired -= 1
        old_position = self.position
        x, y = self.position
        tx, ty = target
        if x < tx:
            x += 1
        elif x > tx:
            x -= 1
        elif y < ty:
            y += 1
        elif y > ty:
            y -= 1

        # Access the class attribute explicitly
        if (x, y) not in postitions.occupied_positions:
            self.position = (x, y)
            self.fuel -= 1
            try:
                postitions.occupied_positions.remove(old_position)
            except:
                pass
            postitions.occupied_positions.append(self.position)
            self.recharge_num = 3


    def get_nearest_bot(self, bots):
        living_bots = [bot for bot in bots if bot.live and bot != self]
        if not living_bots:
            return None
        return min(living_bots, key=lambda bot: self.distance_to(bot))

    def is_recharging(self, nearest_bot):
        return nearest_bot.position == nearest_bot.recharge_place
    
    def duplicate(self, fuel, bullets, rockets, new_tank):
        if self.tired < 5:
            print(f"{self.name} is too tired to duplicate!")
            return None

        self.tired -= 5  # Deduct tiredness for duplication

        # Create the duplicate tank
        new_tank.name = self.name
        new_tank.fuel = max(0, min(fuel, self.fuel))
        new_tank.bullets = max(0, min(bullets, self.bullets))
        new_tank.rockets = max(0, min(rockets, self.rockets))
        new_tank.health = 10
        new_tank.color = "blue"  # Distinct color for clones
        new_tank.position = self.position  # Start at the same position
        new_tank.recharge_place = self.recharge_place
        new_tank.duplicate = False

        self.fuel -= new_tank.fuel
        self.bullets -= new_tank.bullets
        self.rockets -= new_tank.rockets

        print(f"{self.name} duplicated itself! New tank: {new_tank.name}")
        return new_tank

#%% Tank game
class TankGame:
    def __init__(self):
        self.grid_size = 12
        self.bots = []
        self.living_bots = []

    def register_bot(self, bot_class):
        while True:
            position = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if position not in [bot.position for bot in self.bots]:
                break
        bot = bot_class()
        bot.position = position
        bot.recharge_place = (
            random.randint(0, self.grid_size - 1),
            random.randint(0, self.grid_size - 1),
        )
        self.bots.append(bot)

    def run_game(self, max_rounds=10):
        try:
            for round in range(max_rounds):
                for bot in self.bots:
                    if bot and bot.live:
                        time.sleep(0.5)
                        bot.run(self.bots)
                self.living_bots = [bot for bot in self.bots if bot and bot.live]
                living_bots = self.living_bots
                
                if len(living_bots) > 0 and all(bot.name == living_bots[0].name for bot in living_bots):
                    print(f"Game Over! Winners: {', '.join(bot.name for bot in living_bots)}")
                    exit()
                    break
                
                if len(living_bots) <= 1:
                    print(f"Game Over! Winner: {living_bots[0].name if living_bots else 'No one'}")
                    exit()
                    break
        except Exception as e:
            print(f"An error occurred during game execution: {e}")


#%% Visualizer

class TankVisualizer:
    def __init__(self, game, cell_size=50):
        self.game = game
        self.cell_size = cell_size
        self.round = 0
        self.root = tk.Tk()
        self.root.title("Tank Battle Visualizer")

        self.canvas = tk.Canvas(
            self.root,
            width=game.grid_size * cell_size,
            height=game.grid_size * cell_size,
            bg="white"
        )
        self.canvas.pack()

        self.status_frame = tk.Frame(self.root, bg="lightgray")
        self.status_frame.pack(fill=tk.X)
        self.round_label = tk.Label(
            self.status_frame, text=f"Round: {self.round}", font=("Arial", 14), bg="lightgray"
        )
        self.round_label.pack(side=tk.LEFT, padx=10)
        self.status_text = tk.Text(
            self.status_frame, height=5, width=60, font=("Courier", 12), state=tk.DISABLED
        )
        self.status_text.pack(side=tk.RIGHT, padx=10)

        self.bot_sprites = {}
        self.bot_paths = {}
        self.grid_size = game.grid_size

    def draw_grid(self):
        for i in range(self.grid_size + 1):
            self.canvas.create_line(
                i * self.cell_size, 0, i * self.cell_size, self.grid_size * self.cell_size
            )
            self.canvas.create_line(
                0, i * self.cell_size, self.grid_size * self.cell_size, i * self.cell_size
            )

    def draw_recharge_points(self):
        for bot in self.game.bots:
            rx, ry = bot.recharge_place
            self.canvas.create_rectangle(
                rx * self.cell_size + 5,
                ry * self.cell_size + 5,
                rx * self.cell_size + self.cell_size - 5,
                ry * self.cell_size + self.cell_size - 5,
                outline="green",
                width=2
            )
            self.canvas.create_text(
                rx * self.cell_size + self.cell_size // 2,
                ry * self.cell_size + self.cell_size // 2,
                text=bot.name,
                fill="green",
                font=("Arial", 10, "bold")
            )

    def draw_bots(self):
        for bot in self.game.bots:
            x, y = bot.position
            if bot not in self.bot_sprites:
                # Create a new sprite for the bot
                self.bot_sprites[bot] = self.canvas.create_oval(
                    x * self.cell_size + 5,
                    y * self.cell_size + 5,
                    x * self.cell_size + self.cell_size - 5,
                    y * self.cell_size + self.cell_size - 5,
                    fill=bot.color if bot.live else "grey",  # Set color based on live status
                )
                self.bot_paths[bot] = [bot.position]
            else:
                # Update the color of the sprite based on live status
                current_color = "grey" if not bot.live else bot.color
                self.canvas.itemconfig(self.bot_sprites[bot], fill=current_color)

                if bot.way:
                    old_positions = self.bot_paths.get(bot, [])
                    if old_positions and old_positions[-1] != bot.position:
                        old_positions.append(bot.position)
                        for i in range(1, len(old_positions)):
                            x1, y1 = old_positions[i - 1]
                            x2, y2 = old_positions[i]
                            self.canvas.create_line(
                                x1 * self.cell_size + self.cell_size // 2,
                                y1 * self.cell_size + self.cell_size // 2,
                                x2 * self.cell_size + self.cell_size // 2,
                                y2 * self.cell_size + self.cell_size // 2,
                                fill=bot.color if bot.live else "grey",
                                width=2
                            )
                        self.bot_paths[bot] = old_positions  # Update the path

                # Update the position of the bot's sprite
                self.canvas.coords(
                    self.bot_sprites[bot],
                    x * self.cell_size + 5,
                    y * self.cell_size + 5,
                    x * self.cell_size + self.cell_size - 5,
                    y * self.cell_size + self.cell_size - 5,
                )

    def update_bot_status(self, bot):
        """Log the bot's status."""
        status_message = (
            f"{bot.name} moved to {bot.position}, "
            f"fuel: {bot.fuel}, bullets: {bot.bullets}, "
            f"rockets: {bot.rockets}, health: {bot.health}, tired: {bot.tired}\n"
        )
        self.status_text.configure(state=tk.NORMAL)
        self.status_text.insert(tk.END, status_message)
        self.status_text.configure(state=tk.DISABLED)
        self.status_text.see(tk.END)  # Auto-scroll to the latest status

    def animate(self, max_rounds=10):
        self.draw_grid()
        self.draw_recharge_points()
        self.draw_bots()

        for _ in range(max_rounds):
            self.round += 1
            self.round_label.config(text=f"Round: {self.round}")

            # Run game logic and update visuals
            self.game.run_game(1)
            self.draw_bots()
            for bot in self.game.bots:
                self.update_bot_status(bot)

            self.root.update()
            time.sleep(0.5)

        self.root.mainloop()



#%% Enemy Tank
class EnemyTank(Tank):
    def __init__(self):
        super().__init__()
        self.name = "Enemy tank"
        self.way = False
        self.color = "red"

    def run(self, bots):
        if not self.live:
            return
        max_tired = 35
        max_fuel = 25
        nearest_bot = self.get_nearest_bot(bots)
        distance_to_recharge = self.distance_to(self.recharge_place)

        # Quickly return to the recharge point if out of bullets or rockets
        if self.bullets == 0 or self.rockets == 0:
            if self.position != self.recharge_place:
                self.move(self.recharge_place)
            else:
                # Attempt to recharge if possible
                if self.recharge_num > 0:
                    self.recharge()
            return

        # Recharge logic if resources are critically low
        if self.tired <= 3 or self.fuel <= distance_to_recharge:
            if self.position != self.recharge_place:
                self.move(self.recharge_place)
            else:
                # Recharge if there are uses left
                if self.recharge_num > 0:
                    self.recharge()
            return

        # Combat Logic: Engage nearest bot if resources allow
        if nearest_bot and nearest_bot.name != self.name:
            if self.can_shoot(nearest_bot):
                self.shoot(nearest_bot)
            elif self.can_rocket(nearest_bot):
                self.rocket(nearest_bot)
            else:
                self.move(nearest_bot.position)
        else:
            # If no bots are alive, return to recharge point for safety
            self.move(self.recharge_place)
