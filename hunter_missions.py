# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - MISSIONS & EVENTS
#  Sistema missioni giornaliere ed eventi stile Solo Leveling
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import wndMgr
import app
import nonplayer

from hunter_core import DraggableMixin, WINDOW_POSITIONS, COLOR_SCHEMES, FormatNumber

# Funzione T() - restituisce direttamente il testo (no multilingua)
def T(key, default=None):
    return default if default else key


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION GUIDE TOOLTIP - Tooltip flottante per la guida missioni
# ═══════════════════════════════════════════════════════════════════════════════
_g_missionGuideTooltip = None

def _GetMissionGuideTooltip():
    global _g_missionGuideTooltip
    if _g_missionGuideTooltip is None:
        _g_missionGuideTooltip = MissionGuideTooltip()
    return _g_missionGuideTooltip


class MissionGuideTooltip(ui.Window):
    """Tooltip flottante per spiegare il sistema missioni giornaliere."""

    MAX_WIDTH = 360
    LINE_H = 15
    HEADER_H = 26

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(self.MAX_WIDTH, 50)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        self.tooltipH = 50
        self.linePool = []
        self.barPool = []
        self.usedLines = 0
        self.usedBars = 0
        self.__BuildFrame()
        self.__BuildPool()
        self.Hide()

    def __BuildFrame(self):
        # Sfondo scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.MAX_WIDTH, 50)
        self.bg.SetColor(0xF2080812)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Header colorato
        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(0, 0)
        self.headerBg.SetSize(self.MAX_WIDTH, self.HEADER_H)
        self.headerBg.SetColor(0xCC001a33)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        # Bordi cyan
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.MAX_WIDTH, 2)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 48)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()

        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, 50)
        self.borderLeft.SetColor(0xFF00CCFF)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, 50)
        self.borderRight.SetColor(0xFF00CCFF)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(2, self.HEADER_H)
        self.headerLine.SetSize(self.MAX_WIDTH - 4, 1)
        self.headerLine.SetColor(0xFF00CCFF)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # Titolo header
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.MAX_WIDTH // 2, 5)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(0xFFFFFFFF)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()

    def __BuildPool(self):
        for i in range(35):
            tl = ui.TextLine()
            tl.SetParent(self)
            tl.AddFlag("not_pick")
            tl.Hide()
            self.linePool.append(tl)
        for i in range(8):
            b = ui.Bar()
            b.SetParent(self)
            b.AddFlag("not_pick")
            b.Hide()
            self.barPool.append(b)

    def __ResetPool(self):
        for tl in self.linePool:
            tl.Hide()
        for b in self.barPool:
            b.Hide()
        self.usedLines = 0
        self.usedBars = 0

    def __PutLine(self, text, color, x, y, outline=False):
        if self.usedLines < len(self.linePool):
            tl = self.linePool[self.usedLines]
            tl.SetPosition(x, y)
            tl.SetText(text)
            tl.SetPackedFontColor(color)
            if outline:
                tl.SetOutline()
            tl.Show()
            self.usedLines += 1

    def __PutSep(self, y, color=0xFF003355):
        if self.usedBars < len(self.barPool):
            b = self.barPool[self.usedBars]
            b.SetPosition(14, y)
            b.SetSize(self.MAX_WIDTH - 28, 1)
            b.SetColor(color)
            b.Show()
            self.usedBars += 1

    def ShowGuide(self):
        """Mostra la guida completa delle missioni giornaliere."""
        self.__ResetPool()

        titleColor = 0xFF00CCFF
        self.titleText.SetText("GUIDA MISSIONI GIORNALIERE")
        self.titleText.SetPackedFontColor(titleColor)
        self.headerBg.SetColor(0xCC001a33)

        y = self.HEADER_H + 10

        # --- SEZIONE: Cosa sono ---
        self.__PutLine("COSA SONO?", 0xFF00FFFF, 14, y, True)
        y += self.LINE_H + 2
        self.__PutLine("Ogni giorno ricevi 3 missioni da completare.", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("Uccidi mostri, raccogli oggetti o esplora", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("per ottenere Gloria e ricompense!", 0xFFCCCCCC, 14, y)
        y += self.LINE_H + 6

        # --- Separatore ---
        self.__PutSep(y, 0xFF004466)
        y += 10

        # --- SEZIONE: Come vengono assegnate ---
        self.__PutLine("COME VENGONO ASSEGNATE?", 0xFFFFD700, 14, y, True)
        y += self.LINE_H + 2
        self.__PutLine("Le missioni si basano sul LIVELLO del tuo PG.", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("Piu' il tuo livello e' alto, piu' le sfide", 0xFFFFAAAA, 14, y)
        y += self.LINE_H
        self.__PutLine("saranno ardue ma con ricompense maggiori!", 0xFFFFAAAA, 14, y)
        y += self.LINE_H + 2
        self.__PutLine("Lv 1-30: Missioni facili (mob bassi)", 0xFF88FF88, 14, y)
        y += self.LINE_H
        self.__PutLine("Lv 31-60: Missioni medie (mob intermedi)", 0xFFFFFF88, 14, y)
        y += self.LINE_H
        self.__PutLine("Lv 61-90: Missioni difficili (mob alti)", 0xFFFFAA66, 14, y)
        y += self.LINE_H
        self.__PutLine("Lv 90+: Missioni estreme (boss/elite)", 0xFFFF6666, 14, y)
        y += self.LINE_H + 6

        # --- Separatore ---
        self.__PutSep(y, 0xFF004466)
        y += 10

        # --- SEZIONE: Bonus e Malus ---
        self.__PutLine("BONUS & MALUS", 0xFF00FF00, 14, y, True)
        y += self.LINE_H + 2
        self.__PutLine("Completa TUTTE e 3 le missioni per ottenere", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("il BONUS Gloria x1.5 fino al reset!", 0xFF00FF00, 14, y)
        y += self.LINE_H + 4
        self.__PutLine("ATTENZIONE: Se NON completi una missione,", 0xFFFF4444, 14, y)
        y += self.LINE_H
        self.__PutLine("subisci una penalita' di Gloria (malus).", 0xFFFF4444, 14, y)
        y += self.LINE_H + 6

        # --- Separatore ---
        self.__PutSep(y, 0xFF004466)
        y += 10

        # --- SEZIONE: Come completarle ---
        self.__PutLine("COME COMPLETARLE?", 0xFF00CCFF, 14, y, True)
        y += self.LINE_H + 2
        self.__PutLine("1. Apri la finestra missioni dal Terminale", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("2. Leggi l'obiettivo di ogni missione", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("3. Uccidi i mob / raccogli gli oggetti", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("4. Il progresso si aggiorna in tempo reale", 0xFFCCCCCC, 14, y)
        y += self.LINE_H
        self.__PutLine("5. A missione completa appare [OK] verde", 0xFF00FF00, 14, y)
        y += self.LINE_H + 6

        # --- Separatore ---
        self.__PutSep(y, 0xFF004466)
        y += 10

        # --- SEZIONE: Reset ---
        self.__PutLine("RESET GIORNALIERO", 0xFF888888, 14, y, True)
        y += self.LINE_H + 2
        self.__PutLine("Le missioni si resettano ogni giorno a", 0xFFAAAAAA, 14, y)
        y += self.LINE_H
        self.__PutLine("mezzanotte (00:00). Nuove sfide ti aspettano!", 0xFFAAAAAA, 14, y)
        y += self.LINE_H + 10

        # Resize tooltip
        self.tooltipH = y
        self.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.bg.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.borderLeft.SetSize(2, self.tooltipH)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, self.tooltipH)
        self.borderBot.SetPosition(0, self.tooltipH - 2)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)

        # Posiziona vicino al mouse
        mouseX, mouseY = wndMgr.GetMousePosition()
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()

        px = mouseX + 15
        py = mouseY - self.tooltipH // 2
        if px + self.MAX_WIDTH > screenW:
            px = mouseX - self.MAX_WIDTH - 10
        if py < 5:
            py = 5
        if py + self.tooltipH > screenH - 5:
            py = screenH - self.tooltipH - 5

        self.SetPosition(max(0, px), max(0, py))
        self.Show()
        self.SetTop()

    def HideGuide(self):
        self.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION LOCATION TOOLTIP - Tooltip hover su missione (dove trovare il mob)
# ═══════════════════════════════════════════════════════════════════════════════

# Import location data from uipresentation (lazy to avoid circular import)
def _GetMobLocationInfo(vnum, missionType):
    """Restituisce (location, hint) per un dato vnum/tipo missione.
    Usa i dati della wiki (BOSS_LOCATION, DATA_MGR) + fallback."""
    try:
        from uipresentation import BOSS_LOCATION, FRACTURE_BOSSES, FRACTURE_SUPERMETIN, FRACTURE_CHESTS, DATA_MGR

        # Missioni generiche (vnum=0): qualsiasi mob
        if vnum == 0:
            if missionType == "kill_mob":
                return "Qualsiasi mappa", "Uccidi qualsiasi mostro nel mondo di gioco"
            elif missionType == "kill_boss":
                return "Qualsiasi mappa", "Uccidi qualsiasi boss nel mondo di gioco"
            elif missionType == "kill_metin":
                return "Qualsiasi mappa", "Distruggi qualsiasi Metin nel mondo di gioco"
            elif missionType == "seal_fracture":
                return "Fratture dimensionali", "Sigilla le fratture usando il sistema Fratture"
            elif missionType == "open_chest":
                return "Fratture dimensionali", "Apri i forzieri che appaiono nelle fratture"
            return "Sconosciuta", ""

        # Boss frattura?
        if vnum in FRACTURE_BOSSES:
            fb = FRACTURE_BOSSES[vnum]
            loc = BOSS_LOCATION.get(vnum, "Fratture dimensionali")
            return loc, "Boss Frattura (Tier %d)" % fb.get("tier", 1)

        # Super Metin frattura?
        if vnum in FRACTURE_SUPERMETIN:
            fm = FRACTURE_SUPERMETIN[vnum]
            return "Fratture dimensionali", "Super Metin (Tier %d)" % fm.get("tier", 1)

        # Forziere frattura?
        if vnum in FRACTURE_CHESTS:
            fc = FRACTURE_CHESTS[vnum]
            return "Fratture dimensionali", "Forziere (Tier %d)" % fc.get("tier", 1)

        # Boss con posizione nota?
        if vnum in BOSS_LOCATION:
            return BOSS_LOCATION[vnum], ""

        # Fallback: usa il livello del mob per determinare la zona
        loc = DATA_MGR.GetMobLocation(vnum)
        if loc:
            return loc, ""

        # Ultimo fallback: livello diretto
        try:
            level = nonplayer.GetMonsterLevel(vnum)
            if level > 0:
                zoneName, phaseStr = DATA_MGR.GetZoneForLevel(level)
                if zoneName:
                    return "%s (%s)" % (zoneName, phaseStr), ""
        except:
            pass

        return "Sconosciuta", ""
    except:
        return "Sconosciuta", ""


def _GetMobName(vnum):
    """Restituisce il nome del mob dato il vnum."""
    if vnum <= 0:
        return ""
    try:
        name = nonplayer.GetMonsterName(vnum)
        if name:
            return name
    except:
        pass
    return ""


_g_missionLocationTooltip = None

def _GetMissionLocationTooltip():
    global _g_missionLocationTooltip
    if _g_missionLocationTooltip is None:
        _g_missionLocationTooltip = MissionLocationTooltip()
    return _g_missionLocationTooltip


class MissionLocationTooltip(ui.Window):
    """Tooltip flottante che mostra dove trovare il target della missione."""

    TOOLTIP_WIDTH = 220
    MAX_HEIGHT = 120

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(self.TOOLTIP_WIDTH, self.MAX_HEIGHT)
        self.AddFlag("float")
        self.SetWindowName("MissionLocationTooltip")

        # Background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.TOOLTIP_WIDTH, self.MAX_HEIGHT)
        self.bg.SetColor(0xEE0A0A0A)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Bordo
        self.borders = []
        for pos in [(0, 0, self.TOOLTIP_WIDTH, 1), (0, 0, 1, self.MAX_HEIGHT),
                     (self.TOOLTIP_WIDTH - 1, 0, 1, self.MAX_HEIGHT), (0, self.MAX_HEIGHT - 1, self.TOOLTIP_WIDTH, 1)]:
            b = ui.Bar()
            b.SetParent(self)
            b.SetPosition(pos[0], pos[1])
            b.SetSize(pos[2], pos[3])
            b.SetColor(0xFF00CCFF)
            b.AddFlag("not_pick")
            b.Show()
            self.borders.append(b)

        # Icona tipo missione (testo)
        self.typeLabel = ui.TextLine()
        self.typeLabel.SetParent(self)
        self.typeLabel.SetPosition(10, 8)
        self.typeLabel.SetText("")
        self.typeLabel.SetPackedFontColor(0xFF00FFFF)
        self.typeLabel.AddFlag("not_pick")
        self.typeLabel.Show()

        # Nome target
        self.targetLabel = ui.TextLine()
        self.targetLabel.SetParent(self)
        self.targetLabel.SetPosition(10, 28)
        self.targetLabel.SetText("")
        self.targetLabel.SetPackedFontColor(0xFFFFFFFF)
        self.targetLabel.AddFlag("not_pick")
        self.targetLabel.Show()

        # Posizione / mappa
        self.locIcon = ui.TextLine()
        self.locIcon.SetParent(self)
        self.locIcon.SetPosition(10, 50)
        self.locIcon.SetText("Posizione:")
        self.locIcon.SetPackedFontColor(0xFFAAAAAA)
        self.locIcon.AddFlag("not_pick")
        self.locIcon.Show()

        self.locLabel = ui.TextLine()
        self.locLabel.SetParent(self)
        self.locLabel.SetPosition(10, 68)
        self.locLabel.SetText("")
        self.locLabel.SetPackedFontColor(0xFFFFD700)
        self.locLabel.AddFlag("not_pick")
        self.locLabel.Show()

        # Hint extra (es. "Boss Frattura Tier 3")
        self.hintLabel = ui.TextLine()
        self.hintLabel.SetParent(self)
        self.hintLabel.SetPosition(10, 88)
        self.hintLabel.SetText("")
        self.hintLabel.SetPackedFontColor(0xFF888888)
        self.hintLabel.AddFlag("not_pick")
        self.hintLabel.Show()

        self.Hide()

    def ShowForMission(self, mission, parentX, parentY):
        """Mostra tooltip per una missione specifica.
        mission = dict con id, name, type, target_vnum, ecc.
        parentX, parentY = posizione del mission slot sullo schermo."""
        mType = mission.get("type", "kill_mob")
        vnum = mission.get("target_vnum", 0)

        # Tipo missione label
        TYPE_LABELS = {
            "kill_mob":       "Tipo: Uccidi Mostri",
            "kill_boss":      "Tipo: Caccia al Boss",
            "kill_metin":     "Tipo: Distruggi Metin",
            "seal_fracture":  "Tipo: Sigilla Frattura",
            "open_chest":     "Tipo: Apri Forziere",
        }
        self.typeLabel.SetText(TYPE_LABELS.get(mType, "Tipo: %s" % mType))

        # Nome mob target
        mobName = _GetMobName(vnum)
        if mobName:
            self.targetLabel.SetText("Target: %s" % mobName[:30])
        elif vnum > 0:
            self.targetLabel.SetText("Target: Vnum %d" % vnum)
        else:
            self.targetLabel.SetText("Target: Qualsiasi")

        # Posizione
        location, hint = _GetMobLocationInfo(vnum, mType)
        isDungeon = location.startswith("DG ")
        if isDungeon:
            locText = location[3:]
            self.locIcon.SetText("Dungeon:")
            self.locIcon.SetPackedFontColor(0xFFFF8800)
        else:
            locText = location
            self.locIcon.SetText("Posizione:")
            self.locIcon.SetPackedFontColor(0xFFAAAAAA)

        self.locLabel.SetText(locText[:35])
        self.hintLabel.SetText(hint[:40] if hint else "")

        # Calcola altezza dinamica
        h = 88
        if hint:
            h = 108
        self.SetSize(self.TOOLTIP_WIDTH, h)
        self.bg.SetSize(self.TOOLTIP_WIDTH, h)
        # Aggiorna bordi
        self.borders[1].SetSize(1, h)  # left
        self.borders[2].SetSize(1, h)  # right
        self.borders[3].SetPosition(0, h - 1)  # bottom

        # Posiziona accanto allo slot (a destra)
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        tx = parentX + 250  # a destra dello slot
        ty = parentY

        # Se esce dallo schermo, mettilo a sinistra
        if tx + self.TOOLTIP_WIDTH > screenW:
            tx = parentX - self.TOOLTIP_WIDTH - 5

        if ty + h > screenH:
            ty = screenH - h - 5

        self.SetPosition(tx, ty)
        self.SetTop()
        self.Show()

    def HideTooltip(self):
        self.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  DAILY MISSIONS WINDOW - Finestra principale missioni
# ═══════════════════════════════════════════════════════════════════════════════
class DailyMissionsWindow(ui.Window, DraggableMixin):
    """Finestra missioni giornaliere - Trascinabile"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(340, 340)  # Aumentato per info bonus/malus
        
        # Inizializza drag con memoria posizione
        self.InitDraggable("DailyMissionsWindow", 200, 150)
        
        self.missions = []
        self.missionSlots = []
        self.progressBars = []
        self.theme = None
        self.lastUpdateTime = 0
        self.autoCloseTimer = 0.0
        self.resetTime = "00:00"  # Orario reset missioni (mezzanotte)
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background principale
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(340, 340)
        self.bgBar.SetColor(0xEE0A0A0A)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi cyan
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(340, 2)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 338)
        self.borderBot.SetSize(340, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()
        
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, 340)
        self.borderLeft.SetColor(0xFF00CCFF)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()
        
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(338, 0)
        self.borderRight.SetSize(2, 340)
        self.borderRight.SetColor(0xFF00CCFF)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(170, 10)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("DAILY_MISSIONS_TITLE", "< MISSIONI GIORNALIERE >"))
        self.titleText.SetPackedFontColor(0xFF00FFFF)
        self.titleText.Show()
        
        # Linea separatore
        self.sepLine = ui.Bar()
        self.sepLine.SetParent(self)
        self.sepLine.SetPosition(10, 35)
        self.sepLine.SetSize(320, 1)
        self.sepLine.SetColor(0xFF00CCFF)
        self.sepLine.AddFlag("not_pick")
        self.sepLine.Show()
        
        # Crea 3 slot per le missioni
        for i in range(3):
            slot = self.__CreateMissionSlot(i)
            self.missionSlots.append(slot)
        
        # ====== SEZIONE INFO BONUS/MALUS ======
        # Separatore
        self.sepLine2 = ui.Bar()
        self.sepLine2.SetParent(self)
        self.sepLine2.SetPosition(10, 235)
        self.sepLine2.SetSize(320, 1)
        self.sepLine2.SetColor(0xFF00CCFF)
        self.sepLine2.AddFlag("not_pick")
        self.sepLine2.Show()
        
        # Titolo BONUS
        self.bonusTitle = ui.TextLine()
        self.bonusTitle.SetParent(self)
        self.bonusTitle.SetPosition(20, 245)
        self.bonusTitle.SetText(T("BONUS", "BONUS"))
        self.bonusTitle.SetPackedFontColor(0xFF00FF00)
        self.bonusTitle.Show()
        
        self.bonusDesc = ui.TextLine()
        self.bonusDesc.SetParent(self)
        self.bonusDesc.SetPosition(70, 245)
        self.bonusDesc.SetText("Completa tutte: Gloria x1.5 fino al reset!")
        self.bonusDesc.SetPackedFontColor(0xFFFFD700)
        self.bonusDesc.Show()
        
        # Titolo MALUS
        self.malusTitle = ui.TextLine()
        self.malusTitle.SetParent(self)
        self.malusTitle.SetPosition(20, 265)
        self.malusTitle.SetText(T("MALUS", "MALUS"))
        self.malusTitle.SetPackedFontColor(0xFFFF4444)
        self.malusTitle.Show()
        
        self.malusDesc = ui.TextLine()
        self.malusDesc.SetParent(self)
        self.malusDesc.SetPosition(70, 265)
        self.malusDesc.SetText(T("MALUS_DESC", "Non completare: -Gloria (vedi penalita)"))
        self.malusDesc.SetPackedFontColor(0xFFAAAAAA)
        self.malusDesc.Show()
        
        # Info Reset
        self.resetInfo = ui.TextLine()
        self.resetInfo.SetParent(self)
        self.resetInfo.SetPosition(170, 290)
        self.resetInfo.SetHorizontalAlignCenter()
        self.resetInfo.SetText(T("RESET_INFO", "Reset giornaliero alle 00:00"))
        self.resetInfo.SetPackedFontColor(0xFF888888)
        self.resetInfo.Show()
        
        # Avviso bonus attivo (nascosto di default)
        self.bonusActiveText = ui.TextLine()
        self.bonusActiveText.SetParent(self)
        self.bonusActiveText.SetPosition(170, 310)
        self.bonusActiveText.SetHorizontalAlignCenter()
        self.bonusActiveText.SetText("")
        self.bonusActiveText.SetPackedFontColor(0xFF00FF00)
        self.bonusActiveText.Show()
        
        # ====== PULSANTE GUIDA [?] ======
        self.helpBtn = ui.Window()
        self.helpBtn.SetParent(self)
        self.helpBtn.SetPosition(286, 6)
        self.helpBtn.SetSize(22, 18)
        self.helpBtn.Show()

        self.helpBtnBg = ui.Bar()
        self.helpBtnBg.SetParent(self.helpBtn)
        self.helpBtnBg.SetPosition(0, 0)
        self.helpBtnBg.SetSize(22, 18)
        self.helpBtnBg.SetColor(0xFF004466)
        self.helpBtnBg.AddFlag("not_pick")
        self.helpBtnBg.Show()

        # Bordo top del pulsante (unico bordo, firma visiva)
        self.helpBtnBorder = ui.Bar()
        self.helpBtnBorder.SetParent(self.helpBtn)
        self.helpBtnBorder.SetPosition(0, 0)
        self.helpBtnBorder.SetSize(22, 2)
        self.helpBtnBorder.SetColor(0xFF00CCFF)
        self.helpBtnBorder.AddFlag("not_pick")
        self.helpBtnBorder.Show()

        self.helpBtnText = ui.TextLine()
        self.helpBtnText.SetParent(self.helpBtn)
        self.helpBtnText.SetPosition(11, 2)
        self.helpBtnText.SetHorizontalAlignCenter()
        self.helpBtnText.SetText("?")
        self.helpBtnText.SetPackedFontColor(0xFF00FFFF)
        self.helpBtnText.AddFlag("not_pick")
        self.helpBtnText.Show()

        self.helpBtn.OnMouseOverIn = self.__OnHelpHoverIn
        self.helpBtn.OnMouseOverOut = self.__OnHelpHoverOut

        # Pulsante chiudi (tasto X) - FIX: usa ui.Window con SetSize per area cliccabile
        self.closeBtn = ui.Window()
        self.closeBtn.SetParent(self)
        self.closeBtn.SetPosition(312, 6)
        self.closeBtn.SetSize(20, 18)
        self.closeBtn.Show()

        self.closeBtnBg = ui.Bar()
        self.closeBtnBg.SetParent(self.closeBtn)
        self.closeBtnBg.SetPosition(0, 0)
        self.closeBtnBg.SetSize(20, 18)
        self.closeBtnBg.SetColor(0xFFAA0000)
        self.closeBtnBg.AddFlag("not_pick")
        self.closeBtnBg.Show()

        self.closeBtnText = ui.TextLine()
        self.closeBtnText.SetParent(self.closeBtn)
        self.closeBtnText.SetPosition(10, 2)
        self.closeBtnText.SetHorizontalAlignCenter()
        self.closeBtnText.SetText("X")
        self.closeBtnText.SetPackedFontColor(0xFFFFFFFF)
        self.closeBtnText.AddFlag("not_pick")
        self.closeBtnText.Show()

        self.closeBtn.OnMouseLeftButtonUp = lambda: self.Close()
        
        self.Hide()
    
    def __CreateMissionSlot(self, index):
        """Crea uno slot missione"""
        slot = {}
        
        # yBase parte da y=45 e ogni slot e' alto 65 px
        yBase = 45 + index * 65
        
        # Numero slot con sfondo
        numBg = ui.Bar()
        numBg.SetParent(self)
        numBg.SetPosition(15, yBase + 8)
        numBg.SetSize(45, 45)
        numBg.SetColor(0xFF003366)
        numBg.AddFlag("not_pick")
        numBg.Show()
        slot["numBg"] = numBg
        
        numText = ui.TextLine()
        numText.SetParent(self)
        numText.SetPosition(37, yBase + 22)
        numText.SetHorizontalAlignCenter()
        numText.SetText(str(index + 1))
        numText.SetPackedFontColor(0xFF00FFFF)
        numText.Show()
        slot["numText"] = numText
        
        # Nome missione
        nameText = ui.TextLine()
        nameText.SetParent(self)
        nameText.SetPosition(75, yBase + 8)
        nameText.SetText(T("WAITING", "In attesa..."))
        nameText.SetPackedFontColor(0xFFFFFFFF)
        nameText.Show()
        slot["nameText"] = nameText
        
        # Progresso text
        progressText = ui.TextLine()
        progressText.SetParent(self)
        progressText.SetPosition(75, yBase + 28)
        progressText.SetText("0 / 0")
        progressText.SetPackedFontColor(0xFFAAAAAA)
        progressText.Show()
        slot["progressText"] = progressText
        
        # Progress bar background
        barBg = ui.Bar()
        barBg.SetParent(self)
        barBg.SetPosition(75, yBase + 48)
        barBg.SetSize(200, 12)
        barBg.SetColor(0x44000000)
        barBg.AddFlag("not_pick")
        barBg.Show()
        slot["barBg"] = barBg
        
        # Progress bar fill
        barFill = ui.Bar()
        barFill.SetParent(self)
        barFill.SetPosition(75, yBase + 48)
        barFill.SetSize(0, 12)
        barFill.SetColor(0xFF00CCFF)
        barFill.AddFlag("not_pick")
        barFill.Show()
        slot["barFill"] = barFill
        self.progressBars.append(barFill)
        
        # Reward text
        rewardText = ui.TextLine()
        rewardText.SetParent(self)
        rewardText.SetPosition(285, yBase + 12)
        rewardText.SetText("+0")
        rewardText.SetPackedFontColor(0xFFFFD700)
        rewardText.Show()
        slot["rewardText"] = rewardText
        
        # Penalty text (malus)
        penaltyText = ui.TextLine()
        penaltyText.SetParent(self)
        penaltyText.SetPosition(285, yBase + 28)
        penaltyText.SetText("")
        penaltyText.SetPackedFontColor(0xFFFF4444)
        penaltyText.Show()
        slot["penaltyText"] = penaltyText
        
        # Status icon/text
        statusText = ui.TextLine()
        statusText.SetParent(self)
        statusText.SetPosition(285, yBase + 44)
        statusText.SetText("")
        statusText.SetPackedFontColor(0xFF00FF00)
        statusText.Show()
        slot["statusText"] = statusText
        
        # ====== HOVER AREA per tooltip posizione ======
        hoverArea = ui.Window()
        hoverArea.SetParent(self)
        hoverArea.SetPosition(15, yBase + 8)
        hoverArea.SetSize(260, 52)  # copre l'area del mission slot
        hoverArea.Show()
        slotIndex = index  # cattura per closure
        hoverArea.OnMouseOverIn = lambda idx=slotIndex: self.__OnMissionHoverIn(idx)
        hoverArea.OnMouseOverOut = lambda idx=slotIndex: self.__OnMissionHoverOut(idx)
        slot["hoverArea"] = hoverArea
        
        return slot
    
    def SetMissions(self, missions, theme):
        """Imposta i dati delle missioni"""
        self.missions = missions
        self.theme = theme
        self.__UpdateSlots()
        self.__CheckAllComplete()  # Controlla bonus all'apertura
    
    def __UpdateSlots(self):
        """Aggiorna gli slot con i dati delle missioni"""
        for i, slot in enumerate(self.missionSlots):
            if i < len(self.missions):
                m = self.missions[i]
                slot["nameText"].SetText(m["name"][:35])
                slot["progressText"].SetText("%d / %d" % (m["current"], m["target"]))
                slot["rewardText"].SetText("+%d" % m["reward"])
                
                # Mostra penalita (malus) se presente
                penalty = m.get("penalty", 0)
                if penalty > 0:
                    slot["penaltyText"].SetText("-%d" % penalty)
                else:
                    slot["penaltyText"].SetText("")
                
                # Progress bar
                pct = float(m["current"]) / float(m["target"]) if m["target"] > 0 else 0
                pct = min(1.0, pct)
                slot["barFill"].SetSize(int(200 * pct), 12)
                
                # Status
                if m["status"] == "completed":
                    slot["statusText"].SetText("[OK]")
                    slot["statusText"].SetPackedFontColor(0xFF00FF00)
                    slot["barFill"].SetColor(0xFF00FF00)
                    slot["penaltyText"].SetText("")  # Nascondi penalty se completata
                elif m["status"] == "failed":
                    slot["statusText"].SetText("[X]")
                    slot["statusText"].SetPackedFontColor(0xFFFF0000)
                    slot["barFill"].SetColor(0xFFFF0000)
                else:
                    slot["statusText"].SetText("")
                    slot["barFill"].SetColor(self.theme["accent"] if self.theme else 0xFF00CCFF)
            else:
                slot["nameText"].SetText(T("NO_MISSION", "Nessuna missione"))
                slot["progressText"].SetText("")
                slot["rewardText"].SetText("")
                slot["penaltyText"].SetText("")
                slot["statusText"].SetText("")
                slot["barFill"].SetSize(0, 12)
    
    def UpdateProgress(self, missionId, current, target):
        """Aggiorna progresso di una missione"""
        for i, m in enumerate(self.missions):
            if m["id"] == missionId:
                m["current"] = current
                m["target"] = target
                if i < len(self.missionSlots):
                    slot = self.missionSlots[i]
                    slot["progressText"].SetText("%d / %d" % (current, target))
                    pct = float(current) / float(target) if target > 0 else 0
                    pct = min(1.0, pct)
                    slot["barFill"].SetSize(int(200 * pct), 12)
                break
    
    def SetMissionComplete(self, missionId):
        """Marca una missione come completata"""
        for i, m in enumerate(self.missions):
            if m["id"] == missionId:
                m["status"] = "completed"
                if i < len(self.missionSlots):
                    slot = self.missionSlots[i]
                    slot["statusText"].SetText("[OK]")
                    slot["statusText"].SetPackedFontColor(0xFF00FF00)
                    slot["barFill"].SetColor(0xFF00FF00)
                    slot["barFill"].SetSize(200, 12)
                break
        
        # Controlla se tutte complete
        self.__CheckAllComplete()
    
    def __CheckAllComplete(self):
        """Controlla se tutte le missioni sono complete e mostra bonus"""
        if not self.missions:
            return
        
        allComplete = all(m.get("status") == "completed" for m in self.missions)
        if allComplete:
            self.SetBonusActive(True)
        else:
            self.SetBonusActive(False)
    
    def SetBonusActive(self, active):
        """Mostra/nasconde l'avviso bonus attivo"""
        if active:
            self.bonusActiveText.SetText(T("BONUS_GLORY_ACTIVE", ">>> BONUS GLORIA x1.5 ATTIVO! <<<"))
            self.bonusActiveText.SetPackedFontColor(0xFF00FF00)
            self.bonusDesc.SetText(T("BONUS_ACTIVE_DESC", "ATTIVO! Gloria x1.5 fino alle 00:00!"))
            self.bonusDesc.SetPackedFontColor(0xFF00FF00)
        else:
            self.bonusActiveText.SetText("")
            self.bonusDesc.SetText(T("BONUS_DESC", "Completa tutte: Gloria x1.5 fino al reset!"))
            self.bonusDesc.SetPackedFontColor(0xFFFFD700)
    
    def Open(self, missions=None, theme=None):
        """Apre la finestra, opzionalmente con nuovi dati"""
        if missions is not None:
            self.SetMissions(missions, theme)
        self.lastUpdateTime = app.GetTime()
        self.SetTop()
        self.Show()
    
    def OnPressEscapeKey(self):
        self.autoCloseTimer = 0.0
        tip = _GetMissionGuideTooltip()
        tip.HideGuide()
        locTip = _GetMissionLocationTooltip()
        locTip.HideTooltip()
        self.Hide()
        return True
    
    def Close(self):
        self.autoCloseTimer = 0.0
        # Nascondi anche tooltip guida/posizione se aperti
        tip = _GetMissionGuideTooltip()
        tip.HideGuide()
        locTip = _GetMissionLocationTooltip()
        locTip.HideTooltip()
        self.Hide()

    def __OnHelpHoverIn(self):
        """Mostra tooltip guida quando hover sul ?"""
        self.helpBtnBg.SetColor(0xFF006688)
        tip = _GetMissionGuideTooltip()
        tip.ShowGuide()

    def __OnHelpHoverOut(self):
        """Nasconde tooltip guida"""
        self.helpBtnBg.SetColor(0xFF004466)
        tip = _GetMissionGuideTooltip()
        tip.HideGuide()

    def __OnMissionHoverIn(self, slotIndex):
        """Mostra tooltip posizione mob quando hover su uno slot missione"""
        if slotIndex >= len(self.missions):
            return
        mission = self.missions[slotIndex]
        # Calcola posizione assoluta dello slot sullo schermo
        (selfX, selfY) = self.GetGlobalPosition()
        yBase = 45 + slotIndex * 65
        slotScreenX = selfX + 15
        slotScreenY = selfY + yBase + 8
        tip = _GetMissionLocationTooltip()
        tip.ShowForMission(mission, slotScreenX, slotScreenY)

    def __OnMissionHoverOut(self, slotIndex):
        """Nasconde tooltip posizione mob"""
        tip = _GetMissionLocationTooltip()
        tip.HideTooltip()


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION PROGRESS POPUP - Popup progresso (3 secondi)
# ═══════════════════════════════════════════════════════════════════════════════
class MissionProgressPopup(ui.Window):
    """Popup che appare per 3 sec quando si fa progresso"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(250, 50)
        
        self.endTime = 0
        self.theme = None
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition(screenWidth // 2 - 125, 350)
        
        # Background
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(250, 50)
        self.bgBar.SetColor(0xDD0A0A0A)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(250, 2)
        self.borderTop.SetColor(0xFF00CCFF)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 48)
        self.borderBot.SetSize(250, 2)
        self.borderBot.SetColor(0xFF00CCFF)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(125, 8)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("MISSION", "MISSIONE"))
        self.titleText.SetPackedFontColor(0xFF00FFFF)
        self.titleText.Show()
        
        # Progresso
        self.progressText = ui.TextLine()
        self.progressText.SetParent(self)
        self.progressText.SetPosition(125, 28)
        self.progressText.SetHorizontalAlignCenter()
        self.progressText.SetText("0 / 0")
        self.progressText.SetPackedFontColor(0xFFFFFFFF)
        self.progressText.Show()
        
        self.Hide()
    
    def ShowProgress(self, missionName, current, target, theme=None):
        """Mostra popup con progresso"""
        self.theme = theme
        
        # Nome troncato
        name = missionName[:25] + "..." if len(missionName) > 25 else missionName
        self.titleText.SetText(name)
        self.progressText.SetText("%d / %d" % (current, target))
        
        # Colori tema
        if theme:
            self.borderTop.SetColor(theme.get("accent", 0xFF00CCFF))
            self.borderBot.SetColor(theme.get("accent", 0xFF00CCFF))
            self.titleText.SetPackedFontColor(theme.get("text_title", 0xFF00FFFF))
        
        self.endTime = app.GetTime() + 3.0
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  MISSION COMPLETE WINDOW - Effetto completamento
# ═══════════════════════════════════════════════════════════════════════════════
class MissionCompleteWindow(ui.Window):
    """Finestra effetto completamento missione"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        self.SetSize(screenWidth, screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        
        self.endTime = 0
        self.startTime = 0
        self.theme = None
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        # Flash overlay
        self.flashOverlay = ui.Bar()
        self.flashOverlay.SetParent(self)
        self.flashOverlay.SetPosition(0, 0)
        self.flashOverlay.SetSize(screenWidth, screenHeight)
        self.flashOverlay.SetColor(0x0000FF00)
        self.flashOverlay.AddFlag("not_pick")
        self.flashOverlay.Show()
        
        # Box centrale
        boxWidth = 400
        boxHeight = 120
        boxX = (screenWidth - boxWidth) // 2
        boxY = (screenHeight - boxHeight) // 2 - 50
        
        self.boxBg = ui.Bar()
        self.boxBg.SetParent(self)
        self.boxBg.SetPosition(boxX, boxY)
        self.boxBg.SetSize(boxWidth, boxHeight)
        self.boxBg.SetColor(0xEE0A0A0A)
        self.boxBg.AddFlag("not_pick")
        self.boxBg.Show()
        
        # Bordi box
        self.boxBorderTop = ui.Bar()
        self.boxBorderTop.SetParent(self)
        self.boxBorderTop.SetPosition(boxX, boxY)
        self.boxBorderTop.SetSize(boxWidth, 3)
        self.boxBorderTop.SetColor(0xFF00FF00)
        self.boxBorderTop.AddFlag("not_pick")
        self.boxBorderTop.Show()
        
        self.boxBorderBot = ui.Bar()
        self.boxBorderBot.SetParent(self)
        self.boxBorderBot.SetPosition(boxX, boxY + boxHeight - 3)
        self.boxBorderBot.SetSize(boxWidth, 3)
        self.boxBorderBot.SetColor(0xFF00FF00)
        self.boxBorderBot.AddFlag("not_pick")
        self.boxBorderBot.Show()
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(screenWidth // 2, boxY + 20)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("MISSION_COMPLETED_TITLE", "< MISSIONE COMPLETATA >"))
        self.titleText.SetPackedFontColor(0xFF00FF00)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        # Nome missione
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(screenWidth // 2, boxY + 50)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(0xFFFFFFFF)
        self.nameText.SetOutline()
        self.nameText.Show()
        
        # Reward
        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(screenWidth // 2, boxY + 80)
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFD700)
        self.rewardText.SetOutline()
        self.rewardText.Show()
        
        self.Hide()
    
    def ShowComplete(self, missionName, reward, theme=None):
        """Mostra effetto completamento"""
        self.theme = theme
        self.nameText.SetText(missionName)
        self.rewardText.SetText("+%d %s" % (reward, T("GLORY", "GLORIA")))
        
        if theme:
            self.boxBorderTop.SetColor(theme.get("accent", 0xFF00FF00))
            self.boxBorderBot.SetColor(theme.get("accent", 0xFF00FF00))
            self.titleText.SetPackedFontColor(theme.get("text_title", 0xFF00FF00))
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 3.5
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        elapsed = currentTime - self.startTime
        
        # Flash iniziale (0.5 sec)
        if elapsed < 0.5:
            alpha = int((1.0 - elapsed / 0.5) * 80)
            self.flashOverlay.SetColor((alpha << 24) | 0x00FF00)
        else:
            self.flashOverlay.SetColor(0x00000000)
        
        # Lampeggio bordi
        cycle = (elapsed * 3) % 2
        if cycle < 1:
            c = 0xFF00FF00
        else:
            c = 0xFF00CC00
        self.boxBorderTop.SetColor(c)
        self.boxBorderBot.SetColor(c)


# ═══════════════════════════════════════════════════════════════════════════════
#  ALL MISSIONS COMPLETE WINDOW - Bonus x1.5
# ═══════════════════════════════════════════════════════════════════════════════
class AllMissionsCompleteWindow(ui.Window):
    """Effetto speciale quando si completano tutte e 3 le missioni"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        self.SetSize(screenWidth, screenHeight)
        self.SetPosition(0, 0)
        self.AddFlag("not_pick")
        
        self.endTime = 0
        self.startTime = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        screenHeight = wndMgr.GetScreenHeight()
        
        # Flash overlay dorato
        self.flashOverlay = ui.Bar()
        self.flashOverlay.SetParent(self)
        self.flashOverlay.SetPosition(0, 0)
        self.flashOverlay.SetSize(screenWidth, screenHeight)
        self.flashOverlay.SetColor(0x00FFD700)
        self.flashOverlay.AddFlag("not_pick")
        self.flashOverlay.Show()
        
        # Box centrale grande
        boxWidth = 450
        boxHeight = 150
        boxX = (screenWidth - boxWidth) // 2
        boxY = (screenHeight - boxHeight) // 2 - 50
        
        self.boxBg = ui.Bar()
        self.boxBg.SetParent(self)
        self.boxBg.SetPosition(boxX, boxY)
        self.boxBg.SetSize(boxWidth, boxHeight)
        self.boxBg.SetColor(0xEE0A0A0A)
        self.boxBg.AddFlag("not_pick")
        self.boxBg.Show()
        
        # Bordi oro
        self.boxBorderTop = ui.Bar()
        self.boxBorderTop.SetParent(self)
        self.boxBorderTop.SetPosition(boxX, boxY)
        self.boxBorderTop.SetSize(boxWidth, 4)
        self.boxBorderTop.SetColor(0xFFFFD700)
        self.boxBorderTop.AddFlag("not_pick")
        self.boxBorderTop.Show()
        
        self.boxBorderBot = ui.Bar()
        self.boxBorderBot.SetParent(self)
        self.boxBorderBot.SetPosition(boxX, boxY + boxHeight - 4)
        self.boxBorderBot.SetSize(boxWidth, 4)
        self.boxBorderBot.SetColor(0xFFFFD700)
        self.boxBorderBot.AddFlag("not_pick")
        self.boxBorderBot.Show()
        
        # Titolo speciale
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(screenWidth // 2, boxY + 20)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("ALL_MISSIONS_COMPLETE_TITLE", "=== TUTTE LE MISSIONI COMPLETE ==="))
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.Show()
        
        # Bonus text
        self.bonusText = ui.TextLine()
        self.bonusText.SetParent(self)
        self.bonusText.SetPosition(screenWidth // 2, boxY + 55)
        self.bonusText.SetHorizontalAlignCenter()
        self.bonusText.SetText("BONUS COMPLETAMENTO x1.5")
        self.bonusText.SetPackedFontColor(0xFFFFAA00)
        self.bonusText.SetOutline()
        self.bonusText.Show()
        
        # Reward
        self.rewardText = ui.TextLine()
        self.rewardText.SetParent(self)
        self.rewardText.SetPosition(screenWidth // 2, boxY + 90)
        self.rewardText.SetHorizontalAlignCenter()
        self.rewardText.SetText("")
        self.rewardText.SetPackedFontColor(0xFFFFFFFF)
        self.rewardText.SetOutline()
        self.rewardText.Show()
        
        # Sub text
        self.subText = ui.TextLine()
        self.subText.SetParent(self)
        self.subText.SetPosition(screenWidth // 2, boxY + 115)
        self.subText.SetHorizontalAlignCenter()
        self.subText.SetText(T("GREAT_WORK_HUNTER", "Ottimo lavoro, Cacciatore!"))
        self.subText.SetPackedFontColor(0xFFAAAAAA)
        self.subText.Show()
        
        self.Hide()
    
    def ShowBonus(self, bonusGlory, theme=None, hasFractureBonus=False):
        """Mostra effetto bonus completamento totale"""
        self.rewardText.SetText("+%d %s" % (bonusGlory, T("GLORY_BONUS", "GLORIA BONUS")))
        
        if hasFractureBonus:
            self.bonusText.SetText(T("FRACTURE_BONUS_50", "BONUS FRATTURE +50% PER IL RESTO DEL GIORNO!"))
            self.bonusText.SetPackedFontColor(0xFF00FF00)
        else:
            self.bonusText.SetText(T("COMPLETION_BONUS", "BONUS COMPLETAMENTO x1.5"))
            self.bonusText.SetPackedFontColor(0xFFFFAA00)
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 5.0
        self.SetTop()
        self.Show()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        elapsed = currentTime - self.startTime
        
        # Flash iniziale dorato (0.8 sec)
        if elapsed < 0.8:
            alpha = int((1.0 - elapsed / 0.8) * 100)
            self.flashOverlay.SetColor((alpha << 24) | 0xFFD700)
        else:
            self.flashOverlay.SetColor(0x00000000)
        
        # Lampeggio bordi oro
        cycle = (elapsed * 2.5) % 2
        if cycle < 1:
            self.boxBorderTop.SetColor(0xFFFFD700)
            self.boxBorderBot.SetColor(0xFFFFD700)
            self.titleText.SetPackedFontColor(0xFFFFD700)
        else:
            self.boxBorderTop.SetColor(0xFFFFAA00)
            self.boxBorderBot.SetColor(0xFFFFAA00)
            self.titleText.SetPackedFontColor(0xFFFFEE55)


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENT SLOT HOVER AREA - Tooltip dettagli evento
# ═══════════════════════════════════════════════════════════════════════════════
class EventSlotHoverArea(ui.Window):
    """Area hover per mostrare tooltip dettagli evento"""
    
    EVENT_TYPE_DESC = {
        "glory_rush": ("Gloria x2 per ogni kill!", "Sorteggio finale tra tutti i partecipanti."),
        "first_rift": ("Primo a conquistare una frattura VINCE!", "Non c'e' sorteggio - vince il piu' veloce!"),
        "first_boss": ("Primo a uccidere un boss VINCE!", "Non c'e' sorteggio - vince il piu' veloce!"),
        "boss_massacre": ("Gloria da boss +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "rift_hunt": ("Spawn fratture aumentato +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "super_metin": ("Gloria da metin +50%!", "Sorteggio finale tra tutti i partecipanti."),
        "metin_frenzy": ("Bonus metin aumentato!", "Sorteggio finale tra tutti i partecipanti."),
        "treasure_race": ("Caccia ai tesori speciali!", "Chi trova piu' tesori vince."),
        "double_spawn": ("Spawn Elite x2!", "Sorteggio finale tra tutti i partecipanti."),
        "pvp_tournament": ("Torneo PvP!", "Partecipa e combatti!"),
        "survival": ("Sopravvivenza!", "Resisti piu' a lungo possibile."),
    }
    
    def __init__(self):
        ui.Window.__init__(self)
        self.eventData = None
        self.toolTip = None
        self.AddFlag("float")
    
    def SetEventData(self, eventData):
        """Imposta i dati dell'evento per il tooltip"""
        self.eventData = eventData
    
    def OnMouseOverIn(self):
        """Mostra tooltip con dettagli evento"""
        if not self.eventData:
            return
        
        try:
            import uiToolTip
            if not self.toolTip:
                self.toolTip = uiToolTip.ToolTip()
            
            self.toolTip.ClearToolTip()
            
            # Titolo con nome evento
            ename = self.eventData.get("name", "Evento")
            etype = self.eventData.get("type", "glory_rush")
            self.toolTip.SetTitle(ename)
            self.toolTip.AppendSpace(5)
            
            # Tipo evento
            typeColors = {
                "glory_rush": 0xFFFFD700,
                "first_rift": 0xFF9932CC,
                "first_boss": 0xFFFF4444,
                "boss_massacre": 0xFFFF6600,
                "rift_hunt": 0xFF9932CC,
                "super_metin": 0xFFFF8800,
                "metin_frenzy": 0xFFFF8800,
                "double_spawn": 0xFFFF4444,
            }
            typeColor = typeColors.get(etype, 0xFFFFFFFF)
            self.toolTip.AppendTextLine("Tipo: %s" % etype.replace("_", " ").upper(), typeColor)
            self.toolTip.AppendSpace(5)
            
            # Descrizione evento
            desc1, desc2 = self.EVENT_TYPE_DESC.get(etype, ("Evento speciale!", "Partecipa per vincere!"))
            self.toolTip.AppendTextLine(desc1, 0xFF00FF00)
            self.toolTip.AppendTextLine(desc2, 0xFFAAAAAA)
            self.toolTip.AppendSpace(5)
            
            # Orari
            self.toolTip.AppendTextLine("--------------------------------", 0xFF444444)
            startTime = self.eventData.get("start_time", "--:--")
            endTime = self.eventData.get("end_time", "--:--")
            self.toolTip.AppendTextLine("Orario: %s - %s" % (startTime, endTime), 0xFFFFAA00)
            
            # Requisiti
            minRank = self.eventData.get("min_rank", "E")
            self.toolTip.AppendTextLine("Rank minimo: %s" % minRank, 0xFFCCCCCC)
            self.toolTip.AppendSpace(5)
            
            # Premi
            self.toolTip.AppendTextLine("--------------------------------", 0xFF444444)
            self.toolTip.AppendTextLine("[PREMI]", 0xFFFFD700)
            reward = self.eventData.get("reward", "+50 Gloria")
            self.toolTip.AppendTextLine("Partecipazione: %s" % reward, 0xFF88FF88)
            winnerPrize = self.eventData.get("winner_prize", 200)
            self.toolTip.AppendTextLine("Vincitore: +%d Gloria!" % winnerPrize, 0xFF00FF00)
            self.toolTip.AppendSpace(5)
            
            # Status iscrizione player
            isRegistered = self.eventData.get("is_registered", 0)
            playerWon = self.eventData.get("player_won", 0)
            status = self.eventData.get("status", "pending")

            if playerWon == 1:
                self.toolTip.AppendTextLine("[HAI VINTO!]", 0xFF00FF00)
            elif isRegistered == 1:
                self.toolTip.AppendTextLine("[SEI ISCRITTO]", 0xFF00FFFF)
            elif status == "active":
                self.toolTip.AppendTextLine("[EVENTO IN CORSO]", 0xFFFFAA00)
                self.toolTip.AppendTextLine("Gioca per iscriverti!", 0xFFCCCCCC)
            elif status == "ended":
                self.toolTip.AppendTextLine("[TERMINATO]", 0xFF888888)
            else:
                self.toolTip.AppendTextLine("[NON ANCORA INIZIATO]", 0xFFAAAAAA)

            # Info vincitore (per eventi first_rift, first_boss)
            winnerName = self.eventData.get("winner_name", "")
            winnerRank = self.eventData.get("winner_rank", "")
            if winnerName:
                self.toolTip.AppendSpace(5)
                self.toolTip.AppendTextLine("--------------------------------", 0xFF444444)
                self.toolTip.AppendTextLine("[VINCITORE DI OGGI]", 0xFFFFD700)
                rankColors = {"E": 0xFF808080, "D": 0xFF8B4513, "C": 0xFF00FF00, "B": 0xFF00BFFF, "A": 0xFFFFD700, "S": 0xFFFF4500, "N": 0xFFFF00FF}
                rankColor = rankColors.get(winnerRank, 0xFFFFFFFF)
                self.toolTip.AppendTextLine("%s [%s-Rank]" % (winnerName, winnerRank), rankColor)
            elif etype in ("first_rift", "first_boss") and status == "active":
                self.toolTip.AppendSpace(3)
                self.toolTip.AppendTextLine("Nessun vincitore ancora!", 0xFFFF6600)
                self.toolTip.AppendTextLine("Sii il primo!", 0xFFFFFF00)

            self.toolTip.AppendSpace(3)
            self.toolTip.Show()
        except:
            pass
    
    def OnMouseOverOut(self):
        """Nasconde tooltip"""
        if self.toolTip:
            self.toolTip.Hide()


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENTS SCHEDULE WINDOW - Finestra eventi programmati
# ═══════════════════════════════════════════════════════════════════════════════
class EventsScheduleWindow(ui.Window, DraggableMixin):
    """Finestra per visualizzare gli eventi del giorno - Movibile"""
    
    SLOT_HEIGHT = 58
    VISIBLE_SLOTS = 6
    MAX_SLOTS = 50
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.SetSize(420, 480)
        
        # Inizializza drag con memoria posizione
        self.InitDraggable("EventsScheduleWindow", 100, 80)
        
        self.events = []
        self.eventSlots = []
        self.theme = None
        self.scrollPos = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background principale
        self.bgMain = ui.Bar()
        self.bgMain.SetParent(self)
        self.bgMain.SetPosition(0, 0)
        self.bgMain.SetSize(420, 480)
        self.bgMain.SetColor(0xEE0A0A0A)
        self.bgMain.AddFlag("not_pick")
        self.bgMain.Show()
        
        # Bordi arancioni
        self.borders = []
        for i, (x, y, w, h) in enumerate([
            (0, 0, 420, 2),   # top
            (0, 478, 420, 2), # bottom
            (0, 0, 2, 480),   # left
            (418, 0, 2, 480)  # right
        ]):
            b = ui.Bar()
            b.SetParent(self)
            b.SetPosition(x, y)
            b.SetSize(w, h)
            b.SetColor(0xFFFF6600)
            b.AddFlag("not_pick")
            b.Show()
            self.borders.append(b)
        
        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(200, 12)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText(T("TODAY_EVENTS_TITLE", "< EVENTI DI OGGI >"))
        self.titleText.SetPackedFontColor(0xFFFFAA00)
        self.titleText.Show()

        # Bottone chiudi (X)
        self.btnClose = ui.Window()
        self.btnClose.SetParent(self)
        self.btnClose.SetPosition(420 - 30, 6)
        self.btnClose.SetSize(24, 24)

        self.btnCloseBg = ui.Bar()
        self.btnCloseBg.SetParent(self.btnClose)
        self.btnCloseBg.SetPosition(0, 0)
        self.btnCloseBg.SetSize(24, 24)
        self.btnCloseBg.SetColor(0xAA8B0000)
        self.btnCloseBg.AddFlag("not_pick")
        self.btnCloseBg.Show()

        self.btnCloseText = ui.TextLine()
        self.btnCloseText.SetParent(self.btnClose)
        self.btnCloseText.SetPosition(12, 3)
        self.btnCloseText.SetHorizontalAlignCenter()
        self.btnCloseText.SetText("X")
        self.btnCloseText.SetPackedFontColor(0xFFFFFFFF)
        self.btnCloseText.AddFlag("not_pick")
        self.btnCloseText.Show()

        self.btnClose.OnMouseLeftButtonUp = lambda: self.Hide()
        self.btnClose.Show()
        
        # Bottone info (?)
        self.btnInfo = ui.Window()
        self.btnInfo.SetParent(self)
        self.btnInfo.SetPosition(420 - 58, 6)
        self.btnInfo.SetSize(24, 24)

        self.btnInfoBg = ui.Bar()
        self.btnInfoBg.SetParent(self.btnInfo)
        self.btnInfoBg.SetPosition(0, 0)
        self.btnInfoBg.SetSize(24, 24)
        self.btnInfoBg.SetColor(0xAA003366)
        self.btnInfoBg.AddFlag("not_pick")
        self.btnInfoBg.Show()

        self.btnInfoText = ui.TextLine()
        self.btnInfoText.SetParent(self.btnInfo)
        self.btnInfoText.SetPosition(12, 3)
        self.btnInfoText.SetHorizontalAlignCenter()
        self.btnInfoText.SetText("?")
        self.btnInfoText.SetPackedFontColor(0xFF00CCFF)
        self.btnInfoText.AddFlag("not_pick")
        self.btnInfoText.Show()

        self.btnInfo.OnMouseLeftButtonUp = lambda: self.__ToggleInfoPopup()
        self.btnInfo.Show()
        
        # Linea separatore titolo
        self.sepLine = ui.Bar()
        self.sepLine.SetParent(self)
        self.sepLine.SetPosition(10, 38)
        self.sepLine.SetSize(398, 1)
        self.sepLine.SetColor(0xFFFF6600)
        self.sepLine.AddFlag("not_pick")
        self.sepLine.Show()
        
        # Messaggio se non ci sono eventi
        self.noEventsText = ui.TextLine()
        self.noEventsText.SetParent(self)
        self.noEventsText.SetPosition(200, 180)
        self.noEventsText.SetHorizontalAlignCenter()
        self.noEventsText.SetText(T("NO_EVENTS_TODAY", "Nessun evento programmato oggi"))
        self.noEventsText.SetPackedFontColor(0xFF888888)
        self.noEventsText.Hide()
        
        # Area scrollabile
        listAreaHeight = self.VISIBLE_SLOTS * self.SLOT_HEIGHT
        
        # Background area lista
        self.listBg = ui.Bar()
        self.listBg.SetParent(self)
        self.listBg.SetPosition(8, 45)
        self.listBg.SetSize(385, listAreaHeight)
        self.listBg.SetColor(0x22000000)
        self.listBg.AddFlag("not_pick")
        self.listBg.Show()
        
        # ScrollBar
        self.scrollBar = ui.ScrollBar()
        self.scrollBar.SetParent(self)
        self.scrollBar.SetPosition(395, 45)
        self.scrollBar.SetScrollBarSize(listAreaHeight)
        self.scrollBar.SetScrollEvent(self.__OnScroll)
        self.scrollBar.Hide()
        
        # Crea solo gli slot visibili
        for i in range(self.VISIBLE_SLOTS):
            slot = self.__CreateEventSlot(i)
            self.eventSlots.append(slot)
        
        # Sezione INFO
        infoY = 400
        
        self.sepInfo = ui.Bar()
        self.sepInfo.SetParent(self)
        self.sepInfo.SetPosition(10, infoY)
        self.sepInfo.SetSize(398, 1)
        self.sepInfo.SetColor(0xFFFF6600)
        self.sepInfo.AddFlag("not_pick")
        self.sepInfo.Show()
        
        self.infoBox = ui.Bar()
        self.infoBox.SetParent(self)
        self.infoBox.SetPosition(10, infoY + 8)
        self.infoBox.SetSize(398, 62)
        self.infoBox.SetColor(0x33FF6600)
        self.infoBox.AddFlag("not_pick")
        self.infoBox.Show()
        
        self.infoTitle = ui.TextLine()
        self.infoTitle.SetParent(self)
        self.infoTitle.SetPosition(210, infoY + 12)
        self.infoTitle.SetHorizontalAlignCenter()
        self.infoTitle.SetText(T("AUTO_REGISTRATION", "ISCRIZIONE AUTOMATICA"))
        self.infoTitle.SetPackedFontColor(0xFFFFAA00)
        self.infoTitle.Show()
        
        self.infoLine1 = ui.TextLine()
        self.infoLine1.SetParent(self)
        self.infoLine1.SetPosition(210, infoY + 28)
        self.infoLine1.SetHorizontalAlignCenter()
        self.infoLine1.SetText(T("AUTO_REG_INFO1", "Conquista fratture, uccidi boss o metinpietra"))
        self.infoLine1.SetPackedFontColor(0xFFCCCCCC)
        self.infoLine1.Show()
        
        self.infoLine2 = ui.TextLine()
        self.infoLine2.SetParent(self)
        self.infoLine2.SetPosition(210, infoY + 44)
        self.infoLine2.SetHorizontalAlignCenter()
        self.infoLine2.SetText(T("AUTO_REG_INFO2", "per iscriverti automaticamente e partecipare!"))
        self.infoLine2.SetPackedFontColor(0xFF88FF88)
        self.infoLine2.Show()
        
        # Popup info eventi (nascosto di default)
        self.__BuildInfoPopup()
        
        self.Hide()
    
    def __BuildInfoPopup(self):
        """Crea il popup informativo sugli eventi"""
        self.infoPopup = ui.Window()
        self.infoPopup.SetParent(self)
        self.infoPopup.SetPosition(20, 40)
        self.infoPopup.SetSize(380, 390)
        
        # Sfondo scuro semi-trasparente
        # NOTA: Tutti i widget figli DEVONO essere salvati come self.xxx
        # altrimenti Python li garbage-collecta e wndMgr.Destroy() li elimina dal C++.
        self.popupBg = ui.Bar()
        self.popupBg.SetParent(self.infoPopup)
        self.popupBg.SetPosition(0, 0)
        self.popupBg.SetSize(380, 390)
        self.popupBg.SetColor(0xF0080808)
        self.popupBg.AddFlag("not_pick")
        self.popupBg.Show()
        
        # Bordo arancione
        self.popupBorders = []
        for x, y, w, h in [
            (0, 0, 380, 1), (0, 389, 380, 1),
            (0, 0, 1, 390), (379, 0, 1, 390)
        ]:
            brd = ui.Bar()
            brd.SetParent(self.infoPopup)
            brd.SetPosition(x, y)
            brd.SetSize(w, h)
            brd.SetColor(0xFFFF6600)
            brd.AddFlag("not_pick")
            brd.Show()
            self.popupBorders.append(brd)
        
        # Titolo
        self.popupTitle = ui.TextLine()
        self.popupTitle.SetParent(self.infoPopup)
        self.popupTitle.SetPosition(190, 12)
        self.popupTitle.SetHorizontalAlignCenter()
        self.popupTitle.SetText("COME FUNZIONANO GLI EVENTI")
        self.popupTitle.SetPackedFontColor(0xFFFFAA00)
        self.popupTitle.AddFlag("not_pick")
        self.popupTitle.Show()
        
        # Separatore
        self.popupSep = ui.Bar()
        self.popupSep.SetParent(self.infoPopup)
        self.popupSep.SetPosition(15, 30)
        self.popupSep.SetSize(350, 1)
        self.popupSep.SetColor(0xAAFF6600)
        self.popupSep.AddFlag("not_pick")
        self.popupSep.Show()
        
        # Contenuto informativo
        infoLines = [
            (0xFFFF6600, "ISCRIZIONE"),
            (0xFFCCCCCC, "Gli eventi non richiedono iscrizione manuale."),
            (0xFFCCCCCC, "Basta giocare normalmente: uccidi boss, metinpietra"),
            (0xFFCCCCCC, "o conquista fratture per iscriverti automaticamente."),
            (0, ""),
            (0xFFFF6600, "ORARI"),
            (0xFFCCCCCC, "Ogni evento ha una fascia oraria precisa."),
            (0xFFCCCCCC, "Se un evento e' [IN CORSO] puoi partecipare."),
            (0xFFCCCCCC, "Quelli [TERMINATO] sono finiti per oggi."),
            (0, ""),
            (0xFFFF6600, "TIPI DI EVENTO"),
            (0xFF88FF88, "  Glory Rush - Accumula piu' gloria possibile"),
            (0xFF9932CC, "  First Rift / First Boss - Primo a completare vince"),
            (0xFFFF8800, "  Metin Frenzy / Super Metin - Distruggi metinpietra"),
            (0xFFFF4444, "  Boss Massacre - Uccidi il maggior numero di boss"),
            (0, ""),
            (0xFFFF6600, "PREMI"),
            (0xFFCCCCCC, "Ogni evento assegna Gloria come ricompensa."),
            (0xFFCCCCCC, "I premi vengono accreditati automaticamente."),
            (0xFFFFD700, "  [HAI VINTO!] = Hai vinto l'evento"),
            (0xFF00FFFF, "  [ISCRITTO] = Sei iscritto e partecipi"),
        ]
        
        self.popupTextLines = []
        yOff = 40
        for color, text in infoLines:
            if text == "":
                yOff += 6
                continue
            line = ui.TextLine()
            line.SetParent(self.infoPopup)
            line.SetPosition(20, yOff)
            line.SetText(text)
            line.SetPackedFontColor(color)
            line.AddFlag("not_pick")
            line.Show()
            self.popupTextLines.append(line)
            yOff += 16
        
        # Bottone chiudi popup
        self.closeInfoBtn = ui.Window()
        self.closeInfoBtn.SetParent(self.infoPopup)
        self.closeInfoBtn.SetPosition(155, 360)
        self.closeInfoBtn.SetSize(70, 22)
        
        self.closeInfoBg = ui.Bar()
        self.closeInfoBg.SetParent(self.closeInfoBtn)
        self.closeInfoBg.SetPosition(0, 0)
        self.closeInfoBg.SetSize(70, 22)
        self.closeInfoBg.SetColor(0xAA8B0000)
        self.closeInfoBg.AddFlag("not_pick")
        self.closeInfoBg.Show()
        
        self.closeInfoText = ui.TextLine()
        self.closeInfoText.SetParent(self.closeInfoBtn)
        self.closeInfoText.SetPosition(35, 3)
        self.closeInfoText.SetHorizontalAlignCenter()
        self.closeInfoText.SetText("CHIUDI")
        self.closeInfoText.SetPackedFontColor(0xFFFFFFFF)
        self.closeInfoText.AddFlag("not_pick")
        self.closeInfoText.Show()
        
        self.closeInfoBtn.OnMouseLeftButtonUp = lambda: self.infoPopup.Hide()
        self.closeInfoBtn.Show()
        
        self.infoPopup.Hide()
    
    def __ToggleInfoPopup(self):
        """Mostra/nasconde il popup informativo"""
        if self.infoPopup.IsShow():
            self.infoPopup.Hide()
        else:
            self.infoPopup.SetTop()
            self.infoPopup.Show()
    
    def __CreateEventSlot(self, index):
        """Crea uno slot evento"""
        slot = {}
        
        yBase = 48 + index * self.SLOT_HEIGHT
        
        # Background slot
        slotBg = ui.Bar()
        slotBg.SetParent(self)
        slotBg.SetPosition(12, yBase)
        slotBg.SetSize(375, self.SLOT_HEIGHT - 4)
        slotBg.SetColor(0x44222222)
        slotBg.AddFlag("not_pick")
        slotBg.Show()
        slot["bg"] = slotBg
        
        # Indicatore tipo (colore laterale)
        typeBar = ui.Bar()
        typeBar.SetParent(self)
        typeBar.SetPosition(12, yBase)
        typeBar.SetSize(4, self.SLOT_HEIGHT - 4)
        typeBar.SetColor(0xFFFF6600)
        typeBar.AddFlag("not_pick")
        typeBar.Show()
        slot["typeBar"] = typeBar
        
        # Nome evento
        nameText = ui.TextLine()
        nameText.SetParent(self)
        nameText.SetPosition(22, yBase + 5)
        nameText.SetText("Evento")
        nameText.SetPackedFontColor(0xFFFFFFFF)
        nameText.Show()
        slot["nameText"] = nameText
        
        # Orario
        timeText = ui.TextLine()
        timeText.SetParent(self)
        timeText.SetPosition(22, yBase + 22)
        timeText.SetText("--:-- - --:--")
        timeText.SetPackedFontColor(0xFFAAAAAA)
        timeText.Show()
        slot["timeText"] = timeText
        
        # Reward
        rewardText = ui.TextLine()
        rewardText.SetParent(self)
        rewardText.SetPosition(22, yBase + 38)
        rewardText.SetText("+0")
        rewardText.SetPackedFontColor(0xFFFFD700)
        rewardText.Show()
        slot["rewardText"] = rewardText
        
        # Status text
        statusText = ui.TextLine()
        statusText.SetParent(self)
        statusText.SetPosition(320, yBase + 20)
        statusText.SetText("")
        statusText.SetPackedFontColor(0xFF00FF00)
        statusText.Show()
        slot["statusText"] = statusText
        
        # Hover area
        hoverArea = EventSlotHoverArea()
        hoverArea.SetParent(self)
        hoverArea.SetPosition(12, yBase)
        hoverArea.SetSize(375, self.SLOT_HEIGHT - 4)
        hoverArea.Show()
        slot["hoverArea"] = hoverArea
        
        return slot
    
    def __OnScroll(self):
        """Callback quando si scrolla"""
        scrollPos = self.scrollBar.GetPos()
        maxScroll = max(0, len(self.events) - self.VISIBLE_SLOTS)
        self.scrollPos = int(scrollPos * maxScroll + 0.5)
        self.__UpdateSlotPositions()
    
    def __UpdateSlotPositions(self):
        """Aggiorna posizione e visibilita degli slot in base allo scroll"""
        for slotIdx, slot in enumerate(self.eventSlots):
            eventIdx = self.scrollPos + slotIdx
            
            if eventIdx < len(self.events):
                event = self.events[eventIdx]
                self.__UpdateSlotWithEvent(slot, event)
                slot["bg"].Show()
                slot["typeBar"].Show()
                slot["nameText"].Show()
                slot["timeText"].Show()
                slot["rewardText"].Show()
                slot["statusText"].Show()
                slot["hoverArea"].SetEventData(event)
                slot["hoverArea"].Show()
            else:
                slot["bg"].Hide()
                slot["typeBar"].Hide()
                slot["nameText"].Hide()
                slot["timeText"].Hide()
                slot["rewardText"].Hide()
                slot["statusText"].Hide()
                slot["hoverArea"].Hide()
    
    def __UpdateSlotWithEvent(self, slot, event):
        """Aggiorna uno slot con i dati di un evento"""
        typeColors = {
            "glory_rush": 0xFFFFD700,
            "first_rift": 0xFF9932CC,
            "first_boss": 0xFFFF4444,
            "boss_massacre": 0xFFFF6600,
            "rift_hunt": 0xFF9932CC,
            "super_metin": 0xFFFF8800,
            "metin_frenzy": 0xFFFF8800,
            "double_spawn": 0xFFFF4444,
        }

        etype = event.get("type", "glory_rush")
        typeColor = typeColors.get(etype, 0xFFFF6600)

        slot["typeBar"].SetColor(typeColor)
        slot["nameText"].SetText(event.get("name", "Evento")[:40])
        slot["timeText"].SetText("%s - %s" % (event.get("start_time", "--:--"), event.get("end_time", "--:--")))

        # Mostra premio o vincitore se c'e'
        winnerName = event.get("winner_name", "")
        winnerRank = event.get("winner_rank", "")
        if winnerName and etype in ("first_rift", "first_boss"):
            # Mostra vincitore invece del premio
            slot["rewardText"].SetText("Vinto da: %s [%s]" % (winnerName[:12], winnerRank))
            slot["rewardText"].SetPackedFontColor(0xFFFFD700)
        else:
            slot["rewardText"].SetText("+%s" % event.get("reward", "0"))
            slot["rewardText"].SetPackedFontColor(0xFF88FF88)

        # Status con priorita': HAI VINTO > ISCRITTO > IN CORSO > TERMINATO
        status = event.get("status", "pending")
        playerWon = event.get("player_won", 0)
        isRegistered = event.get("is_registered", 0)

        if playerWon == 1:
            slot["statusText"].SetText("[HAI VINTO!]")
            slot["statusText"].SetPackedFontColor(0xFF00FF00)
            slot["bg"].SetColor(0x44006600)
        elif isRegistered == 1:
            slot["statusText"].SetText("[ISCRITTO]")
            slot["statusText"].SetPackedFontColor(0xFF00FFFF)
            slot["bg"].SetColor(0x44003333)
        elif status == "active":
            slot["statusText"].SetText("[IN CORSO]")
            slot["statusText"].SetPackedFontColor(0xFFFFAA00)
            slot["bg"].SetColor(0x44332200)
        elif status == "ended":
            slot["statusText"].SetText("[TERMINATO]")
            slot["statusText"].SetPackedFontColor(0xFF888888)
            slot["bg"].SetColor(0x44222222)
        else:
            slot["statusText"].SetText("")
            slot["bg"].SetColor(0x44222222)
    
    def SetEvents(self, events, theme=None):
        """Imposta la lista eventi"""
        self.events = events if events else []
        self.theme = theme
        self.scrollPos = 0
        
        # Mostra/nascondi scrollbar
        if len(self.events) > self.VISIBLE_SLOTS:
            self.scrollBar.Show()
        else:
            self.scrollBar.Hide()
        
        # Mostra messaggio se nessun evento
        if len(self.events) == 0:
            self.noEventsText.Show()
        else:
            self.noEventsText.Hide()
        
        self.__UpdateSlotPositions()
    
    def Open(self, events=None, theme=None):
        """Apre la finestra"""
        if events is not None:
            self.SetEvents(events, theme)
        self.SetTop()
        self.Show()
    
    def OnPressEscapeKey(self):
        self.Hide()
        return True


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════
g_dailyMissionsWindow = None
g_missionProgressPopup = None
g_missionCompleteWindow = None
g_allMissionsCompleteWindow = None
g_eventsScheduleWindow = None

def GetDailyMissionsWindow():
    global g_dailyMissionsWindow
    if g_dailyMissionsWindow is None:
        g_dailyMissionsWindow = DailyMissionsWindow()
    return g_dailyMissionsWindow

def GetMissionProgressPopup():
    global g_missionProgressPopup
    if g_missionProgressPopup is None:
        g_missionProgressPopup = MissionProgressPopup()
    return g_missionProgressPopup

def GetMissionCompleteWindow():
    global g_missionCompleteWindow
    if g_missionCompleteWindow is None:
        g_missionCompleteWindow = MissionCompleteWindow()
    return g_missionCompleteWindow

def GetAllMissionsCompleteWindow():
    global g_allMissionsCompleteWindow
    if g_allMissionsCompleteWindow is None:
        g_allMissionsCompleteWindow = AllMissionsCompleteWindow()
    return g_allMissionsCompleteWindow

def GetEventsScheduleWindow():
    global g_eventsScheduleWindow
    if g_eventsScheduleWindow is None:
        g_eventsScheduleWindow = EventsScheduleWindow()
    return g_eventsScheduleWindow


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════
def OpenDailyMissions(missions=None, theme=None):
    """Apre finestra missioni giornaliere"""
    GetDailyMissionsWindow().Open(missions, theme)

def ShowMissionProgress(missionName, current, target, theme=None):
    """Mostra popup progresso missione"""
    GetMissionProgressPopup().ShowProgress(missionName, current, target, theme)

def ShowMissionComplete(missionName, reward, theme=None):
    """Mostra effetto missione completata"""
    GetMissionCompleteWindow().ShowComplete(missionName, reward, theme)

def ShowAllMissionsComplete(bonusGlory, theme=None, hasFractureBonus=False):
    """Mostra effetto tutte missioni completate"""
    GetAllMissionsCompleteWindow().ShowBonus(bonusGlory, theme, hasFractureBonus)

def OpenEventsSchedule(events=None, theme=None):
    """Apre finestra eventi"""
    GetEventsScheduleWindow().Open(events, theme)
