# -*- coding: utf-8 -*-
# ============================================================================
#  WIKI HUNTER SYSTEM - ENCYCLOPEDIA COMPLETA
#  Database completo di Boss, Metin, Oggetti con Drop, Origini, 3D Preview
#  Pattern anti-memory-leak identico a hunter_effects.py / hunter_windows.py
# ============================================================================

import ui
import wndMgr
import app
import nonplayer
import item
import renderTarget
import dbg
import os
import zlib
import pack

# ============================================================================
#  CONFIGURAZIONE WIKI
# ============================================================================
WIN_WIDTH = 820
WIN_HEIGHT = 620
SIDEBAR_WIDTH = 140
SEARCH_HEIGHT = 30
LIST_WIDTH = 260
LIST_HEIGHT = WIN_HEIGHT - 45 - SEARCH_HEIGHT - 10  # Area lista risultati
PREVIEW_HEIGHT = 260
RIGHT_X = SIDEBAR_WIDTH + LIST_WIDTH + 30
RIGHT_W = WIN_WIDTH - RIGHT_X - 10
DETAIL_Y = 40 + PREVIEW_HEIGHT + 5
DETAIL_H = WIN_HEIGHT - DETAIL_Y - 10
DETAIL_ITEM_W = RIGHT_W - 20

RENDER_TARGET_INDEX = 66

# Colori Wiki - Solo Leveling Definitive Palette
COLOR_BG_MAIN = 0xF2040410      # Nero-blu abissale
COLOR_BG_PANEL = 0xEC030310     # Panel leggermente piu' chiaro
COLOR_BG_HEADER = 0xCC0A0520    # Viola-blu scuro per header
COLOR_BORDER = 0xFFFFD700       # Oro reale puro (colore principale)
COLOR_BORDER_DIM = 0xFFAA7700   # Oro attenuato per bordi secondari
COLOR_BORDER_ACCENT = 0xFF665500 # Oro molto attenuato per terzo livello
COLOR_TEXT_GOLD = 0xFFFFD700    # Testo oro puro
COLOR_TEXT_LIGHT = 0xFFFFEEAA   # Oro chiaro caldo
COLOR_TEXT_WHITE = 0xFFFFFFFF
COLOR_TEXT_GRAY = 0xFFAAAAAA
COLOR_TEXT_DARK = 0xFF555566    # Grigio-blu scuro
COLOR_TEXT_GREEN = 0xFF66FF88   # Verde neon
COLOR_TEXT_RED = 0xFFFF4444     # Rosso neon
COLOR_TEXT_CYAN = 0xFF00CCFF    # Ciano sistema
COLOR_TEXT_ORANGE = 0xFFFF8833  # Arancione fuoco
COLOR_TEXT_YELLOW = 0xFFFFEE44  # Giallo vivace

# Sottotipi arma/armatura per wiki
WEAPON_SUBTYPES = {
    0: "Spada", 1: "Pugnale", 2: "Arco", 3: "Spadone",
    4: "Campana", 5: "Ventaglio", 6: "Freccia", 7: "Spada Unica",
}
ARMOR_SUBTYPES = {
    0: "Armatura", 1: "Elmo", 2: "Scudo", 3: "Bracciale",
    4: "Scarpe", 5: "Collana", 6: "Orecchini",
}
ITEM_TYPE_NAMES = {
    1: "Arma", 2: "Armatura", 3: "Uso", 4: "Uso Auto", 5: "Materiale",
    6: "Speciale", 7: "Strumento", 8: "Lotteria", 10: "Pietra Metin",
    11: "Contenitore", 12: "Pesce", 13: "Canna", 14: "Risorsa",
    16: "Unico", 17: "Libro Abilita", 18: "Quest", 19: "Polymorph",
    23: "Scatola Regalo", 25: "Acconciatura", 28: "Costume",
    29: "Anima Drago", 32: "Anello", 33: "Cintura", 34: "Pet",
}
COLOR_BTN_NORMAL = 0xCC0A0800
COLOR_BTN_HOVER = 0xCC201200
COLOR_BTN_ACTIVE = 0xCC301A00
COLOR_BTN_BORDER = 0xFFFFD700
COLOR_SEPARATOR = 0xFF222244
COLOR_NO_RESULT = 0xFFAAAAAA

# Categorie disponibili
CATEGORIES_MOB = [
    ("Tutti", "ALL"),
    ("Boss", "BOSS"),
    ("Metin", "METIN"),
]
CATEGORIES_ITEM = [
    ("Oggetti", "ITEM"),
    ("Armi", "ITEM_1"),
    ("Armature", "ITEM_2"),
    ("Costumi", "ITEM_28"),
]
CATEGORIES_FRACTURE = [
    ("Boss Frattura", "FRACT_BOSS"),
    ("Super Metin", "FRACT_METIN"),
    ("Bauli", "FRACT_CHEST"),
]
CATEGORIES = CATEGORIES_MOB + CATEGORIES_ITEM + CATEGORIES_FRACTURE

# Nomi bonus item (Apply Types) in italiano
APPLY_NAMES = {
    1: "HP Max", 2: "SP Max", 3: "Vitalita'", 4: "Intelligenza",
    5: "Forza", 6: "Destrezza", 7: "Vel. Attacco", 8: "Vel. Movimento",
    9: "Vel. Magia", 10: "Regen HP", 11: "Regen SP",
    12: "Avvelenamento", 13: "Stordimento", 14: "Rallentamento",
    15: "Prob. Critico", 16: "Penetrazione",
    17: "Forte vs Umani", 18: "Forte vs Animali", 19: "Forte vs Orchi",
    20: "Forte vs Mistici", 21: "Forte vs Non-morti", 22: "Forte vs Diavoli",
    23: "Assorbi HP", 24: "Assorbi SP", 25: "Brucia Mana",
    26: "Recupero SP", 27: "Blocco", 28: "Schivata",
    29: "Res. Spada", 30: "Res. Spadone", 31: "Res. Pugnale",
    32: "Res. Campana", 33: "Res. Ventaglio", 34: "Res. Arco",
    35: "Res. Fuoco", 36: "Res. Fulmine", 37: "Res. Magia",
    38: "Res. Vento", 39: "Rifletti Danni", 40: "Veleno +",
    41: "EXP Bonus", 43: "Forte vs Metin", 44: "Forte vs Boss",
    53: "Danno Abilita'", 54: "Danni Medi", 71: "Res. Guerriero",
    72: "Res. Ninja", 73: "Res. Sura", 74: "Res. Sciamano",
}

# Nomi razze mob (per bonus "Forte vs")
MOB_RACE_NAMES = {
    0: "Animale", 1: "Umano", 2: "Orc", 3: "Mistico",
    4: "Non-morto", 5: "Insetto", 6: "Drago", 7: "Demone", 8: "Diavolo",
}

# Colori per grado mob
GRADE_COLORS = {
    0: 0xFF888888,  # Comune - grigio
    1: 0xFFBBBBBB,  # Forte - bianco
    2: 0xFF6699FF,  # Raro - blu
    3: 0xFFCC66FF,  # Speciale - viola
    4: 0xFFFFD700,  # Boss - oro
    5: 0xFFFF8800,  # Boss Raid - arancione
    6: 0xFFFF4444,  # Leggendario - rosso
}

# Navigazione
NAV_STACK_MAX = 30

# Paths to data files
FILE_ITEM_LIST = "item_list.txt"
FILE_MOB_DROP = "mob_drop_item.txt"
FILE_NPC_LIST = "npclist.txt"
FILE_SPECIAL_ITEM_GROUP = "special_item_group.txt"

# ============================================================================
_WK = [0x48,0x75,0x6E,0x74,0x33,0x72,0x57,0x31,0x6B,0x69,0x5F,0x32,0x30,0x32,0x36,0x21]
_CF = {"mob_drop_item": "dxsetup", "special_item_group": "msvcp140"}

def _HexDec(s):
    s = s.strip()
    out = []
    for i in xrange(0, len(s), 2):
        out.append(chr(int(s[i:i+2], 16)))
    return "".join(out)

def _WikiDecrypt(raw):
    if len(raw) > 16 and raw[0:4] == "574b":
        try:
            raw = _HexDec(raw)
        except:
            return None
    if len(raw) < 8:
        return None
    if raw[0:2] != "WK":
        return None
    ver = ord(raw[2])
    if ver != 1:
        return None
    salt = ord(raw[3])
    body = raw[8:]
    kLen = len(_WK)
    dec = bytearray(len(body))
    for i in xrange(len(body)):
        dec[i] = ord(body[i]) ^ _WK[(i + salt) % kLen]
    try:
        return zlib.decompress(str(dec))
    except:
        return None

# Override categorizzazione mob: corregge Boss classificati come Metin e viceversa
# Mob che DEVONO essere Boss (anche se il vnum/nome li farebbe sembrare Metin)
FORCE_BOSS_VNUMS = set([
    8213,  # Ra (Landa del Faraone)
    8214,  # Anubi (Landa del Faraone)
    591,   # Capitano Brutale
    691,   # Capo Orco
    719,   # Thaloren
    768,   # Slubina
    986,   # Branzhul
    989,   # Torgal
    1093,  # Spirito della Morte (DG Tempio dei Demoni)
    1901,  # Nove Code
    2092,  # Baronessa Ragno (DG Biblioteca)
    2771,  # Yinlee
    3190,  # Arges (Valle dei Ciclopi)
    3191,  # Polifemo (Valle dei Ciclopi)
    4011,  # Nerzakar
    4035,  # Funglash
    4385,  # Velzahar
    6790,  # Alastor
    6830,  # Nozzera
    6831,  # Grimlor
    9682,  # Wukong (DG Collina di WuKong)
    9694,  # Re Scorpione (DG Rovina dello Scorpione)
    9712,  # Re Artico (DG Grotta Artica)
    16103, # Regina Giungla (DG Antica Giungla)
    29754, # Signore Infernale (DG Porte dell'Inferno)
])

# Posizioni corrette dei Boss (dungeon o mappa)
# I boss non presenti qui usano GetZoneForLevel come fallback
BOSS_LOCATION = {
    # === BOSS DI DUNGEON ===
    2092:  "DG Biblioteca della Conoscenza (Lv.50)",
    1093:  "DG Tempio dei Demoni (Lv.75)",
    9682:  "DG Collina di WuKong (Lv.80)",
    9694:  "DG Rovina dello Scorpione (Lv.105)",
    9712:  "DG Grotta Artica (Lv.130)",
    29754: "DG Porte dell'Inferno (Lv.155)",
    16103: "DG Antica Giungla (Lv.175)",
    # === BOSS OVERWORLD ===
    591:   "Citta' 1 (Zona Iniziale)",
    691:   "Valle degli Orchi",
    4035:  "Monte Sohan",
    719:   "Monte Sohan",
    1901:  "Monte Sohan",
    2771:  "Monte Sohan / Valle degli Orchi",
    768:   "Monte Sohan / Valle degli Orchi",
    3190:  "Valle dei Ciclopi",
    3191:  "Valle dei Ciclopi",
    6790:  "??? Localita' Sconosciuta ???",
    6831:  "Valle dei Ciclopi / Zone Alte",
    986:   "Valle dei Ciclopi / Landa del Faraone",
    8213:  "Landa del Faraone",
    8214:  "Landa del Faraone",
    989:   "Landa del Faraone / Terra Gelida",
    4011:  "Terra Infuocata / Foresta Incantata",
    6830:  "Terra Infuocata / Foresta Incantata",
    4385:  "Foresta Incantata (End-Game)",
}

# Mob che DEVONO essere Metin (anche se il grado li farebbe sembrare Boss)
FORCE_METIN_VNUMS = set([
    6798,  # Metin della Montagna
    6799,  # Pietra Infernale
    6801,  # Metin del Fuoco
    6802,  # Metin della Foresta
    6803,  # Metin del Vento
    8006,  # Metin dell'Oscurita'
    8007,  # Metin della Gelosia
    8008,  # Metin dell'Anima
    8009,  # Metin dell'Ombra
    8011,  # Metin del Diavolo
    8013,  # Metin della Morte
    8052,  # Metin Ardente
    8053,  # Metin della Vanita'
    8203,  # Metin del Gelo
    8207,  # Pietra Antica
    8210,  # Metin del Faraone
])

# Nomi parziali per esclusione (case-insensitive)
EXCLUDED_MOB_NAMES = [
    "mietitor",      # Mietitori delle Zucche - rimossi
    "zucche",         # mob evento Halloween rimossi
]

# Keyword nel nome che forzano la classificazione come Metin
FORCE_METIN_KEYWORDS = [
    "metin", "pietra infernale", "pietra antica",
]

# Limiti per sicurezza
MAX_SEARCH_RESULTS = 500
MAX_GRID_COLS = 7
MAX_GRID_ROWS = 15
MAX_GRID_SIZE = MAX_GRID_COLS * MAX_GRID_ROWS
MAX_DROP_DISPLAY = 200

# ============================================================================
#  DATI ENCICLOPEDICI DAL SISTEMA ARISE (dalla presentazione ufficiale)
# ============================================================================

# Zone di gioco con livelli e descrizione
ZONE_INFO = {
    "Citta' 1":        {"minLv": 1,   "maxLv": 30,  "phase": "Fase Iniziale"},
    "Valle degli Orchi":{"minLv": 30,  "maxLv": 40,  "phase": "Zone Intermedie"},
    "Monte Sohan":     {"minLv": 40,  "maxLv": 75,  "phase": "Zone Intermedie"},
    "Valle dei Ciclopi":{"minLv": 75,  "maxLv": 100, "phase": "Predatore Novizio"},
    "Landa del Faraone":{"minLv": 100, "maxLv": 125, "phase": "Cacciatore Esperto"},
    "Terra Gelida":    {"minLv": 125, "maxLv": 150, "phase": "Predatore Veterano"},
    "Terra Infuocata": {"minLv": 150, "maxLv": 175, "phase": "Maestro Cacciatore"},
    "Foresta Incantata":{"minLv": 175, "maxLv": 200, "phase": "La Leggenda di Hunter"},
}

# Dungeon con livello richiesto, nome e loot principale
DUNGEON_INFO = {
    50:  {"name": "Biblioteca della Conoscenza", "loot": "Gioielli PvM Lv.50, Set Azrael"},
    75:  {"name": "Tempio dei Demoni",           "loot": "Armatura/Arma 75"},
    80:  {"name": "Collina di WuKong",           "loot": "Rocchetto d'Oro"},
    105: {"name": "Rovina dello Scorpione",      "loot": "Gemma Terra"},
    130: {"name": "Grotta Artica",               "loot": "Mat. Equip 130, Gemma Ghiaccio"},
    155: {"name": "Porte dell'Inferno",          "loot": "Mat. Equip 155, Gemma Fuoco"},
    175: {"name": "Antica Giungla",              "loot": "Mat. Equip 175, Gemma Smeraldo"},
    200: {"name": "Nave Fantasma",               "loot": "End-Game!"},
}

# Nomi dungeon associati a vnum chest (dal special_item_group)
CHEST_DUNGEON_MAP = {
    90058: "DG Baronessa",
    90059: "DG Spirito della Morte",
    90060: "Collina di WuKong (Lv.80)",
    90061: "Rovina dello Scorpione (Lv.105)",
    90062: "Grotta Artica (Lv.130)",
    90063: "Porte dell'Inferno (Lv.155)",
    90064: "Antica Giungla (Lv.175)",
}

# Rank Hunter: progressione E -> D -> C -> B -> A -> S -> N
HUNTER_RANKS = ["E", "D", "C", "B", "A", "S", "N"]
RANK_COLORS = {
    "E": 0xFF808080,  # Grigio
    "D": 0xFF2ECC71,  # Verde
    "C": 0xFF4A9EFF,  # Blu
    "B": 0xFFD4AF37,  # Oro
    "A": 0xFF9932CC,  # Viola
    "S": 0xFFFF003C,  # Rosso
    "N": 0xFFFFD700,  # Oro supremo
}

# Consigli per fascia di livello (dalla guida progressione)
LEVEL_TIPS = {
    (1, 30):    "Completa le quest dal Pannello F11: Caccia, Metinologia, Bossologia. Compra Set PvP e Arma Lv.30 dal negozio.",
    (30, 75):   "Farm Boss e Metin per upgrade. Crafta Cintura PvM e PvP. Quest F11 per Punti Obiettivo.",
    (75, 100):  "Prerequisiti: Equip 75 +9, Rune base, Set Azrael (evolvi in Zodiaco). Helper a P prima del Lv.90!",
    (100, 125): "Equip PvM (Zodiaco) e PvP (Polislazuli) +9. Stola con arma assorbita. Rune +1/+2. Usa Riciclaggio.",
    (125, 150): "Pet e Passivi a Grado G. Rune +2/+3. Farm Spedizioni per materiali.",
    (150, 175): "Potenzia Manufatti. Rune +3/+4. Potenziamenti Leggendari (Stola 30%).",
    (175, 200): "Rune MAX (+5), Manufatti, Alchimia. Ottimizzazione finale per End-Game.",
}

# Tasti rapidi del gioco
HOTKEYS = {
    "F5":  "Pannello Potenziamento",
    "F8":  "Teleport a Boss/Metin",
    "F9":  "AutoBuff Automatico",
    "F10": "Pannello Dungeon",
    "F11": "Pannello Quest",
    "F12": "Sistema Riciclaggio",
    "K":   "Inventario Speciale (6 categorie)",
    "P":   "Pannello Pet",
}

# Tipo item -> consiglio/note dalla presentazione
ITEM_TYPE_TIPS = {
    1:  "Le armi si potenziano fino a +9 con Pietre Mistiche, poi Epicizzazione.",
    2:  "Le armature si craftano e potenziano. Priorita': Arma > Armatura > Accessori.",
    5:  "I materiali sono fondamentali per crafting e upgrade. Controlla la Bottegaia.",
    10: "Le Pietre Metin si usano per sockettare l'equipaggiamento.",
    28: "I costumi sono permanenti e puramente cosmetici.",
    33: "Le cinture PvE danno bonus vs Mob/EXP, le PvP danno bonus vs Classi/Danno.",
    34: "I pet forniscono bonus passivi permanenti. Portali a Grado P per i bonus massimi.",
}

# ============================================================================
#  FRATTURE — Dati statici dal Hunter System
# ============================================================================

# Colori Tier (stile Solo Leveling)
TIER_COLORS = {
    1: 0xFF2ECC71,   # GREEN
    2: 0xFF4A9EFF,   # BLUE
    3: 0xFFFF8800,   # ORANGE
    4: 0xFFFF4444,   # RED
    5: 0xFFFFD700,   # GOLD
    6: 0xFF9932CC,   # PURPLE
    7: 0xFFDDDDDD,   # BLACKWHITE
}

TIER_NAMES = {
    1: "E-Rank", 2: "D-Rank", 3: "C-Rank", 4: "B-Rank",
    5: "A-Rank", 6: "S-Rank", 7: "N-Rank",
}

# Boss che spawnano dalle Fratture
# vnum -> {name, gloria, tier, color_name, speed_bonus}
FRACTURE_BOSSES = {
    4035:  {"name": "Funglash",   "gloria": 50,  "tier": 1, "color": "GREEN"},
    719:   {"name": "Thaloren",   "gloria": 70,  "tier": 2, "color": "BLUE"},
    2771:  {"name": "Yinlee",     "gloria": 90,  "tier": 3, "color": "BLUE"},
    768:   {"name": "Slubina",    "gloria": 120, "tier": 3, "color": "ORANGE"},
    6790:  {"name": "Alastor",    "gloria": 150, "tier": 4, "color": "ORANGE"},
    6831:  {"name": "Grimlor",    "gloria": 180, "tier": 4, "color": "RED"},
    986:   {"name": "Branzhul",   "gloria": 220, "tier": 5, "color": "RED"},
    989:   {"name": "Torgal",     "gloria": 280, "tier": 5, "color": "GOLD"},
    4011:  {"name": "Nerzakar",   "gloria": 350, "tier": 6, "color": "GOLD"},
    6830:  {"name": "Nozzera",    "gloria": 450, "tier": 6, "color": "PURPLE"},
    4385:  {"name": "Velzahar",   "gloria": 600, "tier": 7, "color": "BLACKWHITE"},
}
FRACTURE_BOSS_SPEED_BONUS = 200   # +200 Gloria se ucciso entro 60s
FRACTURE_BOSS_SPEED_TIME = 60     # secondi

# Super Metin che spawnano dalle Fratture
FRACTURE_SUPERMETIN = {
    63010: {"name": "Supermetin Glaciale",       "gloria": 35,  "tier": 1, "color": "GREEN"},
    63011: {"name": "Supermetin Infernale",      "gloria": 50,  "tier": 2, "color": "GREEN"},
    63012: {"name": "Supermetin Demoniaca",      "gloria": 70,  "tier": 2, "color": "BLUE"},
    63013: {"name": "Supermetin degli Antichi",  "gloria": 90,  "tier": 3, "color": "BLUE"},
    63014: {"name": "Supermetin Elettrica",      "gloria": 110, "tier": 3, "color": "ORANGE"},
    63015: {"name": "Supermetin della Natura",   "gloria": 140, "tier": 4, "color": "ORANGE"},
    63016: {"name": "Supermetin della Miniera",  "gloria": 180, "tier": 4, "color": "RED"},
    63017: {"name": "Supermetin delle Maree",    "gloria": 230, "tier": 5, "color": "GOLD"},
    63018: {"name": "Supermetin delle Sabbie",   "gloria": 300, "tier": 6, "color": "PURPLE"},
    63019: {"name": "Supermetin Non Morta",      "gloria": 500, "tier": 7, "color": "BLACKWHITE"},
}
FRACTURE_METIN_SPEED_BONUS = 80    # +80 Gloria se distrutto entro 300s
FRACTURE_METIN_SPEED_TIME = 300    # secondi (5 min)
FRACTURE_METIN_GROUP_BONUS = 10    # +10% Gloria per alleato vicino (max +50%)

# Bauli (Forzieri) che spawnano dalle Fratture
# vnum -> {name, gloria_min, gloria_max, tier, color, item_vnum, item_name, item_qty, jackpot_pct}
FRACTURE_CHESTS = {
    63000: {"name": "Forziere Demoniaco",       "gloria_min": 126,  "gloria_max": 256,   "tier": 1, "color": "GREEN",      "item_vnum": 50162, "item_name": "Focus del Cacciatore",      "item_qty": 1, "jackpot": 25},
    63001: {"name": "Forziere Elettrico",       "gloria_min": 180,  "gloria_max": 360,   "tier": 2, "color": "BLUE",       "item_vnum": 50163, "item_name": "Chiave Dimensionale",       "item_qty": 1, "jackpot": 22},
    63002: {"name": "Forziere Glaciale",        "gloria_min": 250,  "gloria_max": 480,   "tier": 3, "color": "ORANGE",     "item_vnum": 50164, "item_name": "Sigillo di Conquista",      "item_qty": 1, "jackpot": 20},
    63003: {"name": "Forziere Infernale",       "gloria_min": 350,  "gloria_max": 650,   "tier": 4, "color": "RED",        "item_vnum": 50165, "item_name": "Segnale di Emergenza",        "item_qty": 1, "jackpot": 18},
    63004: {"name": "Forziere della Natura",    "gloria_min": 480,  "gloria_max": 850,   "tier": 5, "color": "GOLD",       "item_vnum": 50167, "item_name": "Calibratore Fratture",              "item_qty": 1, "jackpot": 15},
    63005: {"name": "Forziere degli Antichi",   "gloria_min": 650,  "gloria_max": 1100,  "tier": 6, "color": "PURPLE",     "item_vnum": 50166, "item_name": "Risonatore di Gruppo",     "item_qty": 1, "jackpot": 12},
    63006: {"name": "Forziere di Ganesha",      "gloria_min": 900,  "gloria_max": 1500,  "tier": 7, "color": "BLACKWHITE", "item_vnum": 50168, "item_name": "Frammento di Monarca",     "item_qty": 1, "jackpot": 10},
    63007: {"name": "Forziere della Miniera",   "gloria_min": 856,  "gloria_max": 3426,  "tier": 7, "color": "PURPLE",     "item_vnum": 50161, "item_name": "Stabilizzatore di Rango",  "item_qty": 2, "jackpot": 40},
}

# Tipi di Frattura (Portali)
FRACTURE_PORTALS = {
    "E": {"name": "Frattura Primordiale",  "gloria_req": 0,       "power_rank": 0,   "weight": 44},
    "D": {"name": "Frattura Astrale",      "gloria_req": 2000,    "power_rank": 0,   "weight": 30},
    "C": {"name": "Frattura Abissale",     "gloria_req": 10000,   "power_rank": 0,   "weight": 15},
    "B": {"name": "Frattura Cremisi",      "gloria_req": 0,       "power_rank": 100, "weight": 5},
    "A": {"name": "Frattura Aurea",        "gloria_req": 0,       "power_rank": 200, "weight": 3},
    "S": {"name": "Frattura Infausta",     "gloria_req": 0,       "power_rank": 350, "weight": 2},
    "N": {"name": "Frattura Instabile",    "gloria_req": 0,       "power_rank": 500, "weight": 1},
}

# Ricompense difesa Frattura (Gloria range)
FRACTURE_DEFENSE_REWARDS = {
    "E": (500, 1500),    "D": (1000, 3000),   "C": (2000, 5000),
    "B": (4000, 8000),   "A": (6000, 12000),  "S": (10000, 20000),
    "N": (20000, 50000),
}

# Acquisizione speciale per keyword nel nome item
SPECIAL_ACQUISITION = {
    "cor draconis":   "Drop da Dungeon e Metin. Serve per Alchimia del Drago.",
    "runa":           "Drop da DG End-Game e Boss. Potenziabili fino a +5.",
    "manufatto":      "Drop da World Boss, DG End-Game e Bauli dei Manufatti.",
    "stola":          "Creata combinando materiali speciali. Puo' assorbire armi.",
    "azrael":         "Ottenibile dalla Biblioteca della Conoscenza (DG Lv.50). Si evolve in Zodiaco.",
    "zodiaco":        "Evoluzione del Set Azrael. Set PvM principale.",
    "polislazuli":    "Set PvP principale. Ottenibile da DG e farming avanzato.",
    "guanto potere":  "LEGGENDARIO: Drop da Boss Leggendari o Nave Fantasma (DG Lv.200). Craftabile.",
    "pietra spirituale": "Usata per portare le Skill al Grado P (30% successo).",
    "pozione":        "Consumabile. Assicurati di averne abbastanza prima dei DG.",
    "rugiada":        "Permanente (Tasto K). Ricevuta al primo login.",
    "elisir":         "Consumabile temporaneo: bonus EXP, Biologo o Collezionista.",
    "costume":        "Puramente cosmetico. Ottenibile da BattlePass, eventi o shop.",
    "rocchetto":      "Drop dalla Collina di WuKong (DG Lv.80).",
    "gemma terra":    "Drop dalla Rovina dello Scorpione (DG Lv.105).",
    "gemma ghiaccio": "Drop dalla Grotta Artica (DG Lv.130).",
    "gemma fuoco":    "Drop dalle Porte dell'Inferno (DG Lv.155).",
    "gemma smeraldo": "Drop dall'Antica Giungla (DG Lv.175).",
}


# ============================================================================
#  DATA MANAGER SINGLETON - Caricamento dati lazy
# ============================================================================
class WikiDataManager(object):
    """Gestore dati centralizzato per la Wiki. Singleton pattern."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.item_models = {}   # vnum -> {"model": path, "icon": path}
        self.mob_drops = {}     # mob_vnum -> [(item_vnum, count, rate), ...]
        self.item_origins = {}  # item_vnum -> [mob_vnum, ...]
        self.item_descs = {}    # vnum -> description_text

        # Refine/Upgrade data
        self.item_refined_vnum = {}  # vnum -> refined_vnum (prossimo upgrade)
        self.item_refined_targets = set()  # set di tutti i refined_vnum (target di upgrade)
        self.item_refine_set = {}    # vnum -> refine_set_id
        self.refine_recipes = {}     # id -> {"materials": [(vnum,count),...], "cost": int, "prob": int}

        # Chest/Box data (special_item_group)
        self.chest_contents = {}    # chest_vnum -> [(item_vnum, count, rate), ...]
        self.item_chest_sources = {} # item_vnum -> [chest_vnum, ...]
        self.chest_names = {}       # chest_vnum -> group_name (readable)

        self.is_loaded = False
        self._refine_loaded = False
        self._chest_loaded = False
        self._descs_loaded = False

    def __ReadFileLines(self, path):
        baseName = os.path.splitext(os.path.basename(path))[0]
        alias = _CF.get(baseName, baseName)
        encPath = "miles/" + alias + ".bin"
        try:
            f = open(encPath, "r")
            raw = f.read()
            f.close()
            text = _WikiDecrypt(raw)
            if text is not None:
                return text.split("\n")
        except:
            pass
        try:
            f = open(path, "r")
            lines = f.readlines()
            f.close()
            return lines
        except:
            pass
        return None

    def LoadData(self):
        """Carica i dati essenziali (item list + mob drops). Dati pesanti caricati on-demand."""
        if self.is_loaded:
            return
        self.__LoadItemList()
        self.__LoadMobDropItem()
        self.is_loaded = True

    def _EnsureDescsLoaded(self):
        """Carica le descrizioni item al primo accesso."""
        if self._descs_loaded:
            return
        self.__LoadItemDescs()
        self._descs_loaded = True

    def _EnsureRefineLoaded(self):
        """Carica i dati refine/upgrade al primo accesso."""
        if self._refine_loaded:
            return
        self.__LoadRefineData()
        self.item_refined_targets = set(self.item_refined_vnum.values())
        self._refine_loaded = True

    def _EnsureChestLoaded(self):
        """Carica i dati forzieri al primo accesso."""
        if self._chest_loaded:
            return
        self.__LoadSpecialItemGroup()
        self._chest_loaded = True

    # ----------------------------------------------------------------
    #  Caricamento item_list.txt
    # ----------------------------------------------------------------
    def __LoadItemList(self):
        paths = [
            "hunter/" + FILE_ITEM_LIST,
            app.GetLocalePath() + "/hunter/" + FILE_ITEM_LIST,
            FILE_ITEM_LIST,
        ]
        for path in paths:
            try:
                if not os.path.exists(path) and not pack.Exist(path):
                    continue
                f = open(path, "r")
                count = 0
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    tokens = line.split()
                    if len(tokens) >= 3:
                        try:
                            vnum = int(tokens[0])
                            icon_path = tokens[2]
                            model_path = tokens[3] if len(tokens) > 3 else ""
                            self.item_models[vnum] = {"model": model_path, "icon": icon_path}
                            count += 1
                        except (ValueError, IndexError):
                            pass
                f.close()
                return
            except IOError:
                pass

    # ----------------------------------------------------------------
    #  Caricamento mob_drop_item.txt
    # ----------------------------------------------------------------
    def __LoadMobDropItem(self):
        paths = [
            "hunter/" + FILE_MOB_DROP,
            app.GetLocalePath() + "/hunter/" + FILE_MOB_DROP,
            FILE_MOB_DROP,
        ]
        for path in paths:
            lines = self.__ReadFileLines(path)
            if lines is None:
                continue
            cur_mob = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                lower = line.lower()
                if lower.startswith("group"):
                    cur_mob = 0
                elif lower.startswith("mob"):
                    try:
                        parts = line.split()
                        if len(parts) >= 2:
                            cur_mob = int(parts[1])
                            if cur_mob not in self.mob_drops:
                                self.mob_drops[cur_mob] = []
                    except (ValueError, IndexError):
                        cur_mob = 0
                elif cur_mob != 0 and len(line) > 0 and line[0].isdigit():
                    tokens = line.split()
                    if len(tokens) >= 3:
                        try:
                            item_vnum = int(tokens[1])
                            count = int(tokens[2])
                            rate = tokens[3] if len(tokens) > 3 else "???"
                            self.mob_drops[cur_mob].append((item_vnum, count, rate))
                            if item_vnum not in self.item_origins:
                                self.item_origins[item_vnum] = []
                            if cur_mob not in self.item_origins[item_vnum]:
                                self.item_origins[item_vnum].append(cur_mob)
                        except (ValueError, IndexError):
                            pass
            return

    # ----------------------------------------------------------------
    #  Caricamento itemdesc.txt
    # ----------------------------------------------------------------
    def __LoadItemDescs(self):
        desc_path = "hunter/itemdesc.txt"
        try:
            f = open(desc_path, "r")
            for line in f:
                parts = line.split("\t")
                if len(parts) >= 3:
                    try:
                        vnum = int(parts[0])
                        desc = parts[2].strip()
                        if desc:
                            self.item_descs[vnum] = desc
                    except ValueError:
                        pass
            f.close()
        except IOError:
            pass

    # ----------------------------------------------------------------
    #  Caricamento dati refine (modulo Python o file txt fallback)
    # ----------------------------------------------------------------
    def __LoadRefineData(self):
        """Carica i dati di potenziamento. Prova prima il modulo Python
        (hunter_refine_data.py, funziona quando e' compilato e paccato),
        poi fallback ai file .txt."""
        loaded = False
        try:
            import hunter_refine_data
            data = hunter_refine_data.ITEM_REFINE
            for vnum, (refined, rset) in data.items():
                if refined > 0:
                    self.item_refined_vnum[vnum] = refined
                if rset > 0:
                    self.item_refine_set[vnum] = rset
            rdata = hunter_refine_data.REFINE_RECIPES
            for rid, (materials, cost, prob) in rdata.items():
                self.refine_recipes[rid] = {
                    "materials": materials,
                    "cost": cost,
                    "prob": prob,
                }
            loaded = True
        except:
            pass

        if not loaded:
            self.__LoadItemRefineFromFile()
            self.__LoadRefineRecipesFromFile()

    def __LoadItemRefineFromFile(self):
        paths = [
            "hunter/item_refine.txt",
            app.GetLocalePath() + "/hunter/item_refine.txt",
            "item_refine.txt",
        ]
        for path in paths:
            try:
                f = open(path, "r")
                count = 0
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        try:
                            vnum = int(parts[0])
                            refined = int(parts[1])
                            rset = int(parts[2])
                            if refined > 0:
                                self.item_refined_vnum[vnum] = refined
                            if rset > 0:
                                self.item_refine_set[vnum] = rset
                            count += 1
                        except (ValueError, IndexError):
                            pass
                f.close()
                return
            except:
                pass

    def __LoadRefineRecipesFromFile(self):
        paths = [
            "hunter/refine_recipe.txt",
            app.GetLocalePath() + "/hunter/refine_recipe.txt",
            "refine_recipe.txt",
        ]
        for path in paths:
            try:
                f = open(path, "r")
                count = 0
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) >= 13:
                        try:
                            rid = int(parts[0])
                            materials = []
                            for i in range(5):
                                mv = int(parts[1 + i * 2])
                                mc = int(parts[2 + i * 2])
                                if mv > 0 and mc > 0:
                                    materials.append((mv, mc))
                            cost = int(parts[11])
                            prob = int(parts[12])
                            self.refine_recipes[rid] = {
                                "materials": materials,
                                "cost": cost,
                                "prob": prob,
                            }
                            count += 1
                        except (ValueError, IndexError):
                            pass
                f.close()
                return
            except:
                pass

    # ----------------------------------------------------------------
    #  Caricamento special_item_group.txt (forzieri / bauli)
    # ----------------------------------------------------------------
    def __LoadSpecialItemGroup(self):
        paths = [
            FILE_SPECIAL_ITEM_GROUP,
            "hunter/" + FILE_SPECIAL_ITEM_GROUP,
            app.GetLocalePath() + "/" + FILE_SPECIAL_ITEM_GROUP,
        ]
        for path in paths:
            lines = self.__ReadFileLines(path)
            if lines is None:
                continue
            curVnum = 0
            curName = ""
            groupCount = 0
            for line in lines:
                line = line.strip()
                if not line or line.startswith("}"):
                    if line == "}":
                        curVnum = 0
                    continue
                commentIdx = line.find("//")
                if commentIdx >= 0:
                    line = line[:commentIdx].strip()
                if not line:
                    continue
                lower = line.lower()
                if lower.startswith("group"):
                    parts = line.split()
                    curName = parts[1] if len(parts) >= 2 else ""
                    curName = curName.replace("_", " ")
                    curVnum = 0
                elif lower.startswith("vnum"):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            curVnum = int(parts[1])
                            if curVnum not in self.chest_contents:
                                self.chest_contents[curVnum] = []
                            self.chest_names[curVnum] = curName
                            groupCount += 1
                        except ValueError:
                            curVnum = 0
                elif lower.startswith("type"):
                    continue
                elif lower.startswith("{"):
                    continue
                elif curVnum > 0 and len(line) > 0 and line[0].isdigit():
                    tokens = line.split()
                    if len(tokens) >= 4:
                        try:
                            itemVnum = int(tokens[1])
                            count = int(tokens[2])
                            rate = tokens[3]
                            self.chest_contents[curVnum].append((itemVnum, count, rate))
                            if itemVnum not in self.item_chest_sources:
                                self.item_chest_sources[itemVnum] = []
                            if curVnum not in self.item_chest_sources[itemVnum]:
                                self.item_chest_sources[itemVnum].append(curVnum)
                        except (ValueError, IndexError):
                            pass
            return

    # ----------------------------------------------------------------
    #  Query helpers
    # ----------------------------------------------------------------
    def GetMobName(self, vnum):
        """Ritorna il nome del mob o stringa vuota."""
        try:
            name = nonplayer.GetMonsterName(vnum)
            return name if name else ""
        except:
            return ""

    def GetMobLevel(self, vnum):
        """Ritorna il livello del mob."""
        try:
            return nonplayer.GetMonsterLevel(vnum)
        except:
            return 0

    def GetMobGrade(self, vnum):
        """Ritorna il grado del mob (0-6)."""
        try:
            return nonplayer.GetMonsterGrade(vnum)
        except:
            return 0

    def IsMetin(self, vnum):
        """Verifica se un mob e' un Metin (con override manuali)."""
        # Override espliciti
        if vnum in FORCE_BOSS_VNUMS:
            return False
        if vnum in FORCE_METIN_VNUMS:
            return True
        # Controlla keyword nel nome
        name = self.GetMobName(vnum).lower()
        for kw in FORCE_METIN_KEYWORDS:
            if kw in name:
                return True
        # Vnum range classico
        if 8000 <= vnum <= 8700:
            return True
        return False

    def IsBoss(self, vnum):
        """Verifica se un mob e' un Boss (con override manuali)."""
        # Override espliciti
        if vnum in FORCE_METIN_VNUMS:
            return False
        if vnum in FORCE_BOSS_VNUMS:
            return True
        # Controlla keyword Metin nel nome — se e' un Metin, non e' un Boss
        name = self.GetMobName(vnum).lower()
        for kw in FORCE_METIN_KEYWORDS:
            if kw in name:
                return False
        # Vnum range Metin — non e' un Boss
        if 8000 <= vnum <= 8700:
            return False
        # Forzieri non sono Boss
        if "forziere" in name:
            return False
        # Grado >= 4 e' Boss
        return self.GetMobGrade(vnum) >= 4

    def IsExcludedMob(self, vnum):
        """Verifica se un mob e' escluso dalla wiki."""
        name = self.GetMobName(vnum).lower()
        for kw in EXCLUDED_MOB_NAMES:
            if kw in name:
                return True
        return False

    def GetItemName(self, vnum):
        """Ritorna il nome dell'item."""
        try:
            item.SelectItem(vnum)
            return item.GetItemName()
        except:
            return "Item #%d" % vnum

    def GetItemIconPath(self, vnum):
        """Ritorna il path dell'icona dell'item."""
        data = self.item_models.get(vnum)
        if data and isinstance(data, dict):
            return data.get("icon", "")
        return ""

    def GetItemDroppers(self, item_vnum):
        """Ritorna la lista dei mob che droppano questo item."""
        return self.item_origins.get(item_vnum, [])

    def GetMobDrops(self, mob_vnum):
        """Ritorna la lista dei drop di un mob."""
        return self.mob_drops.get(mob_vnum, [])

    def GetDropRate(self, mob_vnum, item_vnum):
        """Ritorna count e rate per un drop specifico."""
        drops = self.mob_drops.get(mob_vnum, [])
        for (d_vnum, d_count, d_rate) in drops:
            if d_vnum == item_vnum:
                return (d_count, d_rate)
        return (0, "???")

    def SearchItems(self, query, typeFilter=None):
        """Cerca items per nome. typeFilter filtra per item.GetItemType()."""
        results = []
        q = query.lower().strip()
        for vnum in self.item_models:
            # Filtro per tipo item
            if typeFilter is not None:
                try:
                    item.SelectItem(vnum)
                    if item.GetItemType() != typeFilter:
                        continue
                except:
                    continue
            name = self.GetItemName(vnum).lower()
            if not q or q in name:
                results.append(vnum)
                if len(results) >= MAX_SEARCH_RESULTS:
                    break
        return results

    def SearchMobs(self, query, category):
        """Cerca mobs per nome e categoria. Ritorna lista di (vnum, name)."""
        results = []
        q = query.lower().strip()
        for vnum in self.mob_drops:
            # Escludi mob rimossi
            if self.IsExcludedMob(vnum):
                continue

            name = self.GetMobName(vnum)
            if not name:
                continue

            is_metin = self.IsMetin(vnum)
            is_boss = self.IsBoss(vnum)

            if category != "ALL":
                if category == "METIN" and not is_metin:
                    continue
                if category == "BOSS" and (not is_boss or is_metin):
                    continue
                if category == "MOB" and (is_metin or is_boss):
                    continue

            if not q or q in name.lower():
                results.append((vnum, name))
            if len(results) >= MAX_SEARCH_RESULTS:
                break
        return results

    def GetMobHP(self, vnum):
        """Ritorna HP del mob (se disponibile)."""
        try:
            return nonplayer.GetMonsterMaxHP(vnum)
        except:
            return 0

    def GetMobExp(self, vnum):
        """Ritorna EXP del mob (se disponibile)."""
        try:
            return nonplayer.GetMonsterExp(vnum)
        except:
            return 0

    def GetMobAtkRange(self, vnum):
        """Ritorna range attacco (melee/range)."""
        try:
            return nonplayer.GetMonsterAttackRange(vnum)
        except:
            return 0

    # ----------------------------------------------------------------
    #  Refine/Upgrade query helpers
    # ----------------------------------------------------------------
    def GetRefineRecipe(self, vnum):
        """Ritorna la ricetta per uppare questo item, o None."""
        self._EnsureRefineLoaded()
        rset = self.item_refine_set.get(vnum, 0)
        if rset <= 0:
            return None
        return self.refine_recipes.get(rset, None)

    def GetRefinedVnum(self, vnum):
        """Ritorna il vnum dell'item uppato (+1), o 0."""
        self._EnsureRefineLoaded()
        return self.item_refined_vnum.get(vnum, 0)

    def IsRefinable(self, vnum):
        """Controlla se l'item puo' essere uppato."""
        self._EnsureRefineLoaded()
        return vnum in self.item_refined_vnum

    def GetUpgradeChain(self, vnum):
        """Costruisce la catena upgrade completa (da +0 in poi).
        Ritorna lista di vnum dal +0 fino all'ultimo upgrade.
        Cerca anche all'indietro per trovare il +0."""
        self._EnsureRefineLoaded()
        reverse = {}
        for src, dst in self.item_refined_vnum.items():
            reverse[dst] = src

        base = vnum
        visited = set()
        while base in reverse and base not in visited:
            visited.add(base)
            base = reverse[base]

        chain = [base]
        cur = base
        visited2 = set()
        while cur in self.item_refined_vnum and cur not in visited2:
            visited2.add(cur)
            nxt = self.item_refined_vnum[cur]
            chain.append(nxt)
            cur = nxt

        return chain

    def GetUpgradePosition(self, vnum):
        """Ritorna (posizione_corrente, totale_livelli) nella catena upgrade.
        Es: Spada+5 in una catena di 9 -> (5, 9)."""
        chain = self.GetUpgradeChain(vnum)
        if vnum in chain:
            pos = chain.index(vnum)
            return (pos, len(chain) - 1)
        return (0, 0)

    def GetItemTypeInfo(self, vnum):
        """Ritorna (tipo_str, sottotipo_str) per un item."""
        try:
            item.SelectItem(vnum)
            it = item.GetItemType()
            ist = item.GetItemSubType()
            typeStr = ITEM_TYPE_NAMES.get(it, "")
            subStr = ""
            if it == 1:  # Arma
                subStr = WEAPON_SUBTYPES.get(ist, "")
            elif it == 2:  # Armatura
                subStr = ARMOR_SUBTYPES.get(ist, "")
            return (typeStr, subStr)
        except:
            return ("", "")

    def GetItemSize(self, vnum):
        """Ritorna il numero di slot dell'item (1, 2 o 3)."""
        try:
            item.SelectItem(vnum)
            h = item.GetItemSize()[1]
            if h >= 1:
                return h
        except:
            pass
        # Fallback per tipo item
        try:
            item.SelectItem(vnum)
            t = item.GetItemType()
            if t in (1, 2):  # WEAPON, ARMOR
                return 3
            elif t in (3, 28):  # COSTUME / shield
                return 2
        except:
            pass
        return 1

    def FormatYang(self, amount):
        """Formatta yang con separatori migliaia."""
        if amount <= 0:
            return "0"
        s = str(amount)
        parts = []
        while len(s) > 3:
            parts.append(s[-3:])
            s = s[:-3]
        parts.append(s)
        return ".".join(reversed(parts))

    # ----------------------------------------------------------------
    #  Item stat helpers
    # ----------------------------------------------------------------
    def GetItemLevelLimit(self, vnum):
        """Ritorna il livello minimo richiesto per equipaggiare l'item."""
        try:
            item.SelectItem(vnum)
            for i in xrange(2):
                limitType, limitValue = item.GetItemLimit(i)
                if limitType == 1 and limitValue > 0:  # LIMIT_LEVEL = 1
                    return limitValue
        except:
            pass
        return 0

    def GetItemApplies(self, vnum):
        """Ritorna lista di (nomeBonus, valore) dei bonus base dell'item."""
        result = []
        try:
            item.SelectItem(vnum)
            for i in xrange(3):
                applyType, applyValue = item.GetItemApply(i)
                if applyType > 0 and applyValue != 0:
                    typeStr = APPLY_NAMES.get(applyType, "Bonus %d" % applyType)
                    result.append((typeStr, applyValue))
        except:
            pass
        return result

    def GetItemValue(self, vnum, idx):
        """Ritorna un valore raw dell'item (indice 0-5)."""
        try:
            item.SelectItem(vnum)
            return item.GetItemValue(idx)
        except:
            return 0

    # ----------------------------------------------------------------
    #  Mob combat stat helpers
    # ----------------------------------------------------------------
    def GetMobDamage(self, vnum):
        """Ritorna (min_dmg, max_dmg) del mob."""
        try:
            return (nonplayer.GetMonsterDamage1(vnum), nonplayer.GetMonsterDamage2(vnum))
        except:
            return (0, 0)

    def GetMobDefense(self, vnum):
        """Ritorna la difesa del mob."""
        try:
            return nonplayer.GetMonsterDefense(vnum)
        except:
            return 0

    def GetMobRaceStr(self, vnum):
        """Ritorna la razza del mob come stringa (utile per bonus Forte vs)."""
        try:
            rf = nonplayer.GetMonsterRaceFlag(vnum)
            races = []
            for bit, name in MOB_RACE_NAMES.items():
                if rf & (1 << bit):
                    races.append(name)
            return ", ".join(races) if races else ""
        except:
            return ""

    def GetMobType(self, vnum):
        """Ritorna il tipo del mob come stringa."""
        MOB_TYPES = {0: "Mostro", 1: "NPC", 2: "Pietra", 3: "Cavallo", 4: "Warp", 6: "Goto"}
        try:
            t = nonplayer.GetMonsterType(vnum)
            return MOB_TYPES.get(t, "")
        except:
            return ""

    def FormatDropRate(self, rate):
        """Formatta la drop rate in percentuale leggibile."""
        try:
            rVal = int(rate)
            if rVal <= 0:
                return ""
            if rVal >= 1000000:
                return "100%"
            elif rVal >= 10000:
                pct = rVal / 10000.0
                if pct == int(pct):
                    return "%d%%" % int(pct)
                return "%.1f%%" % pct
            elif rVal >= 100:
                pct = rVal / 10000.0
                return "%.2f%%" % pct
            else:
                pct = rVal / 10000.0
                return "%.3f%%" % pct
        except:
            return str(rate)

    def GetChestContents(self, chestVnum):
        """Ritorna il contenuto di un forziere: [(item_vnum, count, rate), ...]"""
        self._EnsureChestLoaded()
        return self.chest_contents.get(chestVnum, [])

    def GetItemChestSources(self, itemVnum):
        """Ritorna i forzieri che contengono un item: [chest_vnum, ...]"""
        self._EnsureChestLoaded()
        return self.item_chest_sources.get(itemVnum, [])

    def GetChestName(self, chestVnum):
        """Ritorna il nome leggibile del gruppo forziere."""
        self._EnsureChestLoaded()
        return self.chest_names.get(chestVnum, "")

    def IsChest(self, vnum):
        """Verifica se un vnum e' un forziere con contenuti noti."""
        self._EnsureChestLoaded()
        return vnum in self.chest_contents

    def FormatChestRate(self, rate):
        """Formatta la rate dei forzieri (gia' in percentuale, non /10000)."""
        try:
            rVal = float(rate)
            if rVal <= 0:
                return ""
            if rVal >= 100:
                return "100%"
            if rVal == int(rVal):
                return "%d%%" % int(rVal)
            return "%.1f%%" % rVal
        except:
            return str(rate)

    def GetLevelTip(self, level):
        """Ritorna il consiglio di progressione per il livello dato."""
        for (minLv, maxLv), tip in LEVEL_TIPS.items():
            if minLv <= level < maxLv:
                return tip
        return ""

    def GetZoneForLevel(self, level):
        """Ritorna la zona di gioco consigliata per il livello."""
        for zoneName, info in ZONE_INFO.items():
            if info["minLv"] <= level < info["maxLv"]:
                return zoneName, info["phase"]
        if level >= 200:
            return "Foresta Incantata", "La Leggenda di Hunter"
        return "", ""

    def GetMobLocation(self, vnum):
        """Ritorna la posizione corretta del mob (dungeon o mappa overworld).
        Per i boss usa BOSS_LOCATION, per gli altri GetZoneForLevel."""
        # Boss con posizione mappata manualmente
        if vnum in BOSS_LOCATION:
            return BOSS_LOCATION[vnum]
        # Fallback basato sul livello
        level = self.GetMobLevel(vnum)
        if level > 0:
            zoneName, phaseStr = self.GetZoneForLevel(level)
            if zoneName:
                return "%s (%s)" % (zoneName, phaseStr)
        return ""

    def GetDungeonForLevel(self, level):
        """Ritorna il dungeon appropriato per il livello."""
        bestDg = None
        bestLv = 0
        for dgLv, dgInfo in DUNGEON_INFO.items():
            if dgLv <= level and dgLv > bestLv:
                bestLv = dgLv
                bestDg = dgInfo
        return bestDg

    def GetChestDungeonName(self, chestVnum):
        """Ritorna il nome del dungeon associato a un forziere, se noto."""
        self._EnsureChestLoaded()
        return CHEST_DUNGEON_MAP.get(chestVnum, "")

    def GetItemTypeTip(self, itemType):
        """Ritorna un consiglio basato sul tipo di item."""
        return ITEM_TYPE_TIPS.get(itemType, "")

    def GetSpecialAcquisition(self, itemName):
        """Cerca note di acquisizione speciale basate su keyword nel nome."""
        if not itemName:
            return ""
        lowerName = itemName.lower()
        for keyword, note in SPECIAL_ACQUISITION.items():
            if keyword in lowerName:
                return note
        return ""


# Singleton globale
DATA_MGR = WikiDataManager()


# ============================================================================
#  REFINE POPUP - Finestra potenziamento centrata (stile Dracarys)
# ============================================================================
REFINE_POP_W = 560
REFINE_POP_H = 500
REFINE_HEADER_H = 55
REFINE_COL_HDR_H = 24
REFINE_ORIGIN_H = 95
REFINE_SCROLL_W = 16
REFINE_PAD = 15

# Column widths for vertical layout
RCOL_LVL_W = 60
RCOL_ITEM_W = 42
RCOL_MAT_W = 42
RCOL_YANG_W = 80
RCOL_PROB_W = 58

class RefinePopup(ui.ScriptWindow):
    """Popup centrato con tabella upgrade completa a layout verticale.
    Ogni riga = un livello di upgrade. Scrollbar verticale se servono piu' righe.
    Tooltip classico Metin2 su ogni slot."""

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self._bars = []
        self._texts = []
        self._slots = []
        self._slotVnums = {}
        self._itemVnum = 0
        self._chain = []
        self._onNavigate = None
        self._toolTip = None
        # Scroll state
        self._scrollBar = None
        self._scrollOffset = 0
        self._numVisible = 0
        self._maxMats = 1
        self._rowH = 38
        self._visibleRows = []

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    def _GetOrCreateToolTip(self):
        if not self._toolTip:
            try:
                import uiToolTip
                self._toolTip = uiToolTip.ItemToolTip()
            except:
                pass
        return self._toolTip

    def __OnSlotOverInWithVnum(self, vnum):
        """Mostra tooltip per un vnum specifico."""
        tt = self._GetOrCreateToolTip()
        if tt and vnum > 0:
            tt.SetItemToolTip(vnum)
            tt.ShowToolTip()

    def __OnSlotOverOut(self):
        """Nascondi tooltip."""
        if self._toolTip:
            try:
                self._toolTip.HideToolTip()
            except:
                pass

    def __OnRowSlotOverIn(self, rowIdx, slotType, matIdx=0):
        """Hover su uno slot in una riga visibile — risolve vnum e mostra tooltip."""
        dataIdx = self._scrollOffset + rowIdx
        if dataIdx >= len(self._chain):
            return
        v = self._chain[dataIdx]
        vnum = 0
        if slotType == 0:  # item
            vnum = v
        elif slotType == 1:  # materiale
            recipe = DATA_MGR.GetRefineRecipe(v)
            if recipe:
                mats = recipe.get("materials", [])
                if matIdx < len(mats):
                    vnum = mats[matIdx][0]
        if vnum > 0:
            self.__OnSlotOverInWithVnum(vnum)

    def __OnRowSlotClick(self, rowIdx, slotType, matIdx=0):
        """Click su uno slot nella tabella refine — naviga all'item nella wiki."""
        dataIdx = self._scrollOffset + rowIdx
        if dataIdx >= len(self._chain):
            return
        v = self._chain[dataIdx]
        vnum = 0
        if slotType == 0:  # item
            vnum = v
        elif slotType == 1:  # materiale
            recipe = DATA_MGR.GetRefineRecipe(v)
            if recipe:
                mats = recipe.get("materials", [])
                if matIdx < len(mats):
                    vnum = mats[matIdx][0]
        if vnum > 0 and self._onNavigate:
            self.__OnSlotOverOut()
            self._onNavigate(vnum)

    def Destroy(self):
        if self._toolTip:
            try:
                self._toolTip.HideToolTip()
                self._toolTip.Hide()
            except:
                pass
            self._toolTip = None
        for b in self._bars:
            try:
                b.Hide()
            except:
                pass
        self._bars = []
        for t in self._texts:
            try:
                t.Hide()
            except:
                pass
        self._texts = []
        for s in self._slots:
            try:
                s.Hide()
            except:
                pass
        self._slots = []
        self._slotVnums = {}
        self._visibleRows = []
        self._scrollBar = None
        self._chain = []
        self._onNavigate = None
        self.ClearDictionary()
        self.Hide()

    def SetNavigateEvent(self, func):
        self._onNavigate = func

    def Open(self, vnum):
        self._itemVnum = vnum
        self._chain = DATA_MGR.GetUpgradeChain(vnum)
        self.__Build()
        self.SetCenterPosition()
        self.Show()
        self.SetTop()

    def Close(self):
        # Svuota slot per evitare che il C++ GridSlotWindow intercetti input
        if self._toolTip:
            try:
                self._toolTip.HideToolTip()
            except:
                pass
        for s in self._slots:
            try:
                s.SetItemSlot(0, 0, 0)
                s.RefreshSlot()
            except:
                pass
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    # --- helpers ---
    def _Bar(self, parent, x, y, w, h, color, pick=False):
        b = ui.Bar()
        b.SetParent(parent)
        b.SetPosition(x, y)
        b.SetSize(w, h)
        b.SetColor(color)
        if not pick:
            b.AddFlag("not_pick")
        b.Show()
        self._bars.append(b)
        return b

    def _Text(self, parent, x, y, text, color, center=False):
        t = ui.TextLine()
        t.SetParent(parent)
        t.SetPosition(x, y)
        if center:
            t.SetHorizontalAlignCenter()
        t.SetText(text)
        t.SetPackedFontColor(color)
        t.AddFlag("not_pick")
        t.Show()
        self._texts.append(t)
        return t

    def __Build(self):
        # Pulisci vecchio contenuto
        for b in self._bars:
            try:
                b.Hide()
            except:
                pass
        self._bars = []
        for t in self._texts:
            try:
                t.Hide()
            except:
                pass
        self._texts = []
        for s in self._slots:
            try:
                s.Hide()
            except:
                pass
        self._slots = []
        self._slotVnums = {}
        self._visibleRows = []
        self._scrollBar = None

        chain = self._chain
        numLevels = len(chain)
        if numLevels < 1:
            return

        # Conta max materiali nella catena
        maxMats = 0
        for v in chain:
            recipe = DATA_MGR.GetRefineRecipe(v)
            if recipe:
                mats = recipe.get("materials", [])
                if len(mats) > maxMats:
                    maxMats = len(mats)
        maxMats = max(1, min(maxMats, 5))
        self._maxMats = maxMats

        # Altezza riga (basata su dimensione item)
        itemH = DATA_MGR.GetItemSize(chain[0]) if chain else 1
        ROW_H = max(38, itemH * 32 + 6)
        self._rowH = ROW_H

        # Larghezza popup dinamica
        tableDataW = RCOL_LVL_W + RCOL_ITEM_W + maxMats * RCOL_MAT_W + RCOL_YANG_W + RCOL_PROB_W
        POP_W = max(REFINE_POP_W, tableDataW + REFINE_PAD * 2 + REFINE_SCROLL_W + 10)

        # Area scroll — massimo 380px, shrink se pochi livelli
        maxScrollH = 380
        scrollAreaH = min(maxScrollH, ROW_H * numLevels)
        numVisible = max(1, scrollAreaH // ROW_H)
        scrollAreaH = numVisible * ROW_H  # allineato a righe intere
        self._numVisible = numVisible
        needsScroll = numLevels > numVisible

        POP_H = REFINE_HEADER_H + REFINE_COL_HDR_H + scrollAreaH + 6 + REFINE_ORIGIN_H + 10

        TABLE_X = REFINE_PAD
        TABLE_W = POP_W - REFINE_PAD * 2 - (REFINE_SCROLL_W + 4 if needsScroll else 0)

        self.SetSize(POP_W, POP_H)
        self.AddFlag("movable")
        self.AddFlag("float")

        # === SFONDO E BORDI ===
        self._Bar(self, 0, 0, POP_W, POP_H, COLOR_BG_MAIN)
        for (bx, by), (bw, bh) in [((0, 0), (POP_W, 1)), ((0, POP_H - 1), (POP_W, 1)),
                                    ((0, 0), (1, POP_H)), ((POP_W - 1, 0), (1, POP_H))]:
            self._Bar(self, bx, by, bw, bh, COLOR_BORDER)

        # === HEADER ===
        self._Bar(self, 2, 2, POP_W - 4, 30, COLOR_BG_HEADER)
        baseName = DATA_MGR.GetItemName(chain[0]) if chain else "???"
        self._Text(self, POP_W // 2, 8, baseName, COLOR_TEXT_GOLD, center=True)

        # Bottone X
        btnX = ui.Window()
        btnX.SetParent(self)
        btnX.SetPosition(POP_W - 30, 5)
        btnX.SetSize(24, 20)
        xBg = ui.Bar()
        xBg.SetParent(btnX)
        xBg.SetPosition(0, 0)
        xBg.SetSize(24, 20)
        xBg.SetColor(COLOR_BTN_NORMAL)
        xBg.AddFlag("not_pick")
        xBg.Show()
        self._bars.append(xBg)
        xTxt = ui.TextLine()
        xTxt.SetParent(btnX)
        xTxt.SetPosition(12, 2)
        xTxt.SetHorizontalAlignCenter()
        xTxt.SetText("X")
        xTxt.SetPackedFontColor(COLOR_TEXT_LIGHT)
        xTxt.AddFlag("not_pick")
        xTxt.Show()
        self._texts.append(xTxt)
        btnX.OnMouseLeftButtonUp = lambda: self.Close()
        btnX.Show()
        self._bars.append(btnX)

        # Sotto-header: tipo + range
        typeStr, subStr = DATA_MGR.GetItemTypeInfo(chain[0]) if chain else ("", "")
        typeLabel = "%s - %s" % (typeStr, subStr) if subStr else (typeStr or "Oggetto")
        rangeStr = "%s | +0 -> +%d" % (typeLabel, numLevels - 1)
        self._Text(self, POP_W // 2, 36, rangeStr, COLOR_TEXT_GRAY, center=True)

        # === INTESTAZIONI COLONNE ===
        chY = REFINE_HEADER_H
        hdrW = TABLE_W + (REFINE_SCROLL_W + 4 if needsScroll else 0)
        self._Bar(self, TABLE_X, chY, hdrW, REFINE_COL_HDR_H, 0xCC0A0A18)

        cx = TABLE_X
        self._Text(self, cx + RCOL_LVL_W // 2, chY + 5, "Livello", COLOR_TEXT_CYAN, center=True)
        cx += RCOL_LVL_W
        self._Text(self, cx + RCOL_ITEM_W // 2, chY + 5, "Item", COLOR_TEXT_CYAN, center=True)
        cx += RCOL_ITEM_W
        for mi in xrange(maxMats):
            self._Text(self, cx + RCOL_MAT_W // 2, chY + 5, "Mat.%d" % (mi + 1), COLOR_TEXT_CYAN, center=True)
            cx += RCOL_MAT_W
        self._Text(self, cx + RCOL_YANG_W // 2, chY + 5, "Yang", COLOR_TEXT_GOLD, center=True)
        cx += RCOL_YANG_W
        self._Text(self, cx + RCOL_PROB_W // 2, chY + 5, "Prob.", COLOR_TEXT_GRAY, center=True)
        self._Bar(self, TABLE_X, chY + REFINE_COL_HDR_H - 1, hdrW, 1, COLOR_BORDER_DIM)

        # === RIGHE VISIBILI (virtual rows) ===
        rowStartY = REFINE_HEADER_H + REFINE_COL_HDR_H
        self._visibleRows = []

        for r in xrange(numVisible):
            rowY = rowStartY + r * ROW_H
            row = {}

            # Sfondo riga (alternato)
            row['bg'] = self._Bar(self, TABLE_X, rowY, TABLE_W, ROW_H, 0x88000000)
            # Highlight item corrente (nascosto di default)
            row['hl'] = self._Bar(self, TABLE_X, rowY, TABLE_W, ROW_H, 0x33FFD700)
            row['hl'].Hide()
            # Separatore riga
            self._Bar(self, TABLE_X, rowY + ROW_H - 1, TABLE_W, 1, 0x22FFFFFF)

            cx = TABLE_X
            # Testo livello
            row['lvlTxt'] = self._Text(self, cx + 5, rowY + ROW_H // 2 - 6, "", COLOR_TEXT_GOLD)
            cx += RCOL_LVL_W
            self._Bar(self, cx, rowY, 1, ROW_H, 0x22FFFFFF)

            # Slot item
            itemSlot = ui.GridSlotWindow()
            itemSlot.SetParent(self)
            itemSlot.SetPosition(cx + (RCOL_ITEM_W - 32) // 2, rowY + (ROW_H - 32) // 2)
            itemSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
            itemSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
            itemSlot.SetOverInItemEvent(lambda si, ri=r: self.__OnRowSlotOverIn(ri, 0))
            itemSlot.SetOverOutItemEvent(lambda: self.__OnSlotOverOut())
            itemSlot.SetSelectItemSlotEvent(lambda si, ri=r: self.__OnRowSlotClick(ri, 0))
            itemSlot.Show()
            self._slots.append(itemSlot)
            row['itemSlot'] = itemSlot
            cx += RCOL_ITEM_W
            self._Bar(self, cx, rowY, 1, ROW_H, 0x22FFFFFF)

            # Slot materiali
            row['matSlots'] = []
            for mi in xrange(maxMats):
                matSlot = ui.GridSlotWindow()
                matSlot.SetParent(self)
                matSlot.SetPosition(cx + (RCOL_MAT_W - 32) // 2, rowY + (ROW_H - 32) // 2)
                matSlot.ArrangeSlot(0, 1, 1, 32, 32, 0, 0)
                matSlot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
                matSlot.SetOverInItemEvent(lambda si, ri=r, m=mi: self.__OnRowSlotOverIn(ri, 1, m))
                matSlot.SetOverOutItemEvent(lambda: self.__OnSlotOverOut())
                matSlot.SetSelectItemSlotEvent(lambda si, ri=r, m=mi: self.__OnRowSlotClick(ri, 1, m))
                matSlot.Show()
                self._slots.append(matSlot)
                row['matSlots'].append(matSlot)
                cx += RCOL_MAT_W
            self._Bar(self, cx, rowY, 1, ROW_H, 0x22FFFFFF)

            # Testo Yang
            row['yangTxt'] = self._Text(self, cx + RCOL_YANG_W // 2, rowY + ROW_H // 2 - 6,
                                         "", COLOR_TEXT_YELLOW, center=True)
            cx += RCOL_YANG_W
            self._Bar(self, cx, rowY, 1, ROW_H, 0x22FFFFFF)

            # Testo probabilita'
            row['probTxt'] = self._Text(self, cx + RCOL_PROB_W // 2, rowY + ROW_H // 2 - 6,
                                         "", COLOR_TEXT_GRAY, center=True)

            self._visibleRows.append(row)

        # === SCROLLBAR ===
        self._scrollOffset = 0
        self._scrollBar = None
        if needsScroll:
            sb = ui.ScrollBar()
            sb.SetParent(self)
            sb.SetPosition(TABLE_X + TABLE_W + 2, rowStartY)
            sb.SetScrollBarSize(scrollAreaH)
            sb.SetScrollEvent(self.__OnPopupScroll)
            sb.Show()
            self._bars.append(sb)
            self._scrollBar = sb

        # === SEZIONE ORIGINI ===
        origStartY = rowStartY + scrollAreaH + 6
        self._Bar(self, REFINE_PAD, origStartY, POP_W - REFINE_PAD * 2, 1, COLOR_SEPARATOR)
        origY = origStartY + 6

        baseVnum = chain[0] if chain else self._itemVnum
        origins = DATA_MGR.GetItemDroppers(baseVnum)
        if origins:
            self._Text(self, REFINE_PAD + 5, origY, "Droppato da:", COLOR_TEXT_CYAN)
            origY += 16
            for mob_vnum in origins[:4]:
                mobName = DATA_MGR.GetMobName(mob_vnum)
                mobLevel = DATA_MGR.GetMobLevel(mob_vnum)
                grade = DATA_MGR.GetMobGrade(mob_vnum)
                gradeTag = {2: "[R]", 3: "[S]", 4: "[Boss]", 5: "[Raid]", 6: "[Leg]"}.get(grade, "")
                txt = "  %s %s Lv.%d" % (mobName, gradeTag, mobLevel) if mobLevel > 0 else "  %s %s" % (mobName, gradeTag)
                col = GRADE_COLORS.get(grade, COLOR_TEXT_LIGHT)
                self._Text(self, REFINE_PAD + 15, origY, txt, col)
                origY += 15
            if len(origins) > 4:
                self._Text(self, REFINE_PAD + 15, origY,
                           "...e altri %d mob" % (len(origins) - 4), COLOR_TEXT_DARK)
        else:
            self._Text(self, REFINE_PAD + 5, origY, "Nessuna origine nota", COLOR_TEXT_DARK)

        # Popola le righe visibili
        self.__RefreshPopupRows()

    # ================================================================
    #  REFRESH RIGHE VISIBILI
    # ================================================================
    def __RefreshPopupRows(self):
        """Aggiorna i widget delle righe visibili in base a scrollOffset."""
        chain = self._chain
        numLevels = len(chain)

        for r in xrange(self._numVisible):
            row = self._visibleRows[r]
            dataIdx = self._scrollOffset + r

            if dataIdx >= numLevels:
                # Riga vuota — nascondi tutto
                row['bg'].SetColor(0x88000000)
                row['hl'].Hide()
                row['lvlTxt'].SetText("")
                row['itemSlot'].SetItemSlot(0, 0, 0)
                for ms in row['matSlots']:
                    ms.SetItemSlot(0, 0, 0)
                row['yangTxt'].SetText("")
                row['probTxt'].SetText("")
                continue

            v = chain[dataIdx]
            recipe = DATA_MGR.GetRefineRecipe(v)

            # Sfondo alternato
            row['bg'].SetColor(0x88000000 if dataIdx % 2 == 0 else 0x880A0A18)

            # Highlight item corrente
            if v == self._itemVnum:
                row['hl'].Show()
            else:
                row['hl'].Hide()

            # Testo livello
            if recipe:
                row['lvlTxt'].SetText("+%d -> +%d" % (dataIdx, dataIdx + 1))
                row['lvlTxt'].SetPackedFontColor(COLOR_TEXT_GOLD)
            else:
                row['lvlTxt'].SetText("+%d MAX" % dataIdx)
                row['lvlTxt'].SetPackedFontColor(COLOR_TEXT_ORANGE)

            # Slot item
            try:
                row['itemSlot'].SetItemSlot(0, v, 0)
            except:
                pass

            # Materiali
            mats = recipe.get("materials", []) if recipe else []
            for mi in xrange(self._maxMats):
                if mi < len(mats):
                    mat_vnum, mat_count = mats[mi]
                    try:
                        row['matSlots'][mi].SetItemSlot(0, mat_vnum, mat_count)
                    except:
                        pass
                else:
                    row['matSlots'][mi].SetItemSlot(0, 0, 0)

            # Yang
            if recipe:
                cost = recipe.get("cost", 0)
                if cost > 0:
                    if cost >= 1000000:
                        d = cost * 10 // 1000000
                        costStr = "%dkk" % (d // 10) if d % 10 == 0 else "%d.%dkk" % (d // 10, d % 10)
                    elif cost >= 1000:
                        d = cost * 10 // 1000
                        costStr = "%dk" % (d // 10) if d % 10 == 0 else "%d.%dk" % (d // 10, d % 10)
                    else:
                        costStr = str(cost)
                    row['yangTxt'].SetText(costStr)
                    row['yangTxt'].SetPackedFontColor(COLOR_TEXT_YELLOW)
                else:
                    row['yangTxt'].SetText("-")
                    row['yangTxt'].SetPackedFontColor(COLOR_TEXT_DARK)
            else:
                row['yangTxt'].SetText("-")
                row['yangTxt'].SetPackedFontColor(COLOR_TEXT_DARK)

            # Probabilita' (nascosta - dato segreto)
            if recipe:
                prob = recipe.get("prob", 0)
                if prob > 0:
                    row['probTxt'].SetText("?")
                    row['probTxt'].SetPackedFontColor(COLOR_TEXT_DARK)
                else:
                    row['probTxt'].SetText("-")
                    row['probTxt'].SetPackedFontColor(COLOR_TEXT_DARK)
            else:
                row['probTxt'].SetText("-")
                row['probTxt'].SetPackedFontColor(COLOR_TEXT_DARK)

        # Refresh rendering slot
        for r in xrange(self._numVisible):
            row = self._visibleRows[r]
            try:
                row['itemSlot'].RefreshSlot()
            except:
                pass
            for ms in row['matSlots']:
                try:
                    ms.RefreshSlot()
                except:
                    pass

    # ================================================================
    #  SCROLL HANDLER
    # ================================================================
    def __OnPopupScroll(self):
        if not self._scrollBar:
            return
        pos = self._scrollBar.GetPos()
        numLevels = len(self._chain)
        maxOffset = max(0, numLevels - self._numVisible)
        self._scrollOffset = int(pos * maxOffset)
        self.__RefreshPopupRows()




# ============================================================================
#  WIKI WINDOW - Finestra principale completa
# ============================================================================
class WikiWindow(ui.ScriptWindow):
    """
    Finestra Wiki completa con:
    - Sidebar categorie (Boss, Metin, Oggetti)
    - Barra di ricerca
    - Lista risultati / Griglia items
    - Preview 3D modello
    - Pannello dettagli (drop, origini, info)
    - Navigazione incrociata (clicca drop -> vai all'item e viceversa)
    - Pattern anti-memory-leak completo
    """

    # ================================================================
    #  INNER CLASS: ListItem per mob (Boss/Metin)
    # ================================================================
    class MobListItem(ui.ListBoxEx.Item):
        def __init__(self, text, vnum, width, grade=0, level=0):
            ui.ListBoxEx.Item.__init__(self)
            self.vnum = vnum
            self.type_flag = 1  # MOB
            self.name = text
            self._grade = grade
            self.SetSize(width, 28)

            self.bg = ui.Bar()
            self.bg.SetParent(self)
            self.bg.SetPosition(0, 0)
            self.bg.SetSize(width, 27)
            self.bg.SetColor(0x88000000)
            self.bg.AddFlag("not_pick")
            self.bg.Show()

            # Indicatore grado (barra colorata sinistra 3px)
            gradeColor = GRADE_COLORS.get(grade, 0xFF888888)
            self.gradeBar = ui.Bar()
            self.gradeBar.SetParent(self)
            self.gradeBar.SetPosition(0, 0)
            self.gradeBar.SetSize(3, 27)
            self.gradeBar.SetColor(gradeColor)
            self.gradeBar.AddFlag("not_pick")
            self.gradeBar.Show()

            self.line = ui.Bar()
            self.line.SetParent(self)
            self.line.SetPosition(0, 27)
            self.line.SetSize(width, 1)
            self.line.SetColor(COLOR_BORDER_ACCENT)
            self.line.AddFlag("not_pick")
            self.line.Show()

            # Nome mob (troncato per lasciare spazio al livello e grado)
            maxTextW = width - 80
            self.textLine = ui.TextLine()
            self.textLine.SetParent(self)
            self.textLine.SetPosition(8, 6)
            self.textLine.SetText(text)
            self.textLine.SetPackedFontColor(gradeColor if grade >= 4 else COLOR_TEXT_LIGHT)
            self.textLine.SetLimitWidth(maxTextW)
            self.textLine.AddFlag("not_pick")
            self.textLine.Show()

            # Livello (destra) con colore in base al grado
            self.levelText = None
            if level > 0:
                self.levelText = ui.TextLine()
                self.levelText.SetParent(self)
                self.levelText.SetPosition(width - 8, 6)
                self.levelText.SetHorizontalAlignRight()
                self.levelText.SetText("Lv.%d" % level)
                lvlColor = gradeColor if grade >= 3 else COLOR_TEXT_DARK
                self.levelText.SetPackedFontColor(lvlColor)
                self.levelText.AddFlag("not_pick")
                self.levelText.Show()

        def OnMouseOverIn(self):
            self.bg.SetColor(0xCC1A1A30)
            self.textLine.SetPackedFontColor(COLOR_TEXT_WHITE)
            if self.levelText:
                self.levelText.SetPackedFontColor(COLOR_TEXT_GOLD)

        def OnMouseOverOut(self):
            self.bg.SetColor(0x88000000)
            gradeColor = GRADE_COLORS.get(self._grade, 0xFF888888)
            self.textLine.SetPackedFontColor(gradeColor if self._grade >= 4 else COLOR_TEXT_LIGHT)
            if self.levelText:
                lvlColor = gradeColor if self._grade >= 3 else COLOR_TEXT_DARK
                self.levelText.SetPackedFontColor(lvlColor)

        def __del__(self):
            ui.ListBoxEx.Item.__del__(self)

    # ================================================================
    #  INNER CLASS: ListItem per Fratture (Boss/SuperMetin/Bauli)
    # ================================================================
    class FractureListItem(ui.ListBoxEx.Item):
        def __init__(self, text, vnum, width, tier, tierColor, rightText, fractCat):
            ui.ListBoxEx.Item.__init__(self)
            self.vnum = vnum
            self.type_flag = 1
            self.name = text
            self._tier = tier
            self._tierColor = tierColor
            self._fractCat = fractCat
            self.SetSize(width, 28)

            self.bg = ui.Bar()
            self.bg.SetParent(self)
            self.bg.SetPosition(0, 0)
            self.bg.SetSize(width, 27)
            self.bg.SetColor(0x88000000)
            self.bg.AddFlag("not_pick")
            self.bg.Show()

            # Barra tier colorata sinistra (3px)
            self.tierBar = ui.Bar()
            self.tierBar.SetParent(self)
            self.tierBar.SetPosition(0, 0)
            self.tierBar.SetSize(3, 27)
            self.tierBar.SetColor(tierColor)
            self.tierBar.AddFlag("not_pick")
            self.tierBar.Show()

            self.line = ui.Bar()
            self.line.SetParent(self)
            self.line.SetPosition(0, 27)
            self.line.SetSize(width, 1)
            self.line.SetColor(COLOR_BORDER_ACCENT)
            self.line.AddFlag("not_pick")
            self.line.Show()

            # Nome
            maxTextW = width - 100
            self.textLine = ui.TextLine()
            self.textLine.SetParent(self)
            self.textLine.SetPosition(8, 6)
            self.textLine.SetText(text)
            self.textLine.SetPackedFontColor(tierColor)
            self.textLine.SetLimitWidth(maxTextW)
            self.textLine.AddFlag("not_pick")
            self.textLine.Show()

            # Info destra (Gloria + Tier)
            self.rightText = ui.TextLine()
            self.rightText.SetParent(self)
            self.rightText.SetPosition(width - 8, 6)
            self.rightText.SetHorizontalAlignRight()
            self.rightText.SetText(rightText)
            self.rightText.SetPackedFontColor(COLOR_TEXT_DARK)
            self.rightText.AddFlag("not_pick")
            self.rightText.Show()

        def OnMouseOverIn(self):
            self.bg.SetColor(0xCC1A1A30)
            self.textLine.SetPackedFontColor(COLOR_TEXT_WHITE)
            self.rightText.SetPackedFontColor(COLOR_TEXT_GOLD)

        def OnMouseOverOut(self):
            self.bg.SetColor(0x88000000)
            self.textLine.SetPackedFontColor(self._tierColor)
            self.rightText.SetPackedFontColor(COLOR_TEXT_DARK)

        def __del__(self):
            ui.ListBoxEx.Item.__del__(self)

    # ================================================================
    #  INNER CLASS: ListItem per dettagli drop
    # ================================================================
    class DropListItem(ui.ListBoxEx.Item):
        def __init__(self, text, vnum, type_flag, icon_path="", width=DETAIL_ITEM_W):
            ui.ListBoxEx.Item.__init__(self)
            self.vnum = vnum
            self.type_flag = type_flag  # 0=item, 1=mob, 2=refine, -1=info
            self.name = text
            self._toolTipRef = None
            self.isClickable = (type_flag >= 0)
            self.SetSize(width, 30)

            self.bg = ui.Bar()
            self.bg.SetParent(self)
            self.bg.SetPosition(0, 0)
            self.bg.SetSize(width, 29)
            self.bg.SetColor(0x88000000)
            self.bg.AddFlag("not_pick")
            self.bg.Show()

            # Barra tipo indicatore sinistra (3px)
            typeBarColor = {0: COLOR_TEXT_GREEN, 1: COLOR_TEXT_ORANGE, 2: COLOR_TEXT_GOLD}.get(type_flag, 0x00000000)
            if typeBarColor != 0x00000000:
                self.typeBar = ui.Bar()
                self.typeBar.SetParent(self)
                self.typeBar.SetPosition(0, 0)
                self.typeBar.SetSize(3, 29)
                self.typeBar.SetColor(typeBarColor)
                self.typeBar.AddFlag("not_pick")
                self.typeBar.Show()
            else:
                self.typeBar = None

            self.line = ui.Bar()
            self.line.SetParent(self)
            self.line.SetPosition(0, 29)
            self.line.SetSize(width, 1)
            self.line.SetColor(COLOR_BORDER_ACCENT)
            self.line.AddFlag("not_pick")
            self.line.Show()

            textX = 8
            self.iconImage = None
            if icon_path and len(icon_path) > 4 and "/" in icon_path:
                try:
                    self.iconImage = ui.ImageBox()
                    self.iconImage.SetParent(self)
                    self.iconImage.SetPosition(4, 0)
                    self.iconImage.AddFlag("not_pick")
                    self.iconImage.LoadImage(icon_path)
                    self.iconImage.Show()
                    textX = 36
                except:
                    if self.iconImage:
                        self.iconImage.Hide()
                    self.iconImage = None

            textColor = COLOR_TEXT_CYAN if self.isClickable else COLOR_TEXT_GRAY
            self.textLine = ui.TextLine()
            self.textLine.SetParent(self)
            self.textLine.SetPosition(textX, 7)
            self.textLine.SetText(text)
            self.textLine.SetPackedFontColor(textColor)
            self.textLine.SetLimitWidth(max(50, width - textX - 16))
            self.textLine.AddFlag("not_pick")
            self.textLine.Show()

            # Arrow indicator for clickable items
            self.arrowText = None
            if self.isClickable:
                self.arrowText = ui.TextLine()
                self.arrowText.SetParent(self)
                self.arrowText.SetPosition(width - 14, 7)
                self.arrowText.SetText(">")
                self.arrowText.SetPackedFontColor(COLOR_TEXT_DARK)
                self.arrowText.AddFlag("not_pick")
                self.arrowText.Show()

        def SetToolTipRef(self, toolTipRef):
            self._toolTipRef = toolTipRef

        def OnMouseOverIn(self):
            if self.isClickable:
                self.bg.SetColor(0xCC1A1A30)
                self.textLine.SetPackedFontColor(COLOR_TEXT_WHITE)
                if self.arrowText:
                    self.arrowText.SetPackedFontColor(COLOR_TEXT_GOLD)
                    self.arrowText.SetText(">>")
                if self.typeBar:
                    self.typeBar.SetSize(4, self.bg.GetHeight() if self.bg else 29)
            # Tooltip classico per gli item (type_flag 0)
            if self.type_flag == 0 and self.vnum > 0:
                tt = getattr(self, '_toolTipRef', None)
                if tt:
                    try:
                        tt.SetItemToolTip(self.vnum)
                        tt.ShowToolTip()
                    except:
                        pass

        def OnMouseOverOut(self):
            self.bg.SetColor(0x88000000)
            if self.isClickable:
                self.textLine.SetPackedFontColor(COLOR_TEXT_CYAN)
            else:
                self.textLine.SetPackedFontColor(COLOR_TEXT_GRAY)
            if self.arrowText:
                self.arrowText.SetPackedFontColor(COLOR_TEXT_DARK)
                self.arrowText.SetText(">")
            if self.typeBar:
                self.typeBar.SetSize(3, self.bg.GetHeight() if self.bg else 29)
            # Nascondi tooltip
            if self.type_flag == 0:
                tt = getattr(self, '_toolTipRef', None)
                if tt:
                    try:
                        tt.HideToolTip()
                    except:
                        pass

        def __del__(self):
            self._toolTipRef = None
            ui.ListBoxEx.Item.__del__(self)

    # ================================================================
    #  __init__
    # ================================================================
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.isLoaded = False
        self.isDestroyed = False
        self.currentCategory = "BOSS"

        # Fade animation
        self.fadeAlpha = 0.0
        self.isFading = False

        # Item grid state
        self.gridData = []
        self.gridOffset = 0
        self._listViewCount = 18
        self._dropViewCount = 7
        self._slotToDataIdx = {}
        self._gridPageItems = MAX_GRID_SIZE
        self._curSlotH = 32
        self._curGridRows = MAX_GRID_ROWS
        self._curGridSize = MAX_GRID_COLS * MAX_GRID_ROWS

        # References UI (initialized to None for safe cleanup)
        self.board = None
        self.titleText = None
        self.btnClose = None
        self.sidebar = None
        self.catButtons = []
        self.searchBg = None
        self.searchInput = None
        self.btnClear = None
        self.btnSearch = None
        self.noResultLabel = None
        self.listBg = None
        self.listBox = None
        self.scrollBar = None
        self.itemGrid = None
        self.gridContainer = None
        self.fadeCover = None
        self.renderTargetWnd = None
        self.detailBg = None
        self.infoLabel = None
        self.infoSubLabel = None
        self.dropList = None
        self.dropScrollBar = None
        self.upgradeTableBtn = None
        self.toolTip = None
        self.refinePopup = None
        self.statusLabel = None
        self.statMobText = None
        self.statItemText = None
        self.statDropText = None
        self.statRefineText = None
        self.statChestText = None

        # Navigation history
        self._navStack = []
        self._lastSearchText = ""
        self._searchTimer = 0
        self._currentDetailVnum = 0
        self._currentDetailType = -1
        self._upgradeTableVnum = 0

        # Additional UI refs
        self.previewNameLabel = None
        self.previewSubLabel = None
        self.detailHeaderLabel = None
        self.btnBack = None



        # Item preview overlay (replaces 3D when viewing items)
        self.itemPreviewPanel = None
        self.itemPreviewIcon = None
        self.itemPreviewName = None
        self.itemPreviewType = None
        self.itemPreviewSep = None
        self.itemPreviewOriginTitle = None
        self.itemPreviewSep2 = None
        self.itemPreviewUpgradeText = None
        self.itemPreviewUpgradeCost = None
        self._itemPreviewInfoLines = []
        self._previewIconVnum = 0

        # Pools for borders/bars
        self._allBars = []
        self._allTexts = []

        self.LoadWindow()

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    # ================================================================
    #  DESTROY - Pulizia rigorosa anti-memory-leak
    # ================================================================
    def Destroy(self):
        """Pulizia completa di tutti i widget - Pattern hunter_effects.py"""
        if self.isDestroyed:
            return
        self.isDestroyed = True
        self.Hide()

        # Nascondi tooltip
        if self.toolTip:
            try:
                self.toolTip.HideToolTip()
                self.toolTip.Hide()
            except:
                pass
            self.toolTip = None

        # Distruggi RefinePopup correttamente
        if self.refinePopup:
            try:
                self.refinePopup.Destroy()
            except:
                pass
            self.refinePopup = None

        # RenderTarget cleanup
        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
        except:
            pass

        # FIX M2: Svuota le listbox PRIMA di distruggerle, per rilasciare i ListItem children
        for lb in (getattr(self, 'listBox', None), getattr(self, 'dropList', None)):
            if lb:
                try:
                    lb.RemoveAllItems()
                except:
                    pass

        # Pulizia cat buttons
        for i in xrange(len(self.catButtons)):
            try:
                btn_tuple = self.catButtons[i]
                btn = btn_tuple[0] if isinstance(btn_tuple, tuple) else btn_tuple
                if btn:
                    btn.Hide()
                self.catButtons[i] = None
            except:
                pass
        del self.catButtons[:]
        self.catButtons = []

        # Pulizia bars pool
        for i in xrange(len(self._allBars)):
            try:
                b = self._allBars[i]
                if b:
                    b.Hide()
                self._allBars[i] = None
            except:
                pass
        del self._allBars[:]
        self._allBars = []

        # Pulizia texts pool
        for i in xrange(len(self._allTexts)):
            try:
                t = self._allTexts[i]
                if t:
                    t.Hide()
                self._allTexts[i] = None
            except:
                pass
        del self._allTexts[:]
        self._allTexts = []

        # Pulizia singoli widget
        widgetNames = [
            "board", "titleText", "btnClose", "btnCloseBg", "btnCloseText", "sidebar",
            "searchBg", "searchInput", "btnClear", "btnSearch",
            "searchIcon", "searchPlaceholder",
            "noResultLabel", "listBg", "listBox", "scrollBar",
            "itemGrid", "gridContainer", "fadeCover", "renderTargetWnd",
            "detailBg", "infoLabel", "infoSubLabel",
            "dropList", "dropScrollBar", "upgradeTableBtn", "statusLabel",
            "statMobText", "statItemText", "statDropText", "statRefineText", "statChestText",
            "previewNameLabel", "previewSubLabel", "detailHeaderLabel", "btnBack",
            "refinePopup",
            "itemPreviewPanel", "itemPreviewIcon",
            "itemPreviewName", "itemPreviewType",
            "itemPreviewSep", "itemPreviewOriginTitle",
            "itemPreviewSep2", "itemPreviewUpgradeText", "itemPreviewUpgradeCost",
        ]
        for name in widgetNames:
            wnd = getattr(self, name, None)
            if wnd:
                try:
                    wnd.Hide()
                except:
                    pass
                setattr(self, name, None)

        self.gridData = []
        self.gridOffset = 0
        self._slotToDataIdx = {}
        self._gridPageItems = MAX_GRID_SIZE
        self._curSlotH = 32
        self._curGridRows = MAX_GRID_ROWS
        self._curGridSize = MAX_GRID_COLS * MAX_GRID_ROWS
        self._navStack = []
        self._lastSearchText = ""
        self._searchTimer = 0
        self._currentDetailVnum = 0
        self._currentDetailType = -1
        self._previewIconVnum = 0
        self._upgradeTableVnum = 0

        # Cleanup upgrade table button children
        for attr in ("_utBtnBg", "_utAcL", "_utAcR", "_utTpL", "_utBtL", "_utText"):
            wnd = getattr(self, attr, None)
            if wnd:
                try:
                    wnd.Hide()
                except:
                    pass
                setattr(self, attr, None)

        for i in xrange(len(self._itemPreviewInfoLines)):
            try:
                self._itemPreviewInfoLines[i].Hide()
            except:
                pass
            self._itemPreviewInfoLines[i] = None
        self._itemPreviewInfoLines = []

        self.ClearDictionary()
        self.isLoaded = False

    # ================================================================
    #  LOAD WINDOW
    # ================================================================
    def LoadWindow(self):
        if self.isLoaded:
            return True
        try:
            self.__BuildInterface()
        except Exception as e:
            dbg.TraceError("WikiWindow.LoadWindow FAIL: %s" % str(e))
            return False

        self.isLoaded = True
        self.isDestroyed = False

        # Carica dati
        DATA_MGR.LoadData()

        # Aggiorna stats sidebar
        self.__RefreshSidebarStats()

        # Ricerca iniziale
        self.__DoSearch()
        self.__UpdateCategoryButtons()
        return True

    # ================================================================
    #  BUILD INTERFACE PRINCIPALE
    # ================================================================
    def __BuildInterface(self):
        self.SetSize(WIN_WIDTH, WIN_HEIGHT)
        self.SetCenterPosition()
        self.AddFlag("movable")
        self.AddFlag("float")

        # === SFONDO PRINCIPALE ===
        self.board = ui.Bar()
        self.board.SetParent(self)
        self.board.SetPosition(0, 0)
        self.board.SetSize(WIN_WIDTH, WIN_HEIGHT)
        self.board.SetColor(COLOR_BG_MAIN)
        self.board.AddFlag("not_pick")
        self.board.Show()

        # Inner depth layer
        boardInner = ui.Bar()
        boardInner.SetParent(self)
        boardInner.SetPosition(3, 3)
        boardInner.SetSize(WIN_WIDTH - 6, WIN_HEIGHT - 6)
        boardInner.SetColor(0x060808FF)
        boardInner.AddFlag("not_pick")
        boardInner.Show()
        self._allBars.append(boardInner)

        # Top highlight gradient sottile
        topHL = ui.Bar()
        topHL.SetParent(self)
        topHL.SetPosition(3, 3)
        topHL.SetSize(WIN_WIDTH - 6, 12)
        topHL.SetColor(0x0EFFFFFF)
        topHL.AddFlag("not_pick")
        topHL.Show()
        self._allBars.append(topHL)

        # Bordi principali asimmetrici: top 3px, left 3px, bottom 2px, right 2px
        bTop = ui.Bar(); bTop.SetParent(self); bTop.SetPosition(0,0); bTop.SetSize(WIN_WIDTH,3); bTop.SetColor(COLOR_BORDER); bTop.AddFlag("not_pick"); bTop.Show()
        bLeft = ui.Bar(); bLeft.SetParent(self); bLeft.SetPosition(0,0); bLeft.SetSize(3,WIN_HEIGHT); bLeft.SetColor(COLOR_BORDER); bLeft.AddFlag("not_pick"); bLeft.Show()
        bBot = ui.Bar(); bBot.SetParent(self); bBot.SetPosition(0,WIN_HEIGHT-2); bBot.SetSize(WIN_WIDTH,2); bBot.SetColor(COLOR_BORDER_DIM); bBot.AddFlag("not_pick"); bBot.Show()
        bRight = ui.Bar(); bRight.SetParent(self); bRight.SetPosition(WIN_WIDTH-2,0); bRight.SetSize(2,WIN_HEIGHT); bRight.SetColor(COLOR_BORDER_DIM); bRight.AddFlag("not_pick"); bRight.Show()
        self._allBars.extend([bTop, bLeft, bBot, bRight])

        # Bordo interno dim (offset 4)
        bTop2 = ui.Bar(); bTop2.SetParent(self); bTop2.SetPosition(4,4); bTop2.SetSize(WIN_WIDTH-8,1); bTop2.SetColor(COLOR_BORDER_DIM); bTop2.AddFlag("not_pick"); bTop2.Show()
        bLeft2 = ui.Bar(); bLeft2.SetParent(self); bLeft2.SetPosition(4,4); bLeft2.SetSize(1,WIN_HEIGHT-8); bLeft2.SetColor(COLOR_BORDER_DIM); bLeft2.AddFlag("not_pick"); bLeft2.Show()
        self._allBars.extend([bTop2, bLeft2])

        # Corner L-bracket outer (30px) + inner (14px offset 6)
        CORNER_OUTER = 30
        CORNER_INNER = 14
        INNER_OFF = 6
        for (cx, cy, cw, ch, col) in [
            # Outer TL H+V
            (3, 3, CORNER_OUTER, 3, COLOR_BORDER), (3, 3, 3, CORNER_OUTER, COLOR_BORDER),
            # Outer TR H+V
            (WIN_WIDTH-3-CORNER_OUTER, 3, CORNER_OUTER, 3, COLOR_BORDER), (WIN_WIDTH-3, 3, 3, CORNER_OUTER, COLOR_BORDER),
            # Outer BL H+V
            (3, WIN_HEIGHT-3, CORNER_OUTER, 3, COLOR_BORDER), (3, WIN_HEIGHT-3-CORNER_OUTER, 3, CORNER_OUTER, COLOR_BORDER),
            # Outer BR H+V
            (WIN_WIDTH-3-CORNER_OUTER, WIN_HEIGHT-3, CORNER_OUTER, 3, COLOR_BORDER), (WIN_WIDTH-3, WIN_HEIGHT-3-CORNER_OUTER, 3, CORNER_OUTER, COLOR_BORDER),
            # Inner TL H+V
            (3+INNER_OFF, 3+INNER_OFF, CORNER_INNER, 1, COLOR_BORDER_DIM), (3+INNER_OFF, 3+INNER_OFF, 1, CORNER_INNER, COLOR_BORDER_DIM),
            # Inner TR H+V
            (WIN_WIDTH-3-INNER_OFF-CORNER_INNER, 3+INNER_OFF, CORNER_INNER, 1, COLOR_BORDER_DIM), (WIN_WIDTH-3-INNER_OFF, 3+INNER_OFF, 1, CORNER_INNER, COLOR_BORDER_DIM),
            # Inner BL H+V
            (3+INNER_OFF, WIN_HEIGHT-3-INNER_OFF, CORNER_INNER, 1, COLOR_BORDER_DIM), (3+INNER_OFF, WIN_HEIGHT-3-INNER_OFF-CORNER_INNER, 1, CORNER_INNER, COLOR_BORDER_DIM),
            # Inner BR H+V
            (WIN_WIDTH-3-INNER_OFF-CORNER_INNER, WIN_HEIGHT-3-INNER_OFF, CORNER_INNER, 1, COLOR_BORDER_DIM), (WIN_WIDTH-3-INNER_OFF, WIN_HEIGHT-3-INNER_OFF-CORNER_INNER, 1, CORNER_INNER, COLOR_BORDER_DIM),
        ]:
            ct = ui.Bar(); ct.SetParent(self); ct.SetPosition(cx, cy); ct.SetSize(cw, ch)
            ct.SetColor(col); ct.AddFlag("not_pick"); ct.Show()
            self._allBars.append(ct)

        # Header bar (drag handle) - NON not_pick per permettere il drag
        headerBar = ui.Bar()
        headerBar.SetParent(self)
        headerBar.SetPosition(3, 3)
        headerBar.SetSize(WIN_WIDTH - 6, 34)
        headerBar.SetColor(COLOR_BG_HEADER)
        headerBar.AddFlag("not_pick")
        headerBar.Show()
        self._allBars.append(headerBar)

        # Accent bar sinistra nel header (4px, oro)
        headerAccent = ui.Bar()
        headerAccent.SetParent(self)
        headerAccent.SetPosition(3, 3)
        headerAccent.SetSize(4, 34)
        headerAccent.SetColor(COLOR_BORDER)
        headerAccent.AddFlag("not_pick")
        headerAccent.Show()
        self._allBars.append(headerAccent)

        # Separatore sotto header
        headerSep = ui.Bar()
        headerSep.SetParent(self)
        headerSep.SetPosition(10, 37)
        headerSep.SetSize(WIN_WIDTH - 20, 1)
        headerSep.SetColor(0x55FFD700)
        headerSep.AddFlag("not_pick")
        headerSep.Show()
        self._allBars.append(headerSep)

        # Titolo
        self.titleText = self.__Text(self, WIN_WIDTH // 2, 11,
                                      "WIKI HUNTER - ENCYCLOPEDIA", COLOR_TEXT_GOLD, center=True, outline=True)

        # Label header sinistra "[ WIKI ]"
        self.__Text(self, 20, 11, "[ WIKI ]", COLOR_BORDER_DIM)

        # Bottone chiudi (X) - piu' elaborato
        self.btnClose = ui.Window()
        self.btnClose.SetParent(self)
        self.btnClose.SetPosition(WIN_WIDTH - 34, 5)
        self.btnClose.SetSize(28, 26)

        self.btnCloseBg = ui.Bar()
        self.btnCloseBg.SetParent(self.btnClose)
        self.btnCloseBg.SetPosition(0, 0)
        self.btnCloseBg.SetSize(28, 26)
        self.btnCloseBg.SetColor(0xCC080004)
        self.btnCloseBg.AddFlag("not_pick")
        self.btnCloseBg.Show()

        # Bordo top rosso del tasto X
        btnTopBorder = ui.Bar()
        btnTopBorder.SetParent(self.btnClose)
        btnTopBorder.SetPosition(0, 0)
        btnTopBorder.SetSize(28, 2)
        btnTopBorder.SetColor(0xFFFF2222)
        btnTopBorder.AddFlag("not_pick")
        btnTopBorder.Show()

        self.btnCloseText = ui.TextLine()
        self.btnCloseText.SetParent(self.btnClose)
        self.btnCloseText.SetPosition(14, 5)
        self.btnCloseText.SetHorizontalAlignCenter()
        self.btnCloseText.SetText("X")
        self.btnCloseText.SetPackedFontColor(0xFFFF4444)
        self.btnCloseText.AddFlag("not_pick")
        self.btnCloseText.Show()

        self.btnClose.OnMouseLeftButtonUp = lambda: self.Close()
        self.btnClose.Show()

        # === BUILD TUTTE LE SEZIONI ===
        self.__BuildSidebar()
        self.__BuildSearchArea()
        self.__BuildResultList()
        self.__BuildPreview()
        self.__BuildDetailArea()

        # === STATUS BAR ===
        self.statusLabel = self.__Text(self, 10, WIN_HEIGHT - 16,
                                        "Pronto", COLOR_TEXT_DARK)

    # ================================================================
    #  SIDEBAR
    # ================================================================
    def __BuildSidebar(self):
        sideX = 8
        sideY = 40
        sideH = WIN_HEIGHT - 50

        self.sidebar = self.__Bar(self, sideX, sideY, SIDEBAR_WIDTH, sideH, COLOR_BG_PANEL)
        self.__MakeBorder(self, sideX, sideY, SIDEBAR_WIDTH, sideH, COLOR_BORDER_DIM)

        # Accent bar sinistra della sidebar (3px, oro dim)
        self.__Bar(self, sideX, sideY, 3, sideH, COLOR_BORDER_DIM)

        # Top highlight della sidebar
        self.__Bar(self, sideX+3, sideY, SIDEBAR_WIDTH-3, 6, 0x0AFFFFFF)

        # Titolo sidebar
        self.__Text(self, sideX + SIDEBAR_WIDTH // 2, sideY + 9,
                    "CATEGORIE", COLOR_TEXT_GOLD, center=True)
        self.__Bar(self, sideX + 8, sideY + 28, SIDEBAR_WIDTH - 16, 1, COLOR_SEPARATOR)

        # Bottoni categoria - Mob
        btnY = sideY + 35
        self.catButtons = []
        for label, code in CATEGORIES_MOB:
            btn = self.__CreateCatButton(sideX + 8, btnY, SIDEBAR_WIDTH - 16, 28, label, code)
            self.catButtons.append((btn, code))
            btnY += 34

        # Separatore visivo tra mob e item
        self.__Bar(self, sideX + 10, btnY + 2, SIDEBAR_WIDTH - 20, 1, COLOR_SEPARATOR)
        self.__Text(self, sideX + SIDEBAR_WIDTH // 2, btnY + 6,
                    "OGGETTI", COLOR_TEXT_GRAY, center=True)
        btnY += 24

        # Bottoni categoria - Item
        for label, code in CATEGORIES_ITEM:
            btn = self.__CreateCatButton(sideX + 8, btnY, SIDEBAR_WIDTH - 16, 28, label, code)
            self.catButtons.append((btn, code))
            btnY += 34

        # Separatore Fratture
        self.__Bar(self, sideX + 10, btnY + 2, SIDEBAR_WIDTH - 20, 1, COLOR_SEPARATOR)
        self.__Text(self, sideX + SIDEBAR_WIDTH // 2, btnY + 6,
                    "FRATTURE", 0xFF00DDFF, center=True)
        btnY += 24

        # Bottoni categoria - Fratture
        for label, code in CATEGORIES_FRACTURE:
            btn = self.__CreateCatButton(sideX + 8, btnY, SIDEBAR_WIDTH - 16, 28, label, code)
            self.catButtons.append((btn, code))
            btnY += 34

        # Separatore
        self.__Bar(self, sideX + 10, btnY + 5, SIDEBAR_WIDTH - 20, 1, COLOR_SEPARATOR)

        # Info stats (aggiornate dopo il caricamento dati)
        infoY = btnY + 15
        self.__Text(self, sideX + 10, infoY, "Statistiche:", COLOR_TEXT_GRAY)
        infoY += 18
        self.statMobText = self.__Text(self, sideX + 10, infoY, "Mob: ...", COLOR_TEXT_DARK)
        infoY += 15
        self.statItemText = self.__Text(self, sideX + 10, infoY, "Items: ...", COLOR_TEXT_DARK)
        infoY += 15
        self.statDropText = self.__Text(self, sideX + 10, infoY, "Drop: ...", COLOR_TEXT_DARK)
        infoY += 15
        self.statRefineText = self.__Text(self, sideX + 10, infoY, "Refine: ...", COLOR_TEXT_DARK)
        infoY += 15
        self.statChestText = self.__Text(self, sideX + 10, infoY, "Forzieri: ...", COLOR_TEXT_DARK)

    def __CreateCatButton(self, x, y, w, h, label, code):
        """Crea un bottone categoria stile Solo Leveling con accent bar sinistra."""
        btn = ui.Window()
        btn.SetParent(self)
        btn.SetPosition(x, y)
        btn.SetSize(w, h)

        btn.bg = ui.Bar()
        btn.bg.SetParent(btn)
        btn.bg.SetPosition(0, 0)
        btn.bg.SetSize(w, h)
        btn.bg.SetColor(COLOR_BTN_NORMAL)
        btn.bg.AddFlag("not_pick")
        btn.bg.Show()

        # Accent bar sinistra (3px, oro)
        btn.accentL = ui.Bar()
        btn.accentL.SetParent(btn)
        btn.accentL.SetPosition(0, 0)
        btn.accentL.SetSize(3, h)
        btn.accentL.SetColor(0xFF554400)
        btn.accentL.AddFlag("not_pick")
        btn.accentL.Show()

        # Top highlight
        btn.topHL = ui.Bar()
        btn.topHL.SetParent(btn)
        btn.topHL.SetPosition(3, 0)
        btn.topHL.SetSize(w - 3, 4)
        btn.topHL.SetColor(0x0AFFFFFF)
        btn.topHL.AddFlag("not_pick")
        btn.topHL.Show()

        self.__MakeBorderOn(btn, 0, 0, w, h, COLOR_BTN_BORDER)

        btn.textLine = ui.TextLine()
        btn.textLine.SetParent(btn)
        btn.textLine.SetPosition(w // 2 + 2, (h - 14) // 2)
        btn.textLine.SetHorizontalAlignCenter()
        btn.textLine.SetText(label)
        btn.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
        btn.textLine.SetOutline()
        btn.textLine.AddFlag("not_pick")
        btn.textLine.Show()

        btn.code = code
        btn.OnMouseLeftButtonUp = lambda: self.__OnCatClick(code)
        btn.OnMouseOverIn = lambda: self.__OnCatHover(btn, True)
        btn.OnMouseOverOut = lambda: self.__OnCatHover(btn, False)

        btn.Show()
        return btn

    def __OnCatClick(self, code):
        if self.currentCategory == code:
            return
        self.currentCategory = code
        self.__UpdateCategoryButtons()
        self.searchInput.SetText("")
        self.scrollBar.SetPos(0.0)

        # Chiudi popup refine se aperto
        if self.refinePopup:
            self.refinePopup.Close()

        # Reset pannello dettagli quando si cambia categoria
        self.__ResetDetailArea()

        # Fade
        self.fadeAlpha = 1.0
        self.isFading = True
        if self.fadeCover:
            self.fadeCover.SetColor(0xFF000000)
            self.fadeCover.Show()

        self.__DoSearch()

    def __OnCatHover(self, btn, isOver):
        code = btn.code
        if code == self.currentCategory:
            return
        if isOver:
            btn.bg.SetColor(COLOR_BTN_HOVER)
            if hasattr(btn, "accentL"):
                btn.accentL.SetColor(0xFFAA7700)
        else:
            btn.bg.SetColor(COLOR_BTN_NORMAL)
            if hasattr(btn, "accentL"):
                btn.accentL.SetColor(0xFF554400)

    def __UpdateCategoryButtons(self):
        """Aggiorna l'aspetto dei bottoni categoria."""
        for (btn, code) in self.catButtons:
            if code == self.currentCategory:
                btn.bg.SetColor(COLOR_BTN_ACTIVE)
                btn.textLine.SetPackedFontColor(COLOR_TEXT_GOLD)
                if hasattr(btn, "accentL"):
                    btn.accentL.SetColor(COLOR_BORDER)  # Oro pieno = attivo
            else:
                btn.bg.SetColor(COLOR_BTN_NORMAL)
                btn.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
                if hasattr(btn, "accentL"):
                    btn.accentL.SetColor(0xFF554400)  # Oro scuro = inattivo

    # ================================================================
    #  SEARCH AREA
    # ================================================================
    def __BuildSearchArea(self):
        searchX = SIDEBAR_WIDTH + 18
        searchY = 40
        searchW = LIST_WIDTH

        self.searchBg = self.__Bar(self, searchX, searchY, searchW, SEARCH_HEIGHT, COLOR_BG_PANEL)
        self.__MakeBorder(self, searchX, searchY, searchW, SEARCH_HEIGHT, COLOR_BORDER_DIM)

        # Icona lente di ricerca
        self.searchIcon = ui.TextLine()
        self.searchIcon.SetParent(self)
        self.searchIcon.SetPosition(searchX + 6, searchY + 7)
        self.searchIcon.SetText("Q")
        self.searchIcon.SetPackedFontColor(0xFF666688)
        self.searchIcon.AddFlag("not_pick")
        self.searchIcon.Show()

        self.searchInput = ui.EditLine()
        self.searchInput.SetParent(self)
        self.searchInput.SetPosition(searchX + 20, searchY + 8)
        self.searchInput.SetSize(searchW - 67, 14)
        self.searchInput.SetMax(30)
        self.searchInput.SetText("")
        self.searchInput.SetReturnEvent(ui.__mem_func__(self.__DoSearch))
        self.searchInput.Show()

        # Placeholder/hint text "Cerca un oggetto..."
        self.searchPlaceholder = ui.TextLine()
        self.searchPlaceholder.SetParent(self)
        self.searchPlaceholder.SetPosition(searchX + 22, searchY + 8)
        self.searchPlaceholder.SetText("Cerca un oggetto...")
        self.searchPlaceholder.SetPackedFontColor(0xFF555566)
        self.searchPlaceholder.AddFlag("not_pick")
        self.searchPlaceholder.Show()

        # Bottone X (clear)
        self.btnClear = self.__CreateSmallBtn(self, searchX + searchW - 44, searchY + 4, 20, 22, "X")
        self.btnClear.OnMouseLeftButtonUp = lambda: self.__OnClearSearch()

        # Bottone cerca
        self.btnSearch = self.__CreateSmallBtn(self, searchX + searchW - 22, searchY + 4, 20, 22, ">")
        self.btnSearch.OnMouseLeftButtonUp = lambda: self.__DoSearch()

        # Label "nessun risultato"
        self.noResultLabel = self.__Text(self, searchX + searchW // 2, searchY + SEARCH_HEIGHT + LIST_HEIGHT // 2,
                                          "Nessun risultato trovato", COLOR_NO_RESULT, center=True)
        self.noResultLabel.Hide()

    def __CreateSmallBtn(self, parent, x, y, w, h, text):
        btn = ui.Window()
        btn.SetParent(parent)
        btn.SetPosition(x, y)
        btn.SetSize(w, h)

        btn.bg = ui.Bar()
        btn.bg.SetParent(btn)
        btn.bg.SetPosition(0, 0)
        btn.bg.SetSize(w, h)
        btn.bg.SetColor(COLOR_BTN_NORMAL)
        btn.bg.AddFlag("not_pick")
        btn.bg.Show()

        btn.text = ui.TextLine()
        btn.text.SetParent(btn)
        btn.text.SetPosition(w // 2, (h - 14) // 2)
        btn.text.SetHorizontalAlignCenter()
        btn.text.SetText(text)
        btn.text.SetPackedFontColor(COLOR_TEXT_LIGHT)
        btn.text.AddFlag("not_pick")
        btn.text.Show()

        btn.Show()
        return btn

    def __OnClearSearch(self):
        self.searchInput.SetText("")
        if hasattr(self, 'searchPlaceholder') and self.searchPlaceholder:
            self.searchPlaceholder.Show()
        self.__DoSearch()

    # ================================================================
    #  RESULT LIST (Mob) + GRID (Items)
    # ================================================================
    def __BuildResultList(self):
        listX = SIDEBAR_WIDTH + 18
        listY = 40 + SEARCH_HEIGHT + 4
        listW = LIST_WIDTH
        listH = LIST_HEIGHT

        self.listBg = self.__Bar(self, listX, listY, listW, listH, COLOR_BG_PANEL)
        self.__MakeBorder(self, listX, listY, listW, listH, COLOR_BORDER_DIM)

        innerW = listW - 10
        innerH = listH - 10
        viewCount = max(1, innerH // 28)
        self._listViewCount = viewCount

        # ListBox per mob
        self.listBox = ui.ListBoxEx()
        self.listBox.SetParent(self)
        self.listBox.SetPosition(listX + 5, listY + 5)
        # IMPORTANTE: SetViewItemCount PRIMA di SetItemSize/SetItemStep!
        # SetItemSize e SetItemStep chiamano __UpdateSize() internamente
        # che calcola height = itemStep * viewItemCount. Se viewItemCount
        # e' ancora il default (10), l'area cliccabile diventa solo 10*28=280px
        # e gli item sotto la meta' della lista non ricevono click.
        self.listBox.SetViewItemCount(viewCount)
        self.listBox.SetItemSize(innerW, 28)
        self.listBox.SetItemStep(28)
        self.listBox.SetSelectEvent(self.__OnSelectListItem)
        self.listBox.Show()

        # ScrollBar
        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetPosition(listX + listW, listY)
        self.scrollBar.SetScrollBarSize(listH)
        self.scrollBar.SetScrollEvent(self.__OnScroll)
        self.scrollBar.Show()
        # NON fare SetScrollBar sul listbox - gestione manuale in __OnScroll
        # per supportare sia listBox (mob) che gridContainer (items)

        # Container per grid items - Il GridSlotWindow a livello C++ intercetta
        # click anche se nascosto. Soluzione: svuotare gli slot E spostare
        # off-screen quando si passa in modalita' lista mob.
        self.gridContainer = ui.Window()
        self.gridContainer.SetParent(self)
        self.gridContainer.SetPosition(-5000, -5000)
        self.gridContainer.SetSize(innerW, innerH)
        self.gridContainer.Hide()

        # Grid per items (child del container)
        self.itemGrid = ui.GridSlotWindow()
        self.itemGrid.SetParent(self.gridContainer)
        self.itemGrid.SetPosition(0, 0)
        self._curSlotH = 32
        self._curGridRows = MAX_GRID_ROWS
        self._curGridSize = MAX_GRID_COLS * MAX_GRID_ROWS
        self.itemGrid.ArrangeSlot(0, MAX_GRID_COLS, MAX_GRID_ROWS, 32, 32, 4, 4)
        self.itemGrid.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
        self.itemGrid.SetOverInItemEvent(self.__OnGridOverIn)
        self.itemGrid.SetOverOutItemEvent(self.__OnGridOverOut)
        self.itemGrid.SetSelectItemSlotEvent(self.__OnGridSelect)
        self.itemGrid.Show()

        # Fade cover
        self.fadeCover = ui.Bar()
        self.fadeCover.SetParent(self)
        self.fadeCover.SetPosition(listX + 3, listY + 3)
        self.fadeCover.SetSize(listW - 6, listH - 6)
        self.fadeCover.SetColor(0xFF000000)
        self.fadeCover.AddFlag("not_pick")
        self.fadeCover.Hide()

    # ================================================================
    #  PREVIEW 3D
    # ================================================================
    def __BuildPreview(self):
        prevX = RIGHT_X
        prevY = 40
        prevW = RIGHT_W
        prevH = PREVIEW_HEIGHT

        self.__Bar(self, prevX, prevY, prevW, prevH, COLOR_BG_PANEL)
        self.__MakeBorder(self, prevX, prevY, prevW, prevH, COLOR_BORDER_DIM)

        # === 3D RENDER TARGET ===
        rtX = prevX + 3
        rtY = prevY + 3
        rtW = prevW - 6
        rtH = prevH - 6

        self.renderTargetWnd = ui.RenderTarget()
        self.renderTargetWnd.SetParent(self)
        self.renderTargetWnd.SetPosition(rtX, rtY)
        self.renderTargetWnd.SetSize(rtW, rtH)
        self.renderTargetWnd.SetRenderTarget(RENDER_TARGET_INDEX)
        self.renderTargetWnd.Show()

        try:
            renderTarget.SetBackground(RENDER_TARGET_INDEX,
                                        "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
        except:
            pass

        # Label "Preview 3D" centered in preview
        self.__Text(self, prevX + prevW // 2, prevY + prevH - 18,
                    "Preview 3D", COLOR_TEXT_DARK, center=True)

        # Nome mob nel preview (aggiornato dinamicamente)
        self.previewNameLabel = self.__Text(self, prevX + prevW // 2, prevY + 6,
                                             "", COLOR_TEXT_GOLD, center=True, outline=True)

        # Sotto-info mob (grado, livello, HP - aggiornate dinamicamente)
        self.previewSubLabel = self.__Text(self, prevX + prevW // 2, prevY + 22,
                                            "", COLOR_TEXT_GRAY, center=True)

        # === ITEM PREVIEW OVERLAY (per items - sovrapposto al 3D) ===
        self.itemPreviewPanel = ui.Bar()
        self.itemPreviewPanel.SetParent(self)
        self.itemPreviewPanel.SetPosition(prevX + 3, prevY + 3)
        self.itemPreviewPanel.SetSize(prevW - 6, prevH - 6)
        self.itemPreviewPanel.SetColor(COLOR_BG_PANEL)
        self.itemPreviewPanel.Hide()

        ipW = prevW - 6
        ipH = prevH - 6

        # Icona item (slot centrato in alto - ricreato dinamicamente in __ShowItemPreview)
        self.itemPreviewIcon = ui.GridSlotWindow()
        self.itemPreviewIcon.SetParent(self.itemPreviewPanel)
        self.itemPreviewIcon.SetPosition((ipW - 32) // 2, 8)
        self.itemPreviewIcon.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
        self.itemPreviewIcon.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
        self.itemPreviewIcon.SetOverInItemEvent(self.__OnPreviewIconOverIn)
        self.itemPreviewIcon.SetOverOutItemEvent(self.__OnPreviewIconOverOut)
        self.itemPreviewIcon.Show()
        self._previewIconVnum = 0
        self._previewSlotH = 3  # altezza corrente in slot (default 3)

        # Nome item (posizione dinamica, aggiornata in __ShowItemPreview)
        self.itemPreviewName = ui.TextLine()
        self.itemPreviewName.SetParent(self.itemPreviewPanel)
        self.itemPreviewName.SetPosition(ipW // 2, 108)
        self.itemPreviewName.SetHorizontalAlignCenter()
        self.itemPreviewName.SetText("")
        self.itemPreviewName.SetPackedFontColor(COLOR_TEXT_GOLD)
        self.itemPreviewName.SetOutline()
        self.itemPreviewName.AddFlag("not_pick")
        self.itemPreviewName.Show()

        # Tipo item
        self.itemPreviewType = ui.TextLine()
        self.itemPreviewType.SetParent(self.itemPreviewPanel)
        self.itemPreviewType.SetPosition(ipW // 2, 124)
        self.itemPreviewType.SetHorizontalAlignCenter()
        self.itemPreviewType.SetText("")
        self.itemPreviewType.SetPackedFontColor(COLOR_TEXT_GRAY)
        self.itemPreviewType.AddFlag("not_pick")
        self.itemPreviewType.Show()

        # Separatore
        self.itemPreviewSep = ui.Bar()
        self.itemPreviewSep.SetParent(self.itemPreviewPanel)
        self.itemPreviewSep.SetPosition(20, 142)
        self.itemPreviewSep.SetSize(ipW - 40, 1)
        self.itemPreviewSep.SetColor(COLOR_SEPARATOR)
        self.itemPreviewSep.AddFlag("not_pick")
        self.itemPreviewSep.Show()

        # Titolo origini
        self.itemPreviewOriginTitle = ui.TextLine()
        self.itemPreviewOriginTitle.SetParent(self.itemPreviewPanel)
        self.itemPreviewOriginTitle.SetPosition(ipW // 2, 148)
        self.itemPreviewOriginTitle.SetHorizontalAlignCenter()
        self.itemPreviewOriginTitle.SetText("")
        self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_CYAN)
        self.itemPreviewOriginTitle.AddFlag("not_pick")
        self.itemPreviewOriginTitle.Show()

        # Righe info item (bonus, vnum, stats) - 6 righe multiuso
        self._itemPreviewInfoLines = []
        for i in xrange(6):
            t = ui.TextLine()
            t.SetParent(self.itemPreviewPanel)
            t.SetPosition(ipW // 2, 166 + i * 14)
            t.SetHorizontalAlignCenter()
            t.SetText("")
            t.SetPackedFontColor(COLOR_TEXT_LIGHT)
            t.AddFlag("not_pick")
            t.Show()
            self._itemPreviewInfoLines.append(t)

        # Separatore 2 (per sezione upgrade)
        self.itemPreviewSep2 = ui.Bar()
        self.itemPreviewSep2.SetParent(self.itemPreviewPanel)
        self.itemPreviewSep2.SetPosition(20, 226)
        self.itemPreviewSep2.SetSize(ipW - 40, 1)
        self.itemPreviewSep2.SetColor(COLOR_SEPARATOR)
        self.itemPreviewSep2.AddFlag("not_pick")
        self.itemPreviewSep2.Show()

        # Riga upgrade brief
        self.itemPreviewUpgradeText = ui.TextLine()
        self.itemPreviewUpgradeText.SetParent(self.itemPreviewPanel)
        self.itemPreviewUpgradeText.SetPosition(ipW // 2, 232)
        self.itemPreviewUpgradeText.SetHorizontalAlignCenter()
        self.itemPreviewUpgradeText.SetText("")
        self.itemPreviewUpgradeText.SetPackedFontColor(COLOR_TEXT_GREEN)
        self.itemPreviewUpgradeText.AddFlag("not_pick")
        self.itemPreviewUpgradeText.Show()

        # Riga costo upgrade
        self.itemPreviewUpgradeCost = ui.TextLine()
        self.itemPreviewUpgradeCost.SetParent(self.itemPreviewPanel)
        self.itemPreviewUpgradeCost.SetPosition(ipW // 2, 246)
        self.itemPreviewUpgradeCost.SetHorizontalAlignCenter()
        self.itemPreviewUpgradeCost.SetText("")
        self.itemPreviewUpgradeCost.SetPackedFontColor(COLOR_TEXT_GRAY)
        self.itemPreviewUpgradeCost.AddFlag("not_pick")
        self.itemPreviewUpgradeCost.Show()

    # ================================================================
    #  DETAIL AREA
    # ================================================================
    def __BuildDetailArea(self):
        detX = RIGHT_X
        detY = DETAIL_Y
        detW = RIGHT_W
        detH = DETAIL_H

        self.detailBg = self.__Bar(self, detX, detY, detW, detH, COLOR_BG_PANEL)
        self.__MakeBorder(self, detX, detY, detW, detH, COLOR_BORDER_DIM)

        # Header detail area
        self.__Bar(self, detX + 3, detY + 3, detW - 6, 24, COLOR_BG_HEADER)

        # Bottone indietro (nascosto finche' non c'e' cronologia)  --- STILE SOLO LEVELING ---
        backW = 80
        backH = 22
        self.btnBack = ui.Window()
        self.btnBack.SetParent(self)
        self.btnBack.SetPosition(detX + 5, detY + 4)
        self.btnBack.SetSize(backW, backH)

        self.btnBack.border = ui.Bar()
        self.btnBack.border.SetParent(self.btnBack)
        self.btnBack.border.SetPosition(0, 0)
        self.btnBack.border.SetSize(backW, backH)
        self.btnBack.border.SetColor(0xFF00DDFF)
        self.btnBack.border.AddFlag("not_pick")
        self.btnBack.border.Show()

        self.btnBack.bg = ui.Bar()
        self.btnBack.bg.SetParent(self.btnBack)
        self.btnBack.bg.SetPosition(1, 1)
        self.btnBack.bg.SetSize(backW - 2, backH - 2)
        self.btnBack.bg.SetColor(0xEE120820)
        self.btnBack.bg.AddFlag("not_pick")
        self.btnBack.bg.Show()

        # Accent bar sinistra
        self.btnBack.acL = ui.Bar()
        self.btnBack.acL.SetParent(self.btnBack)
        self.btnBack.acL.SetPosition(0, 0)
        self.btnBack.acL.SetSize(3, backH)
        self.btnBack.acL.SetColor(0xFF00DDFF)
        self.btnBack.acL.AddFlag("not_pick")
        self.btnBack.acL.Show()

        self.btnBack.text = ui.TextLine()
        self.btnBack.text.SetParent(self.btnBack)
        self.btnBack.text.SetPosition(backW // 2, 3)
        self.btnBack.text.SetHorizontalAlignCenter()
        self.btnBack.text.SetText("<< Indietro")
        self.btnBack.text.SetPackedFontColor(0xFF00DDFF)
        self.btnBack.text.SetOutline()
        self.btnBack.text.AddFlag("not_pick")
        self.btnBack.text.Show()

        self.btnBack.OnMouseLeftButtonUp = lambda: self.__OnBackClick()
        self.btnBack.OnMouseOverIn = lambda: (self.btnBack.bg.SetColor(0xEE1E1040), self.btnBack.text.SetPackedFontColor(0xFFFFFFFF), self.btnBack.border.SetColor(0xFFFFFFFF)) if self.btnBack and hasattr(self.btnBack, 'bg') else None
        self.btnBack.OnMouseOverOut = lambda: (self.btnBack.bg.SetColor(0xEE120820), self.btnBack.text.SetPackedFontColor(0xFF00DDFF), self.btnBack.border.SetColor(0xFF00DDFF)) if self.btnBack and hasattr(self.btnBack, 'bg') else None
        self.btnBack.Hide()

        # Nome item/mob
        self.infoLabel = self.__Text(self, detX + detW // 2, detY + 7,
                                      "Seleziona un elemento", COLOR_TEXT_GOLD, center=True, outline=True)

        # Sub-label (tipo/livello)
        self.infoSubLabel = self.__Text(self, detX + detW // 2, detY + 30,
                                         "", COLOR_TEXT_GRAY, center=True)

        # Header sezione drop/origini (dinamico)
        self.detailHeaderLabel = self.__Text(self, detX + 10, detY + 46,
                                              "", COLOR_TEXT_CYAN)

        # Drop list (spostata giu' per fare spazio all'header)
        dropY = detY + 62
        dropH = detH - 69
        dropW = DETAIL_ITEM_W

        dropViewCount = max(1, dropH // 30)
        self._dropViewCount = dropViewCount
        dropH = dropViewCount * 30  # Allinea altezza per evitare overlap

        self.dropList = ui.ListBoxEx()
        self.dropList.SetParent(self)
        self.dropList.SetPosition(detX + 5, dropY)
        self.dropList.SetViewItemCount(dropViewCount)
        self.dropList.SetItemSize(dropW, 30)
        self.dropList.SetItemStep(30)
        self.dropList.SetSelectEvent(self.__OnSelectDropItem)
        self.dropList.Show()

        # Drop scrollbar
        self.dropScrollBar = ui.ScrollBar()
        self.dropScrollBar.SetParent(self)
        self.dropScrollBar.SetPosition(detX + detW - 16, dropY)
        self.dropScrollBar.SetScrollBarSize(dropH)
        self.dropScrollBar.SetScrollEvent(self.__OnDropScroll)
        self.dropScrollBar.Show()
        self.dropList.SetScrollBar(self.dropScrollBar)

        # === PULSANTE FISSO UPGRADE TABLE (fuori dalla dropList) ===
        utBtnW = 200
        utBtnH = 30
        utBtnX = detX + (detW - utBtnW) // 2
        utBtnY = dropY + dropH + 2

        self.upgradeTableBtn = ui.Window()
        self.upgradeTableBtn.SetParent(self)
        self.upgradeTableBtn.SetPosition(utBtnX, utBtnY)
        self.upgradeTableBtn.SetSize(utBtnW, utBtnH)

        self._utBtnBg = ui.Bar()
        self._utBtnBg.SetParent(self.upgradeTableBtn)
        self._utBtnBg.SetPosition(0, 0)
        self._utBtnBg.SetSize(utBtnW, utBtnH)
        self._utBtnBg.SetColor(0xEE120820)
        self._utBtnBg.AddFlag("not_pick")
        self._utBtnBg.Show()

        self._utAcL = ui.Bar()
        self._utAcL.SetParent(self.upgradeTableBtn)
        self._utAcL.SetPosition(0, 0)
        self._utAcL.SetSize(3, utBtnH)
        self._utAcL.SetColor(0xFF00DDFF)
        self._utAcL.AddFlag("not_pick")
        self._utAcL.Show()

        self._utAcR = ui.Bar()
        self._utAcR.SetParent(self.upgradeTableBtn)
        self._utAcR.SetPosition(utBtnW - 3, 0)
        self._utAcR.SetSize(3, utBtnH)
        self._utAcR.SetColor(0xFF00DDFF)
        self._utAcR.AddFlag("not_pick")
        self._utAcR.Show()

        self._utTpL = ui.Bar()
        self._utTpL.SetParent(self.upgradeTableBtn)
        self._utTpL.SetPosition(3, 0)
        self._utTpL.SetSize(utBtnW - 6, 1)
        self._utTpL.SetColor(0x6600DDFF)
        self._utTpL.AddFlag("not_pick")
        self._utTpL.Show()

        self._utBtL = ui.Bar()
        self._utBtL.SetParent(self.upgradeTableBtn)
        self._utBtL.SetPosition(3, utBtnH - 1)
        self._utBtL.SetSize(utBtnW - 6, 1)
        self._utBtL.SetColor(0x6600DDFF)
        self._utBtL.AddFlag("not_pick")
        self._utBtL.Show()

        self._utText = ui.TextLine()
        self._utText.SetParent(self.upgradeTableBtn)
        self._utText.SetPosition(utBtnW // 2, 7)
        self._utText.SetHorizontalAlignCenter()
        self._utText.SetText("TABELLA POTENZIAMENTO")
        self._utText.SetPackedFontColor(0xFF00DDFF)
        self._utText.AddFlag("not_pick")
        self._utText.Show()

        def _utHoverIn():
            self._utBtnBg.SetColor(0xEE1E1040)
            self._utAcL.SetColor(0xFFFFFFFF)
            self._utAcR.SetColor(0xFFFFFFFF)
            self._utTpL.SetColor(0xCC00DDFF)
            self._utBtL.SetColor(0xCC00DDFF)
            self._utText.SetPackedFontColor(0xFFFFFFFF)
        def _utHoverOut():
            self._utBtnBg.SetColor(0xEE120820)
            self._utAcL.SetColor(0xFF00DDFF)
            self._utAcR.SetColor(0xFF00DDFF)
            self._utTpL.SetColor(0x6600DDFF)
            self._utBtL.SetColor(0x6600DDFF)
            self._utText.SetPackedFontColor(0xFF00DDFF)

        self.upgradeTableBtn.OnMouseOverIn = _utHoverIn
        self.upgradeTableBtn.OnMouseOverOut = _utHoverOut
        self.upgradeTableBtn.OnMouseLeftButtonUp = lambda: self.__OpenRefinePopup(self._upgradeTableVnum)
        self.upgradeTableBtn.Hide()

    # ================================================================
    #  SEARCH LOGIC
    # ================================================================
    def __DoSearch(self):
        """Esegue la ricerca nella categoria corrente."""
        self.__HideToolTip()
        if not self.searchInput:
            return
        query = self.searchInput.GetText().lower().strip()
        self._lastSearchText = self.searchInput.GetText()
        self._searchTimer = 0
        hasResults = False

        isItemCategory = self.currentCategory == "ITEM" or self.currentCategory.startswith("ITEM_")
        isFractureCategory = self.currentCategory.startswith("FRACT_")

        if isFractureCategory:
            # === FRACTURE LIST MODE ===
            for _si in xrange(self._curGridSize):
                self.itemGrid.SetItemSlot(_si, 0, 0)
            self.itemGrid.RefreshSlot()
            self.gridContainer.SetPosition(-5000, -5000)
            self.gridContainer.Hide()
            self.listBox.RemoveAllItems()
            self.listBox.Show()
            self.scrollBar.SetPos(0.0)

            innerW = LIST_WIDTH - 10
            fractResults = self.__SearchFracture(query, self.currentCategory)
            for (fVnum, fName, fTier, fGloria) in fractResults:
                tierColor = TIER_COLORS.get(fTier, COLOR_TEXT_LIGHT)
                tierName = TIER_NAMES.get(fTier, "")
                rightText = "%s Gloria | %s" % (str(fGloria), tierName)
                self.listBox.AppendItem(
                    self.FractureListItem(fName, fVnum, innerW, fTier, tierColor, rightText, self.currentCategory))
            hasResults = len(fractResults) > 0
            catFractNames = {"FRACT_BOSS": "Boss Frattura", "FRACT_METIN": "Super Metin", "FRACT_CHEST": "Bauli Frattura"}
            self.__UpdateStatus("%s trovati: %d" % (catFractNames.get(self.currentCategory, "Fratture"), len(fractResults)))

        elif isItemCategory:
            # Grid mode
            self.listBox.Hide()
            # Disconnetti scrollbar dalla listbox per gestirla manualmente
            listX = SIDEBAR_WIDTH + 18
            listY = 40 + SEARCH_HEIGHT + 4
            self.gridContainer.SetPosition(listX + 5, listY + 5)
            self.gridContainer.Show()

            itemTypeFilter = None
            if self.currentCategory.startswith("ITEM_"):
                try:
                    itemTypeFilter = int(self.currentCategory.split("_")[1])
                except:
                    pass
            self.gridData = DATA_MGR.SearchItems(query, itemTypeFilter)
            try:
                self.gridData.sort(key=lambda v: v)
            except:
                pass
            self.gridOffset = 0
            self.__RefreshGrid()
            self.scrollBar.SetPos(0.0)
            hasResults = len(self.gridData) > 0

            catSubNames = {"ITEM": "Oggetti", "ITEM_1": "Armi", "ITEM_2": "Armature", "ITEM_28": "Costumi"}
            catLabel = catSubNames.get(self.currentCategory, "Oggetti")
            self.__UpdateStatus("%s trovati: %d" % (catLabel, len(self.gridData)))
        else:
            # List mode - svuota TUTTI gli slot della griglia per evitare che
            # il GridSlotWindow C++ intercetti click anche da nascosto
            for _si in xrange(self._curGridSize):
                self.itemGrid.SetItemSlot(_si, 0, 0)
            self.itemGrid.RefreshSlot()
            self.gridContainer.SetPosition(-5000, -5000)
            self.gridContainer.Hide()
            self.listBox.RemoveAllItems()
            self.listBox.Show()
            self.scrollBar.SetPos(0.0)

            results = DATA_MGR.SearchMobs(query, self.currentCategory)
            try:
                # Ordina per grado (decrescente) poi livello (decrescente) poi nome
                results.sort(key=lambda x: (-DATA_MGR.GetMobGrade(x[0]), -DATA_MGR.GetMobLevel(x[0]), x[1].lower()))
            except:
                pass
            innerW = LIST_WIDTH - 10
            for (vnum, name) in results:
                grade = DATA_MGR.GetMobGrade(vnum)
                level = DATA_MGR.GetMobLevel(vnum)
                self.listBox.AppendItem(self.MobListItem(name, vnum, innerW, grade, level))

            hasResults = len(results) > 0
            catNames = {"BOSS": "Boss", "METIN": "Metin", "ALL": "Tutti"}
            catName = catNames.get(self.currentCategory, "Mob")
            self.__UpdateStatus("%s trovati: %d" % (catName, len(results)))

        # No result label
        if self.noResultLabel:
            if hasResults or not query:
                self.noResultLabel.Hide()
            else:
                self.noResultLabel.Show()

    def __ArrangeGridForCategory(self):
        """Ricalcola griglia in base alla categoria corrente."""
        cat = getattr(self, 'currentCategory', 'ITEM')
        if cat in ("ITEM_1", "ITEM_2"):   # Armi / Armature (slot 1x3)
            slotH = 96
            rows = 5
        elif cat == "ITEM_28":             # Costumi (slot 1x2)
            slotH = 64
            rows = 7
        else:                              # Oggetti generici (slot 1x1)
            slotH = 32
            rows = MAX_GRID_ROWS

        if slotH != self._curSlotH:
            self._curSlotH = slotH
            self._curGridRows = rows
            self._curGridSize = MAX_GRID_COLS * rows
            self.itemGrid.ArrangeSlot(0, MAX_GRID_COLS, rows, 32, slotH, 4, 4)

    def __RefreshGrid(self):
        """Aggiorna la griglia items - 1 item per slot, slot dimensionati per categoria."""
        self.__ArrangeGridForCategory()
        gridSize = self._curGridSize

        # Svuota tutti gli slot
        for i in xrange(gridSize):
            self.itemGrid.SetItemSlot(i, 0, 0)

        self._slotToDataIdx = {}
        placed = 0
        idx = self.gridOffset

        while idx < len(self.gridData) and placed < gridSize:
            vnum = self.gridData[idx]
            self.itemGrid.SetItemSlot(placed, vnum, 0)
            self._slotToDataIdx[placed] = idx
            placed += 1
            idx += 1

        self._gridPageItems = max(1, placed)
        self.itemGrid.RefreshSlot()

    # ================================================================
    #  SCROLL HANDLERS
    # ================================================================
    def __OnScroll(self):
        self.__HideToolTip()
        pos = self.scrollBar.GetPos()
        isItemCategory = self.currentCategory == "ITEM" or self.currentCategory.startswith("ITEM_")
        if isItemCategory:
            totalItems = len(self.gridData)
            if totalItems <= self._gridPageItems:
                self.gridOffset = 0
            else:
                maxOffset = max(0, totalItems - self._gridPageItems)
                self.gridOffset = int(pos * maxOffset)
            self.__RefreshGrid()
        else:
            count = self.listBox.GetItemCount()
            maxPos = max(0, count - self._listViewCount)
            self.listBox.SetBasePos(int(pos * maxPos))

    def __OnDropScroll(self):
        self.__HideToolTip()
        pos = self.dropScrollBar.GetPos()
        count = self.dropList.GetItemCount()
        maxPos = max(0, count - self._dropViewCount)
        self.dropList.SetBasePos(int(pos * maxPos))

    # ================================================================
    #  SELECTION HANDLERS
    # ================================================================
    def __OnSelectListItem(self, selectedItem):
        """Selezionato un mob o fracture dalla lista."""
        if not selectedItem:
            return
        self.__HideToolTip()
        # Controlla se e' un item frattura
        fractCat = getattr(selectedItem, '_fractCat', None)
        if fractCat:
            self.__ShowFractureDetails(selectedItem.vnum, fractCat)
        else:
            self.__ShowMobDetails(selectedItem.vnum)

    def __OnGridSelect(self, slotIndex):
        """Selezionato un item dalla griglia."""
        self.__HideToolTip()
        if slotIndex not in self._slotToDataIdx:
            return
        idx = self._slotToDataIdx[slotIndex]
        if idx < len(self.gridData):
            vnum = self.gridData[idx]
            self.__ShowItemDetails(vnum)

    def __OnGridOverIn(self, slotIndex):
        """Hover su item nella griglia - mostra tooltip classico di Metin2."""
        if slotIndex not in self._slotToDataIdx:
            return
        idx = self._slotToDataIdx[slotIndex]
        if idx >= len(self.gridData):
            return
        vnum = self.gridData[idx]

        if not self.toolTip:
            try:
                import uiToolTip
                self.toolTip = uiToolTip.ItemToolTip()
            except:
                return

        self.toolTip.SetItemToolTip(vnum)
        self.toolTip.ShowToolTip()

    def __OnGridOverOut(self):
        """Mouse esce dalla griglia - nascondi tooltip."""
        self.__HideToolTip()

    def __HideToolTip(self):
        """Nasconde il tooltip condiviso - chiamare in ogni punto di transizione."""
        if self.toolTip:
            try:
                self.toolTip.HideToolTip()
            except:
                pass

    def __GetOrCreateToolTip(self):
        """Crea o restituisce il tooltip condiviso."""
        if not self.toolTip:
            try:
                import uiToolTip
                self.toolTip = uiToolTip.ItemToolTip()
            except:
                pass
        return self.toolTip

    def __OnPreviewIconOverIn(self, slotIndex):
        """Hover sull'icona item nel preview panel - mostra tooltip classico."""
        vnum = self._previewIconVnum
        if vnum <= 0:
            return
        tt = self.__GetOrCreateToolTip()
        if tt:
            tt.SetItemToolTip(vnum)
            tt.ShowToolTip()

    def __OnPreviewIconOverOut(self):
        """Mouse esce dall'icona item nel preview panel."""
        self.__HideToolTip()

    # ================================================================
    #  SHOW DETAILS
    # ================================================================
    def __MakeDropItem(self, text, vnum, type_flag, icon_path="", width=DETAIL_ITEM_W):
        """Crea un DropListItem con il tooltip ref impostato automaticamente."""
        dli = self.DropListItem(text, vnum, type_flag, icon_path, width)
        if type_flag == 0 and vnum > 0:
            dli.SetToolTipRef(self.__GetOrCreateToolTip())
        return dli

    def __MakeSectionItem(self, text, color, width=DETAIL_ITEM_W):
        """Crea un item separatore di sezione con barre orizzontali e testo centrato."""
        dli = self.DropListItem(text, 0, -1, "", width)
        dli.bg.SetColor(0xAA0A0A18)
        dli.textLine.SetPackedFontColor(color)
        # Linea sopra e sotto
        topL = ui.Bar()
        topL.SetParent(dli)
        topL.SetPosition(0, 0)
        topL.SetSize(width, 1)
        topL.SetColor(color)
        topL.AddFlag("not_pick")
        topL.Show()
        botL = ui.Bar()
        botL.SetParent(dli)
        botL.SetPosition(0, 29)
        botL.SetSize(width, 1)
        botL.SetColor(color)
        botL.AddFlag("not_pick")
        botL.Show()
        dli._sectionTop = topL
        dli._sectionBot = botL
        return dli

    def __AggregateDrops(self, drops):
        """Aggrega drop duplicati per vnum, sommando le quantita'.
        Input:  [(vnum, count, rate), ...]
        Output: [(vnum, totalCount, maxRate), ...] senza duplicati.
        """
        agg = {}
        order = []
        for entry in drops:
            v = entry[0]
            c = int(entry[1]) if entry[1] else 1
            r = entry[2] if len(entry) > 2 else 0
            if v in agg:
                agg[v][0] += c
                if r > agg[v][1]:
                    agg[v][1] = r
            else:
                agg[v] = [c, r]
                order.append(v)
        result = []
        for v in order:
            result.append((v, agg[v][0], agg[v][1]))
        return result

    def __ShowMobDetails(self, vnum):
        """Mostra i dettagli di un Mob/Boss/Metin."""
        self.__HideToolTip()
        if self.refinePopup:
            self.refinePopup.Close()
        if self.upgradeTableBtn:
            self.upgradeTableBtn.Hide()
        self.dropList.RemoveAllItems()
        self.dropScrollBar.SetPos(0.0)
        self._currentDetailVnum = vnum
        self._currentDetailType = 1

        name = DATA_MGR.GetMobName(vnum)
        level = DATA_MGR.GetMobLevel(vnum)
        grade = DATA_MGR.GetMobGrade(vnum)

        gradeNames = {0: "Comune", 1: "Forte", 2: "Raro", 3: "Speciale",
                      4: "Boss", 5: "Boss Raid", 6: "Boss Leggendario"}
        gradeName = gradeNames.get(grade, "Grado %d" % grade)

        nameColor = GRADE_COLORS.get(grade, COLOR_TEXT_GOLD)
        self.infoLabel.SetText(name)
        self.infoLabel.SetPackedFontColor(nameColor)

        # Sub-label con stats mob
        subParts = ["Lv.%s" % str(level), gradeName]
        hp = DATA_MGR.GetMobHP(vnum)
        if hp > 0:
            subParts.append("HP: %s" % DATA_MGR.FormatYang(hp))
        self.infoSubLabel.SetText(" | ".join(subParts))

        # Header sezione drop
        drops = DATA_MGR.GetMobDrops(vnum)
        aggDrops = self.__AggregateDrops(drops)
        self.__UpdateDetailHeader("Drop di %s (%d oggetti)" % (name, len(aggDrops)))

        # === SEZIONE STATS COMBATTIMENTO ===
        statLines = []
        exp = DATA_MGR.GetMobExp(vnum)
        if exp > 0:
            statLines.append(("EXP: %s" % DATA_MGR.FormatYang(exp), COLOR_TEXT_GREEN))
        minD, maxD = DATA_MGR.GetMobDamage(vnum)
        if maxD > 0:
            statLines.append(("ATK: %s ~ %s" % (DATA_MGR.FormatYang(minD), DATA_MGR.FormatYang(maxD)), COLOR_TEXT_ORANGE))
        mobDef = DATA_MGR.GetMobDefense(vnum)
        if mobDef > 0:
            statLines.append(("DEF: %s" % DATA_MGR.FormatYang(mobDef), COLOR_TEXT_ORANGE))
        raceStr = DATA_MGR.GetMobRaceStr(vnum)
        if raceStr:
            statLines.append(("Razza: %s" % raceStr, COLOR_TEXT_CYAN))

        if statLines:
            self.dropList.AppendItem(self.__MakeSectionItem("Stats Combattimento", COLOR_TEXT_ORANGE))
            for (sText, sColor) in statLines:
                sItem = self.__MakeDropItem(sText, 0, -1, "", DETAIL_ITEM_W)
                sItem.textLine.SetPackedFontColor(sColor)
                self.dropList.AppendItem(sItem)

        # === SEZIONE ZONA E PROGRESSIONE ===
        mobLv = 0
        try:
            mobLv = int(level)
        except:
            pass

        # Posizione corretta del boss/mob
        mobLocation = DATA_MGR.GetMobLocation(vnum)
        if mobLocation:
            isDungeon = mobLocation.startswith("DG ")
            locColor = COLOR_TEXT_ORANGE if isDungeon else COLOR_TEXT_LIGHT
            locLabel = "Dungeon" if isDungeon else "Zona"
            locText = mobLocation[3:] if isDungeon else mobLocation  # rimuovi prefisso "DG "
            locItem = self.__MakeDropItem("%s: %s" % (locLabel, locText), 0, -1, "", DETAIL_ITEM_W)
            locItem.textLine.SetPackedFontColor(locColor)
            self.dropList.AppendItem(locItem)

        if mobLv > 0:
            tip = DATA_MGR.GetLevelTip(mobLv)
            if tip:
                tipItem = self.__MakeDropItem("Tip: %s" % tip, 0, -1, "", DETAIL_ITEM_W)
                tipItem.textLine.SetPackedFontColor(COLOR_TEXT_GRAY)
                self.dropList.AppendItem(tipItem)

        # Aggrega duplicati e mostra totali
        self.dropList.AppendItem(self.__MakeSectionItem("Drop (%d oggetti unici)" % len(aggDrops), COLOR_TEXT_CYAN))

        # Drops (ordinati per nome)
        if aggDrops:
            sortedDrops = list(aggDrops[:MAX_DROP_DISPLAY])
            try:
                sortedDrops.sort(key=lambda d: DATA_MGR.GetItemName(d[0]).lower())
            except:
                pass
            for (item_vnum, item_count, rate) in sortedDrops:
                itemName = DATA_MGR.GetItemName(item_vnum)
                iconPath = DATA_MGR.GetItemIconPath(item_vnum)
                if int(item_count) > 1:
                    text = "%s x%d" % (itemName, int(item_count))
                else:
                    text = itemName
                self.dropList.AppendItem(
                    self.__MakeDropItem(text, item_vnum, 0, iconPath, DETAIL_ITEM_W))
        else:
            self.dropList.AppendItem(
                self.__MakeDropItem("Nessun drop registrato", 0, -1, "", DETAIL_ITEM_W))

        # 3D Preview
        self.__ShowMobPreview(vnum, name)

        self.__UpdateBackButton()
        self.__UpdateStatus("Mob: %s | Drop: %d" % (name, len(aggDrops)))

    # ================================================================
    #  FRACTURE SEARCH & DETAILS
    # ================================================================
    def __SearchFracture(self, query, category):
        """Cerca nelle liste frattura. Ritorna [(vnum, name, tier, gloria), ...]"""
        results = []
        q = query.lower().strip()
        if category == "FRACT_BOSS":
            source = FRACTURE_BOSSES
        elif category == "FRACT_METIN":
            source = FRACTURE_SUPERMETIN
        elif category == "FRACT_CHEST":
            source = FRACTURE_CHESTS
        else:
            return results

        for fVnum, fData in source.items():
            name = fData["name"]
            if not q or q in name.lower():
                gloria = fData.get("gloria", fData.get("gloria_min", 0))
                results.append((fVnum, name, fData["tier"], gloria))

        # Ordina per tier crescente, poi gloria
        try:
            results.sort(key=lambda x: (x[2], x[3]))
        except:
            pass
        return results

    def __ShowFractureDetails(self, vnum, fractCat):
        """Mostra dettagli di un elemento Frattura (Boss, Super Metin o Baule)."""
        self.__HideToolTip()
        if self.refinePopup:
            self.refinePopup.Close()
        if self.upgradeTableBtn:
            self.upgradeTableBtn.Hide()
        self.dropList.RemoveAllItems()
        self.dropScrollBar.SetPos(0.0)
        self._currentDetailVnum = vnum
        self._currentDetailType = 3  # tipo frattura

        # Identifica i dati
        if fractCat == "FRACT_BOSS":
            data = FRACTURE_BOSSES.get(vnum, {})
        elif fractCat == "FRACT_METIN":
            data = FRACTURE_SUPERMETIN.get(vnum, {})
        elif fractCat == "FRACT_CHEST":
            data = FRACTURE_CHESTS.get(vnum, {})
        else:
            data = {}
        if not data:
            return

        name = data["name"]
        tier = data["tier"]
        tierColor = TIER_COLORS.get(tier, COLOR_TEXT_LIGHT)
        tierName = TIER_NAMES.get(tier, "Tier %d" % tier)

        self.infoLabel.SetText(name)
        self.infoLabel.SetPackedFontColor(tierColor)

        # === SUB-LABEL ===
        if fractCat == "FRACT_BOSS":
            self.infoSubLabel.SetText("Boss Frattura | %s | Tier %d" % (tierName, tier))
        elif fractCat == "FRACT_METIN":
            self.infoSubLabel.SetText("Super Metin | %s | Tier %d" % (tierName, tier))
        elif fractCat == "FRACT_CHEST":
            self.infoSubLabel.SetText("Baule Frattura | %s | Tier %d" % (tierName, tier))

        self.__UpdateDetailHeader("Frattura: %s" % name)

        # === SEZIONE GLORIA ===
        self.dropList.AppendItem(self.__MakeSectionItem("Ricompense Gloria", 0xFF00DDFF))

        if fractCat == "FRACT_BOSS":
            gloria = data["gloria"]
            gItem = self.__MakeDropItem("Gloria Base: %d" % gloria, 0, -1, "", DETAIL_ITEM_W)
            gItem.textLine.SetPackedFontColor(COLOR_TEXT_GREEN)
            self.dropList.AppendItem(gItem)

            speedItem = self.__MakeDropItem("Speed Kill (<%ds): +%d Gloria" % (FRACTURE_BOSS_SPEED_TIME, FRACTURE_BOSS_SPEED_BONUS), 0, -1, "", DETAIL_ITEM_W)
            speedItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
            self.dropList.AppendItem(speedItem)

            totalMax = gloria + FRACTURE_BOSS_SPEED_BONUS
            totItem = self.__MakeDropItem("Gloria Massima: %d" % totalMax, 0, -1, "", DETAIL_ITEM_W)
            totItem.textLine.SetPackedFontColor(COLOR_TEXT_GOLD)
            self.dropList.AppendItem(totItem)

        elif fractCat == "FRACT_METIN":
            gloria = data["gloria"]
            gItem = self.__MakeDropItem("Gloria Base: %d" % gloria, 0, -1, "", DETAIL_ITEM_W)
            gItem.textLine.SetPackedFontColor(COLOR_TEXT_GREEN)
            self.dropList.AppendItem(gItem)

            speedItem = self.__MakeDropItem("Speed Kill (<%ds): +%d Gloria" % (FRACTURE_METIN_SPEED_TIME, FRACTURE_METIN_SPEED_BONUS), 0, -1, "", DETAIL_ITEM_W)
            speedItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
            self.dropList.AppendItem(speedItem)

            grpItem = self.__MakeDropItem("Bonus Gruppo: +%d%% per alleato (max +50%%)" % FRACTURE_METIN_GROUP_BONUS, 0, -1, "", DETAIL_ITEM_W)
            grpItem.textLine.SetPackedFontColor(COLOR_TEXT_CYAN)
            self.dropList.AppendItem(grpItem)

            proxItem = self.__MakeDropItem("Prossimita': 5-15 Gloria ogni 15s (alleati)", 0, -1, "", DETAIL_ITEM_W)
            proxItem.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
            self.dropList.AppendItem(proxItem)

        elif fractCat == "FRACT_CHEST":
            gMin = data["gloria_min"]
            gMax = data["gloria_max"]
            gItem = self.__MakeDropItem("Gloria: %d ~ %d" % (gMin, gMax), 0, -1, "", DETAIL_ITEM_W)
            gItem.textLine.SetPackedFontColor(COLOR_TEXT_GREEN)
            self.dropList.AppendItem(gItem)

            jpPct = data.get("jackpot", 0)
            if jpPct > 0:
                jpItem = self.__MakeDropItem("Jackpot: %d%% probabilita'" % jpPct, 0, -1, "", DETAIL_ITEM_W)
                jpItem.textLine.SetPackedFontColor(COLOR_TEXT_GOLD)
                self.dropList.AppendItem(jpItem)

        # === SEZIONE OGGETTI (per i bauli) ===
        if fractCat == "FRACT_CHEST":
            self.dropList.AppendItem(self.__MakeSectionItem("Contenuto Garantito", COLOR_TEXT_ORANGE))
            iName = data.get("item_name", "Oggetto")
            iQty = data.get("item_qty", 1)
            iVnum = data.get("item_vnum", 0)
            if iQty > 1:
                iText = "%s x%d" % (iName, iQty)
            else:
                iText = iName
            cItem = self.__MakeDropItem(iText, iVnum, 0, "", DETAIL_ITEM_W)
            cItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
            self.dropList.AppendItem(cItem)

            # Accesso esclusivo
            ownItem = self.__MakeDropItem("Accesso esclusivo: 60s al conquistatore", 0, -1, "", DETAIL_ITEM_W)
            ownItem.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
            self.dropList.AppendItem(ownItem)

        # === SEZIONE TIER / FRATTURA ===
        self.dropList.AppendItem(self.__MakeSectionItem("Info Frattura", COLOR_TEXT_CYAN))

        tierItem = self.__MakeDropItem("Tier: %d - %s" % (tier, tierName), 0, -1, "", DETAIL_ITEM_W)
        tierItem.textLine.SetPackedFontColor(tierColor)
        self.dropList.AppendItem(tierItem)

        lvlItem = self.__MakeDropItem("Livello Richiesto: 75+", 0, -1, "", DETAIL_ITEM_W)
        lvlItem.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
        self.dropList.AppendItem(lvlItem)

        # Fratture associate a questo tier
        portalData = None
        for rankK, pData in FRACTURE_PORTALS.items():
            rankTier = {"E": 1, "D": 2, "C": 3, "B": 4, "A": 5, "S": 6, "N": 7}.get(rankK, 0)
            if rankTier == tier:
                portalData = pData
                break
        if portalData:
            pName = portalData["name"]
            gReq = portalData["gloria_req"]
            pwReq = portalData["power_rank"]
            pWeight = portalData["weight"]
            portItem = self.__MakeDropItem("Portale: %s" % pName, 0, -1, "", DETAIL_ITEM_W)
            portItem.textLine.SetPackedFontColor(tierColor)
            self.dropList.AppendItem(portItem)
            if gReq > 0:
                reqItem = self.__MakeDropItem("Requisito: %s Gloria" % DATA_MGR.FormatYang(gReq), 0, -1, "", DETAIL_ITEM_W)
                reqItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
                self.dropList.AppendItem(reqItem)
            if pwReq > 0:
                reqItem = self.__MakeDropItem("Requisito: %d Power Rank" % pwReq, 0, -1, "", DETAIL_ITEM_W)
                reqItem.textLine.SetPackedFontColor(COLOR_TEXT_ORANGE)
                self.dropList.AppendItem(reqItem)
            spawnItem = self.__MakeDropItem("Probabilita' spawn: %d%%" % pWeight, 0, -1, "", DETAIL_ITEM_W)
            spawnItem.textLine.SetPackedFontColor(COLOR_TEXT_GRAY)
            self.dropList.AppendItem(spawnItem)

        # === DIFESA FRATTURA (Gloria per difesa) ===
        defRank = {1: "E", 2: "D", 3: "C", 4: "B", 5: "A", 6: "S", 7: "N"}.get(tier, "E")
        defReward = FRACTURE_DEFENSE_REWARDS.get(defRank, (0, 0))
        if defReward[1] > 0:
            self.dropList.AppendItem(self.__MakeSectionItem("Difesa Frattura (%s)" % defRank, COLOR_TEXT_GREEN))
            dItem = self.__MakeDropItem("Gloria Difesa: %s ~ %s" % (DATA_MGR.FormatYang(defReward[0]), DATA_MGR.FormatYang(defReward[1])), 0, -1, "", DETAIL_ITEM_W)
            dItem.textLine.SetPackedFontColor(COLOR_TEXT_GREEN)
            self.dropList.AppendItem(dItem)
            if tier >= 4:
                warnItem = self.__MakeDropItem("ATTENZIONE: Distrutta se la difesa fallisce!", 0, -1, "", DETAIL_ITEM_W)
                warnItem.textLine.SetPackedFontColor(0xFFFF4444)
                self.dropList.AppendItem(warnItem)

        # === LINK AD ALTRI NELLA STESSA CATEGORIA ===
        if fractCat == "FRACT_BOSS" and vnum in DATA_MGR.mob_drops:
            drops = DATA_MGR.GetMobDrops(vnum)
            if drops:
                self.dropList.AppendItem(self.__MakeSectionItem("Drop Boss (%d)" % len(drops), COLOR_TEXT_CYAN))
                sortedDrops = list(drops[:MAX_DROP_DISPLAY])
                try:
                    sortedDrops.sort(key=lambda d: DATA_MGR.GetItemName(d[0]).lower())
                except:
                    pass
                for (item_vnum, item_count, rate) in sortedDrops:
                    itemName = DATA_MGR.GetItemName(item_vnum)
                    iconPath = DATA_MGR.GetItemIconPath(item_vnum)
                    if int(item_count) > 1:
                        text = "%s x%s" % (itemName, str(item_count))
                    else:
                        text = itemName
                    self.dropList.AppendItem(
                        self.__MakeDropItem(text, item_vnum, 0, iconPath, DETAIL_ITEM_W))

        # === PREVIEW ===
        if fractCat in ("FRACT_BOSS", "FRACT_METIN"):
            # 3D mob preview
            self.__ShowMobPreview(vnum, name)
            # Sovrascrivi sub-label con info frattura
            if hasattr(self, 'previewSubLabel') and self.previewSubLabel:
                self.previewSubLabel.SetText("%s | Tier %d | Gloria %d" % (tierName, tier, data.get("gloria", 0)))
                self.previewSubLabel.SetPackedFontColor(tierColor)
        elif fractCat == "FRACT_CHEST":
            # Preview item del contenuto garantito
            try:
                renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
            except:
                pass
            if self.renderTargetWnd:
                self.renderTargetWnd.Hide()
            if self.previewNameLabel:
                self.previewNameLabel.SetText("")
            if hasattr(self, 'previewSubLabel') and self.previewSubLabel:
                self.previewSubLabel.SetText("")

            iVnum = data.get("item_vnum", 0)
            if self.itemPreviewPanel and iVnum > 0:
                self.itemPreviewPanel.Show()
                # Icona dell'oggetto garantito
                itemSlotH = DATA_MGR.GetItemSize(iVnum)
                if itemSlotH < 1:
                    itemSlotH = 1
                if itemSlotH > 3:
                    itemSlotH = 3
                if self.itemPreviewIcon:
                    if itemSlotH != self._previewSlotH:
                        self._previewSlotH = itemSlotH
                        ipW = self.itemPreviewPanel.GetWidth()
                        self.itemPreviewIcon.SetPosition((ipW - 32) // 2, 8)
                        self.itemPreviewIcon.ArrangeSlot(0, 1, itemSlotH, 32, 32, 0, 0)
                        self.itemPreviewIcon.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
                        self.itemPreviewIcon.Show()
                    try:
                        self.itemPreviewIcon.SetItemSlot(0, iVnum, 0)
                    except:
                        try:
                            item.SelectItem(iVnum)
                            self.itemPreviewIcon.SetItemSlot(0, iVnum, 1)
                        except:
                            pass
                iconBottomY = 8 + itemSlotH * 32 + 4
                ipW = self.itemPreviewPanel.GetWidth()
                if self.itemPreviewName:
                    self.itemPreviewName.SetText(name)
                    self.itemPreviewName.SetPackedFontColor(tierColor)
                    self.itemPreviewName.SetPosition(ipW // 2, iconBottomY)
                if self.itemPreviewType:
                    self.itemPreviewType.SetText("Baule %s | Tier %d" % (tierName, tier))
                    self.itemPreviewType.SetPackedFontColor(COLOR_TEXT_GRAY)
                    self.itemPreviewType.SetPosition(ipW // 2, iconBottomY + 16)
                sepY = iconBottomY + 34
                if self.itemPreviewSep:
                    self.itemPreviewSep.SetPosition(20, sepY)
                originTitleY = sepY + 6
                if self.itemPreviewOriginTitle:
                    iName = data.get("item_name", "Oggetto")
                    iQty = data.get("item_qty", 1)
                    if iQty > 1:
                        self.itemPreviewOriginTitle.SetText("Contiene: %s x%d" % (iName, iQty))
                    else:
                        self.itemPreviewOriginTitle.SetText("Contiene: %s" % iName)
                    self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_GOLD)
                    self.itemPreviewOriginTitle.SetPosition(ipW // 2, originTitleY)
                # Righe info baule
                for i in xrange(len(self._itemPreviewInfoLines)):
                    line = self._itemPreviewInfoLines[i]
                    if i == 0:
                        gMin = data.get("gloria_min", 0)
                        gMax = data.get("gloria_max", 0)
                        line.SetText("Gloria: %d ~ %d" % (gMin, gMax))
                        line.SetPackedFontColor(COLOR_TEXT_GREEN)
                    elif i == 1:
                        jpPct = data.get("jackpot", 0)
                        if jpPct > 0:
                            line.SetText("Jackpot: %d%%" % jpPct)
                            line.SetPackedFontColor(COLOR_TEXT_GOLD)
                        else:
                            line.SetText("")
                    elif i == 2:
                        line.SetText("Accesso: 60s esclusivo")
                        line.SetPackedFontColor(COLOR_TEXT_LIGHT)
                    else:
                        line.SetText("")
                    line.SetPosition(ipW // 2, originTitleY + 18 + i * 14)
                # Nascondi upgrade section
                sep2Y = originTitleY + 18 + 6 * 14 + 4
                if self.itemPreviewSep2:
                    self.itemPreviewSep2.SetPosition(20, sep2Y)
                if self.itemPreviewUpgradeText:
                    self.itemPreviewUpgradeText.SetText("")
                if self.itemPreviewUpgradeCost:
                    self.itemPreviewUpgradeCost.SetText("")

        self.__UpdateBackButton()
        self.__UpdateStatus("Frattura: %s | Tier %d | %s" % (name, tier, tierName))

    def __ShowItemDetails(self, vnum):
        """Mostra i dettagli di un Item."""
        self.__HideToolTip()
        if self.refinePopup:
            self.refinePopup.Close()
        if self.upgradeTableBtn:
            self.upgradeTableBtn.Hide()
        self.dropList.RemoveAllItems()
        self.dropScrollBar.SetPos(0.0)
        self._currentDetailVnum = vnum
        self._currentDetailType = 0

        name = DATA_MGR.GetItemName(vnum)
        self.infoLabel.SetText(name)
        self.infoLabel.SetPackedFontColor(COLOR_TEXT_GOLD)

        # Tipo e sottotipo item
        typeStr, subStr = DATA_MGR.GetItemTypeInfo(vnum)
        if subStr:
            fullType = "%s - %s" % (typeStr, subStr) if typeStr else subStr
        else:
            fullType = typeStr if typeStr else "Oggetto"

        # Dimensione slot
        slotSize = DATA_MGR.GetItemSize(vnum)
        slotNames = {1: "1 Slot", 2: "2 Slot", 3: "3 Slot"}
        slotInfo = slotNames.get(slotSize, "")
        if slotInfo:
            fullType = "%s (%s)" % (fullType, slotInfo)

        # Posizione upgrade chain
        upgradeInfo = ""
        isInRefineChain = DATA_MGR.IsRefinable(vnum)
        if not isInRefineChain:
            isInRefineChain = vnum in DATA_MGR.item_refined_targets
        if isInRefineChain:
            pos, total = DATA_MGR.GetUpgradePosition(vnum)
            if total > 0:
                upgradeInfo = " | +%d/%d" % (pos, total)

        # Livello richiesto
        levelReq = DATA_MGR.GetItemLevelLimit(vnum)
        levelInfo = ""
        if levelReq > 0:
            levelInfo = " | Lv.%d" % levelReq

        # Indicatore forziere
        chestInfo = ""
        if DATA_MGR.IsChest(vnum):
            chestInfo = " | Forziere"

        self.infoSubLabel.SetText("%s%s%s%s" % (fullType, upgradeInfo, levelInfo, chestInfo))

        # Header sezione origini
        origins = DATA_MGR.GetItemDroppers(vnum)
        self.__UpdateDetailHeader("Info: %s" % name)

        # Descrizione
        DATA_MGR._EnsureDescsLoaded()
        desc = DATA_MGR.item_descs.get(vnum, "")
        if desc:
            descItem = self.__MakeDropItem(desc, 0, -1, "", DETAIL_ITEM_W)
            descItem.textLine.SetPackedFontColor(COLOR_TEXT_GRAY)
            self.dropList.AppendItem(descItem)

        # === SEZIONE STATISTICHE ITEM ===
        itemApplies = DATA_MGR.GetItemApplies(vnum)
        if levelReq > 0 or itemApplies:
            self.dropList.AppendItem(self.__MakeSectionItem("Statistiche", COLOR_TEXT_ORANGE))

            if levelReq > 0:
                lvlItem = self.__MakeDropItem("Livello richiesto: %d" % levelReq, 0, -1, "", DETAIL_ITEM_W)
                lvlItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
                self.dropList.AppendItem(lvlItem)

                # Zona consigliata per il livello
                zName, zPhase = DATA_MGR.GetZoneForLevel(levelReq)
                if zName:
                    zItem = self.__MakeDropItem("Zona: %s (%s)" % (zName, zPhase), 0, -1, "", DETAIL_ITEM_W)
                    zItem.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
                    self.dropList.AppendItem(zItem)

            for (bonusName, bonusValue) in itemApplies:
                if bonusValue > 0:
                    bText = "%s: +%s" % (bonusName, str(bonusValue))
                else:
                    bText = "%s: %s" % (bonusName, str(bonusValue))
                bItem = self.__MakeDropItem(bText, 0, -1, "", DETAIL_ITEM_W)
                bItem.textLine.SetPackedFontColor(COLOR_TEXT_GREEN)
                self.dropList.AppendItem(bItem)

        # === SEZIONE CONTENUTO FORZIERE (se l'item e' un baule/forziere) ===
        chestContents = DATA_MGR.GetChestContents(vnum)
        if chestContents:
            # Aggrega duplicati e ordina per nome
            aggChest = self.__AggregateDrops(chestContents)
            self.dropList.AppendItem(self.__MakeSectionItem("Contenuto Forziere (%d)" % len(aggChest), COLOR_TEXT_GOLD))
            # Mostra dungeon associato al forziere
            dgName = DATA_MGR.GetChestDungeonName(vnum)
            if dgName:
                dgItem = self.__MakeDropItem("Fonte: %s" % dgName, 0, -1, "", DETAIL_ITEM_W)
                dgItem.textLine.SetPackedFontColor(COLOR_TEXT_LIGHT)
                self.dropList.AppendItem(dgItem)
            sortedChest = list(aggChest[:MAX_DROP_DISPLAY])
            try:
                sortedChest.sort(key=lambda c: DATA_MGR.GetItemName(c[0]).lower())
            except:
                pass
            for (cItemVnum, cCount, cRate) in sortedChest:
                cName = DATA_MGR.GetItemName(cItemVnum)
                cIcon = DATA_MGR.GetItemIconPath(cItemVnum)
                if int(cCount) > 1:
                    cText = "%s x%d" % (cName, int(cCount))
                else:
                    cText = cName
                self.dropList.AppendItem(
                    self.__MakeDropItem(cText, cItemVnum, 0, cIcon, DETAIL_ITEM_W))

        # === SEZIONE OTTENIBILE DA FORZIERI ===
        chestSources = DATA_MGR.GetItemChestSources(vnum)
        if chestSources:
            self.dropList.AppendItem(self.__MakeSectionItem("Ottenibile da %d Forzieri" % len(chestSources), 0xFFDDA0DD))
            for chestVnum in chestSources[:MAX_DROP_DISPLAY]:
                chestName = DATA_MGR.GetItemName(chestVnum)
                chestIcon = DATA_MGR.GetItemIconPath(chestVnum)
                dgName = DATA_MGR.GetChestDungeonName(chestVnum)
                if dgName:
                    cText = "%s (%s)" % (chestName, dgName)
                else:
                    cText = chestName
                self.dropList.AppendItem(
                    self.__MakeDropItem(cText, chestVnum, 0, chestIcon, DETAIL_ITEM_W))

        # Origini (chi lo droppa) - ordinate per livello decrescente
        if origins:
            self.dropList.AppendItem(self.__MakeSectionItem("Droppato da %d mob" % len(origins), COLOR_TEXT_CYAN))
            sortedOrigins = list(origins[:MAX_DROP_DISPLAY])
            try:
                sortedOrigins.sort(key=lambda mv: DATA_MGR.GetMobLevel(mv), reverse=True)
            except:
                pass
            for mob_vnum in sortedOrigins:
                mobName = DATA_MGR.GetMobName(mob_vnum)
                level = DATA_MGR.GetMobLevel(mob_vnum)
                grade = DATA_MGR.GetMobGrade(mob_vnum)
                gradeTag = {2: " [R]", 3: " [S]", 4: " [Boss]", 5: " [Raid]", 6: " [Leg]"}.get(grade, "")
                text = "%s%s Lv.%s" % (mobName, gradeTag, str(level))
                self.dropList.AppendItem(
                    self.__MakeDropItem(text, mob_vnum, 1, "", DETAIL_ITEM_W))

        # === SEZIONE POTENZIAMENTO ===
        self.__AppendRefineSection(vnum)

        # Item Preview
        self.__ShowItemPreview(vnum, name, fullType, origins)

        self.__UpdateBackButton()
        statusParts = ["Item: %s" % name, "Origini: %d" % len(origins)]
        if chestContents:
            statusParts.append("Contenuto: %d" % len(chestContents))
        if chestSources:
            statusParts.append("Forzieri: %d" % len(chestSources))
        self.__UpdateStatus(" | ".join(statusParts))

    # ================================================================
    #  REFINE SECTION - Aggiunge info potenziamento alla detail list
    # ================================================================
    def __AppendRefineSection(self, vnum):
        """Aggiunge la sezione potenziamento alla dropList per l'item corrente."""
        # Controlla se e' potenziabile o almeno nella catena upgrade
        isRefinable = DATA_MGR.IsRefinable(vnum)
        isInChain = vnum in DATA_MGR.item_refined_targets

        if not isRefinable and not isInChain:
            self.dropList.AppendItem(self.__MakeSectionItem("Non Potenziabile", COLOR_TEXT_DARK))
            return

        # Info posizione
        pos, total = DATA_MGR.GetUpgradePosition(vnum)

        if not isRefinable:
            # Livello MAX
            self.dropList.AppendItem(self.__MakeSectionItem("Livello MAX (+%d/%d)" % (pos, total), COLOR_TEXT_ORANGE))
        else:
            # Breve riepilogo inline
            recipe = DATA_MGR.GetRefineRecipe(vnum)
            refinedVnum = DATA_MGR.GetRefinedVnum(vnum)
            if total > 0:
                self.dropList.AppendItem(self.__MakeSectionItem("Potenziamento +%d -> +%d" % (pos, pos + 1), COLOR_TEXT_GREEN))

            if recipe:
                cost = recipe.get("cost", 0)
                if cost > 0:
                    infoItem = self.__MakeDropItem("Costo: %s Yang" % DATA_MGR.FormatYang(cost), 0, -1, "", DETAIL_ITEM_W)
                    infoItem.textLine.SetPackedFontColor(COLOR_TEXT_YELLOW)
                    self.dropList.AppendItem(infoItem)

            # Link al prossimo livello (con icona adattata alla dimensione item)
            if refinedVnum > 0:
                refinedName = DATA_MGR.GetItemName(refinedVnum)
                refinedIcon = DATA_MGR.GetItemIconPath(refinedVnum)
                slotH = DATA_MGR.GetItemSize(refinedVnum)
                if slotH < 1:
                    slotH = 1
                if slotH > 3:
                    slotH = 3
                rowH = max(30, slotH * 32 + 6)
                nextItem = self.__MakeDropItem("Prossimo: %s >>" % refinedName, refinedVnum, 0, refinedIcon, DETAIL_ITEM_W)
                # Adatta altezza riga alla dimensione dell'icona
                nextItem.SetSize(DETAIL_ITEM_W, rowH)
                if nextItem.bg:
                    nextItem.bg.SetSize(DETAIL_ITEM_W, rowH - 1)
                if nextItem.line:
                    nextItem.line.SetPosition(0, rowH - 1)
                if nextItem.iconImage:
                    iconH = slotH * 32
                    nextItem.iconImage.SetPosition(4, max(0, (rowH - 1 - iconH) // 2))
                if nextItem.textLine:
                    nextItem.textLine.SetPosition(36, max(0, (rowH - 1 - 14) // 2))
                if nextItem.arrowText:
                    nextItem.arrowText.SetPosition(DETAIL_ITEM_W - 14, max(0, (rowH - 1 - 14) // 2))
                if nextItem.typeBar:
                    nextItem.typeBar.SetSize(3, rowH - 1)
                self.dropList.AppendItem(nextItem)

        # === MOSTRA PULSANTE FISSO UPGRADE TABLE ===
        if self.upgradeTableBtn:
            self._upgradeTableVnum = vnum
            self.upgradeTableBtn.Show()



    # ================================================================
    #  PREVIEW SWITCH (3D mob vs Item icon+recap)
    # ================================================================
    def __ShowMobPreview(self, vnum, name):
        """Mostra il 3D del mob, nascondi l'overlay item."""
        if self.itemPreviewPanel:
            self.itemPreviewPanel.Hide()

        # Mostra render target + overlay 3D
        if self.renderTargetWnd:
            self.renderTargetWnd.Show()

        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, True)
            if vnum > 0:
                renderTarget.SelectModel(RENDER_TARGET_INDEX, vnum)
        except:
            pass

        if self.previewNameLabel:
            self.previewNameLabel.SetText(name)

        # Sotto-info mob (grado + livello + HP compatto)
        if hasattr(self, 'previewSubLabel') and self.previewSubLabel:
            grade = DATA_MGR.GetMobGrade(vnum)
            level = DATA_MGR.GetMobLevel(vnum)
            gradeNames = {0: "Comune", 1: "Forte", 2: "Raro", 3: "Speciale",
                          4: "Boss", 5: "Raid", 6: "Leggendario"}
            parts = []
            gName = gradeNames.get(grade, "")
            if gName:
                parts.append(gName)
            if level > 0:
                parts.append("Lv.%d" % level)
            hp = DATA_MGR.GetMobHP(vnum)
            if hp > 0:
                parts.append("HP %s" % DATA_MGR.FormatYang(hp))
            self.previewSubLabel.SetText(" | ".join(parts))
            gradeColor = GRADE_COLORS.get(grade, COLOR_TEXT_GRAY)
            self.previewSubLabel.SetPackedFontColor(gradeColor)

    def __ShowItemPreview(self, vnum, name, itemTypeStr, origins):
        """Mostra overlay item (icona + recap origini), nascondi 3D."""
        # Nascondi 3D completamente (visibility + window hide)
        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
        except:
            pass
        if self.renderTargetWnd:
            self.renderTargetWnd.Hide()

        if self.previewNameLabel:
            self.previewNameLabel.SetText("")
        if hasattr(self, 'previewSubLabel') and self.previewSubLabel:
            self.previewSubLabel.SetText("")

        # Icona item nel slot - ricrea griglia in base all'altezza reale dell'item
        self._previewIconVnum = vnum
        itemSlotH = DATA_MGR.GetItemSize(vnum)  # 1, 2 o 3
        if itemSlotH < 1:
            itemSlotH = 1
        if itemSlotH > 3:
            itemSlotH = 3

        if self.itemPreviewIcon:
            # Ricrea la griglia solo se l'altezza e' cambiata
            if itemSlotH != self._previewSlotH:
                self._previewSlotH = itemSlotH
                ipW = self.itemPreviewPanel.GetWidth()
                self.itemPreviewIcon.SetPosition((ipW - 32) // 2, 8)
                self.itemPreviewIcon.ArrangeSlot(0, 1, itemSlotH, 32, 32, 0, 0)
                self.itemPreviewIcon.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
                self.itemPreviewIcon.Show()

            try:
                self.itemPreviewIcon.SetItemSlot(0, vnum, 0)
            except:
                try:
                    item.SelectItem(vnum)
                    self.itemPreviewIcon.SetItemSlot(0, vnum, 1)
                except:
                    pass

        # Posizioni testo dinamiche in base all'altezza dell'icona
        iconBottomY = 8 + itemSlotH * 32 + 4  # fine icona + padding

        # Nome e tipo (con livello richiesto)
        if self.itemPreviewName:
            self.itemPreviewName.SetText(name)
            self.itemPreviewName.SetPosition(self.itemPreviewPanel.GetWidth() // 2, iconBottomY)
        if self.itemPreviewType:
            typeDisplay = itemTypeStr if itemTypeStr else "Oggetto"
            levelReq = DATA_MGR.GetItemLevelLimit(vnum)
            if levelReq > 0:
                typeDisplay = "%s | Lv.%d" % (typeDisplay, levelReq)
            self.itemPreviewType.SetText(typeDisplay)
            self.itemPreviewType.SetPosition(self.itemPreviewPanel.GetWidth() // 2, iconBottomY + 16)

        # Riposiziona separatore e sezioni sotto in base all'altezza icona
        ipW = self.itemPreviewPanel.GetWidth()
        sepY = iconBottomY + 34
        if self.itemPreviewSep:
            self.itemPreviewSep.SetPosition(20, sepY)
        originTitleY = sepY + 6
        if self.itemPreviewOriginTitle:
            self.itemPreviewOriginTitle.SetPosition(ipW // 2, originTitleY)
        for i in xrange(len(self._itemPreviewInfoLines)):
            self._itemPreviewInfoLines[i].SetPosition(ipW // 2, originTitleY + 18 + i * 14)

        # Posiziona sep2 e upgrade text
        sep2Y = originTitleY + 18 + 6 * 14 + 4
        if self.itemPreviewSep2:
            self.itemPreviewSep2.SetPosition(20, sep2Y)
        if self.itemPreviewUpgradeText:
            self.itemPreviewUpgradeText.SetPosition(ipW // 2, sep2Y + 6)
        if self.itemPreviewUpgradeCost:
            self.itemPreviewUpgradeCost.SetPosition(ipW // 2, sep2Y + 20)

        # ---- Raccogli dati item ----
        itemApplies = DATA_MGR.GetItemApplies(vnum)
        originCount = len(origins)
        chestSourceCount = len(DATA_MGR.GetItemChestSources(vnum))

        # ---- Titolo sezione: bonus o fonti ----
        if self.itemPreviewOriginTitle:
            if itemApplies:
                self.itemPreviewOriginTitle.SetText("Bonus base")
                self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_GREEN)
            else:
                # Nessun bonus - mostra direttamente fonti
                parts = []
                if originCount > 0:
                    parts.append("%d mob" % originCount)
                if chestSourceCount > 0:
                    parts.append("%d forzieri" % chestSourceCount)
                if DATA_MGR.IsChest(vnum):
                    dgName = DATA_MGR.GetChestDungeonName(vnum)
                    parts.append(dgName if dgName else "Forziere")
                if parts:
                    self.itemPreviewOriginTitle.SetText("Fonti: %s" % ", ".join(parts))
                    self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_CYAN)
                else:
                    specialNote = DATA_MGR.GetSpecialAcquisition(name)
                    if specialNote:
                        self.itemPreviewOriginTitle.SetText("Vedi info sotto")
                        self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_LIGHT)
                    else:
                        self.itemPreviewOriginTitle.SetText("Nessuna origine nota")
                        self.itemPreviewOriginTitle.SetPackedFontColor(COLOR_TEXT_DARK)

        # ---- Popola le 6 righe info ----
        # Reset tutte le righe
        for ln in self._itemPreviewInfoLines:
            ln.SetText("")
            ln.SetPackedFontColor(COLOR_TEXT_LIGHT)

        lineIdx = 0

        # A) Bonus base (max 3 righe, colore verde)
        for bi in xrange(min(len(itemApplies), 3)):
            bName, bVal = itemApplies[bi]
            if bVal > 0:
                self._itemPreviewInfoLines[lineIdx].SetText("%s +%d" % (bName, bVal))
            else:
                self._itemPreviewInfoLines[lineIdx].SetText("%s %d" % (bName, bVal))
            self._itemPreviewInfoLines[lineIdx].SetPackedFontColor(COLOR_TEXT_GREEN)
            lineIdx += 1

        # B) Danno arma / difesa armatura (solo se tipo appropriato)
        typeStr2, subStr2 = DATA_MGR.GetItemTypeInfo(vnum)
        if typeStr2 == "Arma":
            atkMin = DATA_MGR.GetItemValue(vnum, 3)
            atkMax = DATA_MGR.GetItemValue(vnum, 4)
            if atkMin > 0 or atkMax > 0:
                if lineIdx < 6:
                    self._itemPreviewInfoLines[lineIdx].SetText("Danno: %d ~ %d" % (atkMin, atkMax))
                    self._itemPreviewInfoLines[lineIdx].SetPackedFontColor(COLOR_TEXT_ORANGE)
                    lineIdx += 1
        elif typeStr2 == "Armatura" and subStr2 == "Armatura":
            defVal = DATA_MGR.GetItemValue(vnum, 1)
            if defVal > 0:
                if lineIdx < 6:
                    self._itemPreviewInfoLines[lineIdx].SetText("Difesa: %d" % defVal)
                    self._itemPreviewInfoLines[lineIdx].SetPackedFontColor(COLOR_TEXT_ORANGE)
                    lineIdx += 1

        # C) Fonti (nelle righe rimanenti) - solo se ci sono bonus (altrimenti gia' in titolo)
        if itemApplies and lineIdx < 6:
            parts = []
            if originCount > 0:
                parts.append("%d mob" % originCount)
            if chestSourceCount > 0:
                parts.append("%d forzieri" % chestSourceCount)
            if DATA_MGR.IsChest(vnum):
                dgName = DATA_MGR.GetChestDungeonName(vnum)
                parts.append(dgName if dgName else "Forziere")
            if parts:
                self._itemPreviewInfoLines[lineIdx].SetText("Fonti: %s" % ", ".join(parts))
                self._itemPreviewInfoLines[lineIdx].SetPackedFontColor(COLOR_TEXT_CYAN)
                lineIdx += 1

        # D) Mob principali (nelle righe restanti)
        slotsLeft = 6 - lineIdx
        if slotsLeft > 0 and originCount > 0:
            showCount = min(originCount, slotsLeft)
            for oi in xrange(showCount):
                mobVnum = origins[oi]
                mobName = DATA_MGR.GetMobName(mobVnum)
                mobLevel = DATA_MGR.GetMobLevel(mobVnum)
                grade = DATA_MGR.GetMobGrade(mobVnum)
                if mobLevel > 0:
                    self._itemPreviewInfoLines[lineIdx].SetText("Lv.%d %s" % (mobLevel, mobName))
                else:
                    self._itemPreviewInfoLines[lineIdx].SetText(mobName)
                self._itemPreviewInfoLines[lineIdx].SetPackedFontColor(GRADE_COLORS.get(grade, COLOR_TEXT_LIGHT))
                lineIdx += 1
            # Se ce ne sono di piu', sostituisci l'ultima con "...e altri"
            if originCount > showCount and lineIdx > 0:
                extra = originCount - (showCount - 1)
                self._itemPreviewInfoLines[lineIdx - 1].SetText("...e altri %d mob" % extra)
                self._itemPreviewInfoLines[lineIdx - 1].SetPackedFontColor(COLOR_TEXT_DARK)

        # === Breve recap upgrade nel preview ===
        if self.itemPreviewUpgradeText:
            isRefinable = DATA_MGR.IsRefinable(vnum)
            isInChain = vnum in DATA_MGR.item_refined_targets

            if isRefinable:
                refinedVnum = DATA_MGR.GetRefinedVnum(vnum)
                refinedName = DATA_MGR.GetItemName(refinedVnum) if refinedVnum > 0 else "?"
                pos, total = DATA_MGR.GetUpgradePosition(vnum)
                if total > 0:
                    self.itemPreviewUpgradeText.SetText("+%d -> +%d (%s)" % (pos, pos + 1, refinedName))
                else:
                    self.itemPreviewUpgradeText.SetText("UP -> %s" % refinedName)
                self.itemPreviewUpgradeText.SetPackedFontColor(COLOR_TEXT_GREEN)

                recipe = DATA_MGR.GetRefineRecipe(vnum)
                if recipe and self.itemPreviewUpgradeCost:
                    cost = recipe.get("cost", 0)
                    if cost > 0:
                        self.itemPreviewUpgradeCost.SetText("%s Yang" % DATA_MGR.FormatYang(cost))
                    else:
                        self.itemPreviewUpgradeCost.SetText("")
                elif self.itemPreviewUpgradeCost:
                    self.itemPreviewUpgradeCost.SetText("")

                if self.itemPreviewSep2:
                    self.itemPreviewSep2.Show()

            elif isInChain:
                pos, total = DATA_MGR.GetUpgradePosition(vnum)
                self.itemPreviewUpgradeText.SetText("Livello MAX (+%d/%d)" % (pos, total))
                self.itemPreviewUpgradeText.SetPackedFontColor(COLOR_TEXT_ORANGE)
                if self.itemPreviewUpgradeCost:
                    self.itemPreviewUpgradeCost.SetText("")
                if self.itemPreviewSep2:
                    self.itemPreviewSep2.Show()
            else:
                self.itemPreviewUpgradeText.SetText("Non potenziabile")
                self.itemPreviewUpgradeText.SetPackedFontColor(COLOR_TEXT_DARK)
                if self.itemPreviewUpgradeCost:
                    self.itemPreviewUpgradeCost.SetText("")
                if self.itemPreviewSep2:
                    self.itemPreviewSep2.Show()

        # Mostra panel
        if self.itemPreviewPanel:
            self.itemPreviewPanel.Show()

    # ================================================================
    #  NAVIGATION (clicca drop -> naviga)
    # ================================================================
    def __OnSelectDropItem(self, dropItem):
        """Cliccato un elemento nella lista drop/origini -> naviga."""
        self.__HideToolTip()
        if not dropItem or dropItem.type_flag < 0:
            return

        targetVnum = dropItem.vnum
        targetType = dropItem.type_flag

        if targetType == 2:
            # Apri popup potenziamento completo
            self.__OpenRefinePopup(targetVnum)
            return

        # Salva posizione corrente nello stack di navigazione
        self.__PushNav()

        if targetType == 0:
            # Naviga direttamente a un ITEM (chiamata diretta, no search hack)
            self.__ShowItemDetails(targetVnum)

        elif targetType == 1:
            # Naviga direttamente a un MOB
            self.__ShowMobDetails(targetVnum)

    def __OpenRefinePopup(self, vnum):
        """Apre la finestra popup di potenziamento centrata."""
        if not self.refinePopup:
            self.refinePopup = RefinePopup()
            self.refinePopup.SetNavigateEvent(self.__OnRefineNavigate)
        self.refinePopup.Open(vnum)

    def __OnRefineNavigate(self, vnum):
        """Callback dal RefinePopup: naviga all'item nella wiki."""
        if vnum <= 0:
            return
        self.__PushNav()
        self.__ShowItemDetails(vnum)

    # ================================================================
    #  UPDATE
    # ================================================================
    def OnUpdate(self):
        # Live search (debounced - cerca mentre scrivi)
        if self.searchInput:
            try:
                curText = self.searchInput.GetText()

                # Placeholder: mostra/nascondi in base al testo
                if hasattr(self, 'searchPlaceholder') and self.searchPlaceholder:
                    if curText and len(curText) > 0:
                        self.searchPlaceholder.Hide()
                    else:
                        self.searchPlaceholder.Show()

                if curText != self._lastSearchText:
                    self._lastSearchText = curText
                    self._searchTimer = 12  # ~0.4s debounce a 30fps
                elif self._searchTimer > 0:
                    self._searchTimer -= 1
                    if self._searchTimer == 0:
                        self.__DoSearch()
            except:
                pass

        # Fade animation
        if self.isFading:
            self.fadeAlpha -= 0.06
            if self.fadeAlpha <= 0.0:
                self.fadeAlpha = 0.0
                self.isFading = False
                if self.fadeCover:
                    self.fadeCover.Hide()
            else:
                alpha = int(self.fadeAlpha * 255)
                if self.fadeCover:
                    self.fadeCover.SetColor((alpha << 24))
                    self.fadeCover.Show()

    # ================================================================
    #  OPEN / CLOSE
    # ================================================================
    def SearchByVnum(self, vnum):
        """Apre la wiki nella sezione Oggetti e cerca per VNUM/nome."""
        if not self.isLoaded:
            self.LoadWindow()
        DATA_MGR.LoadData()

        # FIX H1: Normalizza vnum a int per evitare mismatch str/int nei lookup
        try:
            vnum = int(vnum)
        except:
            pass

        # Ottieni nome item dal vnum
        searchText = ""
        try:
            item.SelectItem(vnum)
            searchText = item.GetItemName()
        except:
            searchText = str(vnum)

        # Switcha alla categoria ITEM se non siamo gia' li'
        if not self.currentCategory.startswith("ITEM"):
            self.currentCategory = "ITEM"
            self.__UpdateCategoryButtons()

        # Inserisci il nome nella barra di ricerca
        if self.searchInput:
            self.searchInput.SetText(searchText)
        if hasattr(self, 'searchPlaceholder') and self.searchPlaceholder:
            self.searchPlaceholder.Hide()

        self.Show()
        self.SetTop()

        # Lancia la ricerca
        self.__DoSearch()

        # Se c'e' un solo risultato o il vnum e' nei risultati, mostra i dettagli
        if hasattr(self, 'gridData') and self.gridData:
            if vnum in self.gridData:
                self.__ShowItemDetails(vnum)
            elif len(self.gridData) == 1:
                self.__ShowItemDetails(self.gridData[0])

    def Open(self):
        if not self.isLoaded:
            self.LoadWindow()
        DATA_MGR.LoadData()
        self.Show()
        self.SetTop()

    def Close(self):
        if self.refinePopup:
            self.refinePopup.Close()
        if self.toolTip:
            try:
                self.toolTip.HideToolTip()
            except:
                pass
        if self.noResultLabel:
            self.noResultLabel.Hide()
        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
        except:
            pass
        # FIX M6: Reset fade state per evitare flash alla riapertura
        self.isFading = False
        self.fadeAlpha = 0
        if self.fadeCover:
            try:
                self.fadeCover.SetColor(0x00000000)
                self.fadeCover.Hide()
            except:
                pass
        self.Hide()

    def OnPressEscapeKey(self):
        self.Close()
        return True

    # ================================================================
    #  UI HELPER FACTORIES - Pattern pulito, trackano tutti i widget
    # ================================================================
    def __Bar(self, parent, x, y, w, h, color):
        """Crea una Bar e la tracka per cleanup."""
        b = ui.Bar()
        b.SetParent(parent)
        b.SetPosition(x, y)
        b.SetSize(w, h)
        b.SetColor(color)
        b.AddFlag("not_pick")
        b.Show()
        self._allBars.append(b)
        return b

    def __Text(self, parent, x, y, text, color, center=False, outline=False):
        """Crea un TextLine e lo tracka per cleanup."""
        t = ui.TextLine()
        t.SetParent(parent)
        t.SetPosition(x, y)
        if center:
            t.SetHorizontalAlignCenter()
        t.SetText(text)
        t.SetPackedFontColor(color)
        if outline:
            t.SetOutline()
        t.AddFlag("not_pick")
        t.Show()
        self._allTexts.append(t)
        return t

    def __MakeBorder(self, parent, x, y, w, h, color):
        """Crea 4 barre bordo sul parent e le tracka."""
        self.__Bar(parent, x, y, w, 1, color)           # top
        self.__Bar(parent, x, y + h - 1, w, 1, color)   # bottom
        self.__Bar(parent, x, y, 1, h, color)            # left
        self.__Bar(parent, x + w - 1, y, 1, h, color)   # right

    def __MakeBorderOn(self, parent, x, y, w, h, color):
        """Crea bordi su un widget qualsiasi (con track per cleanup)."""
        for pos, sz in [((x, y), (w, 1)), ((x, y + h - 1), (w, 1)),
                        ((x, y), (1, h)), ((x + w - 1, y), (1, h))]:
            b = ui.Bar()
            b.SetParent(parent)
            b.SetPosition(pos[0], pos[1])
            b.SetSize(sz[0], sz[1])
            b.SetColor(color)
            b.AddFlag("not_pick")
            b.Show()
            self._allBars.append(b)

    # ================================================================
    #  NAVIGATION HISTORY
    # ================================================================
    def __PushNav(self):
        """Salva stato corrente nello stack di navigazione."""
        state = {
            "category": self.currentCategory,
            "search": self.searchInput.GetText() if self.searchInput else "",
            "selectedVnum": self._currentDetailVnum,
            "selectedType": self._currentDetailType,
        }
        self._navStack.append(state)
        if len(self._navStack) > NAV_STACK_MAX:
            self._navStack = self._navStack[-NAV_STACK_MAX:]
        self.__UpdateBackButton()

    def __PopNav(self):
        """Ripristina stato precedente dalla cronologia."""
        if not self._navStack:
            return
        state = self._navStack.pop()
        self.__UpdateBackButton()

        oldCat = state.get("category", "BOSS")
        oldSearch = state.get("search", "")
        selVnum = state.get("selectedVnum", 0)
        selType = state.get("selectedType", -1)

        if oldCat != self.currentCategory:
            self.currentCategory = oldCat
            self.__UpdateCategoryButtons()

        if self.searchInput:
            self.searchInput.SetText(oldSearch)
        self.__DoSearch()

        # Ripristina dettagli se presenti
        if selVnum > 0:
            if selType == 1:
                self.__ShowMobDetails(selVnum)
            elif selType == 0:
                self.__ShowItemDetails(selVnum)

    def __OnBackClick(self):
        """Handler per bottone indietro."""
        self.__PopNav()

    def __UpdateBackButton(self):
        """Mostra/nasconde il bottone indietro in base allo stack."""
        if self.btnBack:
            if self._navStack:
                self.btnBack.Show()
            else:
                self.btnBack.Hide()

    def __ResetDetailArea(self):
        """Resetta il pannello dettagli (quando si cambia categoria o si pulisce)."""
        # Chiudi popup refine se aperto
        if self.refinePopup:
            self.refinePopup.Close()

        # Nascondi pulsante fisso upgrade table
        if self.upgradeTableBtn:
            self.upgradeTableBtn.Hide()
        self._upgradeTableVnum = 0

        if self.dropList:
            self.dropList.RemoveAllItems()
        if self.dropScrollBar:
            self.dropScrollBar.SetPos(0.0)
        if self.infoLabel:
            self.infoLabel.SetText("Seleziona un elemento")
            self.infoLabel.SetPackedFontColor(COLOR_TEXT_GOLD)
        if self.infoSubLabel:
            self.infoSubLabel.SetText("")
        if self.detailHeaderLabel:
            self.detailHeaderLabel.SetText("")
        # Nascondi preview item e 3D
        if self.itemPreviewPanel:
            self.itemPreviewPanel.Hide()
        try:
            renderTarget.SetVisibility(RENDER_TARGET_INDEX, False)
        except:
            pass
        if self.renderTargetWnd:
            self.renderTargetWnd.Show()
        if self.previewNameLabel:
            self.previewNameLabel.SetText("")
        if hasattr(self, 'previewSubLabel') and self.previewSubLabel:
            self.previewSubLabel.SetText("")
        # Resetta preview item text lines
        if hasattr(self, 'itemPreviewName') and self.itemPreviewName:
            self.itemPreviewName.SetText("")
        if hasattr(self, 'itemPreviewUpgradeText') and self.itemPreviewUpgradeText:
            self.itemPreviewUpgradeText.SetText("")
        if hasattr(self, '_itemPreviewInfoLines'):
            for ol in self._itemPreviewInfoLines:
                if ol:
                    ol.SetText("")
        if hasattr(self, 'itemPreviewIcon') and self.itemPreviewIcon:
            self.itemPreviewIcon.SetItemSlot(0, 0, 0)
            self.itemPreviewIcon.RefreshSlot()
        self._currentDetailVnum = 0
        self._currentDetailType = -1
        self._navStack = []
        self.__HideToolTip()
        self.__UpdateBackButton()

    def __UpdateDetailHeader(self, text):
        """Aggiorna l'header della sezione dettagli."""
        if self.detailHeaderLabel:
            self.detailHeaderLabel.SetText(text)

    def __RefreshSidebarStats(self):
        """Aggiorna le statistiche nella sidebar dopo il caricamento dati."""
        if hasattr(self, "statMobText") and self.statMobText:
            self.statMobText.SetText("Mob: %d" % len(DATA_MGR.mob_drops))
        if hasattr(self, "statItemText") and self.statItemText:
            self.statItemText.SetText("Items: %d" % len(DATA_MGR.item_models))
        if hasattr(self, "statDropText") and self.statDropText:
            totalDrops = sum(len(v) for v in DATA_MGR.mob_drops.values())
            self.statDropText.SetText("Drop: %d" % totalDrops)
        if hasattr(self, "statRefineText") and self.statRefineText:
            DATA_MGR._EnsureRefineLoaded()
            self.statRefineText.SetText("Refine: %d" % len(DATA_MGR.item_refined_vnum))
        if hasattr(self, "statChestText") and self.statChestText:
            DATA_MGR._EnsureChestLoaded()
            self.statChestText.SetText("Forzieri: %d" % len(DATA_MGR.chest_contents))

    def __UpdateStatus(self, text):
        """Aggiorna la status bar."""
        if self.statusLabel:
            self.statusLabel.SetText(text)


# ============================================================================
#  WINDOW MANAGER GLOBALE
# ============================================================================
_wikiWindow = None

def OpenWindow():
    """Apre (o crea) la finestra Wiki."""
    global _wikiWindow
    if _wikiWindow is None:
        _wikiWindow = WikiWindow()
    _wikiWindow.Open()

def CloseWindow():
    """Chiude la finestra Wiki."""
    global _wikiWindow
    if _wikiWindow:
        _wikiWindow.Close()

def DestroyWindow():
    """Distrugge completamente la finestra Wiki (anti-leak)."""
    global _wikiWindow
    if _wikiWindow:
        _wikiWindow.Destroy()
        _wikiWindow = None

def GetWikiWindow():
    """Ritorna l'istanza della Wiki (o None)."""
    global _wikiWindow
    return _wikiWindow

def OpenSearchByVnum(vnum):
    """Apre la Wiki e cerca un item per VNUM. Usato da CTRL+J."""
    global _wikiWindow
    if _wikiWindow is None:
        _wikiWindow = WikiWindow()
    _wikiWindow.SearchByVnum(vnum)

def ToggleWindow():
    """Apri/chiudi la Wiki. Usato dal tasto J."""
    global _wikiWindow
    if _wikiWindow and _wikiWindow.IsShow():
        CloseWindow()
    else:
        OpenWindow()

# Alias per compatibilita'
OpenHunterGuide = OpenWindow
