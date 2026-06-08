import random

class IPRotator:
    def __init__(self, incoming_ips=None):
        self.base_list = incoming_ips if incoming_ips else []
        self.viable_ips = list(self.base_list)
        self.blocked_ips = set()
        self.ip_trackers = {
            ip: {"good_hits": 0, "bad_hits": 0, "streak_failures": 0} 
            for ip in self.base_list
        }

    def fetch_next_node(self):
        """Picks a random working proxy server node from the current viable pool."""
        if not self.viable_ips:
            if self.blocked_ips:
                print("⚠️ IP address allocation exhausted. Re-evaluating restricted nodes...")
                self.viable_ips = list(self.blocked_ips)
                self.blocked_ips.clear()
            else:
                print("ℹ️ Network pool is empty. Routing traffic via default local adapter...")
                return None
        return random.choice(self.viable_ips)

    def register_success(self, active_ip):
        """Clears consecutive fault steps when a network packet is successfully confirmed."""
        if active_ip in self.ip_trackers:
            self.ip_trackers[active_ip]["good_hits"] += 1
            self.ip_trackers[active_ip]["streak_failures"] = 0

    def register_fault(self, active_ip):
        """Logs network drops and isolates problematic hosts using circuit-breaker thresholds."""
        if not active_ip:
            return
        if active_ip in self.ip_trackers:
            self.ip_trackers[active_ip]["bad_hits"] += 1
            self.ip_trackers[active_ip]["streak_failures"] += 1
            
            # Isolates host node if 3 consecutive packet requests drop out
            if self.ip_trackers[active_ip]["streak_failures"] >= 3:
                if active_ip in self.viable_ips:
                    self.viable_ips.remove(active_ip)
                    self.blocked_ips.add(active_ip)
                    print(f"🚫 Isolated unreliable host from active matrix routing: {active_ip}")