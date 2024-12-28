from bleak import BleakScanner, BleakClient
from typing import Callable

class PowerupConnection:
    # Service UUIDs
    POWERUP_SERVICE_UUID = "86c3810e-f171-40d9-a117-26b300768cd6"
    BATTERY_SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"
    
    # Characteristic UUIDs
    MOTOR_CONTROL_UUID = "86c3810e-0010-40d9-a117-26b300768cd6"
    RUDDER_CONTROL_UUID = "86c3810e-0021-40d9-a117-26b300768cd6"
    BATTERY_LEVEL_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
    BATTERY_CHARGING_UUID = "86c3810e-0040-40d9-a117-26b300768cd6"

    def __init__(self):
        self.connected = False
        self.client = None
        self.device = None
        self._battery_callback = None
        
    async def connect(self, target_name: str = "TailorToys PowerUp", timeout: float = 5):
        print(f"Searching for device: {target_name}")
        self.device = await BleakScanner.find_device_by_filter(
            lambda d, ad: d.name and d.name.lower() == target_name.lower(),
            timeout=timeout
        )
        if not self.device:
            return False, "CouldNotFind"
            
        self.client = BleakClient(self.device.address)
        await self.client.connect()
        self.connected = True
        print(f"Connected to {self.device.name}")
        return True

    async def disconnect(self):
        if self.client and self.connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected")

    async def set_motor_speed(self, speed: int):
        """Sets the motor speed (0-254)"""
        if not self.connected:
            raise Exception("Not connected to the device")
        if not (0 <= speed <= 254):
            raise ValueError("Speed must be between 0 and 254")
        speed_hex = bytes([speed])
        await self.client.write_gatt_char(self.MOTOR_CONTROL_UUID, speed_hex)
        print(f"Motor speed set to {speed}")

    async def set_rudder_angle(self, angle: int):
        """Sets the rudder angle (-128 to 127)"""
        if not self.connected:
            raise Exception("Not connected to the device")
        if not (-128 <= angle <= 127):
            raise ValueError("Angle must be between -128 and 127")
        angle_hex = bytes([angle & 0xFF])  # Convert to signed byte
        await self.client.write_gatt_char(self.RUDDER_CONTROL_UUID, angle_hex)
        print(f"Rudder angle set to {angle}")

    async def get_battery_level(self) -> int:
        """Gets battery level percentage (0-100)"""
        if not self.connected:
            raise Exception("Not connected to the device")
        data = await self.client.read_gatt_char(self.BATTERY_LEVEL_UUID)
        level = int(data[0])
        print(f"Battery level: {level}%")
        return level

    async def get_charging_status(self) -> bool:
        """Gets charging status (True if charging)"""
        if not self.connected:
            raise Exception("Not connected to the device")
        data = await self.client.read_gatt_char(self.BATTERY_CHARGING_UUID)
        is_charging = bool(data[0])
        print(f"Charging status: {'Charging' if is_charging else 'Not charging'}")
        return is_charging

    async def enable_battery_notifications(self, callback: Callable[[int], None]):
        """Enable notifications for battery level changes"""
        if not self.connected:
            raise Exception("Not connected to the device")
            
        def notification_handler(sender: int, data: bytearray):
            battery_level = int(data[0])
            callback(battery_level)
            
        await self.client.start_notify(self.BATTERY_LEVEL_UUID, notification_handler)
        print("Battery notifications enabled")

    async def test_all_characteristics(self):
        """Test function to read all available characteristics"""
        if not self.connected:
            raise Exception("Not connected to the device")
            
        services = self.client.services
        for service in services:
            print(f"\nTesting service: {service.uuid}")
            for char in service.characteristics:
                print(f"\nCharacteristic: {char.uuid}")
                print(f"Properties: {char.properties}")
                
                try:
                    if "read" in char.properties:
                        value = await self.client.read_gatt_char(char.uuid)
                        print(f"Read value: {value.hex()}")
                except Exception as e:
                    print(f"Error reading: {str(e)}")