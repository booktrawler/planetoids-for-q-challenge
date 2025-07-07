# Planetoids - ZX81 Classic Recreation

A faithful recreation of the 1981 Macronics classic "Planetoids" for the Sinclair ZX81, bringing the fast-paced asteroid-blasting action to modern systems with enhanced visual and audio feedback.

## About the Original

Planetoids was released in 1981 for the Sinclair ZX81 and required 16K of RAM. It was an adaptation of the popular arcade game Asteroids, featuring:

- Fast-paced space combat
- Strategic fuel management
- Eight-directional movement
- Hyperspace "panic button" for emergency escapes
- Progressive difficulty with more asteroids per level

## Enhanced Features

This recreation includes all the core gameplay elements plus modern enhancements:

### Core Gameplay
- **Ship Control**: Rotate and thrust in eight directions
- **Fuel Management**: Strategic element requiring fuel conservation to "get home safely"
- **Hyperspace**: Emergency teleportation with risk of destruction
- **Progressive Levels**: More asteroids spawn each level
- **Alien Ships**: Hostile UFOs that hunt the player
- **Asteroid Physics**: Large asteroids split into smaller ones when destroyed
- **Score System**: Points for destroying asteroids and aliens

### Enhanced Visual Feedback
- **Health System**: Ships now have 3 hit points instead of instant destruction
- **Damage Flash Effects**: Different colored flashes for different damage types:
  - **Red-Orange**: Asteroid collisions
  - **Bright Red**: Alien ship collisions (2 damage)
  - **Yellow-Red**: Alien bullet hits
  - **Purple**: Hyperspace malfunctions
- **Fading Flash Intensity**: Damage flashes fade out smoothly over time
- **Health Bar**: Visual health indicator in the HUD
- **Damage Type Indicators**: On-screen notifications for different hit types

### Enhanced Audio Feedback
- **Hit Sounds**: Different tones for each damage type:
  - Low thud for asteroid hits
  - Sharp crash for alien collisions
  - High-pitched zap for alien bullets
  - Warbling sound for hyperspace damage
- **Shooting Sounds**: Audio feedback for weapon fire
- **Explosion Sounds**: Different explosion sounds based on object size

## Controls

- **Arrow Keys / WASD**: Rotate ship and thrust
- **Spacebar**: Fire weapons
- **H**: Hyperspace (panic button) - teleports to random location with 10% destruction risk
- **P**: Pause game
- **Enter**: Start game / Restart after game over
- **Escape**: Quit game

## Installation

1. Install Python 3.6 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python planetoids.py
   ```

## Gameplay Tips

1. **Health Management**: You now have 3 hit points - use them strategically!
2. **Fuel Management**: Your ship has limited fuel. Use thrust wisely to conserve fuel for the journey "home"
3. **Hyperspace Strategy**: Use hyperspace (H key) as a last resort - there's a 10% chance of destruction
4. **Asteroid Tactics**: Large asteroids split into 2-3 smaller ones, so position yourself carefully
5. **Alien Threats**: UFOs appear periodically and actively hunt you - they're worth 500 points but deal 2 damage
6. **Invulnerability**: You have 2 seconds of invulnerability after taking damage
7. **Visual Cues**: Pay attention to the flash colors to understand what hit you

## Scoring

- Large Asteroids: 20 points
- Medium Asteroids: 50 points  
- Small Asteroids: 100 points
- Alien Ships: 500 points

## Damage System

- **Asteroids**: 1 damage per hit
- **Alien Ships**: 2 damage per collision
- **Alien Bullets**: 1 damage per hit
- **Hyperspace Malfunction**: Instant destruction (10% chance)

## Technical Notes

This recreation captures the spirit of the original ZX81 version while adding modern conveniences:

- Smooth 60 FPS gameplay (vs. the original's more limited framerate)
- Vector-based graphics maintaining the minimalist aesthetic
- Faithful physics and collision detection
- Strategic fuel management system as described in the original
- Enhanced health system for more forgiving gameplay
- Procedural sound generation for authentic retro audio
- Dynamic visual feedback system with fading effects

The game maintains the core challenge and addictive gameplay that made Planetoids a standout title for the ZX81 platform, while adding quality-of-life improvements that enhance the player experience.

## Credits

Original Planetoids (1981) - Developed and Published by Macronics for Sinclair ZX81
This recreation - A tribute to the classic space shooter genre with modern enhancements
