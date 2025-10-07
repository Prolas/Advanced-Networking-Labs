#!/bin/bash

# Supress actual IP addresses on eth0
ip addr flush PC3-eth0

# Add new IP addresses on eth0
ip addr add 10.10.30.3/24 dev PC3-eth0
ip -6 addr add fd24:ec43:12ca:c001:30::3/80 dev PC3-eth0

# Configure the default gateway
ip route add default via 10.10.30.4
ip -6 route add default via fd24:ec43:12ca:c001:30::4

