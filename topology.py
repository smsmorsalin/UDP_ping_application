from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.link import TCLink


class LinuxRouter(Node):

    def config(self, **params):
        super(LinuxRouter, self).config(**params)

        # Enable IPv4 forwarding
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl -w net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):

    def build(self):

        # ==========================================
        # HOSTS
        # ==========================================

        h1 = self.addHost(
            "h1",
            ip="10.0.1.2/24"
        )

        h2 = self.addHost(
            "h2",
            ip="10.0.2.2/24"
        )


        # ==========================================
        # SWITCHES
        # ==========================================

        s1 = self.addSwitch(
            "s1",
            failMode="standalone"
        )

        s2 = self.addSwitch(
            "s2",
            failMode="standalone"
        )


        # ==========================================
        # ROUTERS
        # ==========================================

        r1 = self.addNode(
            "r1",
            cls=LinuxRouter,
            ip=None
        )

        r2 = self.addNode(
            "r2",
            cls=LinuxRouter,
            ip=None
        )


        # ==========================================
        # h1 -- s1 -- r1
        # ==========================================

        self.addLink(
            h1,
            s1,
            bw=10,
            delay="5ms"
        )

        self.addLink(
            s1,
            r1,
            intfName2="r1-eth0",
            bw=10,
            delay="5ms"
        )


        # ==========================================
        # r1 -- r2
        # ==========================================

        self.addLink(
            r1,
            r2,
            intfName1="r1-eth1",
            intfName2="r2-eth0",
            bw=10,
            delay="5ms"
        )


        # ==========================================
        # r2 -- s2 -- h2
        # ==========================================

        self.addLink(
            r2,
            s2,
            intfName1="r2-eth1",
            bw=10,
            delay="5ms"
        )

        self.addLink(
            s2,
            h2,
            bw=10,
            delay="5ms"
        )


# ==============================================
# CREATE NETWORK
# ==============================================

topo = NetworkTopo()

net = Mininet(
    topo=topo,
    link=TCLink,
    controller=None
)

net.start()


# ==============================================
# CLEAR AUTOMATIC ROUTER IP ADDRESSES
# ==============================================

net["r1"].cmd("ip addr flush dev r1-eth0")
net["r1"].cmd("ip addr flush dev r1-eth1")

net["r2"].cmd("ip addr flush dev r2-eth0")
net["r2"].cmd("ip addr flush dev r2-eth1")


# ==============================================
# ASSIGN ROUTER IP ADDRESSES
# ==============================================

# r1
net["r1"].cmd(
    "ip addr add 10.0.1.1/24 dev r1-eth0"
)

net["r1"].cmd(
    "ip addr add 10.0.3.1/24 dev r1-eth1"
)


# r2
net["r2"].cmd(
    "ip addr add 10.0.3.2/24 dev r2-eth0"
)

net["r2"].cmd(
    "ip addr add 10.0.2.1/24 dev r2-eth1"
)


# ==============================================
# HOST DEFAULT ROUTES
# ==============================================

net["h1"].cmd(
    "ip route add default via 10.0.1.1"
)

net["h2"].cmd(
    "ip route add default via 10.0.2.1"
)


# ==============================================
# ROUTER ROUTES
# ==============================================

# r1 -> r2 -> h2
net["r1"].cmd(
    "ip route add 10.0.2.0/24 via 10.0.3.2 dev r1-eth1"
)

# r2 -> r1 -> h1
net["r2"].cmd(
    "ip route add 10.0.1.0/24 via 10.0.3.1 dev r2-eth0"
)


# ==============================================
# SHOW CONFIGURATION
# ==============================================

print("\n========== r1 interfaces ==========")
print(net["r1"].cmd("ip addr"))

print("\n========== r2 interfaces ==========")
print(net["r2"].cmd("ip addr"))

print("\n========== r1 routing table ==========")
print(net["r1"].cmd("ip route"))

print("\n========== r2 routing table ==========")
print(net["r2"].cmd("ip route"))


# ==============================================
# TESTS
# ==============================================

print("\n*** h1 -> r1")
print(
    net["h1"].cmd(
        "ping -c 3 10.0.1.1"
    )
)

print("\n*** r1 -> r2")
print(
    net["r1"].cmd(
        "ping -c 3 10.0.3.2"
    )
)

print("\n*** r2 -> h2")
print(
    net["r2"].cmd(
        "ping -c 3 10.0.2.2"
    )
)

print("\n*** h1 -> h2")
print(
    net["h1"].cmd(
        "ping -c 3 10.0.2.2"
    )
)


# ==============================================
# CLI
# ==============================================

CLI(net)

net.stop()
