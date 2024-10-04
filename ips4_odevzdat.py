class IAddressIPv4:
    def __init__(self, address: str):
        self.set(address)
    
    def isValid(self) -> bool:
        # Ověření platnosti adresy (musí mít 4 oktety, každý mezi 0 a 255)
        parts = self.address.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    def set(self, address: str) -> 'IAddressIPv4':
        self.address = address
        if not self.isValid():
            raise ValueError("Neplatná IPv4 adresa.")
        return self

    def getAsString(self) -> str:
        return self.address

    def getAsInt(self) -> int:
        # Převod IP adresy na integer
        parts = list(map(int, self.address.split('.')))
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    def getAsBinaryString(self) -> str:
        # Převod na binární řetězec
        return f"{self.getAsInt():032b}"

    def getOctet(self, number: int) -> int:
        # Získání specifického oktetu (1 až 4)
        parts = self.address.split('.')
        if not 1 <= number <= 4:
            raise ValueError("Oktet musí být mezi 1 a 4.")
        return int(parts[number - 1])

    def getClass(self) -> str:
        # Získání třídy IP adresy (A, B, C, D, nebo E)
        first_octet = self.getOctet(1)
        if 1 <= first_octet <= 126:
            return 'A'
        elif 128 <= first_octet <= 191:
            return 'B'
        elif 192 <= first_octet <= 223:
            return 'C'
        elif 224 <= first_octet <= 239:
            return 'D'
        elif 240 <= first_octet <= 255:
            return 'E'
        return 'Unknown'

    def isPrivate(self) -> bool:
        # Kontrola, zda je adresa privátní podle RFC 1918
        first_octet = self.getOctet(1)
        second_octet = self.getOctet(2)
        if first_octet == 10:
            return True
        elif first_octet == 172 and 16 <= second_octet <= 31:
            return True
        elif first_octet == 192 and second_octet == 168:
            return True
        return False


# Příklad použití:
try:
    ip = IAddressIPv4("192.168.1.1")
    print(f"IP adresa: {ip.getAsString()}")  # Výstup: 192.168.1.1
    print(f"Platná adresa: {ip.isValid()}")  # Výstup: True
    print(f"IP jako integer: {ip.getAsInt()}")  # Výstup: 3232235777
    print(f"IP jako binární řetězec: {ip.getAsBinaryString()}")  # Výstup: 11000000101010000000000100000001
    print(f"1. oktet: {ip.getOctet(1)}")  # Výstup: 192
    print(f"Třída adresy: {ip.getClass()}")  # Výstup: C
    print(f"Je privátní: {ip.isPrivate()}")  # Výstup: True
except ValueError as e:
    print(e)