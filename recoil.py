import makcu
import win32api
import win32con
import time
import threading
import math

class Config:
    SENS = 0.52
    FOV = 90
    SHOOT_KEY = win32con.VK_LBUTTON
    AIM_KEY = win32con.VK_RBUTTON
    CROUCH_KEY = win32con.VK_CONTROL
    EXIT_KEY = 0x2D
    COM_PORT = "COM1"
    X_STRENGTH_MULTIPLIER = 1
    Y_STRENGTH_MULTIPLIER = 1
    X_DIRECTION = 1
    Y_DIRECTION = 1
    STAND_MULTIPLIER = 2.22
    STAND_MULTIPLIER_HMLMG = 4.53
    STAND_MULTIPLIER_M249 = 4.46
    CROUCH_MULTIPLIER = 0.51
    CROUCH_MULTIPLIER_HMLMG = 0.43
    CROUCH_MULTIPLIER_M249 = 0.41

WEAPON_HOTKEYS = {
    "AK47":        0x21,
    "LR300":       None,
    "MP5":         None,
    "THOMPSON":    None,
    "CUSTOM_SMG":  None,
    "HMLMG":       None,
    "M249":        0x22,
    "SAR":         None,
    "M39":         None,
}

ATTACHMENT_HOTKEYS = {
    "8x":          0x04,
    "16x":         None,
    "holosight":   0x27,
    "silencer":    None,
    "muzzleboost": None,
}

GunsPatterns = {
    1: {  # AK47
        "x": [0, 0.194914926, 0.391704579, 0.511817958, 0.648471024, 0.764900073, 0.802570690, 0.806110299, 0.907826148, 0.907167069, 0.869595948, 0.901561429, 0.839903022, 0.902936872, 0.963032607, 0.874347588, 0.825614937, 0.954164890, 0.914673816, 0.903444147, 0.883858707, 0.943581636, 0.915063957, 0.857727099, 0.936576585, 0.910809190, 0.936988434, 0.91679014, 0.936988434, 0.936576585],
        "y": [-1.361448576, -1.387357074, -1.386754677, -1.362197502, -1.401340041, -1.336221468, -1.348643268, -1.337576409, -1.292502762, -1.346553873, -1.369026982, -1.329203754, -1.305987651, -1.313265861, -1.369361745, -1.293973479, -1.36908135, -1.385905402, -1.347744798, -1.349755803, -1.405980126, -1.352300463, -1.388740356, -1.333803438, -1.355569929, -1.378052181, -1.350748341, -1.339769017, -1.350748341, -1.355569929],
        "rpm": 450,
        "at": 100,
        "bullets": 30,
        "scope_scales_hip": [1.2, 7.3, 14.4, 0.8],
        "scope_scales_ads": [1.2, 7.3, 14.4, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    2: {  # LR300
        "x": [0, 0.033517152, -0.149077278, -0.147054213, 0.057723381, 0.064947321, 0.195907464, -0.109225611, 0.097926597, -0.176121828, 0.039038725, -0.076399497, -0.054612504, 0.039398814, -0.119097829, -0.130586283, 0.025667901, -0.039517002, 0.05208714, -0.058687578, -0.128459502, -0.01072737, -0.027482931, -0.032145327, 0.033208416, -0.055400022, -0.020332557, 0.160677792, 0.04769127, 0.020668428],
        "y": [-1.237727448, -1.144310085, -1.123522866, -1.16982603, -1.185950853, -1.13696856, -1.173873366, -1.133846226, -1.097524521, -1.20294882, -1.107805068, -1.13839164, -1.105177797, -1.09091044, -1.028650464, -1.076927247, -1.090241713, -1.059846669, -1.14811803, -1.187485488, -1.115723664, -1.043712801, -1.075562658, -1.13741478, -1.081224828, -1.159009318, -1.08308448, -1.202353056, -1.158462495, -1.158462495],
        "rpm": 500,
        "at": 100,
        "bullets": 30,
        "scope_scales_hip": [1.2, 6.9, 13.5, 0.8],
        "scope_scales_ads": [1.2, 6.9, 13.5, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    3: {  # MP5
        "x": [0.075592683, -0.060027444, 0.016778475, -0.008270145, -0.004792041, 0.057945888, -0.027700011, 0.020692548, -0.002392704, -0.005670009, 0.084910239, -0.009076356, 0.057706497, -0.162594729, 0.000171855, 0.011103039, 0.059812173, 0.120394377, -0.04984398, 0.004116078, 0.055300527, -0.065532231, 0.102276036, -0.023061132, -0.051564339, 0.082176237, 0.118424376, -0.091965339, -0.12934953, 0.020668428],
        "y": [-0.634624938, -0.561723444, -0.575318682, -0.513456912, -0.645559137, -0.613864251, -0.479012248, -0.670908654, -0.56081412, -0.535767309, -0.585396621, -0.631070253, -0.518866425, -0.626454288, -0.506808234, -0.625990978, -0.513575703, -0.538503723, -0.644774634, -0.531540279, -0.694026468, -0.582204339, -0.662997907, -0.675410652, -0.528804468, -0.631696167, -0.627106131, -0.729202473, -0.576858744, -0.576858744],
        "rpm": 600,
        "at": 100,
        "bullets": 30,
        "scope_scales_hip": [1.2, 6.9, 13.5, 0.8],
        "scope_scales_ads": [1.2, 6.9, 13.5, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    4: {  # THOMPSON
        "x": [-0.069091039, 0.005237658, 0.006218136, 0.039090475, 0.062757225, -0.053135154, 0.054213318, 0.022353813, 0.107614395, 0.020906362, -0.049842774, 0.01540665, 0.049695642, -0.074352915, 0.016982902, -0.070759638, -0.162072531, -0.032010858, 0.02555514, 0.02555514],
        "y": [-0.410422905, -0.407988594, -0.411750711, -0.416881035, -0.395337654, -0.398238687, -0.407135349, -0.381471669, -0.382746411, -0.403674129, -0.400900078, -0.383888493, -0.390212154, -0.399248712, -0.399399462, -0.418165425, -0.398657169, -0.408528279, -0.390163914, -0.390163914],
        "rpm": 462,
        "at": 100,
        "bullets": 20,
        "scope_scales_hip": [1.48, 8.4, 17, 0.8],
        "scope_scales_ads": [1.48, 8.4, 17, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    5: {  # CUSTOM_SMG
        "x": [-0.069091642, 0.005237055, 0.006218136, 0.039090475, 0.062757225, -0.053135154, 0.054213318, 0.022353813, 0.107614998, 0.020905759, -0.049842774, 0.015407253, 0.049695039, -0.074352915, 0.016982902, -0.070759035, -0.162072531, -0.032010858, 0.002555514, 0.008543907, -0.005973921, 0.026577828, -0.026041761, 0.002555514],
        "y": [-0.410422905, -0.407987991, -0.411750711, -0.416880432, -0.395337051, -0.398238687, -0.407135349, -0.381471669, -0.382746411, -0.403674732, -0.400900681, -0.383888493, -0.390212154, -0.399248712, -0.399399462, -0.418164822, -0.398656566, -0.408528279, -0.390163311, -0.33251832, -0.332903637, -0.348349482, -0.331397343, -0.331397343],
        "rpm": 600,
        "at": 100,
        "bullets": 24,
        "scope_scales_hip": [1.5, 7.95, 15.9, 0.8],
        "scope_scales_ads": [1.5, 7.95, 15.9, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    6: {  # HMLMG
        "x": [0, -0.536458333, -0.536458333, -0.556458333] + [-0.556458333] * 56,
        "y": [-1.047375] * 60,
        "rpm": 480,
        "at": 125,
        "bullets": 60,
        "scope_scales_hip": [1.2, 7.2, 14.4, 0.8],
        "scope_scales_ads": [1.2, 7.2, 14.4, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    7: {  # M249
        "x": [0, 0.39375, 0.525] + [0.525] * 97,
        "y": [-0.81] + [-1.0800] * 99,
        "rpm": 500,
        "at": 120,
        "bullets": 100,
        "scope_scales_hip": [1.175, 6.95, 13.9, 0.8],
        "scope_scales_ads": [1.175, 6.95, 13.9, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    8: {  # SAR
        "x": [0] * 16,
        "y": [-0.90] * 16,
        "rpm": 343,
        "at": 75,
        "bullets": 16,
        "scope_scales_hip": [1.2, 7.35, 14.7, 0.8],
        "scope_scales_ads": [1.2, 7.35, 14.7, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
    9: {  # M39
        "x": [0.54] * 20,
        "y": [-0.95] * 20,
        "rpm": 343,
        "at": 75,
        "bullets": 20,
        "scope_scales_hip": [1.6, 9.7, 19.1, 0.8],
        "scope_scales_ads": [1.6, 9.7, 19.1, 0.8],
        "attachments1": [False, False, False, False],
        "attachments2": [False, False, False, False],
        "muzzleboost": [False, False],
        "silencer": [False, False],
    },
}

RPM_Tables = [GunsPatterns[i]["rpm"] for i in range(1, 10)]
AT_Tables = [GunsPatterns[i]["at"] for i in range(1, 10)]
GunsBullets = [GunsPatterns[i]["bullets"] for i in range(1, 10)]
screenMultiplier = -0.03 * (Config.SENS * 3) * (Config.FOV / 100)

def compute_weapon_tables(weapon_idx, variant_idx):
    a = weapon_idx
    b = variant_idx + 1
    weapon = GunsPatterns[a]

    silencer = 1.0
    muzzleboost = 1.0

    if a < 13 and weapon["muzzleboost"][b-1]:
        muzzleboost = 0.9

    if a in (4, 5) and weapon.get("silencer") and weapon["silencer"][b-1] and weapon[f"attachments{b}"][0]:
        silencer = 0.9

    stance_tables = []
    for d in [1, 2]:
        scale_array = weapon["scope_scales_hip"] if d == 1 else weapon["scope_scales_ads"]
        attachment_active = weapon[f"attachments{b}"]

        module_multiplier = 1.0
        for e in range(4):
            if attachment_active[e]:
                module_multiplier *= scale_array[e]

        bullet_data = []
        overflow_x = 0.0
        overflow_y = 0.0

        for f in range(1, weapon["bullets"] + 1):
            idx = f - 1
            pattern_x = weapon["x"][idx]
            pattern_y = weapon["y"][idx]

            has_8x_or_16x = attachment_active[1] or attachment_active[2]
            if a == 6:
                if has_8x_or_16x:
                    if f > 30:
                        pattern_x = 0
                else:
                    if f > 45:
                        pattern_x = 0
            elif a == 7:
                if has_8x_or_16x:
                    if f > 31:
                        pattern_x = 0
                else:
                    if f > 47:
                        pattern_x = 0

            if a == 6:
                mult = Config.STAND_MULTIPLIER_HMLMG   # 2.0
            elif a == 7:
                mult = Config.STAND_MULTIPLIER_M249    # 1.93
            else:
                mult = Config.STAND_MULTIPLIER         # 2.47

            base_x = pattern_x / screenMultiplier
            base_y = pattern_y / screenMultiplier

            X = base_x * module_multiplier * silencer * mult
            Y = base_y * module_multiplier * silencer * mult

            X *= muzzleboost
            Y *= muzzleboost

            overflow_x += X - int(X)
            overflow_y += Y - int(Y)

            int_x = int(X)
            int_y = int(Y)

            if overflow_x >= 1.0:
                extra_x = int(overflow_x)
                int_x += extra_x
                overflow_x -= extra_x
            if overflow_y >= 1.0:
                extra_y = int(overflow_y)
                int_y += extra_y
                overflow_y -= extra_y

            X_rounded = int_x
            Y_rounded = int_y

            bullet_data.append((X_rounded, Y_rounded))

        stance_tables.append(bullet_data)



    return stance_tables

FullTables = []
for a in range(1, len(GunsPatterns) + 1):
    weapon_variants = []
    for b in [1, 2]:
        stance_tables = compute_weapon_tables(a, b-1)
        weapon_variants.append(stance_tables)
    FullTables.append(weapon_variants)

running = True
shooting = False
bullet_count = 0
current_gun_index = 0
active_attachments_variant = 0
is_ads = False
is_crouching = False
makcu_controller = None
connection_lock = threading.Lock()
last_connection_attempt = 0
connection_interval = 5

gun_name_to_index = {name: i for i, name in enumerate(["AK47", "LR300", "MP5", "THOMPSON", "CUSTOM_SMG", "HMLMG", "M249", "SAR", "M39"])}
ATTACHMENT_NAMES = ["holosight", "8x", "16x", "handmade"]

def reset_attachments(weapon_idx):
    weapon = GunsPatterns[weapon_idx + 1]
    weapon["attachments1"] = [False, False, False, False]
    weapon["attachments2"] = [False, False, False, False]

def recompute_current_weapon_tables():
    global FullTables
    weapon_idx = current_gun_index + 1
    variant = active_attachments_variant
    new_stance_tables = compute_weapon_tables(weapon_idx, variant)
    FullTables[current_gun_index][variant] = new_stance_tables

def smooth_move(total_x, total_y, duration_ms):
    steps = 50
    if steps <= 0:
        steps = 1
    acc_x = 0
    acc_y = 0
    step_time = duration_ms / 1000.0 / steps
    for step in range(1, steps + 1):
        target_x = round(step * total_x / steps)
        target_y = round(step * total_y / steps)
        move_x = round(target_x - acc_x)
        move_y = round(target_y - acc_y)
        if (move_x != 0 or move_y != 0) and makcu_controller:
            try:
                makcu_controller.move(move_x, move_y)
            except:
                pass
        acc_x, acc_y = target_x, target_y
        if step < steps:
            end = time.perf_counter() + step_time
            while time.perf_counter() < end:
                pass

def apply_recoil(bullet_idx):
    global current_gun_index, active_attachments_variant, is_ads, is_crouching
    x, y = FullTables[current_gun_index][active_attachments_variant][1 if is_ads else 0][bullet_idx]

    if is_crouching:
        weapon_num = current_gun_index + 1
        if weapon_num == 6:
            crouch_mult = Config.CROUCH_MULTIPLIER_HMLMG
        elif weapon_num == 7:
            crouch_mult = Config.CROUCH_MULTIPLIER_M249
        else:
            crouch_mult = Config.CROUCH_MULTIPLIER
        x *= crouch_mult
        y *= crouch_mult

    x = x * Config.X_STRENGTH_MULTIPLIER * Config.X_DIRECTION
    y = y * Config.Y_STRENGTH_MULTIPLIER * Config.Y_DIRECTION

    weapon = GunsPatterns[current_gun_index + 1]
    duration = (60000.0 / weapon["rpm"]) * (weapon["at"] / 100.0)
    smooth_move(x, y, duration)

def connection_monitor():
    global makcu_controller, running, last_connection_attempt
    while running:
        with connection_lock:
            if makcu_controller is None and Config.COM_PORT:
                if time.time() - last_connection_attempt > connection_interval:
                    last_connection_attempt = time.time()
                    try:
                        print(f"\nTrying {Config.COM_PORT}...")
                        makcu_controller = makcu.create_controller(debug=False, auto_reconnect=True)
                        makcu_controller.move(0, 0)
                        print(f"Connected")
                    except Exception as e:
                        print(f"{e}")
                        makcu_controller = None
        time.sleep(1)

def recoil_thread():
    global bullet_count, shooting, current_gun_index, running, is_ads, is_crouching
    while running:
        try:
            shooting_key = (win32api.GetAsyncKeyState(Config.SHOOT_KEY) & 0x8000) != 0
            aiming = (win32api.GetAsyncKeyState(Config.AIM_KEY) & 0x8000) != 0
            is_crouching = (win32api.GetAsyncKeyState(Config.CROUCH_KEY) & 0x8000) != 0
            is_ads = aiming

            if shooting_key and aiming:
                if not shooting:
                    shooting = True
                    bullet_count = 0
                    stance = "CROUCH" if is_crouching else "STAND"
                if makcu_controller:
                    apply_recoil(bullet_count)
                    bullet_count += 1
                    if bullet_count >= GunsBullets[current_gun_index]:
                        bullet_count = GunsBullets[current_gun_index] - 1
                else:
                    time.sleep(0.005)
            else:
                if shooting:
                    shooting = False
                    bullet_count = 0
                time.sleep(0.001)
        except Exception as e:
            print(f"{e}")
            time.sleep(0.01)

def hotkey_thread():
    global current_gun_index, active_attachments_variant, shooting, bullet_count, running
    last_press = {}
    while running:
        try:
            for gun_name, key in WEAPON_HOTKEYS.items():
                if key and (win32api.GetAsyncKeyState(key) & 0x8000):
                    now = time.time()
                    if key not in last_press or now - last_press[key] > 0.3:
                        reset_attachments(gun_name_to_index[gun_name])
                        current_gun_index = gun_name_to_index[gun_name]
                        active_attachments_variant = 0
                        shooting = False
                        bullet_count = 0
                        new_tables = compute_weapon_tables(current_gun_index+1, 0)
                        FullTables[current_gun_index][0] = new_tables
                        last_press[key] = now

            for att_name, key in ATTACHMENT_HOTKEYS.items():
                if key and (win32api.GetAsyncKeyState(key) & 0x8000):
                    now = time.time()
                    if key not in last_press or now - last_press[key] > 0.3:
                        idx = ATTACHMENT_NAMES.index(att_name) if att_name in ATTACHMENT_NAMES else -1
                        if idx >= 0:
                            att_list = GunsPatterns[current_gun_index+1][f"attachments{active_attachments_variant+1}"]
                            att_list[idx] = not att_list[idx]
                            state = "ON" if att_list[idx] else "OFF"
                            print(f"{att_name} is now {state}")  # <-- added feedback
                            recompute_current_weapon_tables()
                        last_press[key] = now
            time.sleep(0.01)
        except Exception as e:
            print(f"{e}")
            time.sleep(0.01)

def exit_listener():
    global running
    while running:
        if win32api.GetAsyncKeyState(Config.EXIT_KEY) & 0x8000:
            running = False
            print("\nExited")
            break
        time.sleep(0.01)

def select_com_port():
    while True:
        port = input("Enter COM port (e.g., COM4): ").strip().upper()
        if port.startswith("COM"):
            try:
                num = int(port[3:])
                if 1 <= num <= 256:
                    return port
            except:
                pass
        print("Invalid, just put com(1) just connect you")

def main():
    global running, makcu_controller
    Config.COM_PORT = select_com_port()

    monitor = threading.Thread(target=connection_monitor, daemon=True)
    monitor.start()
    time.sleep(3)

    if makcu_controller is None:
        print("No makcu detected.")

    threads = [
        threading.Thread(target=recoil_thread, daemon=True),
        threading.Thread(target=hotkey_thread, daemon=True),
        threading.Thread(target=exit_listener, daemon=True),
    ]
    for t in threads:
        t.start()

    try:
        while running:
            time.sleep(5)
    except KeyboardInterrupt:
        print("Interrupted")
    finally:
        running = False
        if makcu_controller:
            makcu_controller.disconnect()
        print("Macku disconnected.")

if __name__ == "__main__":
    main()