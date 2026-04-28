import random
import time
from datetime import datetime, timezone

_attack_state = {
    "in_attack":   False,
    "attack_end":  0.0,
    "next_attack": time.time() + random.randint(120, 300),
}

def is_attack_wave() -> bool:
    now   = time.time()
    state = _attack_state

    if state["in_attack"]:
        if now < state["attack_end"]:
            return random.random() < 0.90
        else:
            state["in_attack"]   = False
            state["next_attack"] = now + random.randint(180, 480)
            print(
                f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] "
                f"⚔️  Attack wave terminat. "
                f"Următor în {int(state['next_attack'] - now)}s"
            )
            return random.random() < 0.08
    else:
        if now >= state["next_attack"]:
            duration            = random.randint(30, 90)
            state["in_attack"]  = True
            state["attack_end"] = now + duration
            print(
                f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] "
                f"🚨 Attack wave START — durată {duration}s"
            )
            return random.random() < 0.90
        else:
            return random.random() < 0.08


def random_ip():
    private_ranges = [
        lambda: f"172.{random.randint(16,27)}.{random.randint(0,25)}.{random.randint(1,25)}",
        lambda: f"192.168.{random.randint(0,25)}.{random.randint(1,25)}"
    ]
    public_ranges = [
        lambda: f"31.{random.randint(0,25)}.{random.randint(0,25)}.{random.randint(0,25)}",
        lambda: f"52.{random.randint(0,25)}.{random.randint(0,25)}.{random.randint(0,25)}"
    ]
    return random.choice(private_ranges + public_ranges)()


def random_user():
    users = [
        "admin", "root", "user1", "user2",
        "service", "backup", "test",
        "guest", "support"
    ]
    return random.choice(users)


def timestamp_syslog():
    return datetime.now(timezone.utc).strftime("%b %d %H:%M:%S")