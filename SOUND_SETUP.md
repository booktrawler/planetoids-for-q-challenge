# Sound Setup Guide for Planetoids

## Sound System Status

The Planetoids game includes authentic retro sound effects, but requires a working audio system to function.

### Current Status
When you run the game, you'll see one of these messages:

- ✅ `✓ Sound system initialized successfully` - Sound effects are working
- ⚠️ `⚠ Sound system unavailable: [error]` - Sound effects are disabled

### Sound Effects Included

The game features procedurally generated retro-style sound effects:

#### **Weapon Sounds**
- **Shooting**: 600Hz tone (0.1s) - Classic "pew" laser sound

#### **Damage Sounds** (Different tones for each damage type)
- **Asteroid Hit**: 200Hz low thud (0.2s)
- **Alien Ship Collision**: 800Hz sharp crash (0.3s) 
- **Alien Bullet Hit**: 1200Hz high-pitched zap (0.15s)
- **Hyperspace Malfunction**: 400Hz warbling sound (0.4s)

#### **Explosion Sounds** (Size-based)
- **Small Asteroid**: 150Hz base frequency (0.3s)
- **Medium Asteroid**: 150Hz base frequency (0.4s)
- **Large Asteroid**: 150Hz base frequency (0.5s)
- **Alien Ship**: 150Hz base frequency (0.5s) - Large explosion

### Troubleshooting Sound Issues

#### **Linux Systems**
1. **Check audio system**: `pulseaudio --check -v` or `pipewire --version`
2. **Install audio packages**: `sudo apt install pulseaudio alsa-utils`
3. **Test system audio**: `speaker-test -t sine -f 1000 -l 1`

#### **Headless/Server Environments**
- Sound effects require an audio output device
- The game will run perfectly without sound
- Consider using a virtual audio driver if needed

#### **Container/Docker Environments**
- May need `--device /dev/snd` flag for audio access
- Or run with `--privileged` for full audio access

### Manual Sound Test

You can test the sound system independently:

```bash
python3 sound_test.py
```

This will test:
- Pygame mixer initialization
- Basic sound generation
- All game frequencies (200Hz, 400Hz, 600Hz, 800Hz, 1200Hz)

### Technical Details

- **Audio Format**: 22050 Hz, 16-bit, stereo
- **Sound Generation**: Procedural sine waves (authentic retro style)
- **Volume Levels**: 
  - Shooting: 5% volume
  - Explosions: 8% volume  
  - Damage effects: 10% volume
- **Buffer Size**: 512 samples for low latency

The sound system is designed to fail gracefully - if audio is unavailable, the game continues normally with visual feedback only.
