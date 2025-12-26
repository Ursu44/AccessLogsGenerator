import random
from utils import random_ip, random_user, timestamp_syslog

HOSTNAME = ["server01", "server02", "user04", "laptop01", "laptop04"]
GOOD_RATIO = 0.65


def ssh_log(malicious=False):
    methods = ["password", "publickey", "keyboard-interactive"]
    ports = [22, 2222, 2200, 2022, 22222]
    pid = random.randint(1000, 8000)

    if malicious:
        return (
            f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
            f"Failed {random.choice(methods)} for {random_user()} "
            f"from {random_ip()} port {random.choice(ports)}"
        )

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} sshd[{pid}]: "
        f"Accepted {random.choice(methods)} for {random_user()} "
        f"from {random_ip()} port {random.choice(ports)}"
    )


def password_change_log(malicious=False):
    pid = random.randint(1000, 8000)

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} passwd[{pid}]: "
        f"password changed for user {random_user()}"
    )


def sudo_log(malicious=False):
    pid = random.randint(1000, 8000)
    user = random_user()

    pwds = [
        f"/home/{user}",
        f"/var/www",
        f"/opt/app",
        "/root"
    ]

    commands = [
        "/bin/bash",
        "/usr/bin/apt update",
        "/usr/bin/systemctl restart ssh",
        "/usr/bin/id"
    ]

    if malicious:
        return (
            f"{timestamp_syslog()} {random.choice(HOSTNAME)} sudo[{pid}]: "
            f"{user} : authentication failure ; "
            f"TTY=pts/0 ; PWD={random.choice(pwds)} ; USER=root"
        )

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} sudo[{pid}]: "
        f"{user} : TTY=pts/0 ; PWD={random.choice(pwds)} ; "
        f"USER=root ; COMMAND={random.choice(commands)}"
    )


def account_log(malicious=False):
    good_actions = ["created", "enabled", "password reset"]
    bad_actions = ["deleted", "disabled", "locked"]

    action = random.choice(bad_actions if malicious else good_actions)

    return (
        f"{timestamp_syslog()} {random.choice(HOSTNAME)} ad: "
        f"user account {action} for {random_user()}"
    )


def generate():
    malicious = random.random() > GOOD_RATIO

    generators = [
        lambda: ssh_log(malicious),
        lambda: password_change_log(malicious),
        lambda: sudo_log(malicious),
        lambda: account_log(malicious)
    ]

    return random.choice(generators)()
