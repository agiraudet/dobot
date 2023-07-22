# Dobot - Dofus Retro Bot for Version 1.29

![Dobot Logo](https://github.com/agiraudet/dobot/blob/main/beacons/misc/logo.png)

## Disclaimer

**Dobot** is a bot designed for the game Dofus Retro (version 1.29). It utilizes image recognition using OpenCV and is intended for educational purposes only. It is important to note that **Dobot** is not designed to be an efficient or competitive bot. It is meant to serve as a learning tool for understanding image recognition techniques and game automation.

Using **Dobot** for any form of cheating, exploiting, or gaining an unfair advantage over other players is strictly discouraged and goes against the spirit of fair play in gaming. The developers and maintainers of this project do not endorse or encourage any illegal or unethical activities related to the usage of this bot.

## Project Overview

**Dobot** is a unique bot for Dofus Retro, unlike other similar bots that replace the game client. Instead, **Dobot** runs alongside the game client, using OpenCV for image recognition to interact with the game interface. This approach allows for a safer and more transparent user experience, as it does not interfere with the game files or alter the game client.

### Requirements

For **Dobot** to function correctly, the game settings should meet the following criteria:

- Display style: classique (4/3)
- Tactical mode enabled
- Display coordinates on the map
- Display moves range
- Allow shortcuts

### Collect Jobs Setup

To add a new collect job in **Dobot**, follow these steps:

1. Edit the `conf.json` file and refer to the existing job entries as examples.
2. Create a directory with the name of the job under `beacons/jobs`.
3. Add an `act.png` file to the newly created job directory, using the existing ones as a template.
4. To add a collectible resource to the job, simply add the `.png` file of the resource to the respective job directory.

**Note:** It is essential to use clear and distinct images for accurate image recognition.

## Getting Started

To get started with **Dobot**, follow these steps:

1. Clone this repository to your local machine.

```bash
git clone https://github.com/agiraude/dobot.git
```

2. Ensure you have the necessary dependencies installed. You can find them in the `requirements.txt` file. You can install them using `pip`:

```bash
pip install -r requirements.txt
```

3. Configure the game settings to match the requirements mentioned above.

4. Edit the `conf.json` file to add your desired collect jobs following the guidelines outlined in the project overview.

5. Run **Dobot**:

```bash
chmod +x start.sh && ./start.sh
```

**Note:** Running the bot while the game is active should be done with caution, and it is advisable to thoroughly review the game's terms of service and ensure compliance with the rules and regulations set forth by the game developers.

## Contributing

Contributions to **Dobot** are welcome! If you find any issues, have suggestions for improvements, or would like to add new features, please feel free to submit a pull request. However, keep in mind the educational and non-competitive nature of this project.

## License

This project is licensed under the [MIT License](LICENSE), which means you are free to use, modify, and distribute the code for educational purposes, subject to the terms and conditions of the license.

---

**Disclaimer:** The use of **Dobot** is entirely at your own risk, and the developers shall not be held responsible for any consequences arising from its usage. Always use it responsibly and in compliance with the game's terms of service.
