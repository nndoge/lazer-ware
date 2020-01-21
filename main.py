import keyboard
import pymem
import pymem.process
from threading import Thread

# ОФСЕТЫ ИЗМЕНИ НА НОВЫЕ БЛЕАТЬ
dwEntityList = (0x4D09F44)
dwForceAttack = (0x313B60C)
dwLocalPlayer = (0xCF7A4C)
m_fFlags = (0x104)
m_iCrosshairId = (0xB3AC)
m_iTeamNum = (0xF4)
dwEntityList = (0x4D09EF4)
dwGlowObjectManager = (0x524A330)
m_iGlowIndex = (0xA40C)
m_iTeamNum = (0xF4)

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client_panorama.dll").lpBaseOfDll
trigger_key = "shift"

def Trigger():
    print("Hello, trigger!")
    shooting = False
    while True:
        player = pm.read_int(client + dwLocalPlayer)

        if keyboard.is_pressed(trigger_key):
            entity = pm.read_int(player + m_iCrosshairId)

            if entity > 0 and entity <= 64:
                entity = pm.read_int(client + dwEntityList + (entity -1) * 0x10)
                entity_team = pm.read_int(entity + m_iTeamNum)
                player_team = pm.read_int(player + m_iTeamNum)
                  
                if player_team != entity_team:
                    shooting = True
                    pm.write_int(client + dwForceAttack, 5)
          
        if not keyboard.is_pressed(trigger_key) and shooting == True:
            pm.write_int(client + dwForceAttack, 4)
            shooting = False

def Glow():
    print("Hello, ESP!")

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
Thread(target=Glow).start()
Thread(target=Trigger).start()