import ui
import chr
import player
import net
import wndMgr
import app
import grp
import math

from hunter_components import _DimColor, _BrightenColor

# ==============================================================================
# HUNTER ENTITY FLOATING BOARD SYSTEM
# ==============================================================================
# Mostra testi fluttuanti sopra Bauli e Fratture (NPC).
# Colori basati sul COLOR CODE dell'entita' (dal DB).
# Sostituisce il vecchio sistema target.vid / target.pos (ping minimappa).
#
# Architettura:
#   - Auto-scan client via chr.GetInstanceList():
#     -> Fratture: VNUM 16060-16066
#     -> Bauli:    VNUM 63000-63007
#   - Board creata quando l'NPC e' nel range visivo del player.
#   - Auto-pulizia quando l'NPC muore/despawna (_IsValidEntity).
# ==============================================================================

# --- Dimensioni Board ---
BOARD_WIDTH = 270
BOARD_HEIGHT = 72
FADE_START = 1500.0
MAX_DIST = 3500.0
# Pre-computed squared distances (evita math.sqrt ogni frame)
FADE_START_SQ = FADE_START * FADE_START
MAX_DIST_SQ = MAX_DIST * MAX_DIST

# --- Cache metodo di proiezione 3D->2D (evita hasattr ogni frame) ---
# 0=none, 1=chr.GetProjectPosition, 2=grp.ProjectPosition, 3=wndMgr.ProjectPosition, 4=grp set/get legacy
_PROJECT_METHOD = 0
if hasattr(chr, "GetProjectPosition"):
	_PROJECT_METHOD = 1
elif hasattr(grp, "ProjectPosition"):
	_PROJECT_METHOD = 2
elif hasattr(wndMgr, "ProjectPosition"):
	_PROJECT_METHOD = 3
elif hasattr(grp, "SetProjectPosition") and hasattr(grp, "GetProjectPosition"):
	_PROJECT_METHOD = 4

# --- Fratture: VNUM -> Info (per auto-scan client) ---
# color_code dal DB: srv1_hunabku.hunter_quest_fractures
FRACTURE_VNUMS = {
	16060: {"rank": "E", "name": "Frattura Primordiale", "tier": 1, "color": "GREEN",      "req": "Nessun Requisito",         "req_pts": 0},
	16061: {"rank": "D", "name": "Frattura Astrale",     "tier": 2, "color": "BLUE",       "req": "2.000 Punti Gloria",       "req_pts": 2000},
	16062: {"rank": "C", "name": "Frattura Abissale",    "tier": 3, "color": "ORANGE",     "req": "10.000 Punti Gloria",      "req_pts": 10000},
	16063: {"rank": "B", "name": "Frattura Cremisi",     "tier": 4, "color": "RED",        "req": "Forza 100+",               "req_pts": 0},
	16064: {"rank": "A", "name": "Frattura Aurea",       "tier": 5, "color": "GOLD",       "req": "Forza 200+",               "req_pts": 0},
	16065: {"rank": "S", "name": "Frattura Infausta",    "tier": 6, "color": "PURPLE",     "req": "Forza 350+",               "req_pts": 0},
	16066: {"rank": "N", "name": "Frattura Instabile",   "tier": 7, "color": "BLACKWHITE", "req": "Forza 500+",               "req_pts": 0},
}

# --- Bauli: VNUM -> Info (per auto-scan client) ---
# color_code dal DB: srv1_hunabku.hunter_chest_rewards
CHEST_VNUMS = {
	63000: {"name": "Forziere Demoniaco",     "tier": 1, "color": "GREEN",      "glory": "126~256"},
	63001: {"name": "Forziere Elettrico",     "tier": 2, "color": "BLUE",       "glory": "180~360"},
	63002: {"name": "Forziere Glaciale",      "tier": 3, "color": "ORANGE",     "glory": "250~480"},
	63003: {"name": "Forziere Infernale",     "tier": 4, "color": "RED",        "glory": "350~650"},
	63004: {"name": "Forziere della Natura",  "tier": 5, "color": "GOLD",       "glory": "480~850"},
	63005: {"name": "Forziere degli Antichi", "tier": 6, "color": "PURPLE",     "glory": "650~1100"},
	63006: {"name": "Forziere di Ganesha",    "tier": 7, "color": "BLACKWHITE", "glory": "900~1500"},
	63007: {"name": "Forziere della Miniera", "tier": 1, "color": "PURPLE",     "glory": "856~3426"},
}

# --- Rank Tier Letter ---
TIER_LETTER = {1: "E", 2: "D", 3: "C", 4: "B", 5: "A", 6: "S", 7: "N"}


# ==============================================================================
# COLOR THEMES - Palette basate sul color_code del DB (rank_color)
# ==============================================================================
# Ogni entita' Hunter ha un colore assegnato nel DB (GREEN, BLUE, ORANGE, RED,
# GOLD, PURPLE, BLACKWHITE). Questi temi sostituiscono il vecchio TIER_ACCENT.
COLOR_THEMES = {
	"GREEN": {
		"bg_top":       0xF0010A01,
		"bg_bot":       0xF5000600,
		"border":       0xFF00FF44,
		"glow":         0x3000FF44,
		"text_main":    0xFFEEFFEE,
		"text_sub":     0xFF88FFAA,
		"inner_border": 0xFF005522,
		"accent_hex":   "00FF44",
	},
	"BLUE": {
		"bg_top":       0xF0010818,
		"bg_bot":       0xF5000510,
		"border":       0xFF00AAFF,
		"glow":         0x3000AAFF,
		"text_main":    0xFFEEF8FF,
		"text_sub":     0xFF88CCFF,
		"inner_border": 0xFF003366,
		"accent_hex":   "00AAFF",
	},
	"ORANGE": {
		"bg_top":       0xF0100600,
		"bg_bot":       0xF5060300,
		"border":       0xFFFF8800,
		"glow":         0x30FF8800,
		"text_main":    0xFFFFF8EE,
		"text_sub":     0xFFFFCC88,
		"inner_border": 0xFF663300,
		"accent_hex":   "FF8800",
	},
	"RED": {
		"bg_top":       0xF0100000,
		"bg_bot":       0xF5060000,
		"border":       0xFFFF2222,
		"glow":         0x30FF2222,
		"text_main":    0xFFFFF0F0,
		"text_sub":     0xFFFF9999,
		"inner_border": 0xFF660000,
		"accent_hex":   "FF2222",
	},
	"GOLD": {
		"bg_top":       0xF0100800,
		"bg_bot":       0xF5060400,
		"border":       0xFFFFD700,
		"glow":         0x30FFD700,
		"text_main":    0xFFFFFBEE,
		"text_sub":     0xFFFFEE88,
		"inner_border": 0xFF886600,
		"accent_hex":   "FFD700",
	},
	"PURPLE": {
		"bg_top":       0xF0080018,
		"bg_bot":       0xF5040010,
		"border":       0xFFBB00FF,
		"glow":         0x30BB00FF,
		"text_main":    0xFFF8EEFF,
		"text_sub":     0xFFCC88FF,
		"inner_border": 0xFF550099,
		"accent_hex":   "BB00FF",
	},
	"BLACKWHITE": {
		"bg_top":       0xF0101010,
		"bg_bot":       0xF5060606,
		"border":       0xFFDDDDDD,
		"glow":         0x30FFFFFF,
		"text_main":    0xFFFFFFFF,
		"text_sub":     0xFFCCCCCC,
		"inner_border": 0xFF444444,
		"accent_hex":   "DDDDDD",
	},
}

# Fallback per tier -> colore se il server non manda il colore
TIER_DEFAULT_COLOR = {
	1: "GREEN", 2: "BLUE", 3: "ORANGE", 4: "RED",
	5: "GOLD", 6: "PURPLE", 7: "BLACKWHITE",
}


# ==============================================================================
# COLOR UTILITIES
# ==============================================================================
def _get_colors(color_name):
	"""Ritorna la palette colori per un color_name (GREEN, BLUE, RED, etc.)"""
	return COLOR_THEMES.get(color_name, COLOR_THEMES["PURPLE"])

def _get_accent_hex(color_name):
	"""Ritorna l'hex accent per un color_name (senza 0x prefix)"""
	theme = COLOR_THEMES.get(color_name, COLOR_THEMES["PURPLE"])
	return theme.get("accent_hex", "AA44FF")


# ==============================================================================
# CONFIG FACTORY
# ==============================================================================
def MakeConfig(entity_type, name, tier, color_name=""):
	"""
	Costruisce il config dict per un HunterFloatingBoard.
	entity_type: "C" (Baule/NPC), "F" (Frattura/NPC)
	name:        Nome dell'entita'
	tier:        1-7
	color_name:  Nome colore dal DB (GREEN, BLUE, ORANGE, RED, GOLD, PURPLE, BLACKWHITE)
	"""
	tier = max(1, min(7, tier))
	rl = TIER_LETTER.get(tier, "E")
	
	# Colore: usa il color_name dal DB, fallback per tier
	if not color_name or color_name not in COLOR_THEMES:
		color_name = TIER_DEFAULT_COLOR.get(tier, "PURPLE")
	
	colors = _get_colors(color_name)
	accent_hex = _get_accent_hex(color_name)
	
	if entity_type == "C":
		return {
			"title": "|cFF" + accent_hex + "- BAULE -",
			"subtitles": [
				name,
				"[" + rl + "-Rank] Tesoro Scoperto!",
				"Click per Aprire",
				"|cFFFF4444Attenzione: Rubabile!",
			],
			"info_text": "BAULE [" + rl + "-Rank]\n\n" + name + "\n\nScrigno con ricompense " + rl + ".\n\n|cFFFFD700Contenuto:|r\n- Punti Gloria\n- Oggetti Rari\n- Materiali Cacciatore\n\n|cFFFF4444ATTENZIONE:|r\nPuo' essere rubato da altri\ngiocatori! Aprilo subito!",
			"height_offset": 280,
			"colors": colors,
			"entity_type": "C",
		}
	
	elif entity_type == "F":
		# Info specifica per frattura con requisiti
		frac_req = ""
		for vnum, finfo in FRACTURE_VNUMS.items():
			if finfo["rank"] == rl:
				frac_req = finfo.get("req", "")
				break
		if not frac_req:
			frac_req = "Verifica requisiti in gioco"
		
		return {
			"title": "|cFF" + accent_hex + "- FRATTURA -",
			"subtitles": [
				name,
				"[" + rl + "-Rank] Portale Attivo",
				"Prova del Gate in Attesa",
				"Requisito: " + frac_req,
			],
			"info_text": "FRATTURA [" + rl + "-Rank]\n\n" + name + "\n\nPortale dimensionale " + rl + ".\n\n|cFFFFD700Requisito Ingresso:|r\n" + frac_req + "\n\n|cFF00FF44Ricompense:|r\n- Gloria per completamento\n- Avanzamento Grado Hunter\n- Prova del Gate per Rank Up\n\nClick per interagire col portale.",
			"height_offset": 330,
			"colors": colors,
			"entity_type": "F",
		}
	
	# Fallback (non dovrebbe mai arrivare qui)
	return {
		"title": name,
		"subtitles": ["Entita' Hunter"],
		"info_text": name,
		"height_offset": 350,
		"colors": colors,
		"entity_type": "F",
	}


# ==============================================================================
# CUSTOM BUTTON (self-contained, stile tematico)
# ==============================================================================
class HunterButton(ui.Window):
	def __init__(self, parent, x, y, w, h, colors, text="?"):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.SetSize(w, h)
		self.colors = colors
		self.event_func = None
		self._borders = []
		
		# BG
		self.bg = ui.Bar()
		self.bg.SetParent(self)
		self.bg.SetPosition(0, 0)
		self.bg.SetSize(w, h)
		self.bg.SetColor(colors["bg_bot"])
		self.bg.AddFlag("not_pick")
		self.bg.Show()
		
		# Border
		for pos, sz in [((0, 0), (w, 1)), ((0, h - 1), (w, 1)), ((0, 0), (1, h)), ((w - 1, 0), (1, h))]:
			b = ui.Bar()
			b.SetParent(self)
			b.SetPosition(pos[0], pos[1])
			b.SetSize(sz[0], sz[1])
			b.SetColor(colors["border"])
			b.AddFlag("not_pick")
			b.Show()
			self._borders.append(b)
		
		# Label
		self.label = ui.TextLine()
		self.label.SetParent(self)
		self.label.SetWindowHorizontalAlignCenter()
		self.label.SetWindowVerticalAlignCenter()
		self.label.SetHorizontalAlignCenter()
		self.label.SetVerticalAlignCenter()
		self.label.SetText(text)
		self.label.SetPackedFontColor(colors["text_main"])
		self.label.AddFlag("not_pick")
		self.label.Show()
		
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def SetEvent(self, func):
		self.event_func = func

	def OnMouseLeftButtonUp(self):
		if self.event_func:
			self.event_func()
		return True


# ==============================================================================
# INFO BOARD POPUP (finestra info con "?" button)
# ==============================================================================
class HunterInfoBoard(ui.Window):
	def __init__(self, cfg):
		ui.Window.__init__(self)
		self.cfg = cfg
		self.colors = cfg["colors"]
		self._parts = []
		self._Build()

	def __del__(self):
		ui.Window.__del__(self)

	def _Build(self):
		W = 360
		
		# Calcola altezza dinamica in base al contenuto
		lines = self.cfg.get("info_text", "").split("\n")
		line_h = 17
		title_area = 48       # spazio per titolo + margine
		bottom_area = 42      # spazio per bottone CHIUDI + margine
		content_h = len(lines) * line_h
		H = title_area + content_h + bottom_area
		H = max(H, 160)       # minimo ragionevole
		
		self.SetSize(W, H)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")
		
		# BG gradient
		c_top = self.colors["bg_top"]
		c_bot = self.colors["bg_bot"]
		r1, g1, b1 = (c_top >> 16) & 0xFF, (c_top >> 8) & 0xFF, c_top & 0xFF
		r2, g2, b2 = (c_bot >> 16) & 0xFF, (c_bot >> 8) & 0xFF, c_bot & 0xFF
		
		steps = 4
		step_h = float(H) / steps
		for i in xrange(steps):
			bar = ui.Bar()
			bar.SetParent(self)
			bar.SetPosition(0, int(i * step_h))
			bar.SetSize(W, int(step_h) + 2)
			t = float(i) / max(1, steps - 1)
			r = int(r1 + (r2 - r1) * t)
			g = int(g1 + (g2 - g1) * t)
			b = int(b1 + (b2 - b1) * t)
			bar.SetColor((0xF0 << 24) | (r << 16) | (g << 8) | b)
			bar.Show()
			self._parts.append(bar)
		
		# Borders
		self._MakeBorder(0, 0, W, H, self.colors["border"])
		self._MakeBorder(2, 2, W - 4, H - 4, self.colors["inner_border"])
		
		# Title
		title = ui.TextLine()
		title.SetParent(self)
		title.SetPosition(0, 15)
		title.SetWindowHorizontalAlignCenter()
		title.SetHorizontalAlignCenter()
		title.SetText(self.cfg["title"])
		title.SetOutline()
		title.Show()
		self._parts.append(title)
		
		# Separatore sotto titolo
		sep = ui.Bar()
		sep.SetParent(self)
		sep.SetPosition(20, 38)
		sep.SetSize(W - 40, 1)
		sep.SetColor(self.colors["inner_border"])
		sep.Show()
		self._parts.append(sep)
		
		# Info text (multi-riga)
		y = title_area
		for line in lines:
			t = ui.TextLine()
			t.SetParent(self)
			t.SetPosition(0, y)
			t.SetWindowHorizontalAlignCenter()
			t.SetHorizontalAlignCenter()
			t.SetText(line)
			t.SetPackedFontColor(self.colors["text_main"])
			t.Show()
			self._parts.append(t)
			y += line_h
		
		# Close button (posizionato in basso)
		self.closeBtn = HunterButton(self, int(W / 2) - 40, H - 32, 80, 22, self.colors, "CHIUDI")
		self.closeBtn.SetEvent(self.Close)

	def _MakeBorder(self, x, y, w, h, color):
		# Bordi principali
		for pos, sz in [((x, y), (w, 1)), ((x, y + h - 1), (w, 1)), ((x, y), (1, h)), ((x + w - 1, y), (1, h))]:
			b = ui.Bar()
			b.SetParent(self)
			b.SetPosition(pos[0], pos[1])
			b.SetSize(sz[0], sz[1])
			b.SetColor(color)
			b.AddFlag("not_pick")
			b.Show()
			self._parts.append(b)
		# Corner ticks (4 orizzontali, leggeri)
		tickLen = 10
		colorDim = (color & 0x00FFFFFF) | 0x66000000
		for (cx, cy, cw, ch) in [
			(x + 1, y, tickLen, 1), (x + w - tickLen - 1, y, tickLen, 1),
			(x + 1, y + h - 1, tickLen, 1), (x + w - tickLen - 1, y + h - 1, tickLen, 1),
		]:
			ct = ui.Bar(); ct.SetParent(self); ct.SetPosition(cx, cy); ct.SetSize(cw, ch); ct.SetColor(colorDim); ct.AddFlag("not_pick"); ct.Show()
			self._parts.append(ct)

	def Close(self):
		self.Hide()


# ==============================================================================
# HUNTER FLOATING BOARD (testo fluttuante sopra il mob)
# ==============================================================================
class HunterFloatingBoard(ui.Window):
	def __init__(self, vid, cfg):
		ui.Window.__init__(self)
		self.vid = vid
		self.cfg = cfg
		self.colors = cfg["colors"]
		self.height_offset = cfg.get("height_offset", 380)
		
		# Animazione
		self.pulse_val = 0.0
		self.pulse_dir = 1
		self.info_board = None
		
		# Typewriter
		self.text_cycle_timer = 0
		self.current_subtitle_idx = 0
		self.target_text = ""
		self.current_display_text = ""
		self.typewriter_timer = 0
		
		self._BuildWindow()
		self.target_text = self.cfg["subtitles"][0]
		self.OnUpdate()

	def __del__(self):
		ui.Window.__del__(self)

	def _BuildWindow(self):
		"""Costruisce la board in base al tipo di entita'."""
		self.bg_layers = []
		self.borders = []
		self.arrow_parts = []
		self.arrow_borders = []
		self.deco_bars = []
		
		etype = self.cfg.get("entity_type", "F")
		if etype == "C":
			self._BuildChestBoard()
		else:
			self._BuildFractureBoard()

	def _AddBar(self, x, y, w, h, color, target_list):
		"""Helper: crea un ui.Bar, lo aggiunge a target_list, salva orig_color."""
		b = ui.Bar()
		b.SetParent(self)
		b.SetPosition(int(x), int(y))
		b.SetSize(max(1, int(w)), max(1, int(h)))
		b.SetColor(color)
		b.orig_color = color
		b.AddFlag("not_pick")
		b.Show()
		target_list.append(b)
		return b

	# ------------------------------------------------------------------
	# FRATTURA: Portale del Gate
	# Silhouette a PORTALE: Header spesso colorato (architrave),
	# fondo APERTO al centro, e 2 COLONNE che scendono ai lati.
	# Visivamente unica: sembra un ingresso dimensionale.
	# ------------------------------------------------------------------
	def _BuildFractureBoard(self):
		W = 240
		H = 90
		HEADER_H = 16     # architrave colorato spesso (firma visiva)
		COL_W = 5          # larghezza colonne portale
		COL_H = 18         # altezza colonne sotto la board
		FOOT_W = 55        # segmento bordo bottom (centro aperto)
		self.bw = W
		self.bh = H

		c_top = self.colors["bg_top"]
		c_bot = self.colors["bg_bot"]
		r1 = (c_top >> 16) & 0xFF; g1 = (c_top >> 8) & 0xFF; b1 = c_top & 0xFF
		r2 = (c_bot >> 16) & 0xFF; g2 = (c_bot >> 8) & 0xFF; b2 = c_bot & 0xFF
		bc = self.colors["border"]
		ic = self.colors["inner_border"]

		# === ARCHITRAVE: Header bar spesso colorato (più alto, più drammatico) ===
		header_col = (0xCC << 24) | (bc & 0x00FFFFFF)
		self._AddBar(0, 0, W, HEADER_H, header_col, self.deco_bars)
		# Linee luminose interne all'architrave (doppia riga)
		accent_line = (0x55 << 24) | (bc & 0x00FFFFFF)
		accent_dim = (0x28 << 24) | (bc & 0x00FFFFFF)
		self._AddBar(4, 3, W - 8, 1, accent_line, self.deco_bars)
		self._AddBar(4, 5, W - 8, 1, accent_dim, self.deco_bars)
		self._AddBar(4, HEADER_H - 3, W - 8, 1, accent_line, self.deco_bars)

		# Corner ticks sull'architrave
		tick = 10
		tickC = (0x88 << 24) | (bc & 0x00FFFFFF)
		self._AddBar(0, 0, tick, 2, tickC, self.deco_bars)
		self._AddBar(W - tick, 0, tick, 2, tickC, self.deco_bars)

		# === BG gradient (body sotto header) – 4 step leggeri ===
		body_h = H - HEADER_H
		steps = 4
		for i in xrange(steps):
			y0 = HEADER_H + int(float(i) / steps * body_h)
			y1 = HEADER_H + int(float(i + 1) / steps * body_h)
			rh = max(1, y1 - y0)
			t = float(i) / max(1, steps - 1)
			r = int(r1 + (r2 - r1) * t)
			g = int(g1 + (g2 - g1) * t)
			b = int(b1 + (b2 - b1) * t)
			color = (0xEE << 24) | (r << 16) | (g << 8) | b
			self._AddBar(0, y0, W, rh, color, self.bg_layers)

		# === Glow pulsante (area più ampia per effetto alone) ===
		self.glow_board = ui.Bar()
		self.glow_board.SetParent(self)
		self.glow_board.SetPosition(-3, -3)
		self.glow_board.SetSize(W + 6, H + 6)
		self.glow_board.SetColor(self.colors["glow"])
		self.glow_board.AddFlag("not_pick")
		self.glow_board.Show()

		# === BORDO ESTERNO (2px top – più visibile) ===
		self._AddBar(0, 0, W, 2, bc, self.borders)                          # top (2px)
		self._AddBar(0, HEADER_H, W, 1, bc, self.borders)                   # sotto architrave
		self._AddBar(0, 0, 1, H, bc, self.borders)                          # lato sinistro
		self._AddBar(W - 1, 0, 1, H, bc, self.borders)                      # lato destro
		# Bottom APERTO al centro (il passaggio del portale)
		self._AddBar(0, H - 1, FOOT_W, 1, bc, self.borders)                 # piede sinistro
		self._AddBar(W - FOOT_W, H - 1, FOOT_W, 1, bc, self.borders)        # piede destro

		# === BORDO INTERNO (body) – più definito ===
		self._AddBar(3, HEADER_H + 2, W - 6, 1, ic, self.borders)
		self._AddBar(3, HEADER_H + 2, 1, body_h - 4, ic, self.borders)
		self._AddBar(W - 4, HEADER_H + 2, 1, body_h - 4, ic, self.borders)
		
		# === COLONNE DEL PORTALE (estese sotto la board) ===
		col_col = (0xBB << 24) | (bc & 0x00FFFFFF)
		self._AddBar(0, H, COL_W, COL_H, col_col, self.deco_bars)           # colonna sinistra
		self._AddBar(W - COL_W, H, COL_W, COL_H, col_col, self.deco_bars)   # colonna destra
		# Bordi interni colonne
		self._AddBar(COL_W, H, 1, COL_H, bc, self.arrow_borders)
		self._AddBar(W - COL_W - 1, H, 1, COL_H, bc, self.arrow_borders)
		# Basi colonne (leggermente piu' larghe)
		self._AddBar(0, H + COL_H - 2, COL_W + 2, 2, bc, self.deco_bars)
		self._AddBar(W - COL_W - 2, H + COL_H - 2, COL_W + 2, 2, bc, self.deco_bars)
		
		# === GOCCE DI ENERGIA (dal centro aperto verso il basso) ===
		cx = W / 2
		self._AddBar(cx - 1, H, 2, 6, bc, self.arrow_borders)
		self._AddBar(cx - 1, H + 8, 2, 3, bc, self.arrow_borders)
		self._AddBar(cx - 1, H + 13, 2, 2, bc, self.arrow_borders)
		
		# === NODI ENERGETICI (4 angoli del body) ===
		ns = 3
		ny1 = HEADER_H + 5
		ny2 = H - 5 - ns
		self._AddBar(5, ny1, ns, ns, bc, self.deco_bars)
		self._AddBar(W - 5 - ns, ny1, ns, ns, bc, self.deco_bars)
		self._AddBar(5, ny2, ns, ns, bc, self.deco_bars)
		self._AddBar(W - 5 - ns, ny2, ns, ns, bc, self.deco_bars)
		
		# === Separatore: trattini energetici (4, più puliti) ===
		sep_y = HEADER_H + int(body_h * 0.38)
		dash_n = 4
		dash_w = 10
		dash_gap = 8
		total_w = dash_n * (dash_w + dash_gap) - dash_gap
		dx = (W - total_w) / 2
		for d in xrange(dash_n):
			self._AddBar(dx + d * (dash_w + dash_gap), sep_y, dash_w, 1, ic, self.deco_bars)
		
		# === Testi ===
		self.titleText = ui.TextLine()
		self.titleText.SetParent(self)
		self.titleText.SetPosition(0, HEADER_H + 4)
		self.titleText.SetWindowHorizontalAlignCenter()
		self.titleText.SetHorizontalAlignCenter()
		self.titleText.SetText(self.cfg["title"])
		self.titleText.SetOutline()
		self.titleText.Show()
		
		self.infoBtn = HunterButton(self, W - 25, HEADER_H + 2, 20, 20, self.colors, "?")
		self.infoBtn.SetEvent(self._OnClickInfo)
		
		self.subText = ui.TextLine()
		self.subText.SetParent(self)
		self.subText.SetPosition(0, sep_y + 10)
		self.subText.SetWindowHorizontalAlignCenter()
		self.subText.SetHorizontalAlignCenter()
		self.subText.SetText("")
		self.subText.SetPackedFontColor(self.colors["text_sub"])
		self.subText.SetOutline()
		self.subText.Show()
		
		self.SetSize(W, H + COL_H + 2)
		self.Hide()

	# ------------------------------------------------------------------
	# BAULE: Placca del Tesoro
	# Forma larga e bassa con BARRE SUPERIORE/INFERIORE spesse (firma visiva),
	# L-brackets angolari e gemma centrale. Aspetto "chest plate".
	# ------------------------------------------------------------------
	def _BuildChestBoard(self):
		W = 290
		H = 58
		FRAME = 5        # altezza barre frame top/bottom
		BRACKET = 12     # lunghezza bracci L-corner
		BRACKET_T = 3    # spessore bracci L-corner
		self.bw = W
		self.bh = H
		
		c_top = self.colors["bg_top"]
		c_bot = self.colors["bg_bot"]
		r1 = (c_top >> 16) & 0xFF; g1 = (c_top >> 8) & 0xFF; b1 = c_top & 0xFF
		r2 = (c_bot >> 16) & 0xFF; g2 = (c_bot >> 8) & 0xFF; b2 = c_bot & 0xFF
		bc = self.colors["border"]
		ic = self.colors["inner_border"]
		
		# === BG gradient (area interna tra le barre frame) - 4 step leggeri ===
		inner_h = H - 2 * FRAME
		steps = 4
		for i in xrange(steps):
			y0 = FRAME + int(float(i) / steps * inner_h)
			y1 = FRAME + int(float(i + 1) / steps * inner_h)
			rh = max(1, y1 - y0)
			t = float(i) / max(1, steps - 1)
			r = int(r1 + (r2 - r1) * t)
			g = int(g1 + (g2 - g1) * t)
			b = int(b1 + (b2 - b1) * t)
			color = (0xDD << 24) | (r << 16) | (g << 8) | b
			self._AddBar(0, y0, W, rh, color, self.bg_layers)
		
		# === Glow pulsante (sottile) ===
		self.glow_board = ui.Bar()
		self.glow_board.SetParent(self)
		self.glow_board.SetPosition(-2, -2)
		self.glow_board.SetSize(W + 4, H + 4)
		self.glow_board.SetColor(self.colors["glow"])
		self.glow_board.AddFlag("not_pick")
		self.glow_board.Show()
		
		# === BARRE FRAME TOP/BOTTOM: La firma visiva del Baule ===
		# Barre orizzontali spesse colorate come coperchio/base di un forziere
		frame_col = (0xCC << 24) | (bc & 0x00FFFFFF)
		self._AddBar(0, 0, W, FRAME, frame_col, self.deco_bars)        # top frame
		self._AddBar(0, H - FRAME, W, FRAME, frame_col, self.deco_bars) # bottom frame
		
		# Bordi sottili laterali (1px, NO pilastri spessi)
		self._AddBar(0, 0, 1, H, bc, self.borders)
		self._AddBar(W - 1, 0, 1, H, bc, self.borders)
		
		# === L-CORNER BRACKETS (prominenti, come cardini di un forziere) ===
		boff = FRAME + 2
		# Top-left L
		self._AddBar(3, boff, BRACKET, BRACKET_T, bc, self.deco_bars)
		self._AddBar(3, boff, BRACKET_T, BRACKET, bc, self.deco_bars)
		# Top-right L
		self._AddBar(W - 3 - BRACKET, boff, BRACKET, BRACKET_T, bc, self.deco_bars)
		self._AddBar(W - 3 - BRACKET_T, boff, BRACKET_T, BRACKET, bc, self.deco_bars)
		# Bottom-left L (rovesciata)
		self._AddBar(3, H - FRAME - BRACKET_T - 2, BRACKET, BRACKET_T, bc, self.deco_bars)
		self._AddBar(3, H - FRAME - BRACKET - 2, BRACKET_T, BRACKET, bc, self.deco_bars)
		# Bottom-right L (rovesciata)
		self._AddBar(W - 3 - BRACKET, H - FRAME - BRACKET_T - 2, BRACKET, BRACKET_T, bc, self.deco_bars)
		self._AddBar(W - 3 - BRACKET_T, H - FRAME - BRACKET - 2, BRACKET_T, BRACKET, bc, self.deco_bars)
		
		# === Separatore con gemma centrale (piu' grande, 10px) ===
		sep_y = H / 2
		gem_s = 5
		cx = W / 2
		sep_margin = 24
		self._AddBar(sep_margin, sep_y, cx - sep_margin - gem_s - 3, 1, ic, self.deco_bars)
		self._AddBar(cx + gem_s + 3, sep_y, cx - sep_margin - gem_s - 3, 1, ic, self.deco_bars)
		
		# Gemma compatta (diamante 3px, leggero ma visibile)
		self._AddBar(cx - 1, sep_y - 2, 3, 3, bc, self.deco_bars)
		
		# === Pendente sotto la board (clasp/lucchetto) ===
		self._AddBar(cx - 1, H, 3, 6, bc, self.arrow_borders)
		self._AddBar(cx - 3, H + 6, 7, 2, bc, self.arrow_borders)
		self._AddBar(cx - 1, H + 8, 3, 3, bc, self.arrow_borders)
		
		# === Testi ===
		self.titleText = ui.TextLine()
		self.titleText.SetParent(self)
		self.titleText.SetPosition(0, FRAME + 3)
		self.titleText.SetWindowHorizontalAlignCenter()
		self.titleText.SetHorizontalAlignCenter()
		self.titleText.SetText(self.cfg["title"])
		self.titleText.SetOutline()
		self.titleText.Show()
		
		self.infoBtn = HunterButton(self, W - 26, FRAME + 2, 20, 20, self.colors, "?")
		self.infoBtn.SetEvent(self._OnClickInfo)
		
		self.subText = ui.TextLine()
		self.subText.SetParent(self)
		self.subText.SetPosition(0, sep_y + 8)
		self.subText.SetWindowHorizontalAlignCenter()
		self.subText.SetHorizontalAlignCenter()
		self.subText.SetText("")
		self.subText.SetPackedFontColor(self.colors["text_sub"])
		self.subText.SetOutline()
		self.subText.Show()
		
		self.SetSize(W, H + 12)
		self.Hide()

	def _GetScreenPos(self):
		"""Proiezione 3D -> 2D con metodo pre-cached"""
		vid = self.vid
		try:
			(x, y, z) = chr.GetPixelPosition(vid)
		except:
			return None
		
		ho = float(self.height_offset)
		
		if _PROJECT_METHOD == 1:
			try:
				r = chr.GetProjectPosition(vid, ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
			try:
				r = chr.GetProjectPosition(vid)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]) - int(ho / 3))
			except:
				pass
		elif _PROJECT_METHOD == 2:
			try:
				r = grp.ProjectPosition(x, y, z + ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		elif _PROJECT_METHOD == 3:
			try:
				r = wndMgr.ProjectPosition(x, y, z + ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		elif _PROJECT_METHOD == 4:
			try:
				grp.SetProjectPosition(x, y, z + ho)
				r = grp.GetProjectPosition()
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		
		return None

	def _IsValidEntity(self):
		"""Verifica esistenza entita' (posizione non-zero). Vale per NPC e Mostri."""
		try:
			pos = chr.GetPixelPosition(self.vid)
			return not (pos[0] == 0 and pos[1] == 0 and pos[2] == 0)
		except:
			return False

	def OnMouseLeftButtonUp(self):
		"""Click sulla board: apre dialogo NPC (Bauli/Fratture)"""
		if not self.vid:
			return True
		try:
			net.SendOnClickPacket(self.vid)
		except:
			pass
		return True

	def OnUpdate(self):
		if not self.vid:
			return
		
		# Validazione + distanza in un solo blocco (evita doppio chr.GetPixelPosition)
		try:
			(cx, cy, cz) = chr.GetPixelPosition(self.vid)
		except:
			self.Hide()
			if self.info_board:
				self.info_board.Hide()
			return
		
		if cx == 0 and cy == 0 and cz == 0:
			self.Hide()
			if self.info_board:
				self.info_board.Hide()
			return
		
		# Distanza al quadrato (evita math.sqrt)
		(px, py, pz) = player.GetMainCharacterPosition()
		dist_sq = (px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2
		
		if dist_sq >= MAX_DIST_SQ:
			self.Hide()
			if self.info_board:
				self.info_board.Hide()
			return
		
		# Proiezione schermo
		screen_pos = self._GetScreenPos()
		if not screen_pos:
			self.Hide()
			if self.info_board:
				self.info_board.Hide()
			return
		
		sx, sy = screen_pos
		sw = wndMgr.GetScreenWidth()
		sh = wndMgr.GetScreenHeight()
		
		if sx < 10 or sy < 10 or sx > sw - 10 or sy > sh - 10:
			self.Hide()
			if self.info_board:
				self.info_board.Hide()
			return
		
		# Posiziona e mostra
		self.SetPosition(sx - self.bw / 2, sy - self.bh / 2)
		self.Show()
		
		# Alpha basata sulla distanza (sqrt solo nella zona fade)
		alpha = 1.0
		if dist_sq > FADE_START_SQ:
			dist = math.sqrt(dist_sq)
			alpha = 1.0 - ((dist - FADE_START) / (MAX_DIST - FADE_START))
		
		# Pulsazione glow
		if self.pulse_dir == 1:
			self.pulse_val += 0.03
			if self.pulse_val >= 1.0:
				self.pulse_dir = -1
		else:
			self.pulse_val -= 0.03
			if self.pulse_val <= 0.0:
				self.pulse_dir = 1
		
		# Glow color con pulsazione + fade distanza (alpha ridotto per non mascherare la forma)
		glow_alpha = int(0x20 * self.pulse_val * alpha)
		self.glow_board.SetColor((glow_alpha << 24) | (self.colors["glow"] & 0x00FFFFFF))
		
		# BG layers alpha
		bg_alpha = int(0xDD * alpha)
		for layer in self.bg_layers:
			c = getattr(layer, 'orig_color', 0)
			layer.SetColor((bg_alpha << 24) | (c & 0x00FFFFFF))
		
		# Testi alpha
		ta = int(255 * alpha)
		self.titleText.SetPackedFontColor((ta << 24) | (self.colors["border"] & 0x00FFFFFF))
		self.subText.SetPackedFontColor((ta << 24) | (self.colors["text_sub"] & 0x00FFFFFF))
		
		# Bordi e freccia alpha
		bc = (int(0xFF * alpha) << 24) | (self.colors["border"] & 0x00FFFFFF)
		bgc = (bg_alpha << 24) | (self.colors["bg_bot"] & 0x00FFFFFF)
		for b in self.borders:
			b.SetColor(bc)
		for b in self.arrow_parts:
			b.SetColor(bgc)
		for b in self.arrow_borders:
			b.SetColor(bc)
		
		# Deco bars alpha (corona, borchie, vene, gemma)
		for b in self.deco_bars:
			oc = getattr(b, 'orig_color', bc)
			orig_a = (oc >> 24) & 0xFF
			if orig_a == 0:
				orig_a = 0xFF
			new_a = int(orig_a * alpha)
			b.SetColor((new_a << 24) | (oc & 0x00FFFFFF))
		
		# Typewriter effect
		self.typewriter_timer += 1
		if self.typewriter_timer % 3 == 0:
			if len(self.current_display_text) < len(self.target_text):
				self.current_display_text += self.target_text[len(self.current_display_text)]
				self.subText.SetText(self.current_display_text)
		
		# Ciclo sottotitoli
		self.text_cycle_timer += 1
		if self.text_cycle_timer > 200:
			self.text_cycle_timer = 0
			subs = self.cfg["subtitles"]
			self.current_subtitle_idx = (self.current_subtitle_idx + 1) % len(subs)
			self.target_text = subs[self.current_subtitle_idx]
			self.current_display_text = ""

	def _OnClickInfo(self):
		if self.info_board:
			self.info_board.Hide()
			del self.info_board
		self.info_board = HunterInfoBoard(self.cfg)
		self.info_board.SetTop()
		self.info_board.Show()


# ==============================================================================
# BOARD MANAGEMENT
# ==============================================================================
g_HunterBoards = {}   # VID -> HunterFloatingBoard
g_LastScan = 0.0

def ClearAllHunterBoards():
	"""Rimuove tutte le hunter board (cambio mappa, dungeon, etc.)"""
	global g_HunterBoards
	for vid in g_HunterBoards.keys():
		try:
			g_HunterBoards[vid].Hide()
		except:
			pass
	g_HunterBoards = {}

def UpdateHunterBoards():
	"""
	Chiamata da game.py OnUpdate ogni frame.
	Throttled a 0.5s. Gestisce:
	  1) Cleanup board con NPC morto/despawnato
	  2) Auto-scan Fratture (VNUM 16060-16066) e Bauli (VNUM 63000-63007)
	"""
	global g_HunterBoards, g_LastScan
	
	cur = app.GetTime()
	if cur - g_LastScan < 0.5:
		return
	g_LastScan = cur
	
	# 1. Cleanup board invalide + update quelle valide
	to_remove = []
	(px, py, pz) = player.GetMainCharacterPosition()
	for vid, board in g_HunterBoards.items():
		try:
			(cx, cy, cz) = chr.GetPixelPosition(vid)
			if cx == 0 and cy == 0 and cz == 0:
				board.Hide()
				to_remove.append(vid)
				continue
			# Distanza al quadrato (evita math.sqrt)
			dist_sq = (px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2
			if dist_sq < MAX_DIST_SQ:
				board.OnUpdate()
			else:
				board.Hide()
		except:
			to_remove.append(vid)
	
	for vid in to_remove:
		if vid in g_HunterBoards:
			try:
				g_HunterBoards[vid].Hide()
			except:
				pass
			del g_HunterBoards[vid]
	
	# 2. Auto-scan Fratture (VNUM 16060-16066) e Bauli (VNUM 63000-63007)
	if hasattr(chr, "GetInstanceList"):
		try:
			for vid in chr.GetInstanceList():
				if vid not in g_HunterBoards:
					vnum = chr.GetVirtualNumber(vid)
					if vnum in FRACTURE_VNUMS:
						info = FRACTURE_VNUMS[vnum]
						cfg = MakeConfig("F", info["name"], info["tier"], info["color"])
						board = HunterFloatingBoard(vid, cfg)
						g_HunterBoards[vid] = board
					elif vnum in CHEST_VNUMS:
						info = CHEST_VNUMS[vnum]
						cfg = MakeConfig("C", info["name"], info["tier"], info["color"])
						board = HunterFloatingBoard(vid, cfg)
						g_HunterBoards[vid] = board
		except:
			pass
