# 🚀 **Tank Battle Royale** 🎮💥

![Tank Battle Banner](https://example.com/banner.png)

Welcome to **Tank Battle Royale**, an exciting and strategic tank combat game built with Python! 🐍🔥 Dive into intense battles, strategize your moves, and dominate the battlefield! 🌟

---

## 🛠️ **Features** 🎯

- **Multiple Tank Classes**: Choose between different tank types, each with unique abilities! 🚀🔫
- **Real-Time Visualization**: Watch your tanks move and engage in battles with a dynamic Tkinter GUI! 🖥️✨
- **Resource Management**: Manage your tank's fuel, bullets, rockets, and health strategically to outlast your opponents! ⛽🔫💣❤️
- **Duplication Mechanism**: Clone your tanks to expand your army and overwhelm your enemies! 🪄🛡️
- **Recharge Points**: Navigate to recharge points to replenish your tank's resources and stay in the fight! ⚡🔋
- **Smart AI Opponents**: Face off against intelligent enemy tanks that adapt to your strategies! 🤖🎯

---

## 📦 **Installation** 💻

### **Prerequisites** 📝

- **Python 3.6+**: Ensure you have Python installed. [Download Python](https://www.python.org/downloads/) 🐍
- **Tkinter**: Comes pre-installed with most Python distributions. If not, install it using:

  ```bash
  sudo apt-get install python3-tk
  ```

### **Clone the Repository** 📥

```bash
git clone https://github.com/bbarni2020/tank-battle-royale.git
cd tank-battle-royale
```

### **Install Dependencies** 📦

This project uses only standard Python libraries, so no additional installations are required! 🎉

---

## 🎮 **How to Play** 🕹️

1. **Run the Game** 🚀

   Navigate to the project directory and execute the `main.py` script:

   ```bash
   python main.py
   ```

2. **Game Mechanics** ⚙️

   - **Tanks**: Control your tank (`MyTank` or any name you choose) and defeat enemy tanks (`EnemyTank`).
   - **Resources**: Manage your fuel, bullets, rockets, and health.
   - **Movement**: Move towards recharge points or engage enemies based on your strategy.
   - **Combat**: Use bullets and rockets to eliminate opponents. Running out of resources forces you to recharge.
   - **Duplication**: Clone your tank to create additional allies. Be strategic to avoid overextension!

3. **Victory Conditions** 🏆

   The game continues until only one tank remains or the maximum number of rounds is reached. Destroy all enemy tanks to claim victory! 💪🎉

---


### **Key Components** 🔍

- **`Tank` Class** 🛡️
  - Manages tank attributes like health, fuel, bullets, rockets, position, and more.
  - Handles actions such as shooting, rocket attacks, moving, and duplicating.

- **`EnemyTank` Class** 🤖
  - Inherits from `Tank` and represents AI-controlled enemy tanks.
  - Contains logic for targeting and engaging player tanks.

- **`TankGame` Class** 🎲
  - Manages the overall game state, including registering bots and running game rounds.

- **`TankVisualizer` Class** 🖼️
  - Handles the graphical representation of the game using Tkinter.
  - Draws tanks, recharge points, and updates the game status in real-time.


## 🛡️ **Gameplay Mechanics** 🎮

### **Tank Attributes** 📊

- **Health ❤️**: Determines how much damage a tank can take before being destroyed.
- **Fuel ⛽**: Required for tank movement. Depletes as the tank moves.
- **Bullets 🔫**: Ammunition for standard attacks.
- **Rockets 💣**: Ammunition for long-range attacks.
- **Score 🏅**: Tracks the number of enemy tanks destroyed.
- **Position 📍**: Current location on the grid.
- **Live Status ✅❌**: Indicates whether the tank is operational.
- **Recharge Points ⚡**: Locations where tanks can replenish their resources.

### **Actions** 🔄

- **Move 🚶‍♂️**: Navigate the tank towards a target position.
- **Shoot 🔫**: Fire bullets at adjacent tanks.
- **Rocket 💣**: Fire rockets at tanks within a three-tile radius.
- **Recharge ⚡**: Restore fuel, bullets, rockets, and health at recharge points.
- **Duplicate 🪄**: Clone the tank to create allies, consuming some resources.

---

## 🤝 **Contributing** 🌟

We welcome contributions from the community! If you'd like to contribute, please follow these steps:

1. **Fork the Repository** 🍴
2. **Create a Feature Branch** 🌿

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes** ✍️

   ```bash
   git commit -m "Add awesome feature"
   ```

4. **Push to the Branch** 🚀

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request** 📬

Please ensure your code follows the project's coding standards and includes relevant tests. 🙏

---

## 📜 **License** 📝

*This project uses a custom license. Please refer to the LICENSE file for more details.*

---

## 📧 **Contact** 📱

Have questions or suggestions? Reach out to us!

- **Email**: [your.email@example.com](mailto:barnabas@masterbros.dev) 📧
- **GitHub**: [@yourusername](https://github.com/bbarni2020) 🔗

Follow us on [Instagram](https://www.instagram.com/masterbrosdev/) for the latest updates! 🐦✨

---

## 🎉 **Acknowledgements** 🙌

- Thanks to all contributors and the open-source community for their support! 🌐💖
- Special shoutout to the Python community for providing essential libraries like Tkinter! 🐍🎈

---

Happy Tank Battling! 🚀💥
