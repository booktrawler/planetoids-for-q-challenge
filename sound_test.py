#!/usr/bin/env python3
"""
Test script to check if pygame sound system is working
"""
import pygame
import math
import time

def test_sound():
    pygame.init()
    
    # Test mixer initialization
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✓ Pygame mixer initialized successfully")
        print(f"  Mixer settings: {pygame.mixer.get_init()}")
    except Exception as e:
        print(f"✗ Mixer initialization failed: {e}")
        return False
    
    # Test sound generation
    try:
        print("Generating test sound...")
        
        # Generate a simple beep
        sample_rate = 22050
        frequency = 440  # A note
        duration = 0.5
        frames = int(duration * sample_rate)
        
        arr = []
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr.append([int(wave), int(wave)])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
        sound.set_volume(0.3)
        
        print("Playing test sound...")
        sound.play()
        
        # Wait for sound to finish
        time.sleep(duration + 0.1)
        
        print("✓ Sound generation and playback successful")
        return True
        
    except Exception as e:
        print(f"✗ Sound generation failed: {e}")
        return False

def test_multiple_sounds():
    """Test different frequencies like the game uses"""
    frequencies = [200, 400, 600, 800, 1200]  # From the game
    
    for freq in frequencies:
        try:
            print(f"Testing {freq}Hz...")
            
            sample_rate = 22050
            duration = 0.2
            frames = int(duration * sample_rate)
            
            arr = []
            for i in range(frames):
                wave = 4096 * math.sin(freq * 2 * math.pi * i / sample_rate)
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(pygame.array.array('i', arr))
            sound.set_volume(0.1)
            sound.play()
            
            time.sleep(0.3)  # Brief pause between sounds
            
        except Exception as e:
            print(f"✗ Failed to generate {freq}Hz: {e}")

if __name__ == "__main__":
    print("=== Pygame Sound System Test ===")
    
    if test_sound():
        print("\n=== Testing Game-Style Sounds ===")
        test_multiple_sounds()
        print("\n✓ All sound tests completed")
    else:
        print("\n✗ Basic sound test failed - check your audio system")
    
    pygame.quit()
