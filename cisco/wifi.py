from scapy.all import ARP, Ether, srp, conf

# Create ARP packet to discover devices on the network
arp = ARP(pdst="192.168.1.1/24")  # Adjust the IP range to match your network

# Create Ether broadcast packet
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# Combine Ether and ARP packets
packet = ether/arp

# Send and receive ARP requests
result, _ = srp(packet, timeout=3, verbose=0, iface=conf.iface)

# Process the result
devices = []
for _, received in result:
    devices.append({"ip": received.psrc, "mac": received.hwsrc})

# Display the discovered devices
for device in devices:
    print(f"IP Address: {device['ip']} MAC Address: {device['mac']}")
