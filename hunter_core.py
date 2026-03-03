# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - CORE MODULE
#  Configurazioni, costanti, colori, mixin e utility condivise
#  "I alone level up." - Solo Leveling Style
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import wndMgr
import app
import os

# ═══════════════════════════════════════════════════════════════════════════════
#  CONFIG FILE PATH - Per persistenza posizioni finestre
# ═══════════════════════════════════════════════════════════════════════════════
HUNTER_CONFIG_FILE = "hunter_config.cfg"

# ═══════════════════════════════════════════════════════════════════════════════
#  POSIZIONI DEFAULT OTTIMIZZATE (basate su schermo 1920x1080)
#  Queste posizioni vengono calcolate dinamicamente in base allo schermo
# ═══════════════════════════════════════════════════════════════════════════════
# Layout pensato per evitare sovrapposizioni:
# - SINISTRA: Tips (basso), Notification (medio)
# - CENTRO: SystemMessage, Overtake, WhatIf
# - DESTRA: Rival (alto), Event (alto-medio), SpeedKill (medio), Defense (basso)
# - CENTRO-DESTRA: Emergency
DEFAULT_WINDOW_LAYOUT = {
    # Finestre a SINISTRA (margine 10px)
    "HunterTipsWindow":         {"x": 10,   "y": 0.65},   # 65% schermo, basso sinistra
    "HunterNotificationWindow": {"x": 10,   "y": 0.45},   # 45% schermo, medio sinistra
    "DailyMissionsWindow":      {"x": 10,   "y": 0.15},   # 15% schermo, alto sinistra
    
    # Finestre CENTRO
    "WhatIfChoiceWindow":       {"x": 0.5,  "y": 0.30},   # Centro, 30% dall'alto
    "OvertakeWindow":           {"x": 0.5,  "y": 0.18},   # Centro, 18% dall'alto
    
    # Finestre a DESTRA (margine dalla destra)
    "RivalTrackerWindow":       {"x": -250, "y": 10},     # Alto destra
    "EventStatusWindow":        {"x": -230, "y": 120},    # Sotto Rival
    "SpeedKillTimerWindow":     {"x": -340, "y": 200},    # Sotto Event
    "FractureDefenseWindow":    {"x": -400, "y": 340},    # Basso destra
    
    # Emergency - centro alto
    "EmergencyQuestWindow":     {"x": 0.5,  "y": 0.22},   # Centro, 22% dall'alto
    
    # Trial - centro
    "TrialStatusWindow":        {"x": 0.5,  "y": 0.5},    # Centro esatto
    
    # Eventi Schedule
    "EventsScheduleWindow":     {"x": 10,   "y": 0.10},   # Alto sinistra
}

def GetDefaultPosition(windowName, windowWidth, windowHeight):
    """Calcola la posizione default basata sullo schermo e sul layout predefinito"""
    screenW = wndMgr.GetScreenWidth()
    screenH = wndMgr.GetScreenHeight()
    
    layout = DEFAULT_WINDOW_LAYOUT.get(windowName)
    if layout:
        x = layout["x"]
        y = layout["y"]
        
        # Se x è una frazione (0.0-1.0), calcola posizione proporzionale centrata
        if isinstance(x, float) and 0 <= x <= 1:
            defaultX = int((screenW - windowWidth) * x)
        # Se x è negativo, è offset dalla destra
        elif x < 0:
            defaultX = screenW + x
        else:
            defaultX = int(x)
        
        # Stessa logica per y
        if isinstance(y, float) and 0 <= y <= 1:
            defaultY = int((screenH - windowHeight) * y)
        elif y < 0:
            defaultY = screenH + y
        else:
            defaultY = int(y)
        
        return (defaultX, defaultY)
    
    # Fallback: centro dello schermo
    return ((screenW - windowWidth) // 2, (screenH - windowHeight) // 2)

# ═══════════════════════════════════════════════════════════════════════════════
#  MEMORIA POSIZIONI FINESTRE (Session-based + File Persistence)
# ═══════════════════════════════════════════════════════════════════════════════
# Dizionario globale per memorizzare le posizioni delle finestre durante la sessione
WINDOW_POSITIONS = {}
_configLoaded = False

def _LoadConfigFile():
    """Carica le posizioni salvate dal file di configurazione"""
    global WINDOW_POSITIONS, _configLoaded
    if _configLoaded:
        return
    _configLoaded = True
    
    try:
        if os.path.exists(HUNTER_CONFIG_FILE):
            with open(HUNTER_CONFIG_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            # Formato: windowName_pos=x,y
                            if key.endswith('_pos') and ',' in value:
                                windowName = key[:-4]  # Rimuove "_pos"
                                coords = value.split(',')
                                if len(coords) == 2:
                                    try:
                                        x = int(coords[0])
                                        y = int(coords[1])
                                        WINDOW_POSITIONS[windowName] = (x, y)
                                    except ValueError:
                                        pass
    except Exception as e:
        pass  # Ignora errori di lettura

def _SaveConfigFile():
    """Salva tutte le posizioni nel file di configurazione"""
    try:
        with open(HUNTER_CONFIG_FILE, 'w') as f:
            f.write("# Hunter System Configuration\n")
            f.write("# Window positions (do not edit manually)\n\n")
            for windowName, (x, y) in WINDOW_POSITIONS.items():
                f.write("%s_pos=%d,%d\n" % (windowName, x, y))
    except Exception as e:
        pass  # Ignora errori di scrittura

def SaveWindowPosition(windowName, x, y):
    """Salva la posizione di una finestra (RAM + File)"""
    _LoadConfigFile()  # Assicura che il config sia caricato
    WINDOW_POSITIONS[windowName] = (x, y)
    _SaveConfigFile()  # Persiste su file

def GetWindowPosition(windowName, defaultX, defaultY):
    """Recupera la posizione salvata o ritorna il default"""
    _LoadConfigFile()  # Assicura che il config sia caricato
    return WINDOW_POSITIONS.get(windowName, (defaultX, defaultY))

def HasSavedPosition(windowName):
    """Verifica se esiste una posizione salvata"""
    _LoadConfigFile()  # Assicura che il config sia caricato
    return windowName in WINDOW_POSITIONS

def ResetAllWindowPositions():
    """Resetta tutte le posizioni salvate - Usato se un utente muove una finestra fuori schermo"""
    global WINDOW_POSITIONS, _configLoaded
    WINDOW_POSITIONS = {}
    _configLoaded = True
    # Elimina il file di configurazione
    try:
        if os.path.exists(HUNTER_CONFIG_FILE):
            os.remove(HUNTER_CONFIG_FILE)
    except:
        pass
    return True

def ResetWindowPosition(windowName):
    """Resetta la posizione di una singola finestra"""
    global WINDOW_POSITIONS
    _LoadConfigFile()
    if windowName in WINDOW_POSITIONS:
        del WINDOW_POSITIONS[windowName]
        _SaveConfigFile()
        return True
    return False

# ═══════════════════════════════════════════════════════════════════════════════
#  COLORI BASE DEL SISTEMA - SOLO LEVELING DEFINITIVE EDITION
# ═══════════════════════════════════════════════════════════════════════════════
COLOR_BG_DARK = 0xF0020208          # Sfondo quasi-nero con sfumatura blu profonda
COLOR_BG_DARK2 = 0xF5010105        # Sfondo ancora più scuro (header/footer)
COLOR_BG_HOVER = 0x33FFFFFF         # Hover leggero
COLOR_BG_INNER = 0xDD050510        # Sfondo interno elementi
COLOR_TEXT_NORMAL = 0xFFE8E8F8      # Bianco leggermente blu (più elegante)
COLOR_TEXT_MUTED = 0xFF888899       # Grigio-blu (più sofisticato)
COLOR_TEXT_DIM = 0xFF444455         # Testo quasi invisibile
COLOR_SEPARATOR = 0x33FFFFFF        # Linee separatrici semitrasparenti
COLOR_SEPARATOR_BRIGHT = 0x55FFFFFF # Separatori più visibili
COLOR_GOLD = 0xFFFFD700             # Oro standard
COLOR_GOLD_DIM = 0xFFCC9900         # Oro attenuato
COLOR_SYSTEM_BLUE = 0xFF00A8FF      # Blu sistema scanline
COLOR_SYSTEM_CYAN = 0xFF00EEFF      # Ciano sistema brillante

# Colori per Rank Hunter
RANK_COLORS = {
    "E": 0xFF808080,  # Grigio - Iniziato
    "D": 0xFF00FF00,  # Verde - Apprendista
    "C": 0xFF00FFFF,  # Ciano - Cacciatore
    "B": 0xFF0066FF,  # Blu - Veterano
    "A": 0xFFAA00FF,  # Viola - Elite
    "S": 0xFFFF6600,  # Arancione - Leggenda
    "N": 0xFFFF0000,  # Rosso - Monarca Nazionale
}

RANK_NAMES = {
    "E": "Iniziato",
    "D": "Apprendista", 
    "C": "Cacciatore",
    "B": "Veterano",
    "A": "Elite",
    "S": "Campione",
    "N": "Nazionale",
}

RANK_TITLES = {
    "E": "Il Risvegliato",
    "D": "Il Sopravvissuto",
    "C": "Il Cacciatore",
    "B": "L'Elite",
    "A": "Il Predatore",
    "S": "La Leggenda",
    "N": "Il Monarca delle Ombre",
}

RANK_QUOTES = {
    "E": '"Ogni viaggio inizia con un passo."',
    "D": '"Hai superato i più deboli."',
    "C": '"Il tuo nome inizia a farsi conoscere."',
    "B": '"I Gate tremano al tuo arrivo."',
    "A": '"Solo i folli osano sfidarti."',
    "S": '"Sei tra i più forti dell\'umanità."',
    "N": '"IO SONO IL MONARCA."',
}

# Schemi colori per Fratture e Codici Colore – SOLO LEVELING DEFINITIVE
COLOR_SCHEMES = {
    "GREEN": {
        "border": 0xFF00FF44,       # Verde Neon Smeraldo
        "border_dim": 0xFF004422,
        "glow": 0x4800FF44,
        "title": 0xFF66FF88,
        "text": 0xFFCCFFDD,
        "accent": 0xFF00FF44,
        "accent_dim": 0xFF00AA33,
        "bg": 0xFF020A04,
    },
    "BLUE": {
        "border": 0xFF00AAFF,       # Blu Azzurro Intenso
        "border_dim": 0xFF003355,
        "glow": 0x4800AAFF,
        "title": 0xFF55CCFF,
        "text": 0xFFCCEEFF,
        "accent": 0xFF00AAFF,
        "accent_dim": 0xFF006688,
        "bg": 0xFF020810,
    },
    "ORANGE": {
        "border": 0xFFFF7700,       # Arancione Fuoco Intenso
        "border_dim": 0xFF552200,
        "glow": 0x48FF7700,
        "title": 0xFFFFBB44,
        "text": 0xFFFFDDBB,
        "accent": 0xFFFF7700,
        "accent_dim": 0xFF994400,
        "bg": 0xFF100500,
    },
    "RED": {
        "border": 0xFFFF1111,       # Rosso Sangue Puro
        "border_dim": 0xFF550000,
        "glow": 0x48FF1111,
        "title": 0xFFFF5555,
        "text": 0xFFFFCCCC,
        "accent": 0xFFFF1111,
        "accent_dim": 0xFF880000,
        "bg": 0xFF0C0000,
    },
    "GOLD": {
        "border": 0xFFFFD700,       # Oro Reale
        "border_dim": 0xFF664400,
        "glow": 0x48FFD700,
        "title": 0xFFFFEE66,
        "text": 0xFFFFF5CC,
        "accent": 0xFFFFD700,
        "accent_dim": 0xFFAA8800,
        "bg": 0xFF100C00,
    },
    "PURPLE": {
        "border": 0xFFBB00FF,       # Viola Mistico Profondo
        "border_dim": 0xFF440055,
        "glow": 0x48BB00FF,
        "title": 0xFFDD66FF,
        "text": 0xFFEECCFF,
        "accent": 0xFFBB00FF,
        "accent_dim": 0xFF770099,
        "bg": 0xFF080010,
    },
    "CYAN": {
        "border": 0xFF00FFFF,       # Ciano Cristallo
        "border_dim": 0xFF004455,
        "glow": 0x4800FFFF,
        "title": 0xFF66FFFF,
        "text": 0xFFCCFFFF,
        "accent": 0xFF00FFFF,
        "accent_dim": 0xFF008888,
        "bg": 0xFF020C10,
    },
    "BLACKWHITE": {
        "border": 0xFFDDDDDD,       # Bianco Argentato
        "border_dim": 0xFF444444,
        "glow": 0x48FFFFFF,
        "title": 0xFFEEEEEE,
        "text": 0xFFCCCCCC,
        "accent": 0xFFDDDDDD,
        "accent_dim": 0xFF666666,
        "bg": 0xFF080808,
    },
    "SYSTEM": {
        "border": 0xFF00CCFF,       # Azzurro Sistema Vibrante
        "border_dim": 0xFF004466,
        "glow": 0x4800CCFF,
        "title": 0xFF44DDFF,
        "text": 0xFFCCEEFF,
        "accent": 0xFF00CCFF,
        "accent_dim": 0xFF006688,
        "bg": 0xFF020A14,
    },
}

# Schema default
DEFAULT_SCHEME = COLOR_SCHEMES["PURPLE"]

# Mappatura ID Frattura -> Colore
FRACTURE_ID_MAP = {
    "16060": "GREEN",       # Frattura Primordiale
    "16061": "BLUE",        # Frattura Astrale
    "16062": "ORANGE",      # Frattura Abissale
    "16063": "RED",         # Frattura Cremisi
    "16064": "GOLD",        # Frattura Aurea
    "16065": "PURPLE",      # Frattura Infausta
    "16066": "BLACKWHITE",  # Frattura del Giudizio
    "power_offer": "PURPLE",
    "save_npc": "BLUE",
    "dark_pact": "RED",
    "rival_mercy": "ORANGE",
    "treasure_split": "GOLD",
}


# ═══════════════════════════════════════════════════════════════════════════════
#  FUNZIONI UTILITY
# ═══════════════════════════════════════════════════════════════════════════════

def GetRankColor(rank):
    """Ritorna il colore per un rank specifico"""
    return RANK_COLORS.get(rank, 0xFFFFFFFF)

def GetColorScheme(colorCode):
    """Ritorna lo schema colori per un codice (GREEN, BLUE, etc.)"""
    if colorCode:
        return COLOR_SCHEMES.get(colorCode.upper(), DEFAULT_SCHEME)
    return DEFAULT_SCHEME

def GetColorFromKey(colorKey):
    """Converte chiave colore (E,D,C,BLUE,GREEN...) in intero"""
    # Prova prima i colori scheme
    scheme = COLOR_SCHEMES.get(colorKey.upper() if colorKey else "", None)
    if scheme:
        return scheme["border"]
    # Prova i rank
    return RANK_COLORS.get(colorKey, 0xFF808080)

def DetectColorFromText(text, defaultColor="PURPLE"):
    """Auto-detect colore dal testo (per fratture)"""
    if not text:
        return defaultColor
    upperText = text.upper()
    if "PRIMORDIALE" in upperText: return "GREEN"
    if "ASTRALE" in upperText: return "BLUE"
    if "ABISSALE" in upperText: return "ORANGE"
    if "CREMISI" in upperText: return "RED"
    if "AUREA" in upperText: return "GOLD"
    if "INFAUSTA" in upperText: return "PURPLE"
    if "GIUDIZIO" in upperText or "INSTABILE" in upperText: return "BLACKWHITE"
    return defaultColor

def FormatNumber(num):
    """Formatta un numero con separatori migliaia"""
    s = str(int(num))
    r = ""
    while len(s) > 3:
        r = "." + s[-3:] + r
        s = s[:-3]
    return s + r

def FormatTime(seconds):
    """Formatta secondi in MM:SS o HH:MM:SS"""
    if seconds < 0:
        return "00:00"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return "%02d:%02d:%02d" % (h, m, s)
    return "%02d:%02d" % (m, s)


# ═══════════════════════════════════════════════════════════════════════════════
#  MIXIN PER FINESTRE MOVIBILI
# ═══════════════════════════════════════════════════════════════════════════════
class DraggableMixin:
    """
    Mixin che aggiunge funzionalità di drag a qualsiasi finestra.
    Memorizza automaticamente la posizione durante la sessione.
    
    Uso:
        class MyWindow(ui.Window, DraggableMixin):
            def __init__(self):
                ui.Window.__init__(self)
                self.InitDraggable("MyWindow", defaultX, defaultY)
    """
    
    def InitDraggable(self, windowName, defaultX=None, defaultY=None):
        """Inizializza il sistema di drag per questa finestra"""
        self.windowName = windowName
        self.isDragging = False
        self.dragOffsetX = 0
        self.dragOffsetY = 0
        
        # Imposta flag movable e float
        if hasattr(self, 'AddFlag'):
            self.AddFlag("movable")
            self.AddFlag("float")
        
        # Recupera posizione salvata o usa default
        if defaultX is not None and defaultY is not None:
            savedX, savedY = GetWindowPosition(windowName, defaultX, defaultY)
            self.SetPosition(savedX, savedY)
    
    def OnMouseLeftButtonDown(self):
        """Inizia il drag"""
        self.isDragging = True
        mouseX, mouseY = wndMgr.GetMousePosition()
        winX, winY = self.GetGlobalPosition()
        self.dragOffsetX = mouseX - winX
        self.dragOffsetY = mouseY - winY
        return True
    
    def OnMouseLeftButtonUp(self):
        """Termina il drag e salva la posizione"""
        if self.isDragging:
            self.isDragging = False
            x, y = self.GetGlobalPosition()
            SaveWindowPosition(self.windowName, x, y)
        return True
    
    def OnMouseDrag(self, x, y):
        """Gestisce il movimento durante il drag"""
        if self.isDragging:
            mouseX, mouseY = wndMgr.GetMousePosition()
            newX = mouseX - self.dragOffsetX
            newY = mouseY - self.dragOffsetY
            
            # Limita alla schermata
            screenW = wndMgr.GetScreenWidth()
            screenH = wndMgr.GetScreenHeight()
            winW, winH = self.GetWidth(), self.GetHeight()
            
            newX = max(0, min(newX, screenW - winW))
            newY = max(0, min(newY, screenH - winH))
            
            self.SetPosition(newX, newY)
        return True
    
    def RestorePosition(self):
        """Ripristina la posizione salvata"""
        if hasattr(self, 'windowName'):
            pos = WINDOW_POSITIONS.get(self.windowName)
            if pos:
                self.SetPosition(pos[0], pos[1])


# ═══════════════════════════════════════════════════════════════════════════════
#  RANK THEMES - Schema colori SOLO LEVELING STYLE
#  Design ispirato al manhwa: toni scuri con accenti neon brillanti
#  Ogni rank ha una palette unica che riflette il suo potere
# ═══════════════════════════════════════════════════════════════════════════════
RANK_THEMES = {
    # ─────────────────────────────────────────────────────────────────────────────
    # E-RANK: "Il Risvegliato" - Grigi profondi, umiltà dell'inizio
    # Rappresenta l'inizio del viaggio, quando Sung Jin-Woo era il piu' debole
    # ─────────────────────────────────────────────────────────────────────────────
    "E": {
        "name": "E-Rank",
        "title": "Risvegliato",
        "subtitle": "Il Piu' Debole",
        "min": 0,
        "max": 2000,
        # Sfondi profondi con sfumatura grigio-blu
        "bg_dark": 0xF8030305,
        "bg_medium": 0xF50C0C12,
        "bg_light": 0xF5141420,
        # Bordi e accenti grigi – più contrasto
        "border": 0xFF5A5A6A,
        "border_inner": 0xFF333340,
        "accent": 0xFF7878A0,
        "accent_bright": 0xFFAAAAAA,
        # Testi
        "text_title": 0xFF9898B8,
        "text_value": 0xFFBBBBCC,
        "text_muted": 0xFF444455,
        # Barre e effetti
        "bar_fill": 0xFF6060A0,
        "bar_bg": 0xFF0E0E1A,
        "glow": 0x30505070,
        "glow_strong": 0x55606080,
        "pulse_color": 0xFF7070A0,
        # Bottoni
        "btn_normal": 0xFF18181E,
        "btn_hover": 0xFF24242E,
        "btn_down": 0xFF30303A,
        "btn_border": 0xFF5A5A6A,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # D-RANK: "L'Apprendista" - Verde neon brillante, speranza che germoglia
    # Il primo passo verso la crescita
    # ─────────────────────────────────────────────────────────────────────────────
    "D": {
        "name": "D-Rank",
        "title": "Apprendista",
        "subtitle": "Il Sopravvissuto",
        "min": 2000,
        "max": 10000,
        # Sfondi profondi con sfumatura verde-smeraldo
        "bg_dark": 0xF8020A02,
        "bg_medium": 0xF5061406,
        "bg_light": 0xF50A1E0A,
        # Bordi e accenti verde neon più intenso
        "border": 0xFF00CC00,
        "border_inner": 0xFF004400,
        "accent": 0xFF00FF44,
        "accent_bright": 0xFF66FF88,
        # Testi
        "text_title": 0xFF44FF66,
        "text_value": 0xFFAAFFBB,
        "text_muted": 0xFF1A5522,
        # Barre e effetti
        "bar_fill": 0xFF00EE44,
        "bar_bg": 0xFF081A08,
        "glow": 0x3800EE44,
        "glow_strong": 0x6500EE44,
        "pulse_color": 0xFF00FF44,
        # Bottoni
        "btn_normal": 0xFF060F06,
        "btn_hover": 0xFF0A1E0A,
        "btn_down": 0xFF102810,
        "btn_border": 0xFF00CC00,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # C-RANK: "Il Cacciatore" - Ciano elettrico, competenza riconosciuta
    # Un vero cacciatore che ha dimostrato il suo valore
    # ─────────────────────────────────────────────────────────────────────────────
    "C": {
        "name": "C-Rank",
        "title": "Cacciatore",
        "subtitle": "Il Riconosciuto",
        "min": 10000,
        "max": 50000,
        # Sfondi profondi con sfumatura ciano-oceano
        "bg_dark": 0xF8020A10,
        "bg_medium": 0xF5061520,
        "bg_light": 0xF50A2030,
        # Bordi e accenti ciano neon ultra-brillante
        "border": 0xFF00DDFF,
        "border_inner": 0xFF004455,
        "accent": 0xFF00FFFF,
        "accent_bright": 0xFF88FFFF,
        # Testi
        "text_title": 0xFF55FFFF,
        "text_value": 0xFFBBFFFF,
        "text_muted": 0xFF1A4466,
        # Barre e effetti
        "bar_fill": 0xFF00EEFF,
        "bar_bg": 0xFF081828,
        "glow": 0x4000EEFF,
        "glow_strong": 0x7000EEFF,
        "pulse_color": 0xFF00FFFF,
        # Bottoni
        "btn_normal": 0xFF060F18,
        "btn_hover": 0xFF0A1E28,
        "btn_down": 0xFF102838,
        "btn_border": 0xFF00DDFF,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # B-RANK: "Il Veterano" - Blu reale, autorità indiscussa
    # Un cacciatore esperto rispettato da tutti
    # ─────────────────────────────────────────────────────────────────────────────
    "B": {
        "name": "B-Rank",
        "title": "Veterano",
        "subtitle": "L'Esperto",
        "min": 50000,
        "max": 150000,
        # Sfondi profondi con sfumatura blu-zaffiro
        "bg_dark": 0xF8020218,
        "bg_medium": 0xF5060628,
        "bg_light": 0xF50A0A38,
        # Bordi e accenti blu elettrico ultravibrante
        "border": 0xFF1177FF,
        "border_inner": 0xFF002255,
        "accent": 0xFF55AAFF,
        "accent_bright": 0xFF88CCFF,
        # Testi
        "text_title": 0xFF77BBFF,
        "text_value": 0xFFBBDDFF,
        "text_muted": 0xFF223366,
        # Barre e effetti
        "bar_fill": 0xFF1188FF,
        "bar_bg": 0xFF080828,
        "glow": 0x451188FF,
        "glow_strong": 0x751188FF,
        "pulse_color": 0xFF55AAFF,
        # Bottoni
        "btn_normal": 0xFF060620,
        "btn_hover": 0xFF0A0A30,
        "btn_down": 0xFF101040,
        "btn_border": 0xFF1177FF,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # A-RANK: "Il Maestro" - Viola mistico profondo, élite dell'umanità
    # Tra i migliori cacciatori del mondo
    # ─────────────────────────────────────────────────────────────────────────────
    "A": {
        "name": "A-Rank",
        "title": "Maestro",
        "subtitle": "L'Elite",
        "min": 150000,
        "max": 500000,
        # Sfondi profondi con sfumatura viola-indaco
        "bg_dark": 0xF8060210,
        "bg_medium": 0xF50E0520,
        "bg_light": 0xF5160830,
        # Bordi e accenti viola ultra-brillante
        "border": 0xFFBB00FF,
        "border_inner": 0xFF440033,
        "accent": 0xFFDD55FF,
        "accent_bright": 0xFFEE99FF,
        # Testi
        "text_title": 0xFFEE88FF,
        "text_value": 0xFFF5CCFF,
        "text_muted": 0xFF551188,
        # Barre e effetti
        "bar_fill": 0xFFCC33FF,
        "bar_bg": 0xFF120630,
        "glow": 0x50CC00FF,
        "glow_strong": 0x80CC00FF,
        "pulse_color": 0xFFDD55FF,
        # Bottoni
        "btn_normal": 0xFF0E0620,
        "btn_hover": 0xFF160A30,
        "btn_down": 0xFF1E0E40,
        "btn_border": 0xFFBB00FF,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # S-RANK: "La Leggenda" - Oro-Arancione infuocato, gloria suprema
    # Tra i più forti dell'umanità – il loro nome è conosciuto da tutti
    # ─────────────────────────────────────────────────────────────────────────────
    "S": {
        "name": "S-Rank",
        "title": "Leggenda",
        "subtitle": "Il Prescelto",
        "min": 500000,
        "max": 1500000,
        # Sfondi profondi con sfumatura ambra-bruciata
        "bg_dark": 0xF8100602,
        "bg_medium": 0xF5200C04,
        "bg_light": 0xF5301408,
        # Bordi e accenti fuoco-oro ultraintensivo
        "border": 0xFFFF7700,
        "border_inner": 0xFF662200,
        "accent": 0xFFFFBB00,
        "accent_bright": 0xFFFFDD66,
        # Testi
        "text_title": 0xFFFFCC66,
        "text_value": 0xFFFFEEBB,
        "text_muted": 0xFF773311,
        # Barre e effetti
        "bar_fill": 0xFFFF8800,
        "bar_bg": 0xFF281406,
        "glow": 0x60FF7700,
        "glow_strong": 0x99FF7700,
        "pulse_color": 0xFFFFBB00,
        # Bottoni
        "btn_normal": 0xFF1C1004,
        "btn_hover": 0xFF2C1A08,
        "btn_down": 0xFF3C240C,
        "btn_border": 0xFFFF7700,
    },
    # ─────────────────────────────────────────────────────────────────────────────
    # N-RANK: "Il Monarca" - Rosso sangue / Nero assoluto
    # Ispirato al Re delle Ombre - Sung Jin-Woo nella sua forma finale
    # POTERE ASSOLUTO - il buio che ingoia tutto
    # ─────────────────────────────────────────────────────────────────────────────
    "N": {
        "name": "MONARCA",
        "title": "Monarca Nazionale",
        "subtitle": "Re delle Ombre",
        "min": 1500000,
        "max": 9999999,
        # Sfondi quasi-neri puri con sfumatura sangue
        "bg_dark": 0xFF050101,
        "bg_medium": 0xFF0C0303,
        "bg_light": 0xFF140505,
        # Bordi e accenti rosso sangue – MASSIMA INTENSITA'
        "border": 0xFFEE0000,
        "border_inner": 0xFF550000,
        "accent": 0xFFFF3333,
        "accent_bright": 0xFFFF6666,
        # Testi
        "text_title": 0xFFFF5555,
        "text_value": 0xFFFFBBBB,
        "text_muted": 0xFF661111,
        # Barre e effetti – EPICITÀ TOTALE
        "bar_fill": 0xFFFF1111,
        "bar_bg": 0xFF180606,
        "glow": 0x70FF0000,
        "glow_strong": 0xAAFF0000,
        "pulse_color": 0xFFFF3333,
        # Bottoni
        "btn_normal": 0xFF180404,
        "btn_hover": 0xFF280808,
        "btn_down": 0xFF380C0C,
        "btn_border": 0xFFEE0000,
    },
}

def GetRankKey(points):
    """Determina il rank basato sui punti gloria"""
    if points >= 1500000:
        return "N"
    elif points >= 500000:
        return "S"
    elif points >= 150000:
        return "A"
    elif points >= 50000:
        return "B"
    elif points >= 10000:
        return "C"
    elif points >= 2000:
        return "D"
    return "E"

def GetRankTheme(points):
    """Ritorna il tema completo per un dato punteggio"""
    key = GetRankKey(points)
    return RANK_THEMES[key]

def GetRankProgress(points):
    """Calcola la percentuale di progresso verso il prossimo rank"""
    key = GetRankKey(points)
    theme = RANK_THEMES[key]
    if points >= theme["max"]:
        return 100.0
    rangeSize = float(theme["max"] - theme["min"])
    if rangeSize <= 0:
        return 100.0
    progress = float(points - theme["min"]) / rangeSize * 100
    return min(100, max(0, progress))


# ═══════════════════════════════════════════════════════════════════════════════
#  AWAKENING CONFIGURATION - Livelli speciali con effetti epici
# ═══════════════════════════════════════════════════════════════════════════════
AWAKENING_CONFIG = {
    5: {
        "name": "RISVEGLIO",
        "subtitle": "Il Sistema ti ha scelto",
        "quote": '"Benvenuto, Cacciatore."',
        "color": 0xFF4A90D9,
        "duration": 6.0,
        "effect": "system_boot",
        "tip": "Premi [N] per scegliere le tue abilità",
        "sound_intensity": 1,
    },
    10: {
        "name": "PRIMA EVOLUZIONE",
        "subtitle": "Il tuo potere si manifesta",
        "quote": '"Stai diventando più forte."',
        "color": 0xFF00FF88,
        "duration": 5.0,
        "effect": "power_surge",
        "sound_intensity": 1,
    },
    15: {
        "name": "ADATTAMENTO",
        "subtitle": "Il corpo si adatta al potere",
        "quote": '"Il dolore forgia la forza."',
        "color": 0xFF00FFAA,
        "duration": 5.0,
        "effect": "adaptation",
        "sound_intensity": 1,
    },
    20: {
        "name": "RISONANZA",
        "subtitle": "L'energia fluisce liberamente",
        "quote": '"Senti il potere dentro di te?"',
        "color": 0xFF00FFFF,
        "duration": 5.5,
        "effect": "resonance",
        "sound_intensity": 2,
    },
    25: {
        "name": "MANIFESTAZIONE",
        "subtitle": "Il tuo potere prende forma",
        "quote": '"Non sei più un novizio."',
        "color": 0xFF00DDFF,
        "duration": 5.5,
        "effect": "manifestation",
        "sound_intensity": 2,
    },
    30: {
        "name": "SISTEMA ATTIVATO",
        "subtitle": "Accesso al Terminale Hunter",
        "quote": '"Il Sistema si espande per te."',
        "color": 0xFF0088FF,
        "duration": 8.0,
        "effect": "terminal_unlock",
        "tip": "Il [TERMINALE] è ora disponibile",
        "sound_intensity": 3,
    },
    40: {
        "name": "CONSOLIDAMENTO",
        "subtitle": "Il potere si stabilizza",
        "quote": '"La crescita non si ferma mai."',
        "color": 0xFF0066FF,
        "duration": 5.0,
        "effect": "consolidation",
        "sound_intensity": 2,
    },
    50: {
        "name": "METÀ DEL CAMMINO",
        "subtitle": "Hai percorso metà della via",
        "quote": '"Ma il vero viaggio inizia ora."',
        "color": 0xFFAA00FF,
        "duration": 6.0,
        "effect": "halfway",
        "sound_intensity": 2,
    },
    60: {
        "name": "MATURAZIONE",
        "subtitle": "Il tuo potere matura",
        "quote": '"I deboli iniziano a temerti."',
        "color": 0xFFBB00FF,
        "duration": 5.5,
        "effect": "maturation",
        "sound_intensity": 2,
    },
    70: {
        "name": "RISVEGLIO AVANZATO",
        "subtitle": "Oltre i limiti ordinari",
        "quote": '"Vedi cose che altri non possono vedere."',
        "color": 0xFFFF6600,
        "duration": 6.0,
        "effect": "advanced_awakening",
        "sound_intensity": 3,
    },
    80: {
        "name": "MAESTRIA",
        "subtitle": "Il controllo è assoluto",
        "quote": '"Il potere è nulla senza controllo."',
        "color": 0xFFFF8800,
        "duration": 5.5,
        "effect": "mastery",
        "sound_intensity": 3,
    },
    90: {
        "name": "SOGLIA LEGGENDARIA",
        "subtitle": "Pochi arrivano fin qui",
        "quote": '"Sei degno del tuo titolo."',
        "color": 0xFFFF0000,
        "duration": 7.0,
        "effect": "legendary_threshold",
        "sound_intensity": 3,
    },
    100: {
        "name": "CENTENARIO",
        "subtitle": "Un secolo di potere",
        "quote": '"ARISE."',
        "color": 0xFFFFD700,
        "duration": 9.0,
        "effect": "centennial",
        "sound_intensity": 4,
    },
    110: {
        "name": "TRASCENDENZA",
        "subtitle": "Oltre ogni limite conosciuto",
        "quote": '"I limiti esistono solo per essere infranti."',
        "color": 0xFFFFE066,
        "duration": 7.0,
        "effect": "transcendence",
        "sound_intensity": 4,
    },
    120: {
        "name": "ASCENSIONE",
        "subtitle": "Non sei più umano",
        "quote": '"Io solo... avanzo."',
        "color": 0xFFFF00FF,
        "duration": 9.0,
        "effect": "ascension",
        "sound_intensity": 5,
    },
    130: {
        "name": "MONARCA",
        "subtitle": "Il Re delle Ombre",
        "quote": '"I ALONE LEVEL UP."',
        "color": 0xFF000000,
        "secondary_color": 0xFFFF0000,
        "duration": 12.0,
        "effect": "monarch",
        "sound_intensity": 5,
    },
}

def IsAwakeningLevel(level):
    """Controlla se un livello ha un awakening speciale"""
    return level in AWAKENING_CONFIG

def GetAwakeningConfig(level):
    """Ritorna la configurazione awakening per un livello"""
    return AWAKENING_CONFIG.get(level, None)
