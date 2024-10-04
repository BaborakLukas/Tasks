import ipaddress
import json
import tkinter as tk
from tkinter import messagebox, filedialog

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


# Funkce pro vytvoření UI
def create_ui():
    def on_calculate():
        network_str = entry_network.get()
        prefix = int(entry_prefix.get()) if entry_prefix.get() else None

        try:
            net = NetIPv4(network_str)
            if net.is_valid():
                # Získání základních informací
                info = f"Síť: {net}\n"
                info += f"Maska sítě: {net.netmask()}\n"
                info += f"Počet adres: {net.get_count()['total_addresses']}\n"
                info += f"Broadcast adresa: {net.get_count()['broadcast_address']}\n"
                info += f"Rozsah IP adres: {net.network_range()}\n"
                
                # Validace sítě
                info += f"Je platná: {net.is_valid()}\n"
                
                # Rozdělení sítě na podsítě
                if prefix:
                    try:
                        subnets = net.split(prefix)
                        info += f"Podsítě (/ {prefix}):\n" + "\n".join(str(subnet) for subnet in subnets) + "\n"
                    except ValueError as e:
                        messagebox.showerror("Chyba", str(e))

                result_text.set(info)
            else:
                messagebox.showerror("Chyba", "Neplatná síť")
        except ValueError as e:
            messagebox.showerror("Chyba", str(e))

    def on_save():
        network_str = entry_network.get()

        try:
            net = NetIPv4(network_str)
            if net.is_valid():
                filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                        filetypes=[("JSON files", "*.json")])
                if filename:
                    net.save_to_file(filename)
                    messagebox.showinfo("Hotovo", f"Data uložena do {filename}")
            else:
                messagebox.showerror("Chyba", "Neplatná síť")
        except ValueError as e:
            messagebox.showerror("Chyba", str(e))

    root = tk.Tk()
    root.title("IPv4 Kalkulačka")

    # Nastavení velikosti okna
    root.geometry("600x500")
    
    # Větší font
    font_large = ("Helvetica", 14)
    
    tk.Label(root, text="Zadej síť (např. 192.168.1.0/24):", font=font_large).grid(row=0, column=0, padx=10, pady=10)
    entry_network = tk.Entry(root, font=font_large, width=30)
    entry_network.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Zadej nový prefix (nepovinné, např. 25):", font=font_large).grid(row=1, column=0, padx=10, pady=10)
    entry_prefix = tk.Entry(root, font=font_large, width=10)
    entry_prefix.grid(row=1, column=1, padx=10, pady=10)

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, font=font_large, anchor="w")
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    btn_calculate = tk.Button(root, text="Vypočítat", command=on_calculate, font=font_large, width=20)
    btn_calculate.grid(row=2, column=0, columnspan=2, pady=10)

    btn_save = tk.Button(root, text="Uložit síť do souboru", command=on_save, font=font_large, width=20)
    btn_save.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()