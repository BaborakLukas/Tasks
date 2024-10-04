import ipaddress
import json
 
class NetIPv4:

    def __init__(self, network_str):

        """
        Inicializuje klasy s danou IP sítí (např. '192.168.1.0/24').
        """

        try:

            self.network = ipaddress.IPv4Network(network_str, strict=False)

        except ValueError as e:

            raise ValueError(f"Nedělej si ze mě srandu: {network_str}") from e
 
    def is_valid(self):

        """
        Hodí čučku, aby zadaná IP adresa byla platná.
        """

        try:

            ipaddress.IPv4Network(self.network)

            return True

        except ValueError:

            return False
 
    def get_count(self):

        """
        Getbackne počet adres v této síti (včetně broadcast adresy).
        """

        return {

            "total_addresses": self.network.num_addresses,
            "broadcast_address": str(self.network.broadcast_address)

        }
 
    def split(self, new_prefix):

        """
        Rozdělí síť na menší podsítě podle nového zadanehé prefixu.
        """

        if new_prefix <= self.network.prefixlen:

            raise ValueError(f"Novej prefix {new_prefix} must be větší než {self.network.prefixlen}")

        return list(self.network.subnets(new_prefix=new_prefix))
 
    def contains_ip(self, ip_str):

        """
        Kontroluje, jestli zadaná IP adresa je v rozsahu této sítě.
        """

        try:

            ip = ipaddress.IPv4Address(ip_str)

            return ip in self.network

        except ValueError:

            raise ValueError(f"Invalid IP address format: {ip_str}")
 
    def network_range(self):

        """
        Vrátí first a lástovní IP adresu v síti.
        """

        return (str(self.network.network_address), str(self.network.broadcast_address))
 
    def netmask(self):

        """
        Vrátí masken undersite jako string.
        """

        return str(self.network.netmask)
 
    def is_network_or_broadcast(self, ip_str):

        """
        Zkontroluje, jestli je zadaná IP adresa buď síťová, nebo broadcastová adresa.
        """

        ip = ipaddress.IPv4Address(ip_str)

        return ip == self.network.network_address or ip == self.network.broadcast_address
 
    def to_json(self):

        """
        Exportuje síťové informace do JSON formátu, přičemž IP adresy jsou konvertovány na řetězce.
        """

        return {

            "network": str(self.network),
            "netmask": str(self.network.netmask),
            "hostmask": str(self.network.hostmask),
            "broadcast_address": str(self.network.broadcast_address),
            "total_addresses": self.network.num_addresses,
            "usable_hosts": [str(host) for host in self.network.hosts()]

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
        return str(self.network)

try:

    net = NetIPv4("192.168.1.0/24")


    print(f"Validní: {net.is_valid()}")
    print(f"Počet adres a broadcast: {net.get_count()}")
    print(f"Rozsah sítě: {net.network_range()}")
    print(f"Netmask: {net.netmask()}")
    # Kontrolíren IP adressen

    ip = "192.168.1.0"

    print(f"Je {ip} síťová nebo broadcastová adresa: {net.is_network_or_broadcast(ip)}")
 
    # Uložit do JáSON souboru

    net.save_to_file("network_data.json")
 
except ValueError as e:

    print(e)

 