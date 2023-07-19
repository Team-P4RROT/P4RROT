#! /bin/bash
set -xe

export $(cat network-config.env | xargs)


ip netns add switch
ip netns add h1
ip netns add h2

ip -n h1 link add "$HOST_1_IF" type veth peer name "$SW_IF_H1" netns switch
ip -n switch link add "$SW_IF_H2" type veth peer name "$HOST_2_IF" netns h2

# Setup loopback
ip netns exec switch ip link set lo up
ip netns exec h1 ip link set lo up
ip netns exec h2 ip link set lo up

# Assign ip addresses
ip netns exec h1 ip addr add "$HOST_1_IP/24" dev "$HOST_1_IF"
ip netns exec h2 ip addr add "$HOST_2_IP/24" dev "$HOST_2_IF"

# activate interfaces
ip netns exec h1 ip link set "$HOST_1_IF" up
ip netns exec h2 ip link set "$HOST_2_IF" up

# set default routes
ip netns exec h1 ip route add default via "$HOST_1_GW" dev "$HOST_1_IF"
ip netns exec h2 ip route add default via "$HOST_2_GW" dev "$HOST_2_IF"


# activate switch interfaces
ip netns exec switch ip link set "$SW_IF_H1" up
ip netns exec switch ip link set "$SW_IF_H2" up

#set fixed mac address to hosts (needed for mac forwarding without mac-learning)
ip netns exec h1 ifconfig eth0 hw ether C0:FF:EE:C0:FF:EE
ip netns exec h2 ifconfig eth0 hw ether DE:AD:BE:EF:DE:AD

# set arp table TODO: needs fixing because of constant interfaces
HOST_1_MAC=$(ip netns exec h1 cat /sys/class/net/eth0/address)
HOST_2_MAC=$(ip netns exec h2 cat /sys/class/net/eth0/address)

ip netns exec h1 arp -s "$HOST_2_IP" "$HOST_2_MAC"
ip netns exec h2 arp -s "$HOST_1_IP" "$HOST_1_MAC"

exit 0