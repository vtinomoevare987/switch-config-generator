import os

def get_hostname():
    hostname = input("Entrez le nom du switch (hostname) : ")
    return hostname

def get_vlans():
    vlans = []
    while True:
        try:
            vlan_id = input("ID du VLAN (ou appuyez sur Entrée pour terminer) : ")
            if vlan_id == "":
                break
            vlan_name = input(f"Nom du VLAN {vlan_id} : ")
            vlans.append((int(vlan_id), vlan_name))
        except ValueError:
            print("L'ID du VLAN doit être un nombre entier.")
    return vlans

def get_ports(mode):
    ports_per_vlan = {}
    while True:
        vlan_id = input(f"\nPour quel VLAN souhaitez-vous ajouter des ports {mode} ? (Entrée pour arrêter) : ")
        if vlan_id == "":
            break
        ports = input(f"Liste des ports {mode} pour le VLAN {vlan_id} (séparés par des virgules, ex: 1,2,3) : ")
        port_list = [p.strip() for p in ports.split(",") if p.strip()]
        ports_per_vlan[int(vlan_id)] = port_list
    return ports_per_vlan

def generate_config(hostname, vlans, untagged_ports, tagged_ports):
    lines = []
    lines.append(f"hostname {hostname}")
    lines.append("!")

    for vlan_id, vlan_name in vlans:
        lines.append(f"vlan {vlan_id}")
        lines.append(f" name {vlan_name}")
    lines.append("!")

    for vlan_id, ports in untagged_ports.items():
        for port in ports:
            lines.append(f"interface ethernet {port}")
            lines.append(" switchport mode access")
            lines.append(f" switchport access vlan {vlan_id}")
            lines.append("!")

    for vlan_id, ports in tagged_ports.items():
        for port in ports:
            lines.append(f"interface ethernet {port}")
            lines.append(" switchport mode trunk")
            lines.append(f" switchport trunk allowed vlan add {vlan_id}")
            lines.append("!")

    return "\n".join(lines)

def save_config_file(hostname, config_text):
    filename = f"config_{hostname}.txt"
    with open(filename, "w") as f:
        f.write(config_text)
    print(f"\n✅ Configuration sauvegardée dans : {filename}")

def main():
    print("🛠️ Générateur de configuration de switch\n")

    hostname = get_hostname()
    vlans = get_vlans()
    untagged = get_ports("untagged")
    tagged = get_ports("tagged")

    config = generate_config(hostname, vlans, untagged, tagged)
    save_config_file(hostname, config)

if __name__ == "__main__":
    main()

