#So this was the original file which I have been copied to __init__.py for proper working
#This is a base game setup and my tank registered to the game


from tankbattle import TankGame, Tank, EnemyTank, TankVisualizer


class MyTank(Tank):
    def __init__(self):
        super().__init__()
        self.name = "My Tank"
        self.way = True

    def run(self, bots):
        if not self.live:
            return
        max_tired = 35
        max_fuel = 25
        nearest_bot = self.get_nearest_bot(bots)
        distance_to_recharge = self.distance_to(self.recharge_place)
        
        if self.duplicate:
            if self.tired == max_tired and self.fuel == max_fuel:
                if self.position != self.recharge_place:
                    self.move(self.recharge_place)
                else:
                    if self.fuel > 10 and self.bullets > 2 and self.rockets > 1:
                        game.register_bot(Tank.duplicate(self, max_fuel, 5, 2, MyTank))
                        visualizer.draw_recharge_points()
                return

        if self.bullets == 0 or self.rockets == 0:
            if self.position != self.recharge_place:
                self.move(self.recharge_place)
            else:
                if self.recharge_num > 0:
                    self.recharge()
            return

        if self.tired <= 3 or self.fuel <= distance_to_recharge:
            if self.position != self.recharge_place:
                self.move(self.recharge_place)
            else:

                if self.recharge_num > 0:
                    self.recharge()
            return

        if nearest_bot and nearest_bot.name != self.name:
            if self.can_shoot(nearest_bot):
                self.shoot(nearest_bot)
            elif self.can_rocket(nearest_bot):
                self.rocket(nearest_bot)
            else:
                self.move(nearest_bot.position)
        else:
            self.move(self.recharge_place)





if __name__ == "__main__":
    game = TankGame()
    game.register_bot(MyTank)
    game.register_bot(EnemyTank)
    
    visualizer = TankVisualizer(game)
    visualizer.animate(max_rounds=10000)