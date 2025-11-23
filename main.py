import time
import sys
import argparse
from input_reader import InputReader
from output_emulator import OutputEmulator # Keep for legacy/keyboard mode
from browser_bridge import BrowserBridge
from dsu_server import DSUServer

def main():
    parser = argparse.ArgumentParser(description='Xbox Controller Emulator for HOTAS Warthog')
    parser.add_argument('--mode', choices=['keyboard', 'browser', 'udp'], default='browser', 
                        help='Emulation mode: keyboard (WASD), browser (Cloud Gaming), or udp (Emulators)')
    args = parser.parse_args()

    print(f"Starting Xbox Controller Emulator in {args.mode.upper()} mode...")
    
    reader = InputReader()
    reader.start()

    output = None
    if args.mode == 'keyboard':
        output = OutputEmulator()
    elif args.mode == 'browser':
        output = BrowserBridge()
        output.start()
        print("Browser Bridge running. Open the 'browser_script.js' in your browser console.")
    elif args.mode == 'udp':
        output = DSUServer()
        output.start()
        print("UDP DSU Server running on port 26760. Configure your emulator to use this.")

    try:
        while True:
            state = reader.get_state()
            
            if args.mode == 'keyboard':
                output.update(state)
            elif args.mode == 'browser':
                output.broadcast(state)
                # Debug print to confirm data flow
                # print(f"\rJoy: {state['joy_x']:.2f}, {state['joy_y']:.2f} Btns: {state.get('buttons_1',0):02x} Hat: {state.get('hat',-1)}", end="")
            elif args.mode == 'udp':
                output.update(state)
            
            # Print state every 1s to verify inputs are being read
            if int(time.time() * 10) % 10 == 0:
                 print(f"\rState: Joy=({state['joy_x']:.2f}, {state['joy_y']:.2f}) Hat={state.get('hat',-1)} Btn={state.get('buttons_1',0):02x}", end="")
            
            time.sleep(0.005) # 200Hz
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        reader.stop()
        if args.mode == 'browser':
            output.stop()
        elif args.mode == 'udp':
            output.stop()
        print("Stopped.")

if __name__ == "__main__":
    main()
