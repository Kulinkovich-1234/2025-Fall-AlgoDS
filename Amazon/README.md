# Amazon Chess Matching System

A robust online/offline matching system for Amazon Chess, enabling seamless local and remote gameplay.

## Features
- **Local Two-Player Battles**: Run the system entirely offline for face-to-face matches.
- **Online P2P Battles**: Connect players globally via peer-to-peer (P2P) networking.
- **ZeroTier Integration**: Recommended for reliable online connections (avoids firewall/LAN configuration challenges).
- **Game Replay & Data Management**: Save matches, view replays, and load historical games.

## Quick Start

### Launch the Game
```bash
python two_player_amazon.py
```

### Gameplay Modes
1. **Local Play**  
   Two players on the same device can start a match immediately.

2. **Online Play**  
   - **Host**: Run the game and note your local IP (e.g., `192.168.x.x`).
   - **Client**: Enter the Host's IP to establish connection.
   > *Note: Standard LAN P2P may fail due to firewall restrictions. Always use [ZeroTier](https://www.zerotier.com) for stable virtual LAN connections.*

3. **Post-Game Features**  
   After a match:
   - **Replay**: View the game history in real-time.
   - **Save Match**: Export match data to `.pkl` files.
   - **Load Match**: Open saved `.pkl` files to review past games.

## Usage Notes
- All match data is saved in root directory by default.
- For online matches, ensure both players have ZeroTier installed and connected to the same network.
- The `two_player_amazon.py` script handles game logic, and data management. The `two_player_amazon_network` script handles network setup.
