#!/bin/bash

# Supress actual IP addresses on eth0, eth1 and eth2
ip addr flush PC4-eth0
ip addr flush PC4-eth1
ip addr flush PC4-eth2

# Add new IP addresses on eth0
ip addr add 10.10.10.4/24 dev PC4-eth0
ip -6 addr add fd24:ec43:12ca:c001:10::4/80 dev PC4-eth0

# Add new IP addresses on eth1
ip addr add 10.10.20.4/24 dev PC4-eth1
ip -6 addr add fd24:ec43:12ca:c001:20::4/80 dev PC4-eth1

# Add new IP addresses on eth2
ip addr add 10.10.30.4/24 dev PC4-eth2
ip -6 addr add fd24:ec43:12ca:c001:30::4/80 dev PC4-eth2

