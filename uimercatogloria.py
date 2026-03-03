import ui
import chr
import player
import net
import wndMgr
import app
import chat
import grp
import math
import uiCommon

# ==============================================================================
# CONFIGURAZIONE GENERALE & TEMI
# ==============================================================================
BOARD_WIDTH = 260
BOARD_HEIGHT = 70
HEIGHT_OFFSET = 380

# Pre-computed constants (evita ricalcolo ogni frame)
_BOARD_MAX_DIST = 3500.0
_BOARD_FADE_START = 1500.0
_BOARD_MAX_DIST_SQ = _BOARD_MAX_DIST * _BOARD_MAX_DIST
_BOARD_FADE_START_SQ = _BOARD_FADE_START * _BOARD_FADE_START

# Cache metodo proiezione (evita hasattr ogni frame)
_PROJECT_METHOD = 0
if hasattr(chr, "GetProjectPosition"):
	_PROJECT_METHOD = 1
elif hasattr(grp, "ProjectPosition"):
	_PROJECT_METHOD = 2
elif hasattr(wndMgr, "ProjectPosition"):
	_PROJECT_METHOD = 3
elif hasattr(grp, "SetProjectPosition") and hasattr(grp, "GetProjectPosition"):
	_PROJECT_METHOD = 4

# Configurazioni Specifiche per NPC
NPC_CONFIG = {
	# 1. MERCATO GLORIA (Gold Theme) - WORK IN PROGRESS
	20018: {
		"title": "|cFFFFD700=== MERCATO GLORIA ===",
		"info_text": "Benvenuto al Mercato Gloria!\nQui potrai spendere i tuoi Cristalli Gloria per oggetti rari.\nIl negozio e' in fase di allestimento.\nAccumula Gloria intanto: Fratture, Missioni, Boss, Eventi!",
		"subtitles": [
			"Il Negozio sara' A BREVE Disponibile!",
			"Stiamo Cucinando Per Voi...",
			"Accumulate i vostri Punti!",
			"Preparatevi..."
		],
		"colors": {
			"bg_top": 0xD9201000,    # Marrone/Oro scuro
			"bg_bot": 0xD9050200,    # Quasi nero
			"border": 0xFFFFD700,    # Oro Puro
			"glow":   0x00FFD700,    # Glow Oro
			"text_main": 0xFFFFE0A0, # Oro Chiaro
			"text_sub": 0xFFAAAAAA,  # Grigio
			"inner_border": 0xFFCC8800
		}
	},
	
	# 2. MAESTRO DELLE PROVE (Red/Dark Theme)
	20020: {
		"title": "|cFFFF3333=== MAESTRO DELLE PROVE ===",
		"info_text": "Benvenuto dal Maestro delle Prove.\nPer salire di Rank devi completare una Prova d'Esame!\nRequisito: raggiungi la soglia Gloria del rank successivo.\nOgni prova ha obiettivi unici (Boss, Metin, Fratture...).\nSolo chi supera la prova ottiene il nuovo Rango!",
		"height_offset": 230, # Piu' basso per umani (Standard 200-250)
		"subtitles": [
			"Esegui il Rank-Up Qui!",
			"Solo i Degni Avanzano...",
			"Sorgi!", # Cit. Solo Leveling (Arise)
			"Il Potere del Monarca ti attende.",
			"Non puoi fermare l'ascesa.",
			"La Gloria richiede sacrificio.",
			"Affronta le tue paure..."
		],
		"colors": {
			"bg_top": 0xD9200000,    # Rosso scuro/Sangue
			"bg_bot": 0xD9050000,    # Nero rossastro
			"border": 0xFFFF3333,    # Rosso Acceso
			"glow":   0x00FF0000,    # Glow Rosso
			"text_main": 0xFFFFAAAA, # Rosso Chiaro
			"text_sub": 0xFFCCCCCC,  # Grigio Chiaro
			"inner_border": 0xFF880000
		}
	},
	
	# 3. PANZHUNTER - GUIDA HUNTER (Purple/Violet Theme)
	200099: {
		"title": "|cFF9900FF=== PANZHUNTER ===",
		"info_text": "Sono PanzHunter, la tua guida Hunter!\nApri il Terminale (CTRL+H) > Tab Guida per:\n- Fratture, Coraggio e Bottino Bauli\n- Supremo (World Boss), Prove d'Esame\n- Item Hunter: Scanner, Focus, Calibratore...\n- Missioni, Eventi, Shop, Karma\n- CTRL+J: Wiki Encyclopedia (mob/item/drop)\n12 sezioni di guida + 53 FAQ per te!",
		"height_offset": 350, # NPC alto/montato
		"subtitles": [
			"Apri la Guida Completa!",
			"Tutto cio' che devi sapere...",
			"Serve aiuto? Parla con me!",
			"La conoscenza e' potere.",
			"Hunter, sei pronto?",
			"12 sezioni di guida per te!",
			"Benvenuto nel Sistema Hunter.",
			"Ogni grande viaggio inizia qui."
		],
		"colors": {
			"bg_top": 0xD9180030,    # Viola scuro
			"bg_bot": 0xD9050010,    # Nero violaceo
			"border": 0xFF9900FF,    # Viola Acceso
			"glow":   0x009900FF,    # Glow Viola
			"text_main": 0xFFCC99FF, # Lavanda Chiaro
			"text_sub": 0xFFCCCCCC,  # Grigio Chiaro
			"inner_border": 0xFF6600AA
		}
	}
}

_TARGET_VNUMS = frozenset(NPC_CONFIG)   # Pre-computed set for O(1) lookup

# ==============================================================================
# CLASSE BOTTONE CUSTOM (Stile Tema)
# ==============================================================================
class CustomButton(ui.Window):
	def __init__(self, parent, x, y, width, height, color_cfg, text="?"):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.SetSize(width, height)
		self.color_cfg = color_cfg
		self.text_str = text
		self.event_func = None
		self.BuildVisual()
		self.Show()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildVisual(self):
		# Sfondo con stesso gradiente (ma piccolo)
		c_top = self.color_cfg["bg_top"]
		c_bot = self.color_cfg["bg_bot"]
		
		self.bg = ui.Bar()
		self.bg.SetParent(self)
		self.bg.SetPosition(0, 0)
		self.bg.SetSize(self.GetWidth(), self.GetHeight())
		self.bg.SetColor(c_bot) # Solido per semplicita' su bottone piccolo
		self.bg.AddFlag("not_pick")
		self.bg.Show()
		
		# Bordo
		self.border = []
		self.MakeBorder(0, 0, self.GetWidth(), self.GetHeight(), self.color_cfg["border"])
		
		# Testo
		self.text = ui.TextLine()
		self.text.SetParent(self)
		self.text.SetWindowHorizontalAlignCenter()
		self.text.SetWindowVerticalAlignCenter()
		self.text.SetHorizontalAlignCenter()
		self.text.SetVerticalAlignCenter()
		self.text.SetText(self.text_str)
		self.text.SetPackedFontColor(self.color_cfg["text_main"])
		self.text.AddFlag("not_pick")
		self.text.Show()

	def MakeBorder(self, x, y, w, h, color):
		b_top = ui.Bar(); b_top.SetParent(self); b_top.SetPosition(x, y); b_top.SetSize(w, 1); b_top.SetColor(color); b_top.AddFlag("not_pick"); b_top.Show()
		b_bot = ui.Bar(); b_bot.SetParent(self); b_bot.SetPosition(x, y+h-1); b_bot.SetSize(w, 1); b_bot.SetColor(color); b_bot.AddFlag("not_pick"); b_bot.Show()
		b_left = ui.Bar(); b_left.SetParent(self); b_left.SetPosition(x, y); b_left.SetSize(1, h); b_left.SetColor(color); b_left.AddFlag("not_pick"); b_left.Show()
		b_right = ui.Bar(); b_right.SetParent(self); b_right.SetPosition(x+w-1, y); b_right.SetSize(1, h); b_right.SetColor(color); b_right.AddFlag("not_pick"); b_right.Show()
		self.border.extend([b_top, b_bot, b_left, b_right])

	def SetEvent(self, func):
		self.event_func = func

	def OnMouseLeftButtonUp(self):
		if self.event_func:
			self.event_func()
		return True

# ==============================================================================
# CLASSE GENERICA FLOATING BOARD
# ==============================================================================
class FloatingBoard(ui.Window):
	def __init__(self, vid, cfg):
		ui.Window.__init__(self)
		self.vid = vid
		self.cfg = cfg
		self.colors = cfg["colors"]
		# Default height offset se non specificato
		self.height_offset = cfg.get("height_offset", HEIGHT_OFFSET)
		
		# Variabili Animazione e Info
		self.pulse_val = 0.0
		self.pulse_dir = 1
		self.info_board = None # Rif al popup
		
		self.text_cycle_timer = 0
		self.current_subtitle_idx = 0
		self.target_text = ""
		self.current_display_text = ""
		self.typewriter_timer = 0
		
		self.BuildWindow()
		
		# Init Typewriter
		self.target_text = self.cfg["subtitles"][0]
		
		# Avvio immediato update pos
		self.OnUpdate()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		# 1. Background con Gradiente
		self.bg_layers = []
		steps = 10
		step_h = float(BOARD_HEIGHT) / steps
		
		# Decode colors
		c_top = self.colors["bg_top"]
		c_bot = self.colors["bg_bot"]
		
		r1, g1, b1 = (c_top >> 16) & 0xFF, (c_top >> 8) & 0xFF, c_top & 0xFF
		r2, g2, b2 = (c_bot >> 16) & 0xFF, (c_bot >> 8) & 0xFF, c_bot & 0xFF
		
		for i in xrange(steps):
			lines = ui.Bar()
			lines.SetParent(self)
			lines.SetPosition(0, int(i * step_h))
			lines.SetSize(BOARD_WIDTH, int(step_h) + 1)
			
			# Lerp
			t = float(i) / (steps - 1)
			r = int(r1 + (r2 - r1) * t)
			g = int(g1 + (g2 - g1) * t)
			b = int(b1 + (b2 - b1) * t)
			color = (0xD9 << 24) | (r << 16) | (g << 8) | b
			
			lines.SetColor(color)
			lines.orig_color = color # Safe storage
			lines.Show()
			self.bg_layers.append(lines)

		# 2. Glow effect
		self.glow_board = ui.Bar()
		self.glow_board.SetParent(self)
		self.glow_board.SetPosition(-3, -3)
		self.glow_board.SetSize(BOARD_WIDTH+6, BOARD_HEIGHT+6)
		self.glow_board.SetColor(self.colors["glow"]) 
		self.glow_board.Show()

		# 3. Cornice
		self.borders = []
		self.MakeBorder(1, 1, BOARD_WIDTH-2, BOARD_HEIGHT-2, self.colors["inner_border"])
		self.MakeBorder(0, 0, BOARD_WIDTH, BOARD_HEIGHT, self.colors["border"])

		# 4. Freccia "Fumetto"
		self.arrow_parts = []
		self.arrow_borders = []
		base_w = 24
		steps = 12
		
		for i in xrange(steps):
			w = base_w - (i * 2)
			if w < 2: w = 2
			h = 2 
			
			# Sfondo Freccia
			bar = ui.Bar()
			bar.SetParent(self)
			bar.SetPosition(int(BOARD_WIDTH/2) - int(w/2), BOARD_HEIGHT + (i*1))
			bar.SetSize(w, h)
			bar.SetColor(c_bot) # Usa colore fondo bot
			bar.Show()
			self.arrow_parts.append(bar)
			
			# Bordi Freccia
			if i < steps-1:
				bl = ui.Bar(); bl.SetParent(self); bl.SetPosition(int(BOARD_WIDTH/2) - int(w/2), BOARD_HEIGHT + (i*1)); bl.SetSize(2, h); bl.SetColor(self.colors["border"]); bl.Show()
				br = ui.Bar(); br.SetParent(self); br.SetPosition(int(BOARD_WIDTH/2) + int(w/2) - 2, BOARD_HEIGHT + (i*1)); br.SetSize(2, h); br.SetColor(self.colors["border"]); br.Show()
				self.arrow_borders.extend([bl, br])

		# Punta
		tip = ui.Bar()
		tip.SetParent(self)
		tip.SetPosition(int(BOARD_WIDTH/2) - 1, BOARD_HEIGHT + (steps*1))
		tip.SetSize(2, 4)
		tip.SetColor(self.colors["border"])
		tip.Show()
		self.arrow_borders.append(tip)
		
		# 5. Testi
		self.titleText = ui.TextLine()
		self.titleText.SetParent(self)
		self.titleText.SetPosition(0, 12)
		self.titleText.SetWindowHorizontalAlignCenter()
		self.titleText.SetHorizontalAlignCenter()
		self.titleText.SetText(self.cfg["title"]) 
		self.titleText.SetOutline()
		self.titleText.Show()

		# 6. Bottone Info [?] CUSTOM
		self.infoBtn = CustomButton(self, BOARD_WIDTH - 25, 5, 20, 20, self.cfg["colors"], "?")
		self.infoBtn.SetEvent(self.OnClickInfo)

		self.subText = ui.TextLine()
		self.subText.SetParent(self)
		self.subText.SetPosition(0, 38)
		self.subText.SetWindowHorizontalAlignCenter()
		self.subText.SetHorizontalAlignCenter()
		self.subText.SetText("")
		self.subText.SetPackedFontColor(self.colors["text_main"])
		self.subText.SetOutline()
		self.subText.Show()

		self.SetSize(BOARD_WIDTH, BOARD_HEIGHT + 10)
		self.Hide()

	def MakeBorder(self, x, y, w, h, color):
		b_top = ui.Bar(); b_top.SetParent(self); b_top.SetPosition(x, y); b_top.SetSize(w, 1); b_top.SetColor(color); b_top.Show()
		b_bot = ui.Bar(); b_bot.SetParent(self); b_bot.SetPosition(x, y+h-1); b_bot.SetSize(w, 1); b_bot.SetColor(color); b_bot.Show()
		b_left = ui.Bar(); b_left.SetParent(self); b_left.SetPosition(x, y); b_left.SetSize(1, h); b_left.SetColor(color); b_left.Show()
		b_right = ui.Bar(); b_right.SetParent(self); b_right.SetPosition(x+w-1, y); b_right.SetSize(1, h); b_right.SetColor(color); b_right.Show()
		self.borders.extend([b_top, b_bot, b_left, b_right])

	def _GetScreenPos(self):
		"""Proiezione 3D->2D con metodo pre-cached"""
		ho = float(self.height_offset)
		
		if _PROJECT_METHOD == 1:
			try:
				r = chr.GetProjectPosition(self.vid, ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
			try:
				r = chr.GetProjectPosition(self.vid)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]) - int(ho / 3))
			except:
				pass
		elif _PROJECT_METHOD == 2:
			try:
				(cx, cy, cz) = chr.GetPixelPosition(self.vid)
				r = grp.ProjectPosition(cx, cy, cz + ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		elif _PROJECT_METHOD == 3:
			try:
				(cx, cy, cz) = chr.GetPixelPosition(self.vid)
				r = wndMgr.ProjectPosition(cx, cy, cz + ho)
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		elif _PROJECT_METHOD == 4:
			try:
				(cx, cy, cz) = chr.GetPixelPosition(self.vid)
				grp.SetProjectPosition(cx, cy, cz + ho)
				r = grp.GetProjectPosition()
				if r and len(r) >= 2:
					return (int(r[0]), int(r[1]))
			except:
				pass
		
		return None
	
	def _IsValidNpc(self):
		"""Verifica esistenza NPC con fallback universale"""
		try:
			pos = chr.GetPixelPosition(self.vid)
			# Posizione (0,0,0) = NPC non esiste piu'
			if pos[0] == 0 and pos[1] == 0 and pos[2] == 0:
				return False
			return True
		except:
			return False

	def OnUpdate(self):
		if not self.vid: return

		# Validazione + distanza in un blocco unico (evita doppio chr.GetPixelPosition)
		try:
			(cx, cy, cz) = chr.GetPixelPosition(self.vid)
		except:
			self.Hide()
			if self.info_board: self.info_board.Hide()
			return
		
		if cx == 0 and cy == 0 and cz == 0:
			self.Hide()
			if self.info_board: self.info_board.Hide()
			return

		# Distanza al quadrato (evita math.sqrt)
		(px, py, pz) = player.GetMainCharacterPosition()
		dist_sq = (px-cx)**2 + (py-cy)**2 + (pz-cz)**2

		if dist_sq >= _BOARD_MAX_DIST_SQ:
			self.Hide()
			if self.info_board: self.info_board.Hide()
			return

		# Posizionamento (con fallback multipli)
		screen_pos = self._GetScreenPos()
		if not screen_pos:
			self.Hide()
			if self.info_board: self.info_board.Hide()
			return
		
		x, y = screen_pos
			
		screen_w = wndMgr.GetScreenWidth()
		screen_h = wndMgr.GetScreenHeight()
		
		# Check Bordi Rigoroso
		if x < 10 or y < 10 or x > (screen_w - 10) or y > (screen_h - 10):
			self.Hide()
			if self.info_board: self.info_board.Hide()
			return

		# Show Main Board
		self.SetPosition(x - (BOARD_WIDTH / 2), y - (BOARD_HEIGHT / 2))
		self.Show()

		# Calcolo Alpha (sqrt solo nella zona fade)
		cur_alpha = 1.0
		if dist_sq > _BOARD_FADE_START_SQ:
			dist = math.sqrt(dist_sq)
			cur_alpha = 1.0 - ((dist - _BOARD_FADE_START) / (_BOARD_MAX_DIST - _BOARD_FADE_START))
			
		# Animazione Pulsazione + Alpha
		if self.pulse_dir == 1:
			self.pulse_val += 0.03
			if self.pulse_val >= 1.0: self.pulse_dir = -1
		else:
			self.pulse_val -= 0.03
			if self.pulse_val <= 0.0: self.pulse_dir = 1
		
		# Glow
		glow_alpha_base = int(0x66 * self.pulse_val)
		glow_alpha_final = int(glow_alpha_base * cur_alpha)
		glow_col = (glow_alpha_final << 24) | (self.colors["glow"] & 0x00FFFFFF)
		self.glow_board.SetColor(glow_col)
		
		# Background Layers
		bg_alpha = int(0xD9 * cur_alpha)
		for layer in self.bg_layers:
			col = getattr(layer, 'orig_color', 0)
			layer.SetColor((bg_alpha << 24) | (col & 0x00FFFFFF))

		# Texts
		text_alpha = int(255 * cur_alpha)
		self.titleText.SetPackedFontColor((text_alpha << 24) | (self.colors["border"] & 0x00FFFFFF)) # Titolo color bordo
		self.subText.SetPackedFontColor((text_alpha << 24) | (self.colors["text_main"] & 0x00FFFFFF))
		
		# Borders & Arrows
		border_col = (int(0xFF * cur_alpha) << 24) | (self.colors["border"] & 0x00FFFFFF)
		bg_solid_col = (bg_alpha << 24) | (self.colors["bg_bot"] & 0x00FFFFFF)
		
		for b in self.borders: b.SetColor(border_col)
		for bar in self.arrow_parts: bar.SetColor(bg_solid_col)
		for bar in self.arrow_borders: bar.SetColor(border_col)
		
		# Typewriter
		self.typewriter_timer += 1
		if self.typewriter_timer % 3 == 0: 
			if len(self.current_display_text) < len(self.target_text):
				self.current_display_text += self.target_text[len(self.current_display_text)]
				self.subText.SetText(self.current_display_text)
		
		self.text_cycle_timer += 1
		if self.text_cycle_timer > 200:
			self.text_cycle_timer = 0
			subs = self.cfg["subtitles"]
			self.current_subtitle_idx = (self.current_subtitle_idx + 1) % len(subs)
			self.target_text = subs[self.current_subtitle_idx]
			self.current_display_text = ""

	def OnClickInfo(self):
		# Chiudi precedente se esiste
		if hasattr(self, "info_board") and self.info_board:
			self.info_board.Hide()
			del self.info_board
		
		self.info_board = InfoBoard(self.cfg)
		self.info_board.SetTop()
		self.info_board.Show()

	def OnMouseLeftButtonUp(self):
		if self.vid:
			net.SendOnClickPacket(self.vid)
		return True

# ==============================================================================
# CLASSE POPUP INFO (Themed)
# ==============================================================================
class InfoBoard(ui.Window):
	def __init__(self, cfg):
		ui.Window.__init__(self)
		self.cfg = cfg
		self.colors = cfg["colors"]
		self.BuildWindow()

	def __del__(self):
		ui.Window.__del__(self)

	def BuildWindow(self):
		WIDTH = 350
		# Altezza dinamica basata sul numero di righe del testo
		lines_count = len(self.cfg.get("info_text", "").split("\n"))
		HEIGHT = max(180, 50 + (lines_count * 20) + 45)
		
		self.SetSize(WIDTH, HEIGHT)
		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("float")
		
		# 1. Background (Stesso stile FloatingBoard)
		self.bg_layers = []
		steps = 10
		step_h = float(HEIGHT) / steps
		
		# Decode colors
		c_top = self.colors["bg_top"]
		c_bot = self.colors["bg_bot"]
		
		r1, g1, b1 = (c_top >> 16) & 0xFF, (c_top >> 8) & 0xFF, c_top & 0xFF
		r2, g2, b2 = (c_bot >> 16) & 0xFF, (c_bot >> 8) & 0xFF, c_bot & 0xFF
		
		for i in xrange(steps):
			lines = ui.Bar()
			lines.SetParent(self)
			lines.SetPosition(0, int(i * step_h))
			lines.SetSize(WIDTH, int(step_h) + 1)
			
			t = float(i) / (steps - 1)
			r = int(r1 + (r2 - r1) * t)
			g = int(g1 + (g2 - g1) * t)
			b = int(b1 + (b2 - b1) * t)
			color = (0xF0 << 24) | (r << 16) | (g << 8) | b # Alpha piu' alta (F0) per popup
			
			lines.SetColor(color)
			lines.Show()
			self.bg_layers.append(lines)

		# 2. Bordi
		self.MakeBorder(0, 0, WIDTH, HEIGHT, self.colors["border"])
		self.MakeBorder(2, 2, WIDTH-4, HEIGHT-4, self.colors["inner_border"])

		# 3. Titolo
		self.title = ui.TextLine()
		self.title.SetParent(self)
		self.title.SetPosition(0, 15)
		self.title.SetWindowHorizontalAlignCenter()
		self.title.SetHorizontalAlignCenter()
		self.title.SetText(self.cfg["title"])
		self.title.SetOutline()
		self.title.Show()
		
		# 4. Testo Info (Multi-riga manuale)
		img_desc = self.cfg.get("info_text", "").split("\n")
		start_y = 50
		for line in img_desc:
			t = ui.TextLine()
			t.SetParent(self)
			t.SetPosition(0, start_y)
			t.SetWindowHorizontalAlignCenter()
			t.SetHorizontalAlignCenter()
			t.SetText(line)
			t.SetPackedFontColor(self.colors["text_main"])
			t.Show()
			self.bg_layers.append(t) # Keep ref
			start_y += 20

		# 5. Bottone Chiudi CUSTOM
		self.closeBtn = CustomButton(self, int(WIDTH/2) - 40, HEIGHT - 35, 80, 20, self.cfg["colors"], "CHIUDI")
		self.closeBtn.SetEvent(self.Close)
		
	def MakeBorder(self, x, y, w, h, color):
		b_top = ui.Bar(); b_top.SetParent(self); b_top.SetPosition(x, y); b_top.SetSize(w, 1); b_top.SetColor(color); b_top.Show()
		b_bot = ui.Bar(); b_bot.SetParent(self); b_bot.SetPosition(x, y+h-1); b_bot.SetSize(w, 1); b_bot.SetColor(color); b_bot.Show()
		b_left = ui.Bar(); b_left.SetParent(self); b_left.SetPosition(x, y); b_left.SetSize(1, h); b_left.SetColor(color); b_left.Show()
		b_right = ui.Bar(); b_right.SetParent(self); b_right.SetPosition(x+w-1, y); b_right.SetSize(1, h); b_right.SetColor(color); b_right.Show()
		# Salva ref in bg_layers per comodita'
		self.bg_layers.extend([b_top, b_bot, b_left, b_right])

	def Close(self):
		self.Hide()


# ==============================================================================
# MANAGER (Multi-Board System)
# ==============================================================================
g_ActiveBoards = {} # VID -> FloatingBoard
g_LastScanTime = 0
g_LastVidScanTime = 0   # Throttle separato per scan VID range (piu' pesante)
g_VidScanOffset = 0     # Chunk corrente nella scansione VID
VID_SCAN_CHUNK = 5000   # VID per chunk
VID_SCAN_MAX = 30000    # VID massimo da scansionare

def ScanForOracle(): # Nome mantenuto per compatibilità game.py
	global g_LastScanTime, g_LastVidScanTime, g_VidScanOffset
	cur_time = app.GetTime()
	
	if cur_time - g_LastScanTime < 0.5:
		return
	g_LastScanTime = cur_time
	
	# 1. Cleanup Board Invalide/Lontane
	to_remove = []
	(px, py, pz) = player.GetMainCharacterPosition()
	for vid, board in g_ActiveBoards.items():
		try:
			# Verifica esistenza NPC (universale, non usa GetRace)
			if not board._IsValidNpc():
				board.Hide()
				to_remove.append(vid)
				continue
			
			# Se nascosto ma vicino, forza update per riapparire
			(cx, cy, cz) = chr.GetPixelPosition(vid)
			dx = px - cx
			dy = py - cy
			dz = pz - cz
			if dx*dx + dy*dy + dz*dz < _BOARD_MAX_DIST_SQ:
				board.OnUpdate()
		except:
			to_remove.append(vid)
	
	for vid in to_remove:
		if vid in g_ActiveBoards:
			g_ActiveBoards[vid].Hide()
			del g_ActiveBoards[vid]

	# 2. Scansione Nuovi NPC
	# Controlla quali VNUM abbiamo gia' trovato
	found_vnums = set()
	for vid in g_ActiveBoards:
		try:
			found_vnums.add(chr.GetVirtualNumber(vid))
		except:
			pass
	
	# Se abbiamo gia' tutti gli NPC, skip scansione
	if _TARGET_VNUMS <= found_vnums:
		return
	
	found_vids = []
	
	# Metodo A: chr.GetInstanceList (C++ custom, non presente su tutti i client)
	if hasattr(chr, "GetInstanceList"):
		for vid in chr.GetInstanceList():
			vnum = chr.GetVirtualNumber(vid)
			if vnum in _TARGET_VNUMS:
				found_vids.append((vid, vnum))
	
	# Metodo B: RIMOSSO (Causa Crash su alcuni client)
	# La scansione brute-force dei VID (1-30000) causava segfault in C++
	# se chiamata su VID inesistenti. Si usa solo GetInstanceList o Target.
	
	# Metodo C: Target manuale (sempre attivo come ulteriore fallback)
	t_vid = player.GetTargetVID()
	if t_vid != 0:
		t_vnum = chr.GetVirtualNumber(t_vid)
		if t_vnum in _TARGET_VNUMS:
			found_vids.append((t_vid, t_vnum))
			
	# 3. Creazione Board
	for (vid, vnum) in found_vids:
		if vid not in g_ActiveBoards:
			new_board = FloatingBoard(vid, NPC_CONFIG[vnum])
			g_ActiveBoards[vid] = new_board
