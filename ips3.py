import json

class NetIPv4:
    def __init__(self, network_str):
        """
        Inicializuje klasy s danou IP sítí (např. '192.168.1.0/24').
        """
        try:
            # Rozdělení IP adresy a prefixu
            ip_str, prefix_len = network_str.split('/')
            self.network_address = self.ip_to_int(ip_str)
            self.prefix_len = int(prefix_len)
            
            # Výpočet masky a broadcast adresy
            self.netmask = (0xFFFFFFFF << (32 - self.prefix_len)) & 0xFFFFFFFF
            self.hostmask = (~self.netmask) & 0xFFFFFFFF
            self.broadcast_address = self.network_address | self.hostmask
        except ValueError as e:
            raise ValueError(f"Nedělej si ze mě srandu: {network_str}") from e

    def ip_to_int(self, ip_str):
        """
        Převede IP adresu z textové podoby na 32bitové celé číslo.
        """
        parts = list(map(int, ip_str.split('.')))
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    def int_to_ip(self, ip_int):
        """
        Převede 32bitové celé číslo na IP adresu v textové podobě.
        """
        return '.'.join(map(str, [
            (ip_int >> 24) & 0xFF,
            (ip_int >> 16) & 0xFF,
            (ip_int >> 8) & 0xFF,
            ip_int & 0xFF
        ]))

    def is_valid(self):
        """
        Zkontroluje, jestli je zadaná IP adresa platná.
        """
        return 0 <= self.network_address <= 0xFFFFFFFF and 0 <= self.prefix_len <= 32

    def get_count(self):
        """
        Vrátí počet adres v síti včetně broadcast adresy.
        """
        total_addresses = 2 ** (32 - self.prefix_len)
        return {
            "total_addresses": total_addresses,
            "broadcast_address": self.int_to_ip(self.broadcast_address)
        }

    def contains_ip(self, ip_str):
        """
        Zkontroluje, jestli zadaná IP adresa je v rozsahu této sítě.
        """
        ip = self.ip_to_int(ip_str)
        return (self.network_address & self.netmask) == (ip & self.netmask)

    def network_range(self):
        """
        Vrátí první a poslední IP adresu v síti (první = síťová, poslední = broadcast).
        """
        return (self.int_to_ip(self.network_address), self.int_to_ip(self.broadcast_address))

    def netmask_str(self):
        """
        Vrátí masku podsítě jako řetězec ve tvaru IP adresy.
        """
        return self.int_to_ip(self.netmask)

    def is_network_or_broadcast(self, ip_str):
        """
        Zkontoluje jestli je ip síťová adresa nebo jestli to je broadcastová adresa
        """

        ip = self.ip_to_int(ip_str)
        if ip == self.network_address:
            return "Síťová adresa"
        elif ip == self.broadcast_address:
            return "Broadcastová adresa"
        else:
            return "Ani síťová, ani broadcastová"

    def to_json(self):
        """
        Exportuje síťové informace do JSON formátu.
        """
        usable_hosts = [self.int_to_ip(i) for i in range(self.network_address + 1, self.broadcast_address)]
        return {
            "network": self.int_to_ip(self.network_address) + f"/{self.prefix_len}",
            "netmask": self.netmask_str(),
            "broadcast_address": self.int_to_ip(self.broadcast_address),
            "total_addresses": 2 ** (32 - self.prefix_len),
            "usable_hosts": usable_hosts
        }

    def save_to_file(self, filename):
        """
        Uloží JSON reprezentaci sítě do souboru.
        """
        data = self.to_json()
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data byla uložena do souboru {filename}")

    def __str__(self):
        """
        Vrací textovou reprezentaci sítě.
        """
        return f"{self.int_to_ip(self.network_address)}/{self.prefix_len}"


# Příklad použití
try:
    net = NetIPv4("192.168.1.0/24")
    print(f"Validní: {net.is_valid()}")
    print(f"Počet adres a broadcast: {net.get_count()}")
    print(f"Rozsah sítě: {net.network_range()}")
    print(f"Netmask: {net.netmask_str()}")
    
    # Zkontrolovat IP adresu
    ip = "192.168.1.0"
    print(f"Je {ip} síťová nebo broadcastová adresa: {net.is_network_or_broadcast(ip)}")

    # Uložit do JSON souboru
    net.save_to_file("network_data.json")

except ValueError as e:
    print(e)