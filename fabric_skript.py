from fabric import task, ThreadingGroup, SerialGroup, Connection
from invoke import task as localtask
import json
import os
import serial
import time
from chirpstack.fabfile import APP_ID, headers, URL, DEVICE_PROFILE_ID, DEVICE_PROFILE_NAME
import numpy as np
import requests
from allocate import generate_allocation, abs_slot_to_dsme_coords
import jinja2

CONFIG = {
        "localadmin@rpi_exp_01": {"base": "/home/localadmin"},
        "localadmin@rpi_exp_02": {"base": "/home/localadmin"},
        #"jialamos@localhost": {"base": "/home/jialamos/Development/ipsn-dsme_lora/local"},
          }
HOSTS = [k for k in CONFIG.keys()]
#HOSTS = ["localadmin@rpi_exp_01"]

RIOTBASE = os.environ.get("RIOTBASE", "../src/RIOT")
FLASHFILE = os.environ.get("FLASHFILE", None)
BOARD = os.environ.get("BOARD", "nucleo-wl55jc")
APP = os.environ.get("APP", "")
ELF = os.environ.get("ELF", f"{APP}/bin/{BOARD}/{os.path.dirname(APP)}.elf")
CPUID_FOLDER = "../cpuid"
OUT_FOLDER = "../out"
KEYS_FOLDER = "/tmp"
TUN="tun0"
DEVICES=15

# DSME Config
PAN_COORD="001700355553500A20393256"
ACTUATORS = ["001700355553500A20393256", "001D002B3431510937393937", "003E003B3431511931343632"]

# Deps:
# SSH Services running

def get_serials(c):
    return [s["serial"] for s in list_ttys(c)]

def base(c):
    v = CONFIG[f"{c.user}@{c.host}"]["base"]
    return v

def target_riotbase(c):
    return f"{base(c)}/RIOT"

#@task(hosts=HOSTS)
#def flash(c):
#    target_file = f'/tmp/flash.elf'
#    c.put(f'{ELF}', f'/tmp/flash.elf')
#    for s in get_serials(c):
#        cmd = f"BOARD={BOARD} FLASHFILE=/tmp/flash.elf DEBUG_ADAPTER_ID={s} make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
#        print(cmd)
#        res = c.run(cmd)

def _flash(c):
    target_file = f'/tmp/flash.elf'
    c.put(f'{ELF}', f'/tmp/flash.elf')
    for s in get_serials(c):
        cmd = f"BOARD={BOARD} FLASHFILE=/tmp/flash.elf DEBUG_ADAPTER_ID={s} make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        print(cmd)
        res = c.run(cmd)

@localtask()
def flash(c):
    for _c in ThreadingGroup(*HOSTS):
        _flash(_c)


@task(hosts=HOSTS)
def reset(c):
    for s in get_serials(c):
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={s} make -C {target_riotbase(c)}/examples/hello-world/ reset"
        res = c.run(cmd)


def list_ttys(c):
    res = c.run(f"{target_riotbase(c)}/dist/tools/usb-serial/ttys.py --format json", hide=True)
    data = json.loads(res.stdout)
    return data

@task(hosts=HOSTS)
def ttys(c):
    for d in list_ttys(c):
        print(f"[{c.host}] {d['serial']}: {d['path']}")

@task(hosts=HOSTS)
def dump_cpuid(c):
    data = list_ttys(c)
    target_file = f'/tmp/flash.elf'
    c.local(f"mkdir -p {CPUID_FOLDER}")
    test=f"{RIOTBASE}/tests/periph_cpuid"
    c.local(f"make -C {test} all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        res = c.run(cmd)
        c.run(f'echo "s" > {base(c)}/in/in_{port}')
        time.sleep(1)
        out_file = f"{base(c)}/out/out_{port}"
        serial = v["serial"]
        c.get(out_file, f"{CPUID_FOLDER}/{c.host}.{serial}.cpuid.output")

@task(hosts=HOSTS)
def map_tty(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        serial = v["serial"]
        c.run(f"systemctl --user start riot-dev@{port}.service")

@task(hosts=HOSTS)
def clean_tty(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f"systemctl --user stop riot-dev@{port}.service")

@task(hosts=HOSTS)
def clean_out(c):
    #c.run(f"rm -f {base(c)}/out/*")
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f"systemctl --user reload riot-dev@{port}.service")

@task(hosts=HOSTS)
def dump_keys(c):
    data = list_ttys(c)
    target_file = f'/tmp/flash.elf'
    test = "/home/jialamos/Development/ipsn-dsme_lora/src/tests/config"
    c.local(f"mkdir -p {KEYS_FOLDER}")
    c.local(f"make -C {test} all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.run("rm /tmp/flash.elf")
    c.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        print(cmd)
        res = c.run(cmd)
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        time.sleep(1)
        out_file = f"{base(c)}/out/out_{port}"
        serial = v["serial"]
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ reset"
        res = c.run(cmd)
        time.sleep(5)
        c.get(out_file, f"{KEYS_FOLDER}/{c.host}.{serial}.config.output")
        print(out_file)

@task(hosts=HOSTS)
def test_lorawan(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        #cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ reset"
        #res = c.run(cmd)
        c.run(f'echo "start 10" > {base(c)}/in/in_{port}')
        #time.sleep(1)
        #c.run(f'echo "start 10" > {base(c)}/in/in_{port}')
        #out_file = f"{base(c)}/out/out_{port}"
        #serial = v["serial"]
        #time.sleep(5)
        #c.get(out_file, f"{KEYS_FOLDER}/{c.host}.{serial}.config.output")
        #print(out_file)

@task(hosts=HOSTS)
def test_output(c):
    print(c.host)
    return c.run(f"grep -a ^ /dev/null {base(c)}/out/* | sed -e 's/^/{c.host}/'")

@task(hosts=HOSTS)
def reboot(c):
    if (c.host != "localhost"):
        c.run("sudo reboot")

@task(hosts=HOSTS)
def shutdown(c):
    if (c.host != "localhost"):
        c.run("sudo shutdown now")

@task(hosts=HOSTS)
def test_setup(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ reset"
        res = c.run(cmd)
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        c.run(f'echo "sx126x set freq 869525000" > {base(c)}/in/in_{port}')
        c.run(f'echo "sx126x set bw 125" > {base(c)}/in/in_{port}')
        c.run(f'echo "sx126x set cr 1" > {base(c)}/in/in_{port}')
        c.run(f'echo "sx126x set sf 7" > {base(c)}/in/in_{port}')
        time.sleep(1)

@task(hosts=HOSTS)
def test_rx(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        c.run(f'echo "sx126x rx start" > {base(c)}/in/in_{port}')

@task(hosts=HOSTS)
def test_tx(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "sx126x tx RIOT" > {base(c)}/in/in_{port}')
        time.sleep(1)

def parallel(c):
    conn = []
    env = c.config.run.env
    for h in HOSTS:
        c = Connection(h)
        for k,v in env.items():
            c.config.run.env[k] = v
        c.config.run.env["TARGET_RIOT"] = target_riotbase(c)
        conn.append(c)
    g = ThreadingGroup(*HOSTS).from_connections(conn)
    return g

@localtask
def test_env(c):
    c.config.run.env["IT_WORKED"] = "YES"
    g = parallel(c)
    g.run("env")

@task(hosts=HOSTS)
def dump_ip(c):
    data = list_ttys(c)
    target_file = f'/tmp/flash.elf'
    test = "/home/jialamos/Development/ipsn-dsme_lora/src/SCHC/gnrc_networking"
    c.local(f"mkdir -p {KEYS_FOLDER}")
    c.local(f"make -C {test} all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.run("rm -f /tmp/flash.elf")
    c.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        print(cmd)
        res = c.run(cmd)
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        time.sleep(1)
        out_file = f"{base(c)}/out/out_{port}"
        serial = v["serial"]
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ reset"
        res = c.run(cmd)
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        c.run(f'echo "ifconfig" > {base(c)}/in/in_{port}')
        time.sleep(1)
        c.get(out_file, f"{KEYS_FOLDER}/{c.host}.{serial}.ifconfig.output")
        print(out_file)

@task(hosts=HOSTS)
def test_flash(c):
    data = list_ttys(c)
    target_file = f'/tmp/flash.elf'
    test = "/home/jialamos/Development/lora_sender"
    c.local(f"make -C {test} all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.run("rm -f /tmp/flash.elf")
    c.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        c.run(cmd)

@task(hosts=HOSTS)
def flush(c):
    data = list_ttys(c)
    target_file = f'/tmp/flash.elf'
    test = "/home/jialamos/Development/RIOT/examples/hello-world"
    c.local(f"make -C {test} all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.run("rm -f /tmp/flash.elf")
    c.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    for v in data:
        port = os.path.basename(v["path"])
        cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C {target_riotbase(c)}/examples/hello-world/ flash-only"
        c.run(cmd)

def flash_elf(c,test):
    g = parallel(c)
    target_file = f'/tmp/flash.elf'
    c.run(f"make -C {test} clean BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    c.run(f"make -C {test} -j4 all BOARD={BOARD} ELFFILE=/tmp/elf.elf")
    g.run("rm -f /tmp/flash.elf")
    g.put(f'/tmp/elf.elf', f'/tmp/flash.elf')
    #cmd = f"BOARD={BOARD} DEBUG_ADAPTER_ID={v['serial']} FLASHFILE=/tmp/flash.elf make -C $TARGET_RIOT/examples/hello-world/ flash-only"
    #cmd = f'bash -c "BOARD={BOARD} FLASHFILE=/tmp/flash.elf make -C $TARGET_RIOT/examples/hello-world/ flash-only"'
    g.run(f'$TARGET_RIOT/dist/tools/usb-serial/ttys.py --format serial | xargs -P 8 -I% bash -c "BOARD={BOARD} DEBUG_ADAPTER_ID=% FLASHFILE=/tmp/flash.elf make -C $TARGET_RIOT/examples/hello-world/ flash-only"')

@localtask
def test_flash_fast(c):
    test = "/home/jialamos/Development/ipsn-dsme_lora/src/SCHC/gnrc_networking"
    flash_elf(c,test)

@task(hosts=HOSTS)
def test_ping(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "ifconfig" > {base(c)}/in/in_{port}')
        c.run(f'echo "ping 2001::1 -s 12 -i {int(np.random.uniform(9000, 11000))} -c 70" > {base(c)}/in/in_{port}')

def run_service(c, service, cmd):
    c.run(f"systemctl --user {cmd} {service}.service")
    

@task
def chirpstack_start(c):
    run_service(c, f"chirpstack-sub@{APP_ID}", "start")

@task
def chirpstack_stop(c):
    run_service(c, f"chirpstack-sub@{APP_ID}", "stop")

@task
def chirpstack_wipe(c):
    run_service(c, f"chirpstack-sub@{APP_ID}", "reload")

@task
def chirpstack_logs(c):
    c.run(f"cat /var/chirpstack_mqtt/{APP_ID}.dat")


@localtask
def tshark_start(c):
    run_service(c, f"wireshark@{TUN}", "start")

@localtask
def tshark_stop(c):
    run_service(c, f"wireshark@{TUN}", "stop")

@localtask
def tshark_wipe(c):
    run_service(c, f"wireshark@{TUN}", "reload")

@localtask
def tshark_logs(c):
    c.run(f"cat /var/chirpstack_mqtt/wireshark.{TUN}.dat")

@localtask
def iotschc_start(c):
    run_service(c, f"iotschc", "start")

@localtask
def iotschc_stop(c):
    run_service(c, f"iotschc", "stop")

@localtask
def bootstrap_lw(c):
    tshark_start(c)
    chirpstack_start(c)
    iotschc_start(c)

@localtask
def clean_lw(c):
    remote(clean_tty)
    tshark_stop(c)
    chirpstack_stop(c)
    iotschc_stop(c)

@task(hosts=HOSTS)
def count_joined(c):
    res = c.run(f"cat {base(c)}/out/* | grep -a joined | wc -l", hide=True)
    out = res.stdout.strip()
    print(out)
    return int(out)

@task(hosts=HOSTS)
def count_finished(c):
    res = c.run(f"cat {base(c)}/out/* | grep -a packets | wc -l", hide=True)
    out = res.stdout.strip()
    print(out)
    return int(out)

@localtask
def check_ready(c):
    joined = 0
    devices = 0
    for h in HOSTS:
        c = Connection(h)
        res = count_joined(c)
        devices += len(list_ttys(c))
        joined += res
    print(joined, devices)
    return joined == devices

@localtask
def check_finished(c):
    finished = 0
    devices = 0
    for h in HOSTS:
        c = Connection(h)
        devices += len(list_ttys(c))
        res = count_finished(c)
        finished += res
    print(finished, devices)
    return finished == devices

def remote(func, hosts=HOSTS):
    for h in hosts:
        _c = Connection(h)
        func(_c) 

def run_test(c, func):
    remote(map_tty)
    remote(clean_out)
    test_flash_fast(c)
    while True:
        time.sleep(3)
        print("Waiting for devices")
        if check_ready(c):
            break
    print("Bootstrapping")
    bootstrap_lw(c)
    remote(func)
    while True:
        time.sleep(3)
        print("Waiting for experiment")
        if check_finished(c):
            break
    clean_lw(c)
    print("Finished!")
    pass

@localtask
def run_test_exp(c):
    #set_class_c(False)
    run_test(c, test_ping)

def set_class_c(enable):
    data = {"deviceProfile": {
        "supportsClassC": enable,
        "id": DEVICE_PROFILE_ID,
        "name": DEVICE_PROFILE_NAME
        }}
    data = json.dumps(data)
    res = requests.put(f"{URL}/device-profiles/{DEVICE_PROFILE_ID}", headers = headers, data=data)
    print(res.status_code, res.text)

@localtask
def run_class_c(c):
    c.config.run.env["CFLAGS"] = "-DCONFIG_GNRC_LORAWAN_CLASS_C=1"
    #set_class_c(True)
    run_test(c, test_ping)

@localtask
def flash_dsme(c,folder= "/home/jialamos/Development/ipsn-dsme_lora/src/DSME-LoRa/RIOT/examples/sensor"):
    flash_elf(c,folder)

def up(c,port):
    while True:
        c.run(f'echo "ifconfig 9 up" > {base(c)}/in/in_{port}')
        time.sleep(25)
        c.run(f'echo "ifconfig 9" > {base(c)}/in/in_{port}')
        #break
        res = c.run(f'cat {base(c)}/out/out_{port} | grep -a "Link: up" | wc -l')
        if int(res.stdout.strip()) > 0:
            print("Connected!")
            break
        print("Rebooting")
        c.run(f'echo "reboot" > {base(c)}/in/in_{port}')

@task
def setup_dsme_nodes(c):
    data = list_ttys(c)
    skip_first = False
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "help" > {base(c)}/in/in_{port}')
        if c.host=="localhost" and not skip_first:
            skip_first = True
            print("SKIP")
        else:
            up(c,port)
        c.run(f'echo "ifconfig 9 gts" > {base(c)}/in/in_{port}')
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "ifconfig" > {base(c)}/in/in_{port}')

def setup_pan_coord(c):
    v = list_ttys(c)[0]
    port = os.path.basename(v["path"])
    c.run(f'echo "ifconfig 9 pan_coord" > {base(c)}/in/in_{port}')
    c.run(f'echo "ifconfig 9 up" > {base(c)}/in/in_{port}')
    c.run(f'echo "ifconfig 9" > {base(c)}/in/in_{port}')
    time.sleep(2)

@localtask
def test_dsme(c):
    c.config.run.env["CFLAGS"] = "-O0"
    #flash_dsme(c)
    remote(clean_tty)
    remote(map_tty)
    remote(clean_out)
    #remote(reset)
    flash_dsme(c)
    remote(setup_pan_coord, ["jialamos@localhost"])
    remote(setup_dsme_nodes)
    time.sleep(10)
    print("Start ping test")
    remote(test_ping_dsme)
    print("Waiting")
    time.sleep(120)

@task(hosts=HOSTS)
def count_joined_dsme(c):
    res = c.run(f"cat {base(c)}/out/* | grep -a joined | wc -l", hide=True)
    out = res.stdout.strip()
    return int(out)

@localtask
def check_ready_dsme(c):
    joined = 0
    devices = 0
    for h in HOSTS:
        c = Connection(h)
        res = count_joined_dsme(c)
        devices += len(list_ttys(c))
        joined += res
    print(joined, devices)
    return joined == devices

@task(hosts=HOSTS)
def check_asserted(c):
    for h in HOSTS:
        c = Connection(h)
        res = c.run(f"cat {base(c)}/out/* | grep -a ASSER | wc -l", hide=True)
        out = res.stdout.strip()
        if int(out) > 0:
            return True
    return False

def post(c, file, interval,lw=False):
    remote(clean_tty)
    remote(map_tty)
    remote(clean_out)
    flash_dsme(c, file)
    print("Waiting")
    while True:
        time.sleep(3)
        print("Waiting for devices")
        print(check_asserted(c))
        if check_ready(c):
            break

    if (lw):
        print("Bootstrapping LoRaWAN")
        bootstrap_lw(c)

    for h in HOSTS:
        c = Connection(h)
        data = list_ttys(c)
        for v in data:
            port = os.path.basename(v["path"])
            c.run(f'echo "ifconfig" > {base(c)}/in/in_{port}')
            c.run(f'echo "nib neigh" > {base(c)}/in/in_{port}')
            c.run(f'echo "nib route" > {base(c)}/in/in_{port}')
            c.run(f'echo "6ctx add 0 2001::/64 100" > {base(c)}/in/in_{port}')
            c.run(f'echo "6ctx" > {base(c)}/in/in_{port}')
            c.run(f'echo "start {interval}" > {base(c)}/in/in_{port}')

def dsme_post(c, interval):
    post(c,"/home/jialamos/Development/ipsn-dsme_lora/src/DSME-LoRa/gnrc_networking", interval)

def lw_post(c, interval, class_a=False):
    if not class_a:
        c.config.run.env["CFLAGS"] = "-DCONFIG_GNRC_LORAWAN_CLASS_C=1"
    post(c,"/home/jialamos/Development/ipsn-dsme_lora/src/SCHC/gnrc_networking", interval, True)

@task
def deploy_debug_service(c):
    c.run("echo $HOME")
    c.put("debug%.service","/tmp/")
    c.run("mv /tmp/debug%.service $HOME/.config/systemd/user")

@task(hosts=["localadmin@rpi_exp_02"])
def test_ping_dsme(c):
    data = list_ttys(c)
    for v in data:
        port = os.path.basename(v["path"])
        c.run(f'echo "ifconfig" > {base(c)}/in/in_{port}')
        c.run(f'echo "ifconfig 9 -ack_req" > {base(c)}/in/in_{port}')
        c.run(f'echo "ping fe80::ff:fe00:d133 -s 12 -i {int(np.random.uniform(9000, 11000))} -c 100" > {base(c)}/in/in_{port}')
        time.sleep(8)

@localtask
def collect_results(c):
    hosts = [k for k in CONFIG.keys()]
    name = input("Last experiment:")
    c.run(f"mkdir -p {OUT_FOLDER}/{name}")
    for h in hosts:
        conn = Connection(h)
        with open(f"{OUT_FOLDER}/{name}/{h}.dat", 'w') as fl:
            fl.write(test_output(conn).stdout)
    c.run(f"cp /var/chirpstack_mqtt/* {OUT_FOLDER}/{name}")

@localtask
def setup_tun(c):
    c.run("sudo ip tuntap del mode tun dev tun0")
    c.run("sudo ip tuntap add mode tun dev tun0")
    c.run("sudo ifconfig tun0 up")
    c.run("sudo ip addr add 2001::1/64 dev tun0")

def gen_alloc(num_sensors, num_act, num_slots):
    NUM_SENSORS = num_sensors
    APS = 1
    NUM_ACT = num_act
    NUM_SLOTS = num_slots
    return (generate_allocation(num_slots=NUM_SLOTS, num_channels=16, num_sensors=NUM_SENSORS, num_actuators=NUM_ACT, aps=APS))

def get_dsme_l2():
    d = {}
    with open("../l2_addr_assoc.txt") as f:
        for l in f.readlines():
            data = l.strip().split(" ")
            bts = data[1].split(":")
            hx = bytes.fromhex(f"{bts[0]}{bts[1]}")
            d[data[0]] = hx
    return d

def get_id():
    c = False
    d = {}
    with open("../dev_association.csv") as f:
        for l in f.readlines():
            if not c:
                c = True
                continue
            l = l.strip()
            l = l.split(",")
            d[l[1]] = int(l[3])
    return d

def map_actuator(idx_dsme, num_sensors):
    return idx_dsme - num_sensors

def render_dsme(sensors, acts, slots, offset):
    l2s = get_dsme_l2()
    ids = get_id()
    a = []
    # Generate addresses
    for k,idx in ids.items():
        add = l2s[k]
        hexstring = add.hex()
        bts = [hexstring[:2].upper(), hexstring[2:].upper()]
        a.append(bts)
    file_loader = jinja2.FileSystemLoader('./jinja')
    env = jinja2.Environment(loader=file_loader)

    template = env.get_template('dsme.c')
    di = [{"abs_slot" : 0, "target":255, "channel":0} for i in range(DEVICES)]
    alloc = gen_alloc(sensors,acts,slots)
    # dev_association.txt is ordered, therefore no need to map again.
    count = 0
    for n,r in alloc.iterrows():
        d = {}
        abs_slot = int(r["abs_slot"])
        target = map_actuator(r["dest"], sensors)
        channel = r["channel"]
        print((target, abs_slot, channel))
        d["abs_slot"] = abs_slot
        d["target"] = target
        d["channel"] = channel
        di[offset + count] = d
        count = count+1

    return template.render(num_nodes=15, addresses=a, alloc=di, var_name=f"alloc_{sensors}_{acts}")

@localtask
def gen_dsme_config(c):

    # First three nodes are actuators
    print(render_dsme(8, 1, 11, 3))
    print(render_dsme(8, 3, 3, 3))
    print(render_dsme(12, 3, 7, 3))


# Experiment runs...

@localtask
def dsme_post_10(c):
    dsme_post(c, 10)

@localtask
def dsme_post_20(c):
    dsme_post(c, 20)

@localtask
def lw_post_10(c):
    lw_post(c, 10)

@localtask
def lw_post_20(c):
    lw_post(c, 20)

@localtask
def lw_a_post_10(c):
    lw_post(c, 10, True)

@localtask
def lw_a_post_20(c):
    lw_post(c, 20, True)

