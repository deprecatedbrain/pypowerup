## Installation
The `bleak` package is required for Bluetooth communication. Install it using pip:
```bash
pip install bleak
```

## Class: PowerupConnection

### Initialization
```python
powerup = PowerupConnection()
```

### Constants
- `POWERUP_SERVICE_UUID`: Main service UUID for PowerUp device
- `BATTERY_SERVICE_UUID`: Battery service UUID
- `MOTOR_CONTROL_UUID`: Characteristic UUID for motor control
- `RUDDER_CONTROL_UUID`: Characteristic UUID for rudder control
- `BATTERY_LEVEL_UUID`: Characteristic UUID for battery level
- `BATTERY_CHARGING_UUID`: Characteristic UUID for charging status

### Methods

#### connect
```python
async def connect(target_name: str = "TailorToys PowerUp", timeout: float = 5) -> bool
```
Establishes connection with a PowerUp device.
- **Parameters:**
  - `target_name`: Name of the PowerUp device to connect to (default: "TailorToys PowerUp")
  - `timeout`: Time in seconds to search for device (default: 5)
- **Returns:** `True` if connection successful, `False` otherwise
- **Example:**
```python
success = await powerup.connect()
```

#### disconnect
```python
async def disconnect()
```
Disconnects from the PowerUp device.
- **Example:**
```python
await powerup.disconnect()
```

#### set_motor_speed
```python
async def set_motor_speed(speed: int)
```
Controls the motor speed of the PowerUp device.
- **Parameters:**
  - `speed`: Integer value between 0-254 (0 = off, 254 = maximum speed)
- **Raises:** 
  - `ValueError` if speed is outside valid range
  - `Exception` if not connected
- **Example:**
```python
await powerup.set_motor_speed(128)  # Set to half speed
```

#### set_rudder_angle
```python
async def set_rudder_angle(angle: int)
```
Controls the rudder angle of the PowerUp device.
- **Parameters:**
  - `angle`: Integer value between -128 and 127 (negative = left, positive = right)
- **Raises:**
  - `ValueError` if angle is outside valid range
  - `Exception` if not connected
- **Example:**
```python
await powerup.set_rudder_angle(-64)  # Turn left
```

#### get_battery_level
```python
async def get_battery_level() -> int
```
Retrieves the current battery level.
- **Returns:** Battery level percentage (0-100)
- **Raises:** `Exception` if not connected
- **Example:**
```python
level = await powerup.get_battery_level()
print(f"Battery at {level}%")
```

#### get_charging_status
```python
async def get_charging_status() -> bool
```
Checks if the device is currently charging.
- **Returns:** `True` if charging, `False` otherwise
- **Raises:** `Exception` if not connected
- **Example:**
```python
is_charging = await powerup.get_charging_status()
```

#### enable_battery_notifications
```python
async def enable_battery_notifications(callback: Callable[[int], None])
```
Enables notifications for battery level changes.
- **Parameters:**
  - `callback`: Function that takes an integer parameter (battery level)
- **Raises:** `Exception` if not connected
- **Example:**
```python
def on_battery_change(level: int):
    print(f"Battery changed to {level}%")

await powerup.enable_battery_notifications(on_battery_change)
```

#### test_all_characteristics
```python
async def test_all_characteristics()
```
Debug function that reads all available characteristics from the device.
- **Raises:** `Exception` if not connected
- **Example:**
```python
await powerup.test_all_characteristics()
```

## Example Usage
Here's a complete example showing basic usage of the PowerupConnection class:

```python
import asyncio
from powerup_connection import PowerupConnection

async def main():
    # Create connection instance
    powerup = PowerupConnection()
    
    # Connect to device
    connected = await powerup.connect()
    if not connected:
        print("Failed to connect")
        return
        
    try:
        # Check battery
        battery = await powerup.get_battery_level()
        print(f"Battery level: {battery}%")
        
        # Start motor at half speed
        await powerup.set_motor_speed(127)
        
        # Turn right
        await powerup.set_rudder_angle(64)
        
        # Wait 2 seconds
        await asyncio.sleep(2)
        
        # Stop motor
        await powerup.set_motor_speed(0)
        
    finally:
        # Always disconnect
        await powerup.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Errors
will throw exceptions in these cases:
- Device not connected when trying to use control methods
- Invalid values for motor speed or rudder angle
- Bluetooth communication errors
- Device not found during connection

Always wrap device control code in try/except blocks and ensure proper disconnection in finally blocks.
