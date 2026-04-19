Simple Python library for connecting to and controlling the PowerUp 4.0 (and maybe 3.0? don't have one to test but it seems to be similar).

# Dependencies
* bleak
* Python 3.8+

# Example usage
```py
conn = PowerupConnection()

await conn.connect()

await conn.set_motor_speed(150)
await conn.set_rudder_angle(20)

battery = await conn.get_battery_level()

await conn.disconnect()
```

# Documentation

## Class: `PowerupConnection`
Ititialize it with
```py
conn = PowerupConnection()
```
### Attributes
* `connected` -> `bool` current connection state
* `client` -> `BleakClient` active BLE client
* `device` -> BLE device reference

## Methods for connections

`connect(target_name="TailorToys PowerUp", timeout=5)`
Connects to the BLE device by name.
Returns
* `(True)` on success
* `(False, "CouldNotFind")` if device not found
```py
success = await conn.connect()
```

`disconnect()`
Disconnects from the device.
```py
await conn.disconnect()
```

## Control Methods
`set_motor_speed(speed: int)`
Sets motor speed
* Range `0-254`

`set_rudder_angle(angle: int)`
Sets rudder angle (steering)
* Range `-128–127`

## Battery Methods
`get_battery_level() -> int`
Returns battery percentage `(0–100)`.

`get_charging_status() -> bool`
Returns charging state
* `True` - charging
* `False` - not charging

`enable_battery_notifications(callback)`
Subscribes to battery updates.

**Callback signature**
```py
def callback(level: int):
    print(level)
```
**Usage**
```py
await conn.enable_battery_notifications(callback)
```

# Characteristics UUID reference
UUID Reference
Services
* PowerUp Service: `86c3810e-f171-40d9-a117-26b300768cd6`
* Battery Service: `0000180f-0000-1000-8000-00805f9b34fb`

Characteristics
* Motor Control: `86c3810e-0010-40d9-a117-26b300768cd6`
* Rudder Control: `86c3810e-0021-40d9-a117-26b300768cd6`
* Battery Level: `00002a19-0000-1000-8000-00805f9b34fb`
* Charging Status: `86c3810e-0040-40d9-a117-26b300768cd6`
