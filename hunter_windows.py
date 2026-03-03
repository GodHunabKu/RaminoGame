# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - WINDOWS MODULE
#  Finestre principali del sistema Hunter
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import net
import wndMgr
import app
import math
import player  # Per GetMainCharacterPosition

from hunter_core import (
    DraggableMixin,
    SaveWindowPosition, GetWindowPosition, HasSavedPosition,
    GetDefaultPosition, ResetAllWindowPositions, ResetWindowPosition,
    COLOR_BG_DARK, COLOR_TEXT_NORMAL, COLOR_TEXT_MUTED,
    COLOR_SCHEMES, DEFAULT_SCHEME, FRACTURE_ID_MAP,
    GetColorScheme, GetColorFromKey, DetectColorFromText,
    FormatTime
)
from hunter_components import (
    SoloLevelingWindow, SystemButton, AnimatedProgressBar
)


# ═══════════════════════════════════════════════════════════════════════════════
#  WHAT-IF CHOICE WINDOW - Scelte narrative delle fratture
# ═══════════════════════════════════════════════════════════════════════════════
class WhatIfChoiceWindow(SoloLevelingWindow, DraggableMixin):
    """Finestra di scelta What-If - Movibile con memoria posizione"""
    
    def __init__(self):
        SoloLevelingWindow.__init__(self, 400, 300)
        self.questionId = ""
        self.buttons = []
        self.textLines = []
        
        # Inizializza drag con memoria posizione
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        self.InitDraggable("WhatIfChoiceWindow", (screenW - 400) // 2, (screenH - 300) // 2)
        
        # Header "SYSTEM"
        self.headerText = ui.TextLine()
        self.headerText.SetParent(self)
        self.headerText.SetPosition(200, 10)
        self.headerText.SetHorizontalAlignCenter()
        self.headerText.SetText("SYSTEM")
        self.headerText.SetOutline()
        self.headerText.AddFlag("not_pick")
        self.headerText.Show()
        
        self.subHeaderText = ui.TextLine()
        self.subHeaderText.SetParent(self)
        self.subHeaderText.SetPosition(200, 30)
        self.subHeaderText.SetHorizontalAlignCenter()
        self.subHeaderText.SetText("Una scelta è richiesta.")
        self.subHeaderText.SetPackedFontColor(COLOR_TEXT_MUTED)
        self.subHeaderText.AddFlag("not_pick")
        self.subHeaderText.Show()

    def Create(self, qid, text, options, colorCode="PURPLE"):
        """Crea la finestra con domanda e opzioni"""
        self.questionId = qid
        
        # Pulizia input
        if colorCode:
            colorCode = colorCode.strip()
        
        # 1. Tenta di mappare l'ID al colore
        mappedColor = FRACTURE_ID_MAP.get(str(qid), None)
        if mappedColor:
            colorCode = mappedColor
            
        # 2. Auto-detect se il colore non è valido
        if not colorCode or colorCode not in COLOR_SCHEMES:
            colorCode = DetectColorFromText(text, "PURPLE")
        
        # 3. Applica schema colori
        scheme = GetColorScheme(colorCode)
        self.SetColorScheme(scheme)
        self.headerText.SetPackedFontColor(scheme.get("title", 0xFFFFFFFF))
        
        # Reset UI - distruggi vecchi widget prima di ricreare
        for btn in self.buttons:
            try:
                btn.Hide()
            except:
                pass
        for tl in self.textLines:
            try:
                tl.Hide()
            except:
                pass
        self.buttons = []
        self.textLines = []
        
        # Parsa testo
        lines = text.replace("+", " ").split("|")
        
        # Calcola layout
        baseY = 60
        lineHeight = 20
        windowWidth = 400
        
        # Crea righe testo
        for line in lines:
            t = ui.TextLine()
            t.SetParent(self)
            t.SetPosition(windowWidth // 2, baseY)
            t.SetHorizontalAlignCenter()
            t.SetText(line)
            t.SetPackedFontColor(COLOR_TEXT_NORMAL)
            t.Show()
            self.textLines.append(t)
            baseY += lineHeight
            
        baseY += 15
        
        # Crea bottoni
        for i, opt in enumerate(options):
            if not opt:
                continue
            
            def make_event(idx):
                return lambda: self.__OnClickOption(idx)
                
            btn = SystemButton(self, 20, baseY, windowWidth - 40, opt.replace("+", " "), scheme, make_event(i + 1))
            self.buttons.append(btn)
            baseY += 40
            
        # Ridimensiona finestra
        totalHeight = baseY + 10
        self.SetSize(windowWidth, totalHeight)
        self.bg.SetSize(windowWidth, totalHeight)
        
        # Aggiorna bordi
        self.borders[1].SetPosition(0, totalHeight - 2)
        self.borders[2].SetSize(2, totalHeight)
        self.borders[3].SetSize(2, totalHeight)
        self.borders[3].SetPosition(windowWidth - 2, 0)
        
        # Centra nello schermo SOLO se non esiste posizione salvata
        if not HasSavedPosition("WhatIfChoiceWindow"):
            screenWidth = wndMgr.GetScreenWidth()
            screenHeight = wndMgr.GetScreenHeight()
            self.SetPosition((screenWidth - windowWidth) // 2, (screenHeight - totalHeight) // 3)
        
        self.Show()
        self.SetTop()
        
    def __OnClickOption(self, val):
        net.SendChatPacket("/hunter_whatif_answer %s %d" % (self.questionId, val))
        self.Close()
        
    def Close(self):
        self.Hide()
        
    def OnKeyDown(self, key):
        if key == app.DIK_ESCAPE:
            if len(self.buttons) >= 3:
                self.__OnClickOption(3)
            else:
                self.Close()
            return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM MESSAGE WINDOW - Messaggi di sistema con coda
# ═══════════════════════════════════════════════════════════════════════════════
class SystemMessageWindow(ui.Window):
    """Messaggio di sistema con colori dinamici e coda messaggi"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(500, 60)
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition((screenWidth - 500) // 2, 180)
        self.AddFlag("not_pick")
        self.AddFlag("float")

        self.currentColor = 0xFF0099FF
        self.messageQueue = []
        self.currentMessage = None
        self.messageDelay = 4.0

        # Sfondo
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(500, 60)
        self.bg.SetColor(COLOR_BG_DARK)
        self.bg.Show()

        # Bordi
        self.borders = []
        color = COLOR_SCHEMES["BLUE"]["border"]
        b1 = ui.Bar(); b1.SetParent(self); b1.SetPosition(0, 0); b1.SetSize(500, 2); b1.SetColor(color); b1.Show()
        self.borders.append(b1)
        b2 = ui.Bar(); b2.SetParent(self); b2.SetPosition(0, 58); b2.SetSize(500, 2); b2.SetColor(color); b2.Show()
        self.borders.append(b2)
        b3 = ui.Bar(); b3.SetParent(self); b3.SetPosition(0, 0); b3.SetSize(2, 60); b3.SetColor(color); b3.Show()
        self.borders.append(b3)
        b4 = ui.Bar(); b4.SetParent(self); b4.SetPosition(498, 0); b4.SetSize(2, 60); b4.SetColor(color); b4.Show()
        self.borders.append(b4)

        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(250, 20)
        self.text.SetHorizontalAlignCenter()
        self.text.SetPackedFontColor(COLOR_SCHEMES["BLUE"]["title"])
        self.text.SetOutline()
        self.text.Show()

        self.endTime = 0

    def __UpdateColors(self, color):
        self.currentColor = color
        for b in self.borders:
            b.SetColor(color)
        self.text.SetPackedFontColor(color)

    def ShowMessage(self, msg, color=None):
        """Aggiungi messaggio alla coda"""
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition((screenWidth - 500) // 2, 180)

        finalColor = self.currentColor
        if color:
            # FIX: Compatibilita' Python 2/3 - usa type() invece di isinstance con long
            if type(color) in (int,) or (hasattr(__builtins__, 'long') and type(color) == long):
                finalColor = color
            elif isinstance(color, str):
                finalColor = GetColorFromKey(color)
            else:
                try:
                    finalColor = int(color)
                except:
                    finalColor = GetColorFromKey(str(color))

        self.messageQueue.append((msg.replace("+", " "), finalColor))
        # Anti-leak: limita coda messaggi
        if len(self.messageQueue) > 20:
            self.messageQueue.pop(0)

        if not self.currentMessage:
            self.__ShowNextMessage()

    def __ShowNextMessage(self):
        if len(self.messageQueue) > 0:
            msg, color = self.messageQueue.pop(0)
            self.__UpdateColors(color)
            self.text.SetText(msg)
            self.currentMessage = msg
            self.endTime = app.GetTime() + self.messageDelay
            self.Show()
            self.SetTop()
        else:
            self.currentMessage = None

    def SetRankColor(self, colorKey):
        color = GetColorFromKey(colorKey)
        self.__UpdateColors(color)

    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0
            self.currentMessage = None
            self.__ShowNextMessage()

    def ClearQueue(self):
        self.messageQueue = []
        self.Hide()
        self.currentMessage = None
        self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  EMERGENCY QUEST WINDOW - Solo Leveling Style - Missioni a tempo
# ═══════════════════════════════════════════════════════════════════════════════

# Colori per difficolta' Emergency Quest
DIFFICULTY_COLORS = {
    "EASY": {"bg": 0xCC004400, "border": 0xFF00FF00, "text": 0xFF00FF00, "label": "FACILE"},
    "NORMAL": {"bg": 0xCC001144, "border": 0xFF00CCFF, "text": 0xFF00CCFF, "label": "NORMALE"},
    "HARD": {"bg": 0xCC442200, "border": 0xFFFF8800, "text": 0xFFFF8800, "label": "DIFFICILE"},
    "EXTREME": {"bg": 0xCC440000, "border": 0xFFFF0000, "text": 0xFFFF0000, "label": "ESTREMA"},
    "GOD_MODE": {"bg": 0xCC220044, "border": 0xFFFF00FF, "text": 0xFFFF00FF, "label": "DIVINO"}
}

class EmergencyQuestWindow(ui.Window, DraggableMixin):
    """Emergency Quest - Solo Leveling Style - Finestra Espansa con Descrizione"""

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(420, 220)
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("EmergencyQuestWindow", 420, 220)

        self.InitDraggable("EmergencyQuestWindow", defaultX, defaultY)

        # Variabili di stato
        self.endTime = 0
        self.currentTitle = ""
        self.targetCount = 0
        self.currentProgress = 0
        self.description = ""
        self.difficulty = "NORMAL"
        self.penalty = 0
        self.pulsePhase = 0.0

        # Sfondo principale scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(420, 220)
        self.bg.SetColor(0xEE0A0A14)  # Quasi nero con sfumatura blu scuro
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Inner glow effect (bordo interno luminoso)
        self.innerGlow = ui.Bar()
        self.innerGlow.SetParent(self)
        self.innerGlow.SetPosition(3, 3)
        self.innerGlow.SetSize(414, 214)
        self.innerGlow.SetColor(0x22FFFFFF)
        self.innerGlow.AddFlag("not_pick")
        self.innerGlow.Show()

        # Inner background
        self.innerBg = ui.Bar()
        self.innerBg.SetParent(self)
        self.innerBg.SetPosition(5, 5)
        self.innerBg.SetSize(410, 210)
        self.innerBg.SetColor(0xDD080812)
        self.innerBg.AddFlag("not_pick")
        self.innerBg.Show()

        # Bordi esterni animati (4 lati)
        self.borders = []
        self.borderColor = DIFFICULTY_COLORS["NORMAL"]["border"]
        for y in [0, 218]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(420, 2); b.SetColor(self.borderColor); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, 418]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, 220); b.SetColor(self.borderColor); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)

        # ═══════════ HEADER SECTION ═══════════
        # Linea separatore header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(10, 45)
        self.headerLine.SetSize(400, 1)
        self.headerLine.SetColor(0x66FFFFFF)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # Titolo "EMERGENCY QUEST"
        self.systemLabel = ui.TextLine()
        self.systemLabel.SetParent(self)
        self.systemLabel.SetPosition(210, 8)
        self.systemLabel.SetHorizontalAlignCenter()
        self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
        self.systemLabel.SetPackedFontColor(0xFFFF4444)
        self.systemLabel.SetOutline()
        self.systemLabel.AddFlag("not_pick")
        self.systemLabel.Show()

        # Badge Difficolta'
        self.diffBadgeBg = ui.Bar()
        self.diffBadgeBg.SetParent(self)
        self.diffBadgeBg.SetPosition(10, 25)
        self.diffBadgeBg.SetSize(80, 18)
        self.diffBadgeBg.SetColor(0xCC001144)
        self.diffBadgeBg.AddFlag("not_pick")
        self.diffBadgeBg.Show()

        self.diffBadgeText = ui.TextLine()
        self.diffBadgeText.SetParent(self)
        self.diffBadgeText.SetPosition(50, 27)
        self.diffBadgeText.SetHorizontalAlignCenter()
        self.diffBadgeText.SetText("NORMALE")
        self.diffBadgeText.SetPackedFontColor(0xFF00CCFF)
        self.diffBadgeText.AddFlag("not_pick")
        self.diffBadgeText.Show()

        # Timer grande a destra
        self.timerBg = ui.Bar()
        self.timerBg.SetParent(self)
        self.timerBg.SetPosition(320, 22)
        self.timerBg.SetSize(90, 22)
        self.timerBg.SetColor(0x66000000)
        self.timerBg.AddFlag("not_pick")
        self.timerBg.Show()

        self.timer = ui.TextLine()
        self.timer.SetParent(self)
        self.timer.SetPosition(365, 25)
        self.timer.SetHorizontalAlignCenter()
        self.timer.SetText("00:00")
        self.timer.SetPackedFontColor(0xFFFFD700)
        self.timer.SetOutline()
        self.timer.AddFlag("not_pick")
        self.timer.Show()

        # ═══════════ QUEST INFO SECTION ═══════════
        # Nome Quest
        self.questName = ui.TextLine()
        self.questName.SetParent(self)
        self.questName.SetPosition(210, 52)
        self.questName.SetHorizontalAlignCenter()
        self.questName.SetText("")
        self.questName.SetPackedFontColor(0xFFFFFFFF)
        self.questName.SetOutline()
        self.questName.AddFlag("not_pick")
        self.questName.Show()

        # ═══════════ DESCRIPTION SECTION ═══════════
        self.descBg = ui.Bar()
        self.descBg.SetParent(self)
        self.descBg.SetPosition(10, 72)
        self.descBg.SetSize(400, 60)
        self.descBg.SetColor(0x44000000)
        self.descBg.AddFlag("not_pick")
        self.descBg.Show()

        # Descrizione su piu' linee
        self.descLines = []
        for i in range(3):
            line = ui.TextLine()
            line.SetParent(self)
            line.SetPosition(20, 77 + i * 18)
            line.SetText("")
            line.SetPackedFontColor(0xFFCCCCCC)
            line.AddFlag("not_pick")
            line.Show()
            self.descLines.append(line)

        # ═══════════ PROGRESS SECTION ═══════════
        # Linea separatore progress
        self.progressLine = ui.Bar()
        self.progressLine.SetParent(self)
        self.progressLine.SetPosition(10, 138)
        self.progressLine.SetSize(400, 1)
        self.progressLine.SetColor(0x66FFFFFF)
        self.progressLine.AddFlag("not_pick")
        self.progressLine.Show()

        # Progress Bar Background
        self.progressBg = ui.Bar()
        self.progressBg.SetParent(self)
        self.progressBg.SetPosition(15, 148)
        self.progressBg.SetSize(390, 20)
        self.progressBg.SetColor(0xFF1A1A2E)
        self.progressBg.AddFlag("not_pick")
        self.progressBg.Show()

        # Progress Bar Fill
        self.progressFill = ui.Bar()
        self.progressFill.SetParent(self)
        self.progressFill.SetPosition(15, 148)
        self.progressFill.SetSize(0, 20)
        self.progressFill.SetColor(0xFF00CCFF)
        self.progressFill.AddFlag("not_pick")
        self.progressFill.Show()

        # Progress Text
        self.progressText = ui.TextLine()
        self.progressText.SetParent(self)
        self.progressText.SetPosition(210, 150)
        self.progressText.SetHorizontalAlignCenter()
        self.progressText.SetText("0 / 0")
        self.progressText.SetPackedFontColor(0xFFFFFFFF)
        self.progressText.SetOutline()
        self.progressText.AddFlag("not_pick")
        self.progressText.Show()

        # ═══════════ FOOTER SECTION ═══════════
        # Penalty Warning
        self.penaltyBg = ui.Bar()
        self.penaltyBg.SetParent(self)
        self.penaltyBg.SetPosition(15, 178)
        self.penaltyBg.SetSize(190, 30)
        self.penaltyBg.SetColor(0x44330000)
        self.penaltyBg.AddFlag("not_pick")
        self.penaltyBg.Show()

        self.penaltyLabel = ui.TextLine()
        self.penaltyLabel.SetParent(self)
        self.penaltyLabel.SetPosition(20, 181)
        self.penaltyLabel.SetText("PENALITA' FALLIMENTO:")
        self.penaltyLabel.SetPackedFontColor(0xFFFF6666)
        self.penaltyLabel.AddFlag("not_pick")
        self.penaltyLabel.Show()

        self.penaltyValue = ui.TextLine()
        self.penaltyValue.SetParent(self)
        self.penaltyValue.SetPosition(20, 195)
        self.penaltyValue.SetText("-0 Gloria")
        self.penaltyValue.SetPackedFontColor(0xFFFF4444)
        self.penaltyValue.SetOutline()
        self.penaltyValue.AddFlag("not_pick")
        self.penaltyValue.Show()

        # Status Text (Motivational)
        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(315, 188)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("SORGI, CACCIATORE!")
        self.statusText.SetPackedFontColor(0xFFFFD700)
        self.statusText.SetOutline()
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()

        self.Hide()

    def SetDifficultyTheme(self, difficulty):
        """Imposta tema colori basato sulla difficolta'"""
        if difficulty not in DIFFICULTY_COLORS:
            difficulty = "NORMAL"

        colors = DIFFICULTY_COLORS[difficulty]
        self.borderColor = colors["border"]

        # Aggiorna bordi
        for b in self.borders:
            b.SetColor(colors["border"])

        # Aggiorna badge difficolta'
        self.diffBadgeBg.SetColor(colors["bg"])
        self.diffBadgeText.SetText(colors["label"])
        self.diffBadgeText.SetPackedFontColor(colors["text"])

        # Aggiorna progress bar fill color
        self.progressFill.SetColor(colors["border"])

    def WrapText(self, text, maxCharsPerLine=55):
        """Divide il testo in linee per la descrizione"""
        words = text.split()
        lines = []
        currentLine = ""

        for word in words:
            if len(currentLine) + len(word) + 1 <= maxCharsPerLine:
                if currentLine:
                    currentLine += " " + word
                else:
                    currentLine = word
            else:
                if currentLine:
                    lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        return lines[:3]  # Max 3 linee

    def StartMission(self, title, seconds, vnums, count, description="", difficulty="NORMAL", penalty=0):
        self.currentTitle = title.replace("+", " ")
        self.targetCount = count
        self.currentProgress = 0
        self.description = description.replace("+", " ") if description else "Completa la sfida prima che scada il tempo!"
        self.difficulty = difficulty
        self.penalty = penalty

        # RESET: Resetta il titolo sistema (potrebbe essere rimasto "MISSION FAILED")
        self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
        self.systemLabel.SetPackedFontColor(0xFFFF4444)

        # Imposta tema colori
        self.SetDifficultyTheme(difficulty)

        # Imposta timer
        self.endTime = app.GetTime() + seconds

        # Aggiorna testi
        self.questName.SetText(self.currentTitle)

        # Descrizione su piu' linee
        descLines = self.WrapText(self.description)
        for i, line in enumerate(self.descLines):
            if i < len(descLines):
                line.SetText(descLines[i])
            else:
                line.SetText("")

        # Penalty
        if penalty > 0:
            self.penaltyValue.SetText("-%d Gloria" % penalty)
            self.penaltyBg.Show()
            self.penaltyLabel.Show()
            self.penaltyValue.Show()
        else:
            self.penaltyBg.Hide()
            self.penaltyLabel.Hide()
            self.penaltyValue.Hide()

        # Progress
        self.UpdateProgress(0)

        # Status message basato su difficolta'
        statusMessages = {
            "EASY": "Inizia la caccia!",
            "NORMAL": "Sorgi, Cacciatore!",
            "HARD": "Dimostra il tuo valore!",
            "EXTREME": "Solo i forti sopravvivono!",
            "GOD_MODE": "Diventa il Monarca!"
        }
        self.statusText.SetText(statusMessages.get(difficulty, "Sorgi, Cacciatore!"))
        self.statusText.SetPackedFontColor(0xFFFFD700)  # Reset colore oro

        self.Show()
        self.SetTop()

    def UpdateProgress(self, current):
        self.currentProgress = current
        self.progressText.SetText("%d / %d" % (current, self.targetCount))

        if self.targetCount > 0:
            fillWidth = int((float(current) / float(self.targetCount)) * 390)
            fillWidth = min(fillWidth, 390)
            self.progressFill.SetSize(fillWidth, 20)

    def EndMission(self, status, isEmergency=True):
        if isEmergency:
            if status == "SUCCESS":
                self.systemLabel.SetText("[SYSTEM] MISSION COMPLETE")
                self.systemLabel.SetPackedFontColor(0xFF00FF00)
                self.statusText.SetText("VITTORIA!")
                self.statusText.SetPackedFontColor(0xFF00FF00)
                for b in self.borders:
                    b.SetColor(0xFF00FF00)
            elif status == "FAILED":
                self.systemLabel.SetText("[SYSTEM] MISSION FAILED")
                self.systemLabel.SetPackedFontColor(0xFFFF0000)
                self.statusText.SetText("FALLIMENTO...")
                self.statusText.SetPackedFontColor(0xFFFF0000)
                for b in self.borders:
                    b.SetColor(0xFFFF0000)
        else:
            self.systemLabel.SetText("[SYSTEM] EMERGENCY QUEST")
            self.systemLabel.SetPackedFontColor(0xFFFF4444)

        self.endTime = app.GetTime() + 4.0

    def OnUpdate(self):
        if self.endTime > 0:
            left = self.endTime - app.GetTime()
            if left <= 0:
                self.Hide()
                self.endTime = 0
            else:
                # Formatta timer
                mins = int(left) // 60
                secs = int(left) % 60
                self.timer.SetText("%02d:%02d" % (mins, secs))

                # Effetto pulsante sui bordi quando il tempo sta per scadere
                if left < 10:
                    self.pulsePhase += 0.15
                    alpha = int(128 + 127 * math.sin(self.pulsePhase))
                    pulseColor = (0xFF << 24) | (alpha << 16) | (0x00 << 8) | 0x00
                    for b in self.borders:
                        b.SetColor(pulseColor)

    def OnPressEscapeKey(self):
        # Blocca la chiusura con ESC - la finestra rimane sempre visibile
        return True

    def Close(self):
        # Blocca la chiusura manuale - solo EndMission puo' chiudere
        pass


# ═══════════════════════════════════════════════════════════════════════════════
#  EVENT STATUS WINDOW - Popup evento attivo
# ═══════════════════════════════════════════════════════════════════════════════
class EventStatusWindow(ui.Window, DraggableMixin):
    """Popup Evento Attivo - Finestra Movibile"""

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(220, 60)

        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("EventStatusWindow", 220, 60)
        
        self.InitDraggable("EventStatusWindow", defaultX, defaultY)
        
        self.endTime = 0
        self.parentWindow = None
        self.eventDesc = ""
        self.eventReward = ""
        self.eventType = "default"
        self.toolTip = None
        
        # Background scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(220, 60)
        self.bg.SetColor(0xDD000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordo colorato
        self.borders = []
        eventColor = 0xFFFFD700
        
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(220, 2); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 58); b.SetSize(220, 2); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(2, 60); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        b = ui.Bar(); b.SetParent(self); b.SetPosition(218, 0); b.SetSize(2, 60); b.SetColor(eventColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        
        # Glow effect
        self.glowBar = ui.Bar()
        self.glowBar.SetParent(self)
        self.glowBar.SetPosition(2, 2)
        self.glowBar.SetSize(4, 56)
        self.glowBar.SetColor(0x66FFD700)
        self.glowBar.AddFlag("not_pick")
        self.glowBar.Show()
        
        # Label
        self.labelText = ui.TextLine()
        self.labelText.SetParent(self)
        self.labelText.SetPosition(110, 8)
        self.labelText.SetHorizontalAlignCenter()
        self.labelText.SetText("EVENTO IN CORSO")
        self.labelText.SetPackedFontColor(0xFFFFD700)
        self.labelText.SetOutline()
        self.labelText.AddFlag("not_pick")
        self.labelText.Show()
        
        # Nome evento
        self.eventNameText = ui.TextLine()
        self.eventNameText.SetParent(self)
        self.eventNameText.SetPosition(110, 28)
        self.eventNameText.SetHorizontalAlignCenter()
        self.eventNameText.SetText("")
        self.eventNameText.SetPackedFontColor(0xFFFFD700)
        self.eventNameText.SetOutline()
        self.eventNameText.AddFlag("not_pick")
        self.eventNameText.Show()
        
        # Orario
        self.timeText = ui.TextLine()
        self.timeText.SetParent(self)
        self.timeText.SetPosition(110, 44)
        self.timeText.SetHorizontalAlignCenter()
        self.timeText.SetText("")
        self.timeText.SetPackedFontColor(0xFFAAAAAA)
        self.timeText.AddFlag("not_pick")
        self.timeText.Show()
        
        self.currentEvent = ""
        self.Hide()
    
    def SetEvent(self, eventName, timeInfo=""):
        if not eventName or eventName == "Nessuno" or eventName == "":
            self.currentEvent = ""
            self.Hide()
            return
        
        self.currentEvent = eventName.replace("+", " ")
        self.eventNameText.SetText(self.currentEvent[:25])
        
        if timeInfo:
            self.timeText.SetText(timeInfo)
        else:
            self.timeText.SetText("")
        
        # NON resettiamo la posizione - usa quella salvata dal DraggableMixin
        # La posizione viene impostata solo in InitDraggable()

        self.Show()
        self.SetTop()
    
    def ShowEvent(self, eventName, duration=0, eventType="default", desc="", reward="", minRank="E", winnerPrize=0):
        if not eventName or eventName == "Nessuno" or eventName == "":
            self.currentEvent = ""
            self.Hide()
            return
        
        self.currentEvent = eventName.replace("+", " ")
        self.eventNameText.SetText(self.currentEvent[:25])
        self.eventType = eventType
        self.eventDesc = desc
        self.eventReward = reward
        self.eventMinRank = minRank
        self.eventWinnerPrize = winnerPrize
        
        if duration > 0:
            self.endTime = app.GetTime() + duration
            mins = duration // 60
            secs = duration % 60
            self.timeText.SetText("Tempo: %d:%02d" % (mins, secs))
        else:
            self.endTime = 0
            self.timeText.SetText("")
        
        eventColors = {
            "default": 0xFFFFD700,
            "boss_hunt": 0xFFFF0000,
            "fracture": 0xFF9900FF,
            "glory_rush": 0xFFFFD700,
            "time_trial": 0xFFFFD700,
            "first_rift": 0xFF9900FF,
            "first_boss": 0xFFFF0000,
            "custom": 0xFF00FFFF
        }
        color = eventColors.get(eventType, 0xFFFFD700)
        self.SetEventColor(color)

        # NON resettiamo la posizione - usa quella salvata dal DraggableMixin

        self.Show()
        self.SetTop()
    
    def SetEventColor(self, color):
        for b in self.borders:
            b.SetColor(color)
        self.glowBar.SetColor((color & 0x00FFFFFF) | 0x66000000)
        self.labelText.SetPackedFontColor(color)
    
    def OnUpdate(self):
        if not self.IsShow():
            return
        
        ct = app.GetTime()
        
        if hasattr(self, 'endTime') and self.endTime > 0:
            remaining = self.endTime - ct
            if remaining <= 0:
                self.Hide()
                self.endTime = 0
                return
            mins = int(remaining) // 60
            secs = int(remaining) % 60
            self.timeText.SetText("Tempo: %d:%02d" % (mins, secs))
        
        # Pulse glow
        alpha = int(abs((ct * 2) % 2 - 1) * 60) + 40
        glowColor = 0x00FF88 | (alpha << 24)
        self.glowBar.SetColor(glowColor)

    def SetParentWindow(self, parent):
        self.parentWindow = parent
    
    def SetEventDetails(self, desc="", reward="", eventType="default"):
        """Imposta dettagli aggiuntivi per tooltip"""
        self.eventDesc = desc
        self.eventReward = reward
        self.eventType = eventType
    
    def OnMouseOverIn(self):
        """Mostra tooltip con dettagli evento completi"""
        if not self.currentEvent:
            return
        
        try:
            import uiToolTip
            if not self.toolTip:
                self.toolTip = uiToolTip.ToolTip()
                self.toolTip.ClearToolTip()
            
            self.toolTip.ClearToolTip()
            self.toolTip.SetThinBoardSize(220)
            
            # Titolo evento
            self.toolTip.AppendTextLine("[EVENTO IN CORSO]", 0xFFFFD700)
            self.toolTip.AppendTextLine(self.currentEvent, 0xFFFFFFFF)
            self.toolTip.AppendSpace(5)
            
            # Tipo evento
            eventTypeNames = {
                "default": "Evento Standard",
                "boss_hunt": "Caccia ai Boss",
                "fracture": "Frattura",
                "glory_rush": "Gloria Rush (+100% Gloria)",
                "time_trial": "Sfida a Tempo",
                "first_rift": "PRIMO che conquista VINCE!",
                "first_boss": "PRIMO che uccide boss VINCE!",
                "rift_hunt": "Fratture +50% spawn",
                "boss_massacre": "Boss Gloria +50%",
                "metin_frenzy": "Metin Bonus +50%",
                "double_spawn": "Spawn Elite x2",
                "custom": "Evento Speciale"
            }
            typeName = eventTypeNames.get(self.eventType, "Evento")
            self.toolTip.AppendTextLine("Tipo: %s" % typeName, 0xFF00CCFF)
            
            # Rank minimo
            if hasattr(self, 'eventMinRank') and self.eventMinRank:
                self.toolTip.AppendTextLine("Rank Minimo: %s" % self.eventMinRank, 0xFFAAAAAA)
            
            # Descrizione
            if self.eventDesc:
                self.toolTip.AppendSpace(5)
                # Split descrizione lunga
                desc = self.eventDesc
                if len(desc) > 35:
                    self.toolTip.AppendTextLine(desc[:35], 0xFFCCCCCC)
                    self.toolTip.AppendTextLine(desc[35:70], 0xFFCCCCCC)
                else:
                    self.toolTip.AppendTextLine(desc, 0xFFCCCCCC)
            
            # Premio base
            if self.eventReward:
                self.toolTip.AppendSpace(5)
                self.toolTip.AppendTextLine("Premio Base: %s Gloria" % self.eventReward, 0xFF00FF00)
            
            # Premio vincitore
            if hasattr(self, 'eventWinnerPrize') and self.eventWinnerPrize > 0:
                self.toolTip.AppendTextLine("Premio Vincitore: +%d Gloria!" % self.eventWinnerPrize, 0xFFFFD700)
            
            # Tempo rimasto
            if hasattr(self, 'endTime') and self.endTime > 0:
                remaining = self.endTime - app.GetTime()
                if remaining > 0:
                    mins = int(remaining) // 60
                    secs = int(remaining) % 60
                    self.toolTip.AppendSpace(5)
                    self.toolTip.AppendTextLine("Tempo Rimasto: %d:%02d" % (mins, secs), 0xFFFF8800)
            
            # Hint doppio click
            self.toolTip.AppendSpace(8)
            self.toolTip.AppendTextLine("[Doppio Click = Tutti gli Eventi]", 0xFF888888)
            
            self.toolTip.ShowToolTip()
        except:
            pass
    
    def OnMouseOverOut(self):
        """Nasconde tooltip"""
        if self.toolTip:
            self.toolTip.HideToolTip()
    
    def OnMouseLeftButtonDoubleClick(self):
        """Doppio click: Apre la finestra con tutti gli eventi del giorno"""
        try:
            # Cerca la finestra principale Hunter
            if self.parentWindow and hasattr(self.parentWindow, 'OpenEventsPanel'):
                self.parentWindow.OpenEventsPanel()
            else:
                # Fallback: cerca la finestra globale
                import uihunterlevel
                if hasattr(uihunterlevel, 'g_hunterWindow') and uihunterlevel.g_hunterWindow:
                    wnd = uihunterlevel.g_hunterWindow
                    if hasattr(wnd, 'OpenEventsPanel'):
                        wnd.OpenEventsPanel()
                    elif hasattr(wnd, 'ShowPage'):
                        # Apre la pagina degli eventi (pagina 3 = Guida Eventi)
                        wnd.Show()
                        wnd.SetTop()
                        wnd.ShowPage(3)  # Pagina Guida Eventi
        except Exception as e:
            pass
        return True


# ═══════════════════════════════════════════════════════════════════════════════
#  RIVAL TRACKER WINDOW - Tracker rivale in classifica
# ═══════════════════════════════════════════════════════════════════════════════
class RivalTrackerWindow(ui.Window, DraggableMixin):
    """
    ═══════════════════════════════════════════════════════════════════════════
     RIVAL TRACKER - Sistema Rivale Solo Leveling Style
     Mostra il tuo rivale piu' vicino in classifica con tema hunter
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(240, 100)
        self.screenWidth = wndMgr.GetScreenWidth()
        
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("RivalTrackerWindow", 240, 100)
        
        self.InitDraggable("RivalTrackerWindow", defaultX, defaultY)
        self.eventWndRef = None
        
        # === SFONDO PRINCIPALE ===
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(240, 100)
        self.bg.SetColor(0xEE0A0A12)  # Nero profondo
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # === CORNICE ESTERNA ===
        self.frameOuter = []
        frameColor = 0xFF1A1A2E
        # Top
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(240, 3); b.SetColor(frameColor); b.AddFlag("not_pick"); b.Show()
        self.frameOuter.append(b)
        # Bottom
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 97); b.SetSize(240, 3); b.SetColor(frameColor); b.AddFlag("not_pick"); b.Show()
        self.frameOuter.append(b)
        # Left
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(3, 100); b.SetColor(frameColor); b.AddFlag("not_pick"); b.Show()
        self.frameOuter.append(b)
        # Right
        b = ui.Bar(); b.SetParent(self); b.SetPosition(237, 0); b.SetSize(3, 100); b.SetColor(frameColor); b.AddFlag("not_pick"); b.Show()
        self.frameOuter.append(b)
        
        # === BARRA SUPERIORE COLORATA ===
        self.topAccent = ui.Bar()
        self.topAccent.SetParent(self)
        self.topAccent.SetPosition(3, 3)
        self.topAccent.SetSize(234, 22)
        self.topAccent.SetColor(0xFF8B0000)  # Rosso sangue
        self.topAccent.AddFlag("not_pick")
        self.topAccent.Show()
        
        # === ICONA RANKING (simulata con testo) ===
        self.iconText = ui.TextLine()
        self.iconText.SetParent(self)
        self.iconText.SetPosition(15, 6)
        self.iconText.SetText("[!]")
        self.iconText.SetPackedFontColor(0xFFFF4444)
        self.iconText.SetOutline()
        self.iconText.AddFlag("not_pick")
        self.iconText.Show()
        
        # === TITOLO ===
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(120, 6)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("BERSAGLIO RILEVATO")
        self.titleText.SetPackedFontColor(0xFFFFFFFF)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()
        
        # === LINEA SEPARATRICE ===
        self.sepLine = ui.Bar()
        self.sepLine.SetParent(self)
        self.sepLine.SetPosition(10, 28)
        self.sepLine.SetSize(220, 1)
        self.sepLine.SetColor(0xFF333355)
        self.sepLine.AddFlag("not_pick")
        self.sepLine.Show()
        
        # === NOME RIVALE ===
        self.rivalLabel = ui.TextLine()
        self.rivalLabel.SetParent(self)
        self.rivalLabel.SetPosition(15, 35)
        self.rivalLabel.SetText("Hunter:")
        self.rivalLabel.SetPackedFontColor(0xFF888899)
        self.rivalLabel.AddFlag("not_pick")
        self.rivalLabel.Show()
        
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(225, 35)
        self.nameText.SetHorizontalAlignRight()
        self.nameText.SetText("---")
        self.nameText.SetPackedFontColor(0xFFFFDD44)
        self.nameText.SetOutline()
        self.nameText.AddFlag("not_pick")
        self.nameText.Show()

        # === DISTACCO ===
        self.distLabel = ui.TextLine()
        self.distLabel.SetParent(self)
        self.distLabel.SetPosition(15, 55)
        self.distLabel.SetText("Distacco:")
        self.distLabel.SetPackedFontColor(0xFF888899)
        self.distLabel.AddFlag("not_pick")
        self.distLabel.Show()
        
        self.distText = ui.TextLine()
        self.distText.SetParent(self)
        self.distText.SetPosition(225, 55)
        self.distText.SetHorizontalAlignRight()
        self.distText.SetText("0 Gloria")
        self.distText.SetPackedFontColor(0xFFFF8844)
        self.distText.SetOutline()
        self.distText.AddFlag("not_pick")
        self.distText.Show()
        
        # === MESSAGGIO STATUS ===
        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(120, 78)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("Superalo per salire in classifica!")
        self.statusText.SetPackedFontColor(0xFF666688)
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()
        
        self.endTime = 0
        self.mode = "VICINO"
        self.pulsePhase = 0.0
    
    def SetEventWindowRef(self, eventWnd):
        self.eventWndRef = eventWnd
        
    def ShowRival(self, name, diff, label="Gloria", mode="VICINO"):
        if not HasSavedPosition("RivalTrackerWindow"):
            self.screenWidth = wndMgr.GetScreenWidth()
            self.SetPosition(self.screenWidth - 250, 10)
        
        cleanName = name.replace("+", " ")
        self.nameText.SetText(cleanName)
        self.mode = mode
        
        if mode == "SUPERATO":
            # Sei stato superato - tema rosso intenso
            self.topAccent.SetColor(0xFFCC0000)
            self.titleText.SetText("SORPASSATO!")
            self.titleText.SetPackedFontColor(0xFFFF4444)
            self.iconText.SetText("[X]")
            self.iconText.SetPackedFontColor(0xFFFF0000)
            self.distText.SetText("-%s Gloria" % str(diff))
            self.distText.SetPackedFontColor(0xFFFF4444)
            self.statusText.SetText("%s ti ha superato!" % cleanName)
            self.statusText.SetPackedFontColor(0xFFFF6666)
        else:
            # Rivale da superare - tema ambra
            self.topAccent.SetColor(0xFF8B4000)
            self.titleText.SetText("BERSAGLIO RILEVATO")
            self.titleText.SetPackedFontColor(0xFFFFFFFF)
            self.iconText.SetText("[!]")
            self.iconText.SetPackedFontColor(0xFFFFAA00)
            self.distText.SetText("+%s %s" % (str(diff), label))
            self.distText.SetPackedFontColor(0xFFFFAA44)
            self.statusText.SetText("Superalo per salire in classifica!")
            self.statusText.SetPackedFontColor(0xFF666688)
        
        self.endTime = app.GetTime() + 25.0
        self.Show()
        self.SetTop()
        
    def OnUpdate(self):
        if self.endTime > 0:
            remaining = self.endTime - app.GetTime()
            if remaining <= 0:
                self.Hide()
                self.endTime = 0
                return
            
            # Effetto pulse per SUPERATO
            if self.mode == "SUPERATO":
                self.pulsePhase += 0.15
                pulse = abs(math.sin(self.pulsePhase))
                r = int(140 + pulse * 60)
                color = (0xFF << 24) | (r << 16) | (0x00 << 8) | 0x00
                self.topAccent.SetColor(color)


# ═══════════════════════════════════════════════════════════════════════════════
#  OVERTAKE WINDOW - Notifica Sorpasso Solo Leveling Style
#  Appare quando superi qualcuno in classifica
# ═══════════════════════════════════════════════════════════════════════════════
class OvertakeWindow(ui.Window, DraggableMixin):
    """
    Effetto quando sorpassi qualcuno in classifica
    Tema Solo Leveling - Stile "LEVEL UP" / "RANK UP"
    """
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        self.SetSize(300, 120)
        
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("OvertakeWindow", 300, 120)
        
        self.InitDraggable("OvertakeWindow", defaultX, defaultY)
        self.eventWndRef = None
        
        # === SFONDO PRINCIPALE ===
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(300, 120)
        self.bg.SetColor(0xEE080810)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # === GLOW ESTERNO (simulato con barre) ===
        self.glowBars = []
        # Top glow
        for i in range(3):
            b = ui.Bar()
            b.SetParent(self)
            b.SetPosition(0, i)
            b.SetSize(300, 1)
            alpha = 0x88 - (i * 0x28)
            b.SetColor((alpha << 24) | 0x00FF88)
            b.AddFlag("not_pick")
            b.Show()
            self.glowBars.append(b)
        # Bottom glow
        for i in range(3):
            b = ui.Bar()
            b.SetParent(self)
            b.SetPosition(0, 117 + i)
            b.SetSize(300, 1)
            alpha = 0x88 - (i * 0x28)
            b.SetColor((alpha << 24) | 0x00FF88)
            b.AddFlag("not_pick")
            b.Show()
            self.glowBars.append(b)
        
        # === BORDI PRINCIPALI ===
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 3)
        self.borderTop.SetSize(300, 2)
        self.borderTop.SetColor(0xFF00FF66)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, 115)
        self.borderBottom.SetSize(300, 2)
        self.borderBottom.SetColor(0xFF00FF66)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()
        
        # Bordi laterali
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 3)
        self.borderLeft.SetSize(2, 114)
        self.borderLeft.SetColor(0xFF00CC55)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()
        
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(298, 3)
        self.borderRight.SetSize(2, 114)
        self.borderRight.SetColor(0xFF00CC55)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()
        
        # === HEADER BAR ===
        self.headerBar = ui.Bar()
        self.headerBar.SetParent(self)
        self.headerBar.SetPosition(2, 5)
        self.headerBar.SetSize(296, 25)
        self.headerBar.SetColor(0xFF0A3020)
        self.headerBar.AddFlag("not_pick")
        self.headerBar.Show()
        
        # === FRECCE VERSO L'ALTO ===
        self.arrowText = ui.TextLine()
        self.arrowText.SetParent(self)
        self.arrowText.SetPosition(150, 10)
        self.arrowText.SetHorizontalAlignCenter()
        self.arrowText.SetText("RANK UP")
        self.arrowText.SetPackedFontColor(0xFF00FF88)
        self.arrowText.SetOutline()
        self.arrowText.AddFlag("not_pick")
        self.arrowText.Show()
        
        # === LINEA DECORATIVA ===
        self.decLine = ui.Bar()
        self.decLine.SetParent(self)
        self.decLine.SetPosition(20, 32)
        self.decLine.SetSize(260, 1)
        self.decLine.SetColor(0xFF00AA44)
        self.decLine.AddFlag("not_pick")
        self.decLine.Show()
        
        # === TESTO PRINCIPALE ===
        self.mainText = ui.TextLine()
        self.mainText.SetParent(self)
        self.mainText.SetPosition(150, 42)
        self.mainText.SetHorizontalAlignCenter()
        self.mainText.SetText("")
        self.mainText.SetPackedFontColor(0xFFFFFFFF)
        self.mainText.SetOutline()
        self.mainText.AddFlag("not_pick")
        self.mainText.Show()
        
        # === NOME SUPERATO ===
        self.nameText = ui.TextLine()
        self.nameText.SetParent(self)
        self.nameText.SetPosition(150, 62)
        self.nameText.SetHorizontalAlignCenter()
        self.nameText.SetText("")
        self.nameText.SetPackedFontColor(0xFFFFDD00)
        self.nameText.SetOutline()
        self.nameText.AddFlag("not_pick")
        self.nameText.Show()
        
        # === NUOVA POSIZIONE ===
        self.posText = ui.TextLine()
        self.posText.SetParent(self)
        self.posText.SetPosition(150, 88)
        self.posText.SetHorizontalAlignCenter()
        self.posText.SetText("")
        self.posText.SetPackedFontColor(0xFF00FF88)
        self.posText.SetOutline()
        self.posText.AddFlag("not_pick")
        self.posText.Show()
        
        self.startTime = 0
        self.endTime = 0
        self.pulsePhase = 0.0
        
        self.Hide()
    
    def SetEventWindowRef(self, eventWnd):
        self.eventWndRef = eventWnd
    
    def ShowOvertake(self, overtakenName, newPosition):
        if not HasSavedPosition("OvertakeWindow"):
            self.screenWidth = wndMgr.GetScreenWidth()
            self.SetPosition((self.screenWidth - 300) // 2, 150)
        
        cleanName = overtakenName.replace("+", " ")
        self.mainText.SetText("Hai superato un Hunter!")
        self.nameText.SetText(cleanName)
        self.posText.SetText("Nuova Posizione: #%d" % newPosition)
        
        self.startTime = app.GetTime()
        self.endTime = self.startTime + 5.0
        self.pulsePhase = 0.0
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.endTime == 0:
            return
        
        currentTime = app.GetTime()
        
        if currentTime > self.endTime:
            self.Hide()
            self.endTime = 0
            return
        
        # Effetto pulse sui bordi
        self.pulsePhase += 0.12
        pulse = abs(math.sin(self.pulsePhase))
        
        # Colore che pulsa tra verde chiaro e verde scuro
        g = int(200 + pulse * 55)
        borderColor = (0xFF << 24) | (0x00 << 16) | (g << 8) | 0x66
        self.borderTop.SetColor(borderColor)
        self.borderBottom.SetColor(borderColor)
        
        # Glow che pulsa
        for i, bar in enumerate(self.glowBars):
            baseAlpha = 0x66 - (i % 3) * 0x20
            alpha = int(baseAlpha * (0.5 + pulse * 0.5))
            bar.SetColor((alpha << 24) | 0x00FF88)


# ═══════════════════════════════════════════════════════════════════════════════
#  FRACTURE DEFENSE WINDOW - Solo Leveling Style
#  UI dedicata per la difesa delle fratture, separata dall'Emergency Quest
# ═══════════════════════════════════════════════════════════════════════════════

# Colori per rank frattura
DEFENSE_RANK_COLORS = {
    "E": {"border": 0xFF00FF00, "glow": 0x4400FF00, "title": 0xFF55FF55, "accent": 0xFF00CC00},  # GREEN
    "D": {"border": 0xFF0088FF, "glow": 0x440088FF, "title": 0xFF55AAFF, "accent": 0xFF0066CC},  # BLUE
    "C": {"border": 0xFFFF8800, "glow": 0x44FF8800, "title": 0xFFFFAA55, "accent": 0xFFCC6600},  # ORANGE
    "B": {"border": 0xFFFF0000, "glow": 0x44FF0000, "title": 0xFFFF5555, "accent": 0xFFCC0000},  # RED
    "A": {"border": 0xFFFFD700, "glow": 0x44FFD700, "title": 0xFFFFE455, "accent": 0xFFCCAA00},  # GOLD
    "S": {"border": 0xFFAA00FF, "glow": 0x44AA00FF, "title": 0xFFCC55FF, "accent": 0xFF8800CC},  # PURPLE
    "N": {"border": 0xFFFFFFFF, "glow": 0x44FFFFFF, "title": 0xFFFFFFFF, "accent": 0xFFCCCCCC},  # BLACKWHITE (bianco brillante)
}

class FractureDefenseWindow(ui.Window, DraggableMixin):
    """Finestra Difesa Frattura - Solo Leveling Style - Separata dall'Emergency"""


    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(380, 240)  # Aumentato per includere sezione distanza
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("FractureDefenseWindow", 380, 240)

        self.InitDraggable("FractureDefenseWindow", defaultX, defaultY)

        # Variabili di stato
        self.endTime = 0
        self.startTime = 0
        self.mobsRequired = 0
        self.mobsKilled = 0
        self.currentWave = 0
        self.totalWaves = 3
        self.fractureName = ""
        self.fractureRank = "E"
        self.pulsePhase = 0.0
        self.isActive = False
        self.zeroTimeStart = 0  # FIX: Timestamp di quando il timer ha raggiunto 00:00
        
        # Coordinate zona difesa
        self.defenseCenterX = 0
        self.defenseCenterY = 0
        self.defenseRadius = 1000  # Default 10 metri
        self.currentDistance = 0
        self.distanceStatus = "OK"

        # Schema colori corrente
        self.colorScheme = DEFENSE_RANK_COLORS["E"]

        # ═══════════ SFONDO PRINCIPALE ═══════════
        # Sfondo esterno scuro con bordo colorato
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(380, 240)
        self.bgOuter.SetColor(0xEE0A0A14)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()

        # Glow interno
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(3, 3)
        self.glowInner.SetSize(374, 234)
        self.glowInner.SetColor(0x22FFFFFF)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()

        # Sfondo interno
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 5)
        self.bgInner.SetSize(370, 230)
        self.bgInner.SetColor(0xDD080812)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # ═══════════ BORDI ANIMATI ═══════════
        self.borders = []
        borderColor = self.colorScheme["border"]
        # Top
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(380, 3); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Bottom
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 237); b.SetSize(380, 3); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Left
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(3, 240); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Right
        b = ui.Bar(); b.SetParent(self); b.SetPosition(377, 0); b.SetSize(3, 240); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)

        # ═══════════ HEADER ═══════════
        # Icona scudo (simbolo difesa)
        self.shieldIcon = ui.TextLine()
        self.shieldIcon.SetParent(self)
        self.shieldIcon.SetPosition(15, 12)
        self.shieldIcon.SetText("[#]")
        self.shieldIcon.SetPackedFontColor(0xFFFFD700)
        self.shieldIcon.SetOutline()
        self.shieldIcon.AddFlag("not_pick")
        self.shieldIcon.Show()

        # Titolo "DIFESA FRATTURA"
        self.titleLabel = ui.TextLine()
        self.titleLabel.SetParent(self)
        self.titleLabel.SetPosition(190, 10)
        self.titleLabel.SetHorizontalAlignCenter()
        self.titleLabel.SetText("DIFESA FRATTURA")
        self.titleLabel.SetPackedFontColor(0xFFFFFFFF)
        self.titleLabel.SetOutline()
        self.titleLabel.AddFlag("not_pick")
        self.titleLabel.Show()

        # Nome frattura
        self.fractureNameLabel = ui.TextLine()
        self.fractureNameLabel.SetParent(self)
        self.fractureNameLabel.SetPosition(190, 28)
        self.fractureNameLabel.SetHorizontalAlignCenter()
        self.fractureNameLabel.SetText("")
        self.fractureNameLabel.SetPackedFontColor(0xFFAAAAAA)
        self.fractureNameLabel.AddFlag("not_pick")
        self.fractureNameLabel.Show()

        # Linea separatore header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(10, 48)
        self.headerLine.SetSize(360, 1)
        self.headerLine.SetColor(0x66FFFFFF)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # ═══════════ TIMER SECTION ═══════════
        # Background timer
        self.timerBg = ui.Bar()
        self.timerBg.SetParent(self)
        self.timerBg.SetPosition(290, 8)
        self.timerBg.SetSize(80, 35)
        self.timerBg.SetColor(0x88000000)
        self.timerBg.AddFlag("not_pick")
        self.timerBg.Show()

        self.timerText = ui.TextLine()
        self.timerText.SetParent(self)
        self.timerText.SetPosition(330, 18)
        self.timerText.SetHorizontalAlignCenter()
        self.timerText.SetText("00:00")
        self.timerText.SetPackedFontColor(0xFFFFFFFF)
        self.timerText.SetOutline()
        self.timerText.AddFlag("not_pick")
        self.timerText.Show()

        # ═══════════ PROGRESS SECTION ═══════════
        # Label "PROGRESSO"
        self.progressLabel = ui.TextLine()
        self.progressLabel.SetParent(self)
        self.progressLabel.SetPosition(15, 55)
        self.progressLabel.SetText("PROGRESSO DIFESA")
        self.progressLabel.SetPackedFontColor(0xFFCCCCCC)
        self.progressLabel.AddFlag("not_pick")
        self.progressLabel.Show()

        # Progress bar background
        self.progressBarBg = ui.Bar()
        self.progressBarBg.SetParent(self)
        self.progressBarBg.SetPosition(15, 73)
        self.progressBarBg.SetSize(350, 20)
        self.progressBarBg.SetColor(0xFF1A1A2E)
        self.progressBarBg.AddFlag("not_pick")
        self.progressBarBg.Show()

        # Progress bar fill
        self.progressBarFill = ui.Bar()
        self.progressBarFill.SetParent(self)
        self.progressBarFill.SetPosition(17, 75)
        self.progressBarFill.SetSize(0, 16)
        self.progressBarFill.SetColor(0xFF00FF00)
        self.progressBarFill.AddFlag("not_pick")
        self.progressBarFill.Show()

        # Progress bar glow overlay
        self.progressBarGlow = ui.Bar()
        self.progressBarGlow.SetParent(self)
        self.progressBarGlow.SetPosition(17, 75)
        self.progressBarGlow.SetSize(0, 8)
        self.progressBarGlow.SetColor(0x44FFFFFF)
        self.progressBarGlow.AddFlag("not_pick")
        self.progressBarGlow.Show()

        # Progress text (0 / 20)
        self.progressText = ui.TextLine()
        self.progressText.SetParent(self)
        self.progressText.SetPosition(190, 75)
        self.progressText.SetHorizontalAlignCenter()
        self.progressText.SetText("0 / 0")
        self.progressText.SetPackedFontColor(0xFFFFFFFF)
        self.progressText.SetOutline()
        self.progressText.AddFlag("not_pick")
        self.progressText.Show()

        # ═══════════ WAVE INDICATORS ═══════════
        self.waveLabel = ui.TextLine()
        self.waveLabel.SetParent(self)
        self.waveLabel.SetPosition(15, 100)
        self.waveLabel.SetText("WAVE:")
        self.waveLabel.SetPackedFontColor(0xFFCCCCCC)
        self.waveLabel.AddFlag("not_pick")
        self.waveLabel.Show()

        # Wave indicators (piccoli quadrati)
        self.waveIndicators = []
        for i in range(5):
            ind = ui.Bar()
            ind.SetParent(self)
            ind.SetPosition(70 + i * 30, 100)
            ind.SetSize(22, 16)
            ind.SetColor(0xFF333333)
            ind.AddFlag("not_pick")
            ind.Show()
            self.waveIndicators.append(ind)

        # ═══════════ DISTANZA DALLA FRATTURA ═══════════
        # Separatore
        self.distSep = ui.Bar()
        self.distSep.SetParent(self)
        self.distSep.SetPosition(10, 125)
        self.distSep.SetSize(360, 1)
        self.distSep.SetColor(0x66FFFFFF)
        self.distSep.AddFlag("not_pick")
        self.distSep.Show()
        
        # Label distanza
        self.distLabel = ui.TextLine()
        self.distLabel.SetParent(self)
        self.distLabel.SetPosition(15, 132)
        self.distLabel.SetText("DISTANZA DALLA FRATTURA:")
        self.distLabel.SetPackedFontColor(0xFFCCCCCC)
        self.distLabel.AddFlag("not_pick")
        self.distLabel.Show()
        
        # Valore distanza (in metri)
        self.distValue = ui.TextLine()
        self.distValue.SetParent(self)
        self.distValue.SetPosition(365, 132)
        self.distValue.SetHorizontalAlignRight()
        self.distValue.SetText("0m")
        self.distValue.SetPackedFontColor(0xFF00FF00)
        self.distValue.SetOutline()
        self.distValue.AddFlag("not_pick")
        self.distValue.Show()
        
        # Barra distanza
        self.distBarBg = ui.Bar()
        self.distBarBg.SetParent(self)
        self.distBarBg.SetPosition(15, 150)
        self.distBarBg.SetSize(350, 12)
        self.distBarBg.SetColor(0xFF1A1A2E)
        self.distBarBg.AddFlag("not_pick")
        self.distBarBg.Show()
        
        self.distBarFill = ui.Bar()
        self.distBarFill.SetParent(self)
        self.distBarFill.SetPosition(17, 152)
        self.distBarFill.SetSize(0, 8)
        self.distBarFill.SetColor(0xFF00AA00)
        self.distBarFill.AddFlag("not_pick")
        self.distBarFill.Show()

        # ═══════════ STATUS MESSAGE ═══════════
        self.statusBg = ui.Bar()
        self.statusBg.SetParent(self)
        self.statusBg.SetPosition(15, 170)
        self.statusBg.SetSize(350, 60)
        self.statusBg.SetColor(0x44000000)
        self.statusBg.AddFlag("not_pick")
        self.statusBg.Show()

        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(190, 180)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("Preparati alla difesa...")
        self.statusText.SetPackedFontColor(0xFFFFD700)
        self.statusText.SetOutline()
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()

        self.statusSubText = ui.TextLine()
        self.statusSubText.SetParent(self)
        self.statusSubText.SetPosition(190, 198)
        self.statusSubText.SetHorizontalAlignCenter()
        self.statusSubText.SetText("Uccidi i mob per aprire la frattura!")
        self.statusSubText.SetPackedFontColor(0xFFAAAAAA)
        self.statusSubText.AddFlag("not_pick")
        self.statusSubText.Show()
        
        # Warning text per distanza
        self.warningText = ui.TextLine()
        self.warningText.SetParent(self)
        self.warningText.SetPosition(190, 215)
        self.warningText.SetHorizontalAlignCenter()
        self.warningText.SetText("")
        self.warningText.SetPackedFontColor(0xFFFF0000)
        self.warningText.SetOutline()
        self.warningText.AddFlag("not_pick")
        self.warningText.Hide()

        self.Hide()

    def SetRankColors(self, rank):
        """Imposta i colori in base al rank della frattura"""
        if not rank:
            rank = "E"
        # Pulisci il rank: rimuovi spazi, "-RANK", e prendi solo la prima lettera
        rank = str(rank).strip().upper().replace("-RANK", "").replace(" ", "")
        if len(rank) > 0:
            rank = rank[0]  # Prendi solo la prima lettera (E, D, C, B, A, S, N)
        if rank not in DEFENSE_RANK_COLORS:
            rank = "E"

        self.fractureRank = rank
        self.colorScheme = DEFENSE_RANK_COLORS[rank]

        borderColor = self.colorScheme["border"]
        titleColor = self.colorScheme["title"]

        # Aggiorna bordi
        for b in self.borders:
            b.SetColor(borderColor)

        # Aggiorna titolo
        self.titleLabel.SetPackedFontColor(titleColor)
        self.fractureNameLabel.SetPackedFontColor(self.colorScheme["accent"])

        # Aggiorna progress bar
        self.progressBarFill.SetColor(borderColor)
        
        # Aggiorna barra distanza
        self.distBarFill.SetColor(borderColor)

        # Aggiorna glow
        self.glowInner.SetColor(self.colorScheme["glow"])

        # Aggiorna status text color
        self.statusText.SetPackedFontColor(titleColor)

    def SetDefenseZone(self, centerX, centerY, radius):
        """Imposta la zona di difesa"""
        self.defenseCenterX = centerX
        self.defenseCenterY = centerY
        self.defenseRadius = radius

    def StartDefense(self, fractureName, rank, duration, totalMobs, centerX=0, centerY=0, radius=1000):
        """Inizia la difesa di una frattura"""
        self.fractureName = fractureName
        self.fractureRank = rank
        self.mobsRequired = totalMobs
        self.mobsKilled = 0
        self.currentWave = 0
        self.totalWaves = 3
        self.startTime = app.GetTime()
        self.endTime = self.startTime + duration
        self.isActive = True
        self.zeroTimeStart = 0  # Reset failsafe

        # Imposta colori
        self.SetRankColors(rank)
        
        # Imposta zona difesa
        if centerX > 0 and centerY > 0:
            self.SetDefenseZone(centerX, centerY, radius)

        # Aggiorna UI
        self.fractureNameLabel.SetText(fractureName)
        self.progressText.SetText("0 / %d" % totalMobs)
        self.statusText.SetText("DIFESA IN CORSO!")
        self.statusSubText.SetText("Uccidi tutti i mob per aprire la frattura!")
        self.warningText.Hide()

        # Reset wave indicators
        for ind in self.waveIndicators:
            ind.SetColor(0xFF333333)

        # Reset progress bar
        self.progressBarFill.SetSize(0, 16)
        self.progressBarGlow.SetSize(0, 8)
        
        # Reset distanza
        self.distValue.SetText("0m")
        self.distValue.SetPackedFontColor(0xFF00FF00)
        self.distBarFill.SetSize(0, 8)

        self.Show()
        self.SetTop()

    def UpdateProgress(self, killed, required, wave=0):
        """Aggiorna il progresso della difesa"""
        self.mobsKilled = killed
        if required > 0:
            self.mobsRequired = required

        # Se killed >= required, mostra completato
        if killed >= self.mobsRequired and self.mobsRequired > 0:
            self.progressText.SetText("%d / %d - COMPLETATO!" % (self.mobsRequired, self.mobsRequired))
            self.progressText.SetPackedFontColor(0xFF00FF00)
            # Barra al 100%
            self.progressBarFill.SetSize(346, 16)
            self.progressBarGlow.SetSize(346, 8)
            self.progressBarFill.SetColor(0xFF00FF00)  # Verde
            # Status
            self.statusText.SetText("OBIETTIVO RAGGIUNTO!")
            self.statusText.SetPackedFontColor(0xFF00FF00)
            self.statusSubText.SetText("Resisti fino alla fine del timer!")
        else:
            # Aggiorna testo normale
            self.progressText.SetText("%d / %d" % (killed, self.mobsRequired))
            self.progressText.SetPackedFontColor(0xFFFFFFFF)
            # Aggiorna barra
            if self.mobsRequired > 0:
                progress = float(killed) / float(self.mobsRequired)
                barWidth = int(346 * min(1.0, progress))
                self.progressBarFill.SetSize(barWidth, 16)
                self.progressBarGlow.SetSize(barWidth, 8)
                self.progressBarFill.SetColor(self.colorScheme["border"])

        # Aggiorna wave
        if wave > 0 and wave != self.currentWave:
            self.currentWave = wave
            for i, ind in enumerate(self.waveIndicators):
                if i < wave:
                    ind.SetColor(self.colorScheme["border"])
                else:
                    ind.SetColor(0xFF333333)

    def UpdateDistance(self):
        """Aggiorna la distanza dalla frattura"""
        if not self.isActive or self.defenseCenterX == 0:
            return
        
        try:
            # Ottieni posizione player
            px, py, pz = player.GetMainCharacterPosition()
            
            # Calcola distanza dal centro
            dx = px - self.defenseCenterX
            dy = py - self.defenseCenterY
            distance = math.sqrt(dx * dx + dy * dy)
            
            # Converti in metri (100 unita' = 1 metro)
            distMeters = int(distance / 100)
            maxMeters = int(self.defenseRadius / 100)
            
            self.currentDistance = distance
            self.distValue.SetText("%dm" % distMeters)
            
            # Calcola percentuale per la barra
            if self.defenseRadius > 0:
                ratio = min(1.0, distance / self.defenseRadius)
                barWidth = int(346 * ratio)
                self.distBarFill.SetSize(barWidth, 8)
            
            # Colori in base alla distanza (con buffer di 50 unita = 0.5m per evitare falsi positivi)
            if distance >= self.defenseRadius + 50:
                # FUORI ZONA!
                self.distValue.SetPackedFontColor(0xFFFF0000)
                self.distBarFill.SetColor(0xFFFF0000)
                self.warningText.SetText("!!! TORNA NELLA ZONA !!!")
                self.warningText.Show()
                self.distanceStatus = "DANGER"
            elif distance >= self.defenseRadius * 0.8:
                # Warning
                self.distValue.SetPackedFontColor(0xFFFFAA00)
                self.distBarFill.SetColor(0xFFFFAA00)
                self.warningText.SetText("ATTENZIONE: Stai uscendo dalla zona!")
                self.warningText.SetPackedFontColor(0xFFFFAA00)
                self.warningText.Show()
                self.distanceStatus = "WARNING"
            else:
                # OK
                self.distValue.SetPackedFontColor(0xFF00FF00)
                self.distBarFill.SetColor(self.colorScheme["border"])
                self.warningText.Hide()
                self.distanceStatus = "OK"
                
        except Exception as e:
            pass

    def EndDefense(self, success):
        """Termina la difesa"""
        self.isActive = False
        self.endTime = 0
        self.zeroTimeStart = 0

        if success:
            self.statusText.SetText("DIFESA COMPLETATA!")
            self.statusText.SetPackedFontColor(0xFF00FF00)
            self.statusSubText.SetText("Tocca il portale per aprire la frattura!")
            # Bordi verdi lampeggianti
            for b in self.borders:
                b.SetColor(0xFF00FF00)
        else:
            self.statusText.SetText("DIFESA FALLITA!")
            self.statusText.SetPackedFontColor(0xFFFF0000)
            self.statusSubText.SetText("La frattura rimane chiusa...")
            # Bordi rossi
            for b in self.borders:
                b.SetColor(0xFFFF0000)
        
        self.warningText.Hide()

        # Auto-hide dopo 3 secondi
        self.endTime = app.GetTime() + 3.0

    def Close(self):
        """Chiude la finestra"""
        self.isActive = False
        self.endTime = 0
        self.zeroTimeStart = 0
        self.defenseCenterX = 0
        self.defenseCenterY = 0
        self.Hide()

    def OnUpdate(self):
        if not self.IsShow():
            return

        currentTime = app.GetTime()

        # Auto-close dopo EndDefense
        if self.endTime > 0 and not self.isActive:
            if currentTime > self.endTime:
                self.Hide()
                self.endTime = 0
                return

        # Timer countdown
        if self.isActive and self.endTime > 0:
            remaining = max(0, self.endTime - currentTime)
            minutes = int(remaining) // 60
            seconds = int(remaining) % 60
            self.timerText.SetText("%02d:%02d" % (minutes, seconds))

            # FIX BUG DIFESA BLOCCATA: Failsafe client-side
            # Se il timer e' a 00:00 per 30+ secondi senza risposta dal server,
            # mostra messaggio di errore e chiudi la finestra
            if remaining <= 0:
                if self.zeroTimeStart == 0:
                    self.zeroTimeStart = currentTime
                elif currentTime - self.zeroTimeStart > 30:
                    self.isActive = False
                    self.endTime = currentTime + 3.0
                    self.statusText.SetText("DIFESA TERMINATA")
                    self.statusText.SetPackedFontColor(0xFFFF4444)
                    self.statusSubText.SetText("Nessuna risposta dal server.")
                    self.warningText.Hide()
                    self.zeroTimeStart = 0
                    for b in self.borders:
                        b.SetColor(0xFFFF0000)
                    return
            else:
                self.zeroTimeStart = 0

            # Colore timer (rosso se poco tempo)
            if remaining < 10:
                self.timerText.SetPackedFontColor(0xFFFF0000)
            elif remaining < 30:
                self.timerText.SetPackedFontColor(0xFFFFAA00)
            else:
                self.timerText.SetPackedFontColor(0xFFFFFFFF)
            
            # Aggiorna distanza in tempo reale
            self.UpdateDistance()

        # Effetto pulse sui bordi
        self.pulsePhase += 0.08
        if self.isActive:
            pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
            baseColor = self.colorScheme["border"]
            r = ((baseColor >> 16) & 0xFF)
            g = ((baseColor >> 8) & 0xFF)
            b = (baseColor & 0xFF)

            # Varia luminosita
            factor = 0.7 + (pulse * 0.3)
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))

            pulseColor = 0xFF000000 | (r << 16) | (g << 8) | b
            for border in self.borders:
                border.SetColor(pulseColor)


# ═══════════════════════════════════════════════════════════════════════════════
#  SPEED KILL TIMER WINDOW - Solo Leveling Style
#  UI per Speed Kill challenge (Boss e Super Metin)
# ═══════════════════════════════════════════════════════════════════════════════

# Colori per tipo di mob
SPEEDKILL_COLORS = {
    "BOSS": {
        "border": 0xFFFF0000,
        "glow": 0x66FF0000,
        "title": 0xFFFF4444,
        "accent": 0xFFCC0000,
        "timer_bg": 0xAA440000,
        "icon": "[X]",
        "label": "BOSS HUNT"
    },
    "SUPER_METIN": {
        "border": 0xFFFF8800,
        "glow": 0x66FF8800,
        "title": 0xFFFFAA44,
        "accent": 0xFFCC6600,
        "timer_bg": 0xAA443300,
        "icon": "[*]",
        "label": "METIN STRIKE"
    },
    "DEFAULT": {
        "border": 0xFFFFD700,
        "glow": 0x66FFD700,
        "title": 0xFFFFFF55,
        "accent": 0xFFCCAA00,
        "timer_bg": 0xAA444400,
        "icon": "[!]",
        "label": "SPEED KILL"
    }
}


class SpeedKillTimerWindow(ui.Window, DraggableMixin):
    """Finestra Speed Kill Timer - Solo Leveling Style"""

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(320, 130)
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("SpeedKillTimerWindow", 320, 130)

        self.InitDraggable("SpeedKillTimerWindow", defaultX, defaultY)

        # Variabili di stato
        self.endTime = 0
        self.startTime = 0
        self.totalDuration = 0
        self.mobName = ""
        self.mobType = "DEFAULT"
        self.pulsePhase = 0.0
        self.isActive = False
        self.flashPhase = 0.0
        self.lastUpdateTime = 0  # Timeout fallback se server non manda End

        # Schema colori corrente
        self.colorScheme = SPEEDKILL_COLORS["DEFAULT"]

        # ═══════════ SFONDO PRINCIPALE ═══════════
        # Sfondo esterno scuro
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(320, 130)
        self.bgOuter.SetColor(0xEE0A0A14)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()

        # Glow interno
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(3, 3)
        self.glowInner.SetSize(314, 124)
        self.glowInner.SetColor(0x22FF0000)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()

        # Sfondo interno
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 5)
        self.bgInner.SetSize(310, 120)
        self.bgInner.SetColor(0xDD080812)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # ═══════════ BORDI ANIMATI ═══════════
        self.borders = []
        borderColor = 0xFFFF0000
        # Top
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(320, 3); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Bottom
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 127); b.SetSize(320, 3); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Left
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(3, 130); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Right
        b = ui.Bar(); b.SetParent(self); b.SetPosition(317, 0); b.SetSize(3, 130); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)

        # ═══════════ HEADER ═══════════
        # Icona target
        self.targetIcon = ui.TextLine()
        self.targetIcon.SetParent(self)
        self.targetIcon.SetPosition(15, 12)
        self.targetIcon.SetText("[X]")
        self.targetIcon.SetPackedFontColor(0xFFFF0000)
        self.targetIcon.SetOutline()
        self.targetIcon.AddFlag("not_pick")
        self.targetIcon.Show()

        # Label tipo (BOSS HUNT / METIN STRIKE)
        self.typeLabel = ui.TextLine()
        self.typeLabel.SetParent(self)
        self.typeLabel.SetPosition(160, 10)
        self.typeLabel.SetHorizontalAlignCenter()
        self.typeLabel.SetText("SPEED KILL")
        self.typeLabel.SetPackedFontColor(0xFFFFFFFF)
        self.typeLabel.SetOutline()
        self.typeLabel.AddFlag("not_pick")
        self.typeLabel.Show()

        # Sottotitolo bonus
        self.bonusLabel = ui.TextLine()
        self.bonusLabel.SetParent(self)
        self.bonusLabel.SetPosition(160, 26)
        self.bonusLabel.SetHorizontalAlignCenter()
        self.bonusLabel.SetText(">>> BONUS GLORIA <<<")
        self.bonusLabel.SetPackedFontColor(0xFFFFD700)
        self.bonusLabel.AddFlag("not_pick")
        self.bonusLabel.Show()

        # Linea separatore header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(10, 44)
        self.headerLine.SetSize(300, 1)
        self.headerLine.SetColor(0x88FFFFFF)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # ═══════════ TARGET NAME ═══════════
        self.targetNameLabel = ui.TextLine()
        self.targetNameLabel.SetParent(self)
        self.targetNameLabel.SetPosition(160, 52)
        self.targetNameLabel.SetHorizontalAlignCenter()
        self.targetNameLabel.SetText("")
        self.targetNameLabel.SetPackedFontColor(0xFFFFFFFF)
        self.targetNameLabel.SetOutline()
        self.targetNameLabel.AddFlag("not_pick")
        self.targetNameLabel.Show()

        # ═══════════ TIMER DISPLAY ═══════════
        # Background timer grande
        self.timerBg = ui.Bar()
        self.timerBg.SetParent(self)
        self.timerBg.SetPosition(60, 72)
        self.timerBg.SetSize(200, 45)
        self.timerBg.SetColor(0xAA330000)
        self.timerBg.AddFlag("not_pick")
        self.timerBg.Show()

        # Timer grande
        self.timerText = ui.TextLine()
        self.timerText.SetParent(self)
        self.timerText.SetPosition(160, 80)
        self.timerText.SetHorizontalAlignCenter()
        self.timerText.SetText("00:00")
        self.timerText.SetPackedFontColor(0xFFFFFFFF)
        self.timerText.SetOutline()
        self.timerText.AddFlag("not_pick")
        self.timerText.Show()

        # Timer progress bar
        self.timerProgressBg = ui.Bar()
        self.timerProgressBg.SetParent(self)
        self.timerProgressBg.SetPosition(65, 105)
        self.timerProgressBg.SetSize(190, 8)
        self.timerProgressBg.SetColor(0xFF1A1A2E)
        self.timerProgressBg.AddFlag("not_pick")
        self.timerProgressBg.Show()

        self.timerProgressFill = ui.Bar()
        self.timerProgressFill.SetParent(self)
        self.timerProgressFill.SetPosition(65, 105)
        self.timerProgressFill.SetSize(190, 8)
        self.timerProgressFill.SetColor(0xFFFF0000)
        self.timerProgressFill.AddFlag("not_pick")
        self.timerProgressFill.Show()

        self.Hide()

    def SetMobType(self, mobType):
        """Imposta il tipo di mob e i colori"""
        mobType = str(mobType).upper().replace(" ", "_")
        if mobType not in SPEEDKILL_COLORS:
            # Prova a determinare dal nome
            if "BOSS" in mobType:
                mobType = "BOSS"
            elif "METIN" in mobType:
                mobType = "SUPER_METIN"
            else:
                mobType = "DEFAULT"

        self.mobType = mobType
        self.colorScheme = SPEEDKILL_COLORS[mobType]

        borderColor = self.colorScheme["border"]
        titleColor = self.colorScheme["title"]
        glowColor = self.colorScheme["glow"]

        # Aggiorna bordi
        for b in self.borders:
            b.SetColor(borderColor)

        # Aggiorna icona e label
        self.targetIcon.SetText(self.colorScheme["icon"])
        self.targetIcon.SetPackedFontColor(borderColor)
        self.typeLabel.SetText(self.colorScheme["label"])
        self.typeLabel.SetPackedFontColor(titleColor)

        # Aggiorna glow
        self.glowInner.SetColor(glowColor)

        # Aggiorna timer background
        self.timerBg.SetColor(self.colorScheme["timer_bg"])

        # Aggiorna progress bar
        self.timerProgressFill.SetColor(borderColor)

    def StartSpeedKill(self, mobName, duration, mobType="DEFAULT"):
        """Inizia la sfida Speed Kill"""
        self.mobName = mobName.replace("+", " ")
        self.totalDuration = duration
        self.startTime = app.GetTime()
        self.endTime = self.startTime + duration
        self.isActive = True
        self.pulsePhase = 0.0
        self.flashPhase = 0.0
        self.lastUpdateTime = app.GetTime()  # Reset timeout

        # Imposta tipo e colori
        self.SetMobType(mobType)

        # Aggiorna UI
        self.targetNameLabel.SetText("[ %s ]" % self.mobName)
        self.targetNameLabel.SetPackedFontColor(self.colorScheme["title"])

        # Timer iniziale
        minutes = duration // 60
        seconds = duration % 60
        self.timerText.SetText("%02d:%02d" % (minutes, seconds))
        self.timerText.SetPackedFontColor(0xFFFFFFFF)

        # Progress bar al 100%
        self.timerProgressFill.SetSize(190, 8)

        self.Show()
        self.SetTop()

    def UpdateTimer(self, remainingSeconds):
        """Aggiorna il timer"""
        if not self.isActive:
            return

        self.lastUpdateTime = app.GetTime()  # Reset timeout

        minutes = remainingSeconds // 60
        seconds = remainingSeconds % 60
        self.timerText.SetText("%02d:%02d" % (minutes, seconds))

        # Aggiorna progress bar
        if self.totalDuration > 0:
            progress = float(remainingSeconds) / float(self.totalDuration)
            barWidth = int(190 * progress)
            self.timerProgressFill.SetSize(max(0, barWidth), 8)

        # Colore timer basato sul tempo rimanente
        if remainingSeconds <= 10:
            self.timerText.SetPackedFontColor(0xFFFF0000)
        elif remainingSeconds <= 30:
            self.timerText.SetPackedFontColor(0xFFFF8800)
        else:
            self.timerText.SetPackedFontColor(0xFFFFFFFF)

    def EndSpeedKill(self, success, bonusGlory=0):
        """Termina la sfida"""
        self.isActive = False

        if success:
            # Successo!
            self.typeLabel.SetText("SUCCESS!")
            self.typeLabel.SetPackedFontColor(0xFF00FF00)
            if bonusGlory > 0:
                self.bonusLabel.SetText("+%d GLORIA BONUS!" % bonusGlory)
            else:
                self.bonusLabel.SetText("GLORIA BONUS OTTENUTA!")
            self.bonusLabel.SetPackedFontColor(0xFF00FF00)
            self.timerText.SetText("VITTORIA!")
            self.timerText.SetPackedFontColor(0xFF00FF00)
            for b in self.borders:
                b.SetColor(0xFF00FF00)
            self.glowInner.SetColor(0x6600FF00)
        else:
            # Fallito
            self.typeLabel.SetText("TIME OUT!")
            self.typeLabel.SetPackedFontColor(0xFFFF0000)
            self.bonusLabel.SetText("Gloria normale...")
            self.bonusLabel.SetPackedFontColor(0xFF888888)
            self.timerText.SetText("FALLITO")
            self.timerText.SetPackedFontColor(0xFFFF0000)
            for b in self.borders:
                b.SetColor(0xFFFF0000)

        # Auto-hide dopo 3 secondi
        self.endTime = app.GetTime() + 3.0

    def Close(self):
        """Chiude la finestra"""
        self.isActive = False
        self.endTime = 0
        self.Hide()

    def OnUpdate(self):
        if not self.IsShow():
            return

        currentTime = app.GetTime()

        # Auto-close dopo EndSpeedKill
        if self.endTime > 0 and not self.isActive:
            if currentTime > self.endTime:
                self.Hide()
                self.endTime = 0
                return

        # FALLBACK: Se nessun update ricevuto per 15 secondi mentre attivo,
        # il server potrebbe non aver mandato il segnale End - chiudi in modo neutro
        if self.isActive and self.lastUpdateTime > 0:
            if currentTime - self.lastUpdateTime > 15.0:
                # NON assumere vittoria - chiudi senza risultato
                self.isActive = False
                self.Hide()
                self.endTime = 0
                return

        # Effetto pulse sui bordi quando attivo
        if self.isActive:
            self.pulsePhase += 0.12
            pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
            baseColor = self.colorScheme["border"]
            r = ((baseColor >> 16) & 0xFF)
            g = ((baseColor >> 8) & 0xFF)
            b = (baseColor & 0xFF)

            # Varia luminosita
            factor = 0.6 + (pulse * 0.4)
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))

            pulseColor = 0xFF000000 | (r << 16) | (g << 8) | b
            for border in self.borders:
                border.SetColor(pulseColor)

            # Flash bonus label
            self.flashPhase += 0.15
            flashAlpha = int(200 + 55 * math.sin(self.flashPhase))
            self.bonusLabel.SetPackedFontColor((flashAlpha << 24) | 0x00FFD700)


# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER TIPS WINDOW - Consigli Hunter con fade elegante
#  Mostra UN tip alla volta con layout ampio per testo completo
# ═══════════════════════════════════════════════════════════════════════════════

class HunterTipsWindow(ui.Window, DraggableMixin):
    """Finestra per Hunter Tips - Stile oro elegante, 1 tip alla volta"""

    TIP_DISPLAY_TIME = 12.0  # Secondi di visualizzazione
    TIP_FADE_DURATION = 2.0  # Durata della sfumatura

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(420, 85)
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("HunterTipsWindow", 420, 85)

        self.InitDraggable("HunterTipsWindow", defaultX, defaultY)

        # Stato corrente
        self.currentTip = ""
        self.startTime = 0
        self.alpha = 255
        self.pulsePhase = 0.0

        # ═══════════ SFONDO PRINCIPALE ═══════════
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(420, 85)
        self.bgOuter.SetColor(0xDD0A0A14)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()

        # Glow interno oro
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(2, 2)
        self.glowInner.SetSize(416, 81)
        self.glowInner.SetColor(0x22FFD700)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()

        # Bordi oro animati
        self.borders = []
        borderColor = 0xCCFFD700
        # Top
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(420, 2); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Bottom
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 83); b.SetSize(420, 2); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Left
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(2, 85); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Right
        b = ui.Bar(); b.SetParent(self); b.SetPosition(418, 0); b.SetSize(2, 85); b.SetColor(borderColor); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)

        # ═══════════ HEADER ═══════════
        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(2, 2)
        self.headerBg.SetSize(416, 20)
        self.headerBg.SetColor(0x55FFD700)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        # Icona lampadina/info
        self.titleIcon = ui.TextLine()
        self.titleIcon.SetParent(self)
        self.titleIcon.SetPosition(10, 4)
        self.titleIcon.SetText("[!]")
        self.titleIcon.SetPackedFontColor(0xFFFFD700)
        self.titleIcon.SetOutline()
        self.titleIcon.AddFlag("not_pick")
        self.titleIcon.Show()

        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(30, 4)
        self.titleText.SetText("HUNTER TIP")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()

        # ═══════════ AREA TESTO TIP (3 righe) ═══════════
        self.tipLines = []
        for i in range(3):
            tipLine = ui.TextLine()
            tipLine.SetParent(self)
            tipLine.SetPosition(12, 28 + (i * 18))
            tipLine.SetText("")
            tipLine.SetPackedFontColor(0xFFFFFFFF)
            tipLine.AddFlag("not_pick")
            tipLine.Show()
            self.tipLines.append(tipLine)

        self.Hide()

    def _WrapText(self, text, maxCharsPerLine=55):
        """Spezza il testo in righe di massimo maxCharsPerLine caratteri"""
        words = text.split(' ')
        lines = []
        currentLine = ""

        for word in words:
            if len(currentLine) + len(word) + 1 <= maxCharsPerLine:
                if currentLine:
                    currentLine += " " + word
                else:
                    currentLine = word
            else:
                if currentLine:
                    lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        # Massimo 3 righe
        return lines[:3]

    def AddTip(self, tipText):
        """Mostra un nuovo tip"""
        # Rimuovi prefissi se presenti
        tipText = tipText.replace("[HUNTER TIP] ", "").replace("[HUNTER TIP]", "").strip()

        self.currentTip = tipText
        self.startTime = app.GetTime()
        self.alpha = 255

        # Spezza il testo in righe
        lines = self._WrapText(tipText)

        # Aggiorna le label
        for i, tipLine in enumerate(self.tipLines):
            if i < len(lines):
                tipLine.SetText(lines[i])
                tipLine.SetPackedFontColor(0xFFFFFFFF)
            else:
                tipLine.SetText("")

        # Mostra la finestra
        self.Show()
        self.SetTop()

    def Close(self):
        """Chiude la finestra"""
        self.currentTip = ""
        self.startTime = 0
        self.Hide()

    def OnUpdate(self):
        if not self.IsShow():
            return

        if self.startTime == 0:
            self.Hide()
            return

        currentTime = app.GetTime()
        elapsed = currentTime - self.startTime

        # Calcola alpha per fade
        if elapsed < self.TIP_DISPLAY_TIME:
            # Tip visibile
            self.alpha = 255
        elif elapsed < self.TIP_DISPLAY_TIME + self.TIP_FADE_DURATION:
            # Fase fade out
            fadeProgress = (elapsed - self.TIP_DISPLAY_TIME) / self.TIP_FADE_DURATION
            self.alpha = int(255 * (1.0 - fadeProgress))
        else:
            # Tip terminato
            self.Hide()
            self.startTime = 0
            return

        # Aggiorna alpha dei testi
        textColor = (self.alpha << 24) | 0x00FFFFFF
        goldColor = (self.alpha << 24) | 0x00FFD700
        for tipLine in self.tipLines:
            tipLine.SetPackedFontColor(textColor)
        self.titleText.SetPackedFontColor(goldColor)
        self.titleIcon.SetPackedFontColor(goldColor)

        # Aggiorna alpha sfondo e bordi
        bgAlpha = int(self.alpha * 0.87)  # 0xDD = 221/255 = 0.87
        self.bgOuter.SetColor((bgAlpha << 24) | 0x000A0A14)

        glowAlpha = int(self.alpha * 0.13)  # 0x22 = 34/255 = 0.13
        self.glowInner.SetColor((glowAlpha << 24) | 0x00FFD700)

        headerAlpha = int(self.alpha * 0.33)  # 0x55
        self.headerBg.SetColor((headerAlpha << 24) | 0x00FFD700)

        # Effetto pulse leggero sui bordi
        self.pulsePhase += 0.08
        pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
        borderAlpha = int(self.alpha * (0.7 + pulse * 0.3))
        borderColor = (borderAlpha << 24) | 0x00FFD700
        for border in self.borders:
            border.SetColor(borderColor)


# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER NOTIFICATION WINDOW - Sistema notifiche senza spam chat
# ═══════════════════════════════════════════════════════════════════════════════

class HunterNotificationWindow(ui.Window, DraggableMixin):
    """
    Finestra notifiche Hunter - Stile moderno con coda messaggi
    Usata per: vincitori eventi, achievement claims, rank changes, system messages
    """

    NOTIFICATION_DISPLAY_TIME = 8.0  # Secondi di visualizzazione per notifica
    NOTIFICATION_FADE_DURATION = 1.5  # Durata fade in/out
    MAX_QUEUE_SIZE = 10  # Limite massimo notifiche in coda (MEMORY LEAK PROTECTION)

    # Color schemes per diversi tipi di notifica
    NOTIFICATION_TYPES = {
        "winner": {
            "border": 0xFFFFD700,    # Gold
            "glow": 0x44FFD700,      # Gold glow
            "title": 0xFFFFE455,     # Light gold
            "header_bg": 0x55FFD700, # Gold background
            "icon": "[*]",
            "title_text": "VINCITORE"
        },
        "achievement": {
            "border": 0xFF00FF00,    # Green
            "glow": 0x4400FF00,      # Green glow
            "title": 0xFF55FF55,     # Light green
            "header_bg": 0x5500CC00, # Green background
            "icon": "[+]",
            "title_text": "TRAGUARDO"
        },
        "rank": {
            "border": 0xFFAA00FF,    # Purple
            "glow": 0x44AA00FF,      # Purple glow
            "title": 0xFFCC55FF,     # Light purple
            "header_bg": 0x558800CC, # Purple background
            "icon": "[^]",
            "title_text": "GRADO"
        },
        "system": {
            "border": 0xFF0088FF,    # Blue
            "glow": 0x440088FF,      # Blue glow
            "title": 0xFF55AAFF,     # Light blue
            "header_bg": 0x550066CC, # Blue background
            "icon": "[!]",
            "title_text": "SISTEMA"
        },
        "event": {
            "border": 0xFFFF8800,    # Orange
            "glow": 0x44FF8800,      # Orange glow
            "title": 0xFFFFAA55,     # Light orange
            "header_bg": 0x55CC6600, # Orange background
            "icon": "[E]",
            "title_text": "EVENTO"
        },
        "world_boss": {
            "border": 0xFFFF0000,    # Red (pericolo!)
            "glow": 0x88FF0000,      # Red glow intenso
            "title": 0xFFFF5555,     # Light red
            "header_bg": 0x88CC0000, # Red background
            "icon": "[!]",
            "title_text": "SUPREMO!"
        }
    }

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(450, 90)
        # Usa posizioni default ottimizzate
        defaultX, defaultY = GetDefaultPosition("HunterNotificationWindow", 450, 90)

        self.InitDraggable("HunterNotificationWindow", defaultX, defaultY)

        # Sistema di coda notifiche
        self.notificationQueue = []  # Lista di dict con {type, message}
        self.currentNotification = None
        self.startTime = 0
        self.alpha = 0  # Parte da 0 per fade-in
        self.pulsePhase = 0.0
        self.currentType = "system"  # Tipo corrente

        # ═══════════ SFONDO PRINCIPALE ═══════════
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(450, 90)
        self.bgOuter.SetColor(0xDD0A0A14)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()

        # Glow interno (colore dinamico)
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(2, 2)
        self.glowInner.SetSize(446, 86)
        self.glowInner.SetColor(0x220088FF)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()

        # Bordi animati (colore dinamico)
        self.borders = []
        # Top
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(450, 2); b.SetColor(0xCC0088FF); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Bottom
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 88); b.SetSize(450, 2); b.SetColor(0xCC0088FF); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Left
        b = ui.Bar(); b.SetParent(self); b.SetPosition(0, 0); b.SetSize(2, 90); b.SetColor(0xCC0088FF); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)
        # Right
        b = ui.Bar(); b.SetParent(self); b.SetPosition(448, 0); b.SetSize(2, 90); b.SetColor(0xCC0088FF); b.AddFlag("not_pick"); b.Show()
        self.borders.append(b)

        # ═══════════ HEADER ═══════════
        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(2, 2)
        self.headerBg.SetSize(446, 22)
        self.headerBg.SetColor(0x550088FF)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        # Icona dinamica
        self.titleIcon = ui.TextLine()
        self.titleIcon.SetParent(self)
        self.titleIcon.SetPosition(10, 5)
        self.titleIcon.SetText("[!]")
        self.titleIcon.SetPackedFontColor(0xFF0088FF)
        self.titleIcon.SetOutline()
        self.titleIcon.AddFlag("not_pick")
        self.titleIcon.Show()

        # Titolo dinamico
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(30, 5)
        self.titleText.SetText("NOTIFICA")
        self.titleText.SetPackedFontColor(0xFF0088FF)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()

        # ═══════════ AREA TESTO NOTIFICA (3 righe) ═══════════
        self.messageLines = []
        for i in range(3):
            msgLine = ui.TextLine()
            msgLine.SetParent(self)
            msgLine.SetPosition(12, 30 + (i * 19))
            msgLine.SetText("")
            msgLine.SetPackedFontColor(0xFFFFFFFF)
            msgLine.AddFlag("not_pick")
            msgLine.Show()
            self.messageLines.append(msgLine)

        self.Hide()

    def _WrapText(self, text, maxCharsPerLine=60):
        """Spezza il testo in righe di massimo maxCharsPerLine caratteri"""
        words = text.split(' ')
        lines = []
        currentLine = ""

        for word in words:
            if len(currentLine) + len(word) + 1 <= maxCharsPerLine:
                if currentLine:
                    currentLine += " " + word
                else:
                    currentLine = word
            else:
                if currentLine:
                    lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        # Massimo 3 righe
        return lines[:3]

    def AddNotification(self, notificationType, message):
        """
        Aggiunge una notifica alla coda
        Args:
            notificationType: "winner", "achievement", "rank", "system", "event"
            message: Testo del messaggio
        """
        # Valida tipo
        if notificationType not in self.NOTIFICATION_TYPES:
            notificationType = "system"

        # MEMORY LEAK PROTECTION: Limita dimensione coda
        # Se la coda è piena, rimuovi le notifiche più vecchie
        while len(self.notificationQueue) >= self.MAX_QUEUE_SIZE:
            self.notificationQueue.pop(0)  # Rimuovi la più vecchia

        # Aggiungi a coda
        self.notificationQueue.append({
            "type": notificationType,
            "message": message
        })

        # Se non sta già mostrando una notifica, mostra subito
        if self.currentNotification is None:
            self._ShowNextNotification()

    def _ShowNextNotification(self):
        """Mostra la prossima notifica dalla coda"""
        if len(self.notificationQueue) == 0:
            self.currentNotification = None
            self.Hide()
            return

        # Prendi la prima dalla coda
        notification = self.notificationQueue.pop(0)
        self.currentNotification = notification
        self.currentType = notification["type"]
        self.startTime = app.GetTime()
        self.alpha = 0  # Fade-in da 0

        # Ottieni colori per questo tipo
        colors = self.NOTIFICATION_TYPES[self.currentType]

        # Aggiorna header
        self.titleIcon.SetText(colors["icon"])
        self.titleText.SetText(colors["title_text"])

        # Spezza testo in righe
        lines = self._WrapText(notification["message"])

        # Aggiorna le label
        for i, msgLine in enumerate(self.messageLines):
            if i < len(lines):
                msgLine.SetText(lines[i])
            else:
                msgLine.SetText("")

        # Mostra la finestra
        self.Show()
        self.SetTop()

    def Close(self):
        """Chiude la finestra e pulisce la coda"""
        self.notificationQueue = []
        self.currentNotification = None
        self.startTime = 0
        self.Hide()

    def OnUpdate(self):
        if not self.IsShow():
            return

        if self.currentNotification is None:
            self.Hide()
            return

        currentTime = app.GetTime()
        elapsed = currentTime - self.startTime

        # Calcola alpha per fade-in/fade-out
        if elapsed < self.NOTIFICATION_FADE_DURATION:
            # Fase fade-in
            fadeProgress = elapsed / self.NOTIFICATION_FADE_DURATION
            self.alpha = int(255 * fadeProgress)
        elif elapsed < self.NOTIFICATION_DISPLAY_TIME:
            # Notifica visibile
            self.alpha = 255
        elif elapsed < self.NOTIFICATION_DISPLAY_TIME + self.NOTIFICATION_FADE_DURATION:
            # Fase fade-out
            fadeProgress = (elapsed - self.NOTIFICATION_DISPLAY_TIME) / self.NOTIFICATION_FADE_DURATION
            self.alpha = int(255 * (1.0 - fadeProgress))
        else:
            # Notifica terminata, mostra prossima
            self._ShowNextNotification()
            return

        # Ottieni colori per tipo corrente
        colors = self.NOTIFICATION_TYPES[self.currentType]

        # Aggiorna alpha dei testi
        textColor = (self.alpha << 24) | 0x00FFFFFF
        titleColor = (self.alpha << 24) | (colors["title"] & 0x00FFFFFF)

        for msgLine in self.messageLines:
            msgLine.SetPackedFontColor(textColor)
        self.titleText.SetPackedFontColor(titleColor)
        self.titleIcon.SetPackedFontColor(titleColor)

        # Aggiorna alpha sfondo
        bgAlpha = int(self.alpha * 0.87)  # 0xDD
        self.bgOuter.SetColor((bgAlpha << 24) | 0x000A0A14)

        # Aggiorna glow con colore tipo
        glowAlpha = int(self.alpha * 0.13)  # 0x22
        glowColorBase = colors["glow"] & 0x00FFFFFF
        self.glowInner.SetColor((glowAlpha << 24) | glowColorBase)

        # Aggiorna header background
        headerAlpha = int(self.alpha * 0.33)  # 0x55
        headerColorBase = colors["header_bg"] & 0x00FFFFFF
        self.headerBg.SetColor((headerAlpha << 24) | headerColorBase)

        # Effetto pulse sui bordi
        self.pulsePhase += 0.08
        pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
        borderAlpha = int(self.alpha * (0.7 + pulse * 0.3))
        borderColorBase = colors["border"] & 0x00FFFFFF
        borderColor = (borderAlpha << 24) | borderColorBase
        for border in self.borders:
            border.SetColor(borderColor)


# ═══════════════════════════════════════════════════════════════════════════════
#  SUPREMO SYSTEM - AWAKENING WINDOW
#  Annuncio globale stile Solo Leveling quando un Supremo viene risvegliato
# ═══════════════════════════════════════════════════════════════════════════════
class SupremoAwakeningWindow(ui.Window):
    """Finestra di annuncio globale quando un Supremo viene risvegliato - visibile a TUTTI"""
    
    RANK_COLORS = {
        "E": {"border": 0xFF808080, "title": 0xFFFFFFFF, "text": 0xFFCCCCCC},
        "D": {"border": 0xFF00AA00, "title": 0xFF00FF00, "text": 0xFFAAFFAA},
        "C": {"border": 0xFF0088FF, "title": 0xFF00CCFF, "text": 0xFFAADDFF},
        "B": {"border": 0xFFAA00AA, "title": 0xFFFF00FF, "text": 0xFFFFAAFF},
        "A": {"border": 0xFFFF6600, "title": 0xFFFF9900, "text": 0xFFFFCC88},
        "S": {"border": 0xFFFF0000, "title": 0xFFFF4444, "text": 0xFFFFAAAA},
        "SS": {"border": 0xFFFFD700, "title": 0xFFFFD700, "text": 0xFFFFEEAA},
        "SSS": {"border": 0xFFFF1493, "title": 0xFFFF1493, "text": 0xFFFFAACC}
    }
    
    def __init__(self):
        ui.Window.__init__(self)
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        
        # Dimensioni finestra
        self.winW = 500
        self.winH = 160
        
        self.SetSize(self.winW, self.winH)
        self.SetPosition((screenW - self.winW) // 2, int(screenH * 0.2))
        
        self.endTime = 0
        self.pulsePhase = 0.0
        self.currentRank = "E"
        
        # Background principale scuro con overlay
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(self.winW, self.winH)
        self.bgOuter.SetColor(0xEE080810)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()
        
        # Inner glow
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(3, 3)
        self.glowInner.SetSize(self.winW - 6, self.winH - 6)
        self.glowInner.SetColor(0x22FFFFFF)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()
        
        # Inner background
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 5)
        self.bgInner.SetSize(self.winW - 10, self.winH - 10)
        self.bgInner.SetColor(0xDD0A0A14)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()
        
        # Bordi animati
        self.borders = []
        for y in [0, self.winH - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(self.winW, 2); b.SetColor(0xFFFFD700); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, self.winW - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, self.winH); b.SetColor(0xFFFFD700); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        
        # Sistema Warning Label
        self.warningLabel = ui.TextLine()
        self.warningLabel.SetParent(self)
        self.warningLabel.SetPosition(self.winW // 2, 15)
        self.warningLabel.SetHorizontalAlignCenter()
        self.warningLabel.SetText("⚠ SISTEMA HUNTER ⚠")
        self.warningLabel.SetPackedFontColor(0xFFFF4444)
        self.warningLabel.SetOutline()
        self.warningLabel.AddFlag("not_pick")
        self.warningLabel.Show()
        
        # Titolo principale - RISVEGLIO
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.winW // 2, 38)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("UN SUPREMO SI E' RISVEGLIATO!")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()
        
        # Nome Supremo
        self.supremoNameText = ui.TextLine()
        self.supremoNameText.SetParent(self)
        self.supremoNameText.SetPosition(self.winW // 2, 62)
        self.supremoNameText.SetHorizontalAlignCenter()
        self.supremoNameText.SetText("")
        self.supremoNameText.SetPackedFontColor(0xFFFFFFFF)
        self.supremoNameText.SetOutline()
        self.supremoNameText.AddFlag("not_pick")
        self.supremoNameText.Show()
        
        # Grado Supremo
        self.rankText = ui.TextLine()
        self.rankText.SetParent(self)
        self.rankText.SetPosition(self.winW // 2, 82)
        self.rankText.SetHorizontalAlignCenter()
        self.rankText.SetText("")
        self.rankText.SetPackedFontColor(0xFFFFD700)
        self.rankText.SetOutline()
        self.rankText.AddFlag("not_pick")
        self.rankText.Show()
        
        # Linea separatore
        self.separator = ui.Bar()
        self.separator.SetParent(self)
        self.separator.SetPosition(50, 105)
        self.separator.SetSize(self.winW - 100, 1)
        self.separator.SetColor(0x66FFFFFF)
        self.separator.AddFlag("not_pick")
        self.separator.Show()
        
        # Evocatore
        self.summonerText = ui.TextLine()
        self.summonerText.SetParent(self)
        self.summonerText.SetPosition(self.winW // 2, 115)
        self.summonerText.SetHorizontalAlignCenter()
        self.summonerText.SetText("")
        self.summonerText.SetPackedFontColor(0xFFCCCCCC)
        self.summonerText.AddFlag("not_pick")
        self.summonerText.Show()
        
        # Warning Text
        self.warningSubText = ui.TextLine()
        self.warningSubText.SetParent(self)
        self.warningSubText.SetPosition(self.winW // 2, 135)
        self.warningSubText.SetHorizontalAlignCenter()
        self.warningSubText.SetText("Preparati alla battaglia...")
        self.warningSubText.SetPackedFontColor(0xFFFF6666)
        self.warningSubText.AddFlag("not_pick")
        self.warningSubText.Show()
        
        self.Hide()
    
    def ShowAwakening(self, summonerName, supremoName, rank):
        """Mostra l'annuncio di risveglio Supremo"""
        self.currentRank = rank.upper() if rank else "E"
        colors = self.RANK_COLORS.get(self.currentRank, self.RANK_COLORS["E"])
        
        # Aggiorna testi
        self.supremoNameText.SetText("【 %s 】" % supremoName.replace("+", " "))
        self.supremoNameText.SetPackedFontColor(colors["title"])
        
        self.rankText.SetText("Grado: %s" % self.currentRank)
        self.rankText.SetPackedFontColor(colors["title"])
        
        self.summonerText.SetText("Evocato da: %s" % summonerName.replace("+", " "))
        
        # Aggiorna colori bordi
        for b in self.borders:
            b.SetColor(colors["border"])
        
        # Mostra per 6 secondi
        self.endTime = app.GetTime() + 6.0
        self.pulsePhase = 0.0
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.endTime > 0:
            now = app.GetTime()
            if now >= self.endTime:
                self.Hide()
                self.endTime = 0
            else:
                # Effetto pulse
                self.pulsePhase += 0.12
                colors = self.RANK_COLORS.get(self.currentRank, self.RANK_COLORS["E"])
                
                pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
                alpha = int(200 + 55 * pulse)
                borderColor = (alpha << 24) | (colors["border"] & 0x00FFFFFF)
                for b in self.borders:
                    b.SetColor(borderColor)
    
    def OnPressEscapeKey(self):
        return True  # Blocca chiusura con ESC


# ═══════════════════════════════════════════════════════════════════════════════
#  SUPREMO SYSTEM - CHALLENGE WINDOW
#  UI dedicata per la sfida Supremo con timer, distanza e stato
# ═══════════════════════════════════════════════════════════════════════════════
class SupremoChallengeWindow(ui.Window, DraggableMixin):
    """Finestra sfida Supremo - visibile solo ai partecipanti"""
    
    RANK_COLORS = {
        "E": {"border": 0xFF808080, "progress": 0xFF606060},
        "D": {"border": 0xFF00AA00, "progress": 0xFF008800},
        "C": {"border": 0xFF0088FF, "progress": 0xFF0066CC},
        "B": {"border": 0xFFAA00AA, "progress": 0xFF880088},
        "A": {"border": 0xFFFF6600, "progress": 0xFFCC5500},
        "S": {"border": 0xFFFF0000, "progress": 0xFFCC0000},
        "SS": {"border": 0xFFFFD700, "progress": 0xFFCCAA00},
        "SSS": {"border": 0xFFFF1493, "progress": 0xFFCC1177}
    }
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.winW = 380
        self.winH = 200
        self.SetSize(self.winW, self.winH)
        
        # Posizione default
        defaultX, defaultY = GetDefaultPosition("SupremoChallengeWindow", self.winW, self.winH)
        self.InitDraggable("SupremoChallengeWindow", defaultX, defaultY)
        
        self.endTime = 0
        self.totalDuration = 0
        self.maxDistance = 0
        self.currentDistance = 0
        self.reward = 0
        self.penalty = 0
        self.currentRank = "E"
        self.pulsePhase = 0.0
        self.status = "FIGHTING"
        
        # Background
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(self.winW, self.winH)
        self.bgOuter.SetColor(0xEE0A0A14)
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()
        
        # Inner glow
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(3, 3)
        self.glowInner.SetSize(self.winW - 6, self.winH - 6)
        self.glowInner.SetColor(0x22FFFFFF)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()
        
        # Inner background
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 5)
        self.bgInner.SetSize(self.winW - 10, self.winH - 10)
        self.bgInner.SetColor(0xDD080812)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()
        
        # Bordi
        self.borders = []
        for y in [0, self.winH - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(self.winW, 2); b.SetColor(0xFFFF4444); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, self.winW - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, self.winH); b.SetColor(0xFFFF4444); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        
        # Header
        self.headerText = ui.TextLine()
        self.headerText.SetParent(self)
        self.headerText.SetPosition(self.winW // 2, 10)
        self.headerText.SetHorizontalAlignCenter()
        self.headerText.SetText("⚔ SFIDA SUPREMO ⚔")
        self.headerText.SetPackedFontColor(0xFFFF4444)
        self.headerText.SetOutline()
        self.headerText.AddFlag("not_pick")
        self.headerText.Show()
        
        # Nome Supremo
        self.supremoName = ui.TextLine()
        self.supremoName.SetParent(self)
        self.supremoName.SetPosition(self.winW // 2, 30)
        self.supremoName.SetHorizontalAlignCenter()
        self.supremoName.SetText("")
        self.supremoName.SetPackedFontColor(0xFFFFFFFF)
        self.supremoName.SetOutline()
        self.supremoName.AddFlag("not_pick")
        self.supremoName.Show()
        
        # Linea separatore
        self.sep1 = ui.Bar()
        self.sep1.SetParent(self)
        self.sep1.SetPosition(10, 50)
        self.sep1.SetSize(self.winW - 20, 1)
        self.sep1.SetColor(0x66FFFFFF)
        self.sep1.AddFlag("not_pick")
        self.sep1.Show()
        
        # Timer Section
        self.timerLabel = ui.TextLine()
        self.timerLabel.SetParent(self)
        self.timerLabel.SetPosition(20, 58)
        self.timerLabel.SetText("TEMPO RIMANENTE:")
        self.timerLabel.SetPackedFontColor(0xFFCCCCCC)
        self.timerLabel.AddFlag("not_pick")
        self.timerLabel.Show()
        
        self.timerValue = ui.TextLine()
        self.timerValue.SetParent(self)
        self.timerValue.SetPosition(self.winW - 20, 58)
        self.timerValue.SetHorizontalAlignRight()
        self.timerValue.SetText("00:00")
        self.timerValue.SetPackedFontColor(0xFFFFD700)
        self.timerValue.SetOutline()
        self.timerValue.AddFlag("not_pick")
        self.timerValue.Show()
        
        # Timer Progress Bar
        self.timerBarBg = ui.Bar()
        self.timerBarBg.SetParent(self)
        self.timerBarBg.SetPosition(15, 78)
        self.timerBarBg.SetSize(self.winW - 30, 12)
        self.timerBarBg.SetColor(0xFF1A1A2E)
        self.timerBarBg.AddFlag("not_pick")
        self.timerBarBg.Show()
        
        self.timerBarFill = ui.Bar()
        self.timerBarFill.SetParent(self)
        self.timerBarFill.SetPosition(15, 78)
        self.timerBarFill.SetSize(self.winW - 30, 12)
        self.timerBarFill.SetColor(0xFF00CCFF)
        self.timerBarFill.AddFlag("not_pick")
        self.timerBarFill.Show()
        
        # Distance Section
        self.distLabel = ui.TextLine()
        self.distLabel.SetParent(self)
        self.distLabel.SetPosition(20, 98)
        self.distLabel.SetText("DISTANZA DAL SUPREMO:")
        self.distLabel.SetPackedFontColor(0xFFCCCCCC)
        self.distLabel.AddFlag("not_pick")
        self.distLabel.Show()
        
        self.distValue = ui.TextLine()
        self.distValue.SetParent(self)
        self.distValue.SetPosition(self.winW - 20, 98)
        self.distValue.SetHorizontalAlignRight()
        self.distValue.SetText("0m")
        self.distValue.SetPackedFontColor(0xFF00FF00)
        self.distValue.SetOutline()
        self.distValue.AddFlag("not_pick")
        self.distValue.Show()
        
        # Distance Progress Bar
        self.distBarBg = ui.Bar()
        self.distBarBg.SetParent(self)
        self.distBarBg.SetPosition(15, 118)
        self.distBarBg.SetSize(self.winW - 30, 12)
        self.distBarBg.SetColor(0xFF1A1A2E)
        self.distBarBg.AddFlag("not_pick")
        self.distBarBg.Show()
        
        self.distBarFill = ui.Bar()
        self.distBarFill.SetParent(self)
        self.distBarFill.SetPosition(15, 118)
        self.distBarFill.SetSize(0, 12)
        self.distBarFill.SetColor(0xFF00AA00)
        self.distBarFill.AddFlag("not_pick")
        self.distBarFill.Show()
        
        # Linea separatore
        self.sep2 = ui.Bar()
        self.sep2.SetParent(self)
        self.sep2.SetPosition(10, 138)
        self.sep2.SetSize(self.winW - 20, 1)
        self.sep2.SetColor(0x66FFFFFF)
        self.sep2.AddFlag("not_pick")
        self.sep2.Show()
        
        # Reward/Penalty Section
        self.rewardLabel = ui.TextLine()
        self.rewardLabel.SetParent(self)
        self.rewardLabel.SetPosition(20, 145)
        self.rewardLabel.SetText("Ricompensa:")
        self.rewardLabel.SetPackedFontColor(0xFFAAFFAA)
        self.rewardLabel.AddFlag("not_pick")
        self.rewardLabel.Show()
        
        self.rewardValue = ui.TextLine()
        self.rewardValue.SetParent(self)
        self.rewardValue.SetPosition(100, 145)
        self.rewardValue.SetText("+0 Gloria")
        self.rewardValue.SetPackedFontColor(0xFF00FF00)
        self.rewardValue.AddFlag("not_pick")
        self.rewardValue.Show()
        
        self.penaltyLabel = ui.TextLine()
        self.penaltyLabel.SetParent(self)
        self.penaltyLabel.SetPosition(self.winW // 2 + 10, 145)
        self.penaltyLabel.SetText("Penalita':")
        self.penaltyLabel.SetPackedFontColor(0xFFFFAAAA)
        self.penaltyLabel.AddFlag("not_pick")
        self.penaltyLabel.Show()
        
        self.penaltyValue = ui.TextLine()
        self.penaltyValue.SetParent(self)
        self.penaltyValue.SetPosition(self.winW // 2 + 75, 145)
        self.penaltyValue.SetText("-0 Gloria")
        self.penaltyValue.SetPackedFontColor(0xFFFF4444)
        self.penaltyValue.AddFlag("not_pick")
        self.penaltyValue.Show()
        
        # Status Text
        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(self.winW // 2, 170)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("⚔ COMBATTI! ⚔")
        self.statusText.SetPackedFontColor(0xFFFFD700)
        self.statusText.SetOutline()
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()
        
        # Warning Text (nascosto inizialmente)
        self.warningText = ui.TextLine()
        self.warningText.SetParent(self)
        self.warningText.SetPosition(self.winW // 2, 185)
        self.warningText.SetHorizontalAlignCenter()
        self.warningText.SetText("")
        self.warningText.SetPackedFontColor(0xFFFF0000)
        self.warningText.SetOutline()
        self.warningText.AddFlag("not_pick")
        self.warningText.Hide()
        
        self.Hide()
    
    def StartChallenge(self, summonerName, supremoName, vnum, rank, duration, reward, penalty, spawnX, spawnY, maxDistance):
        """Avvia la sfida Supremo"""
        self.currentRank = rank.upper() if rank else "E"
        self.totalDuration = duration
        self.maxDistance = maxDistance
        self.reward = reward
        self.penalty = penalty
        
        colors = self.RANK_COLORS.get(self.currentRank, self.RANK_COLORS["E"])
        
        # Aggiorna testi
        self.supremoName.SetText("【 %s 】" % supremoName.replace("+", " "))
        self.rewardValue.SetText("+%d Gloria" % reward)
        self.penaltyValue.SetText("-%d Gloria" % penalty)
        
        # Aggiorna colori
        for b in self.borders:
            b.SetColor(colors["border"])
        self.timerBarFill.SetColor(colors["progress"])
        
        # Timer
        self.endTime = app.GetTime() + duration
        
        # Reset stato
        self.status = "FIGHTING"
        self.statusText.SetText("⚔ COMBATTI! ⚔")
        self.statusText.SetPackedFontColor(0xFFFFD700)
        self.warningText.Hide()
        
        self.Show()
        self.SetTop()
    
    def UpdateChallenge(self, timeLeft, distance, status):
        """Aggiorna UI con tempo e distanza"""
        self.currentDistance = distance
        self.status = status
        
        # Timer
        mins = timeLeft // 60
        secs = timeLeft % 60
        self.timerValue.SetText("%02d:%02d" % (mins, secs))
        
        # Timer bar
        if self.totalDuration > 0:
            progress = float(timeLeft) / float(self.totalDuration)
            fillWidth = int(progress * (self.winW - 30))
            self.timerBarFill.SetSize(max(1, fillWidth), 12)
        
        # Distanza
        self.distValue.SetText("%dm / %dm" % (distance, self.maxDistance))
        
        # Distance bar (inverso - piu' lontano = piu' piena = piu' rosso)
        if self.maxDistance > 0:
            distProgress = min(1.0, float(distance) / float(self.maxDistance))
            fillWidth = int(distProgress * (self.winW - 30))
            self.distBarFill.SetSize(fillWidth, 12)
            
            # Colore distanza
            if distProgress < 0.5:
                self.distBarFill.SetColor(0xFF00AA00)  # Verde
                self.distValue.SetPackedFontColor(0xFF00FF00)
            elif distProgress < 0.75:
                self.distBarFill.SetColor(0xFFFFAA00)  # Giallo
                self.distValue.SetPackedFontColor(0xFFFFD700)
            else:
                self.distBarFill.SetColor(0xFFFF0000)  # Rosso
                self.distValue.SetPackedFontColor(0xFFFF0000)
        
        # Status
        if status == "WARNING":
            self.statusText.SetText("⚠ TROPPO LONTANO! ⚠")
            self.statusText.SetPackedFontColor(0xFFFF0000)
            self.warningText.SetText("Torna vicino al Supremo!")
            self.warningText.Show()
        else:
            self.statusText.SetText("⚔ COMBATTI! ⚔")
            self.statusText.SetPackedFontColor(0xFFFFD700)
            self.warningText.Hide()
    
    def EndChallenge(self, result, gloriaChange, message):
        """Termina la sfida con risultato"""
        self.endTime = app.GetTime() + 4.0  # Mostra risultato per 4 secondi
        
        if result == "SUCCESS":
            self.headerText.SetText("⭐ VITTORIA! ⭐")
            self.headerText.SetPackedFontColor(0xFF00FF00)
            self.statusText.SetText("+%d Gloria!" % gloriaChange)
            self.statusText.SetPackedFontColor(0xFF00FF00)
            for b in self.borders:
                b.SetColor(0xFF00FF00)
        elif result == "STOLEN":
            self.headerText.SetText("💀 RUBATO! 💀")
            self.headerText.SetPackedFontColor(0xFFFF6600)
            self.statusText.SetText("-%d Gloria (rubato)" % abs(gloriaChange))
            self.statusText.SetPackedFontColor(0xFFFF6600)
            for b in self.borders:
                b.SetColor(0xFFFF6600)
        elif result == "TIMEOUT":
            self.headerText.SetText("⏰ TEMPO SCADUTO ⏰")
            self.headerText.SetPackedFontColor(0xFFFF0000)
            self.statusText.SetText("-%d Gloria!" % abs(gloriaChange))
            self.statusText.SetPackedFontColor(0xFFFF0000)
            for b in self.borders:
                b.SetColor(0xFFFF0000)
        elif result == "ABANDON":
            self.headerText.SetText("🚫 ABBANDONATO 🚫")
            self.headerText.SetPackedFontColor(0xFFFF0000)
            self.statusText.SetText("-%d Gloria (troppo lontano)" % abs(gloriaChange))
            self.statusText.SetPackedFontColor(0xFFFF0000)
            for b in self.borders:
                b.SetColor(0xFFFF0000)
        
        self.warningText.SetText(message.replace("+", " "))
        self.warningText.Show()
    
    def OnUpdate(self):
        if self.endTime > 0:
            now = app.GetTime()
            if now >= self.endTime:
                self.Hide()
                self.endTime = 0
            else:
                # Effetto pulse
                self.pulsePhase += 0.1
                colors = self.RANK_COLORS.get(self.currentRank, self.RANK_COLORS["E"])
                
                pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
                alpha = int(200 + 55 * pulse)
                borderColor = (alpha << 24) | (colors["border"] & 0x00FFFFFF)
                
                # Pulse piu' intenso se in pericolo
                if self.status == "WARNING":
                    borderColor = (alpha << 24) | 0x00FF0000
                
                for b in self.borders:
                    b.SetColor(borderColor)
    
    def OnPressEscapeKey(self):
        return True  # Blocca chiusura con ESC


# ═══════════════════════════════════════════════════════════════════════════════
#  SUPREMO SYSTEM - VICTORY WINDOW
#  Effetto vittoria epico dopo aver sconfitto un Supremo
# ═══════════════════════════════════════════════════════════════════════════════
class SupremoVictoryWindow(ui.Window):
    """Finestra effetto vittoria Supremo - epica e celebrativa"""
    
    RANK_COLORS = {
        "E": 0xFF808080, "D": 0xFF00AA00, "C": 0xFF0088FF, "B": 0xFFAA00AA,
        "A": 0xFFFF6600, "S": 0xFFFF0000, "SS": 0xFFFFD700, "SSS": 0xFFFF1493
    }
    
    def __init__(self):
        ui.Window.__init__(self)
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        
        self.winW = 450
        self.winH = 200
        self.SetSize(self.winW, self.winH)
        self.SetPosition((screenW - self.winW) // 2, int(screenH * 0.25))
        
        self.endTime = 0
        self.pulsePhase = 0.0
        self.borderColor = 0xFFFFD700
        
        # Background con effetto glow
        self.bgOuter = ui.Bar()
        self.bgOuter.SetParent(self)
        self.bgOuter.SetPosition(0, 0)
        self.bgOuter.SetSize(self.winW, self.winH)
        self.bgOuter.SetColor(0xEE0A140A)  # Verde scuro
        self.bgOuter.AddFlag("not_pick")
        self.bgOuter.Show()
        
        # Inner glow dorato
        self.glowInner = ui.Bar()
        self.glowInner.SetParent(self)
        self.glowInner.SetPosition(3, 3)
        self.glowInner.SetSize(self.winW - 6, self.winH - 6)
        self.glowInner.SetColor(0x33FFD700)
        self.glowInner.AddFlag("not_pick")
        self.glowInner.Show()
        
        # Inner background
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 5)
        self.bgInner.SetSize(self.winW - 10, self.winH - 10)
        self.bgInner.SetColor(0xDD081208)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()
        
        # Bordi dorati
        self.borders = []
        for y in [0, self.winH - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(0, y); b.SetSize(self.winW, 2); b.SetColor(0xFFFFD700); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        for x in [0, self.winW - 2]:
            b = ui.Bar(); b.SetParent(self); b.SetPosition(x, 0); b.SetSize(2, self.winH); b.SetColor(0xFFFFD700); b.AddFlag("not_pick"); b.Show()
            self.borders.append(b)
        
        # Titolo VITTORIA
        self.victoryTitle = ui.TextLine()
        self.victoryTitle.SetParent(self)
        self.victoryTitle.SetPosition(self.winW // 2, 20)
        self.victoryTitle.SetHorizontalAlignCenter()
        self.victoryTitle.SetText("⭐ SUPREMO SCONFITTO! ⭐")
        self.victoryTitle.SetPackedFontColor(0xFFFFD700)
        self.victoryTitle.SetOutline()
        self.victoryTitle.AddFlag("not_pick")
        self.victoryTitle.Show()
        
        # Nome Supremo
        self.supremoName = ui.TextLine()
        self.supremoName.SetParent(self)
        self.supremoName.SetPosition(self.winW // 2, 50)
        self.supremoName.SetHorizontalAlignCenter()
        self.supremoName.SetText("")
        self.supremoName.SetPackedFontColor(0xFFFFFFFF)
        self.supremoName.SetOutline()
        self.supremoName.AddFlag("not_pick")
        self.supremoName.Show()
        
        # Grado
        self.rankText = ui.TextLine()
        self.rankText.SetParent(self)
        self.rankText.SetPosition(self.winW // 2, 75)
        self.rankText.SetHorizontalAlignCenter()
        self.rankText.SetText("")
        self.rankText.SetPackedFontColor(0xFFFFD700)
        self.rankText.SetOutline()
        self.rankText.AddFlag("not_pick")
        self.rankText.Show()
        
        # Linea separatore
        self.separator = ui.Bar()
        self.separator.SetParent(self)
        self.separator.SetPosition(50, 105)
        self.separator.SetSize(self.winW - 100, 1)
        self.separator.SetColor(0x66FFD700)
        self.separator.AddFlag("not_pick")
        self.separator.Show()
        
        # Ricompensa Gloria
        self.rewardLabel = ui.TextLine()
        self.rewardLabel.SetParent(self)
        self.rewardLabel.SetPosition(self.winW // 2, 120)
        self.rewardLabel.SetHorizontalAlignCenter()
        self.rewardLabel.SetText("GLORIA GUADAGNATA:")
        self.rewardLabel.SetPackedFontColor(0xFFCCCCCC)
        self.rewardLabel.AddFlag("not_pick")
        self.rewardLabel.Show()
        
        self.rewardValue = ui.TextLine()
        self.rewardValue.SetParent(self)
        self.rewardValue.SetPosition(self.winW // 2, 145)
        self.rewardValue.SetHorizontalAlignCenter()
        self.rewardValue.SetText("+0")
        self.rewardValue.SetPackedFontColor(0xFF00FF00)
        self.rewardValue.SetOutline()
        self.rewardValue.AddFlag("not_pick")
        self.rewardValue.Show()
        
        # Messaggio motivazionale
        self.motivationText = ui.TextLine()
        self.motivationText.SetParent(self)
        self.motivationText.SetPosition(self.winW // 2, 175)
        self.motivationText.SetHorizontalAlignCenter()
        self.motivationText.SetText("Sei diventato piu' forte!")
        self.motivationText.SetPackedFontColor(0xFFAAFFAA)
        self.motivationText.AddFlag("not_pick")
        self.motivationText.Show()
        
        self.Hide()
    
    def ShowVictory(self, supremoName, rank, gloriaReward):
        """Mostra effetto vittoria"""
        self.borderColor = self.RANK_COLORS.get(rank.upper(), 0xFFFFD700)
        
        self.supremoName.SetText("【 %s 】" % supremoName.replace("+", " "))
        self.rankText.SetText("Grado: %s" % rank.upper())
        self.rankText.SetPackedFontColor(self.borderColor)
        self.rewardValue.SetText("+%d Gloria" % gloriaReward)
        
        # Messaggi motivazionali basati su rank
        messages = {
            "E": "Un buon inizio!",
            "D": "La tua forza cresce!",
            "C": "Degno di un vero Cacciatore!",
            "B": "Il tuo potere e' impressionante!",
            "A": "Sei tra i migliori!",
            "S": "Leggendario!",
            "SS": "Hai raggiunto l'impossibile!",
            "SSS": "SEI IL MONARCA!"
        }
        self.motivationText.SetText(messages.get(rank.upper(), "Vittoria!"))
        
        # Aggiorna colori
        for b in self.borders:
            b.SetColor(self.borderColor)
        self.glowInner.SetColor((0x33 << 24) | (self.borderColor & 0x00FFFFFF))
        
        self.endTime = app.GetTime() + 5.0
        self.pulsePhase = 0.0
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if self.endTime > 0:
            now = app.GetTime()
            if now >= self.endTime:
                self.Hide()
                self.endTime = 0
            else:
                # Effetto pulse dorato
                self.pulsePhase += 0.15
                pulse = (math.sin(self.pulsePhase) + 1.0) / 2.0
                alpha = int(200 + 55 * pulse)
                borderColor = (alpha << 24) | (self.borderColor & 0x00FFFFFF)
                for b in self.borders:
                    b.SetColor(borderColor)
    
    def OnPressEscapeKey(self):
        return True  # Blocca chiusura con ESC


# ═══════════════════════════════════════════════════════════════════════════════
#  GLORY DETAIL WINDOW - Pannello dettaglio Gloria (sostituisce syschat)
#  Appare a sinistra, auto-size, mostra tutti i bonus/malus.
#  Visibile a killer, party, e partecipanti (ognuno vede il proprio dettaglio).
# ═══════════════════════════════════════════════════════════════════════════════

GLORY_CONTEXT_COLORS = {
    "KILLER":          {"border": 0xFFFFD700, "header_bg": 0xCC332200, "label": "DETTAGLIO GLORIA"},
    "PARTY":           {"border": 0xFF00FFFF, "header_bg": 0xCC002233, "label": "GLORIA PARTY"},
    "PARTECIPAZIONE":  {"border": 0xFF00FF00, "header_bg": 0xCC003300, "label": "PARTECIPAZIONE"},
    "BAULE":           {"border": 0xFFFFAA00, "header_bg": 0xCC332200, "label": "BAULE APERTO"},
}

GLORY_TYPE_ICONS = {
    "BOSS":        "|cffFF6600BOSS|r",
    "SUPER_METIN": "|cff00FFFFSM|r",
    "BAULE":       "|cffFFD700BAULE|r",
    "ELITE":       "|cffFFAAAAELITE|r",
    "FRATTURA":    "|cffAA00FFFRATTURA|r",
}


class GloryDetailWindow(ui.Window, DraggableMixin):
    """Pannello dettaglio Gloria. Si auto-dimensiona in base ai modificatori.
       Appare a sinistra dello schermo, fade-out automatico dopo ~8 secondi.
       Coda messaggi: se arriva un nuovo dettaglio mentre uno e' visibile,
       viene accodato e mostrato subito dopo."""

    PANEL_WIDTH = 300
    HEADER_H = 36
    LINE_H = 16
    FOOTER_H = 28
    PADDING = 8
    DISPLAY_TIME = 8.0   # secondi visibilita'
    FADE_TIME = 1.5      # secondi fade-out

    def __init__(self):
        ui.Window.__init__(self)
        self.SetSize(self.PANEL_WIDTH, 200)
        # Default: centro schermo
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        defX = (screenW - self.PANEL_WIDTH) // 2
        defY = (screenH - 200) // 2
        self.InitDraggable("GloryDetail", defX, defY)
        self.AddFlag("float")

        self.queue = []
        self.endTime = 0
        self.fadeStart = 0
        self.activeFadeTime = self.FADE_TIME
        self.isShowing = False

        # --- Sfondo principale ---
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.PANEL_WIDTH, 200)
        self.bg.SetColor(0xDD0A0A14)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # --- Header sfondo ---
        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(0, 0)
        self.headerBg.SetSize(self.PANEL_WIDTH, self.HEADER_H)
        self.headerBg.SetColor(0xCC332200)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        # --- Bordi (top, bottom, left, right) ---
        self.borders = []
        for i in range(4):
            b = ui.Bar()
            b.SetParent(self)
            b.SetColor(0xFFFFD700)
            b.AddFlag("not_pick")
            b.Show()
            self.borders.append(b)

        # --- Testo header (context label) ---
        self.headerLabel = ui.TextLine()
        self.headerLabel.SetParent(self)
        self.headerLabel.SetPosition(self.PADDING, 3)
        self.headerLabel.SetPackedFontColor(0xFFFFD700)
        self.headerLabel.SetOutline()
        self.headerLabel.AddFlag("not_pick")
        self.headerLabel.Show()

        # --- Testo source (tipo + nome mob) ---
        self.sourceText = ui.TextLine()
        self.sourceText.SetParent(self)
        self.sourceText.SetPosition(self.PADDING, 19)
        self.sourceText.SetPackedFontColor(0xFFCCCCCC)
        self.sourceText.AddFlag("not_pick")
        self.sourceText.Show()

        # --- Separatore header ---
        self.headerSep = ui.Bar()
        self.headerSep.SetParent(self)
        self.headerSep.SetPosition(4, self.HEADER_H - 1)
        self.headerSep.SetSize(self.PANEL_WIDTH - 8, 1)
        self.headerSep.SetColor(0x66FFFFFF)
        self.headerSep.AddFlag("not_pick")
        self.headerSep.Show()

        # --- Pool di linee per base + modificatori (pre-allocate 15) ---
        self.lineLabels = []
        self.lineValues = []
        for i in range(15):
            lbl = ui.TextLine()
            lbl.SetParent(self)
            lbl.SetPosition(self.PADDING + 4, 0)
            lbl.SetPackedFontColor(0xFFAAAAAA)
            lbl.AddFlag("not_pick")
            lbl.Show()
            self.lineLabels.append(lbl)

            val = ui.TextLine()
            val.SetParent(self)
            val.SetPosition(self.PANEL_WIDTH - self.PADDING - 4, 0)
            val.SetHorizontalAlignRight()
            val.SetPackedFontColor(0xFF00FF00)
            val.AddFlag("not_pick")
            val.Show()
            self.lineValues.append(val)

        # --- Separatore footer ---
        self.footerSep = ui.Bar()
        self.footerSep.SetParent(self)
        self.footerSep.SetPosition(4, 0)
        self.footerSep.SetSize(self.PANEL_WIDTH - 8, 1)
        self.footerSep.SetColor(0x66FFFFFF)
        self.footerSep.AddFlag("not_pick")
        self.footerSep.Show()

        # --- Totale (grande, evidenziato) ---
        self.totalLabel = ui.TextLine()
        self.totalLabel.SetParent(self)
        self.totalLabel.SetPosition(self.PADDING + 4, 0)
        self.totalLabel.SetPackedFontColor(0xFFFFFFFF)
        self.totalLabel.SetOutline()
        self.totalLabel.AddFlag("not_pick")
        self.totalLabel.Show()

        self.totalValue = ui.TextLine()
        self.totalValue.SetParent(self)
        self.totalValue.SetPosition(self.PANEL_WIDTH - self.PADDING - 4, 0)
        self.totalValue.SetHorizontalAlignRight()
        self.totalValue.SetPackedFontColor(0xFFFFD700)
        self.totalValue.SetOutline()
        self.totalValue.AddFlag("not_pick")
        self.totalValue.Show()

        self.Hide()

    def ShowDetail(self, context, sourceType, sourceName, baseGlory, modifiers, finalGlory):
        """Mostra (o accoda) un dettaglio Gloria.
           context:    KILLER | PARTY | PARTECIPAZIONE | BAULE
           sourceType: BOSS | SUPER_METIN | BAULE | ELITE | FRATTURA
           sourceName: nome del mob/baule
           baseGlory:  punti base
           modifiers:  lista di tuple (name, valueStr, addInt)
           finalGlory: totale finale
        """
        entry = (context, sourceType, sourceName, baseGlory, modifiers, finalGlory)
        if self.isShowing:
            # Anti-leak: max 12 in coda (party frattura con 5 membri puo' generare molti msg)
            if len(self.queue) < 12:
                self.queue.append(entry)
            return
        self._RenderDetail(entry)

    def _RenderDetail(self, entry):
        context, sourceType, sourceName, baseGlory, modifiers, finalGlory = entry

        # --- Colori da context ---
        ctx = GLORY_CONTEXT_COLORS.get(context, GLORY_CONTEXT_COLORS["KILLER"])
        borderColor = ctx["border"]
        headerBgColor = ctx["header_bg"]
        headerText = ctx["label"]

        for b in self.borders:
            b.SetColor(borderColor)
        self.headerBg.SetColor(headerBgColor)
        self.headerLabel.SetPackedFontColor(borderColor)
        self.headerLabel.SetText(headerText)

        # Source text
        typeTag = sourceType
        self.sourceText.SetText(typeTag + " - " + sourceName)

        # --- Calcola righe (base + mods) ---
        numLines = 1 + len(modifiers)  # 1 per base
        if numLines > 15:
            numLines = 15

        yOff = self.HEADER_H + 4

        # Base Gloria (riga 0)
        self.lineLabels[0].SetPosition(self.PADDING + 4, yOff)
        self.lineLabels[0].SetText("Gloria Base")
        self.lineLabels[0].SetPackedFontColor(0xFFCCCCCC)
        self.lineValues[0].SetPosition(self.PANEL_WIDTH - self.PADDING - 4, yOff)
        self.lineValues[0].SetText(str(baseGlory))
        self.lineValues[0].SetPackedFontColor(0xFFFFFFFF)
        yOff += self.LINE_H

        # Modifier lines
        for idx in range(len(modifiers)):
            if idx + 1 >= 15:
                break
            name, valueStr, addVal = modifiers[idx]
            lineIdx = idx + 1
            self.lineLabels[lineIdx].SetPosition(self.PADDING + 4, yOff)
            self.lineLabels[lineIdx].SetText(name + " (" + valueStr + ")")

            self.lineValues[lineIdx].SetPosition(self.PANEL_WIDTH - self.PADDING - 4, yOff)
            addInt = int(addVal)
            if addInt >= 0:
                self.lineValues[lineIdx].SetText("+" + str(addInt))
                self.lineValues[lineIdx].SetPackedFontColor(0xFF00FF00)
                self.lineLabels[lineIdx].SetPackedFontColor(0xFF88CC88)
            else:
                self.lineValues[lineIdx].SetText(str(addInt))
                self.lineValues[lineIdx].SetPackedFontColor(0xFFFF4444)
                self.lineLabels[lineIdx].SetPackedFontColor(0xFFCC8888)
            yOff += self.LINE_H

        # Nascondi linee inutilizzate
        usedLines = min(numLines, 15)
        for i in range(usedLines, 15):
            self.lineLabels[i].SetText("")
            self.lineValues[i].SetText("")

        # Separatore footer
        yOff += 3
        self.footerSep.SetPosition(4, yOff)
        yOff += 4

        # TOTALE
        self.totalLabel.SetPosition(self.PADDING + 4, yOff)
        self.totalLabel.SetText("TOTALE")
        self.totalLabel.SetPackedFontColor(0xFFFFFFFF)
        self.totalValue.SetPosition(self.PANEL_WIDTH - self.PADDING - 4, yOff)
        self.totalValue.SetText("+" + str(finalGlory) + " Gloria")
        self.totalValue.SetPackedFontColor(borderColor)
        yOff += self.LINE_H + self.PADDING

        # --- Auto-size ---
        totalH = yOff
        self.SetSize(self.PANEL_WIDTH, totalH)
        self.bg.SetSize(self.PANEL_WIDTH, totalH)
        self.headerBg.SetSize(self.PANEL_WIDTH, self.HEADER_H)

        # Bordi
        self.borders[0].SetPosition(0, 0)
        self.borders[0].SetSize(self.PANEL_WIDTH, 2)      # top
        self.borders[1].SetPosition(0, totalH - 2)
        self.borders[1].SetSize(self.PANEL_WIDTH, 2)      # bottom
        self.borders[2].SetPosition(0, 0)
        self.borders[2].SetSize(2, totalH)                 # left
        self.borders[3].SetPosition(self.PANEL_WIDTH - 2, 0)
        self.borders[3].SetSize(2, totalH)                 # right

        # Posizione: centro schermo (o salvata se spostata manualmente)
        screenW = wndMgr.GetScreenWidth()
        screenH = wndMgr.GetScreenHeight()
        defX = (screenW - self.PANEL_WIDTH) // 2
        defY = (screenH - totalH) // 2
        if HasSavedPosition("GloryDetail"):
            defX, defY = GetWindowPosition("GloryDetail", defX, defY)
        self.SetPosition(defX, defY)

        # Timer - durata dinamica: se la coda e' piena, velocizza per non
        # bloccare il player per 48+ secondi dopo 6 kill ravvicinati.
        # Coda vuota: 8s normale. Coda piena: min 2.5s (drain veloce).
        now = app.GetTime()
        qLen = len(self.queue)
        if qLen > 0:
            displayTime = max(2.5, self.DISPLAY_TIME - qLen * 1.5)
            fadeTime = min(0.8, displayTime * 0.3)
        else:
            displayTime = self.DISPLAY_TIME
            fadeTime = self.FADE_TIME
        self.endTime = now + displayTime
        self.fadeStart = now + displayTime - fadeTime
        self.activeFadeTime = fadeTime
        self.isShowing = True
        self.Show()
        self.SetTop()

    def OnUpdate(self):
        if not self.isShowing:
            return
        now = app.GetTime()
        if now >= self.endTime:
            self.Hide()
            self.isShowing = False
            self.endTime = 0
            # Mostra prossimo dalla coda
            if len(self.queue) > 0:
                nextEntry = self.queue.pop(0)
                self._RenderDetail(nextEntry)
            return
        # Fade-out effect negli ultimi secondi (durata dinamica)
        if now >= self.fadeStart:
            ft = self.activeFadeTime if self.activeFadeTime > 0 else self.FADE_TIME
            t = (now - self.fadeStart) / ft
            alpha = int(255 * (1.0 - t))
            if alpha < 30:
                alpha = 30
            bgAlpha = int(0xDD * (1.0 - t))
            if bgAlpha < 0x20:
                bgAlpha = 0x20
            self.bg.SetColor((bgAlpha << 24) | 0x0A0A14)

    def ClearQueue(self):
        self.queue = []
        self.Hide()
        self.isShowing = False
        self.endTime = 0

    def OnMouseRightButtonUp(self):
        """Click destro = salta al prossimo messaggio in coda (o chiudi).
           Utile durante fratture con kill ravvicinati per non restare bloccati."""
        if self.isShowing:
            self.Hide()
            self.isShowing = False
            self.endTime = 0
            if len(self.queue) > 0:
                nextEntry = self.queue.pop(0)
                self._RenderDetail(nextEntry)
        return True

    def OnPressEscapeKey(self):
        return True


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL INSTANCES
# ═══════════════════════════════════════════════════════════════════════════════
g_whatIfWindow = None
g_defenseWindow = None
g_systemMsgWindow = None
g_emergencyWindow = None
g_eventWindow = None
g_rivalWindow = None
g_overtakeWindow = None
g_speedKillWindow = None
g_hunterTipsWindow = None
g_hunterNotificationWindow = None
g_supremoAwakeningWindow = None
g_supremoChallengeWindow = None
g_supremoVictoryWindow = None
g_gloryDetailWindow = None

def GetWhatIfWindow():
    global g_whatIfWindow
    if g_whatIfWindow is None:
        g_whatIfWindow = WhatIfChoiceWindow()
    return g_whatIfWindow

def GetSystemMessageWindow():
    global g_systemMsgWindow
    if g_systemMsgWindow is None:
        g_systemMsgWindow = SystemMessageWindow()
    return g_systemMsgWindow

def GetEmergencyWindow():
    global g_emergencyWindow
    if g_emergencyWindow is None:
        g_emergencyWindow = EmergencyQuestWindow()
    return g_emergencyWindow

def GetEventWindow():
    global g_eventWindow
    if g_eventWindow is None:
        g_eventWindow = EventStatusWindow()
    return g_eventWindow

def GetRivalWindow():
    global g_rivalWindow
    if g_rivalWindow is None:
        g_rivalWindow = RivalTrackerWindow()
    return g_rivalWindow

def GetOvertakeWindow():
    global g_overtakeWindow
    if g_overtakeWindow is None:
        g_overtakeWindow = OvertakeWindow()
    return g_overtakeWindow

def GetDefenseWindow():
    global g_defenseWindow
    if g_defenseWindow is None:
        g_defenseWindow = FractureDefenseWindow()
    return g_defenseWindow

def GetSpeedKillWindow():
    global g_speedKillWindow
    if g_speedKillWindow is None:
        g_speedKillWindow = SpeedKillTimerWindow()
    return g_speedKillWindow

def GetHunterTipsWindow():
    global g_hunterTipsWindow
    if g_hunterTipsWindow is None:
        g_hunterTipsWindow = HunterTipsWindow()
    return g_hunterTipsWindow

def GetHunterNotificationWindow():
    global g_hunterNotificationWindow
    if g_hunterNotificationWindow is None:
        g_hunterNotificationWindow = HunterNotificationWindow()
    return g_hunterNotificationWindow


def GetSupremoAwakeningWindow():
    global g_supremoAwakeningWindow
    if g_supremoAwakeningWindow is None:
        g_supremoAwakeningWindow = SupremoAwakeningWindow()
    return g_supremoAwakeningWindow

def GetSupremoChallengeWindow():
    global g_supremoChallengeWindow
    if g_supremoChallengeWindow is None:
        g_supremoChallengeWindow = SupremoChallengeWindow()
    return g_supremoChallengeWindow

def GetSupremoVictoryWindow():
    global g_supremoVictoryWindow
    if g_supremoVictoryWindow is None:
        g_supremoVictoryWindow = SupremoVictoryWindow()
    return g_supremoVictoryWindow

def GetGloryDetailWindow():
    global g_gloryDetailWindow
    if g_gloryDetailWindow is None:
        g_gloryDetailWindow = GloryDetailWindow()
    return g_gloryDetailWindow


# Alias per compatibilità con hunter.py
GetWhatIfChoiceWindow = GetWhatIfWindow
GetEmergencyQuestWindow = GetEmergencyWindow
GetEventStatusWindow = GetEventWindow
GetRivalTrackerWindow = GetRivalWindow
GetFractureDefenseWindow = GetDefenseWindow
GetSpeedKillTimerWindow = GetSpeedKillWindow


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════
def OpenWhatIfChoice(qid, text, options, colorCode="PURPLE"):
    """Apre la finestra di scelta What-If"""
    GetWhatIfWindow().Create(qid, text, options, colorCode)

def ShowSystemMessage(msgType, arg1="", arg2="", arg3=""):
    """Mostra un messaggio di sistema"""
    GetSystemMessageWindow().ShowMessage(msgType, arg1, arg2, arg3)

def ShowEmergencyQuest(questName, duration):
    """Mostra notifica quest emergenza"""
    GetEmergencyWindow().ShowQuest(questName, duration)

def ShowEventStatus(eventName, timeLeft, reward):
    """Mostra stato evento"""
    GetEventWindow().ShowEvent(eventName, timeLeft, reward)

def ShowRivalTracker(rivalName, rivalGlory, myGlory, position):
    """Mostra tracker rivale"""
    GetRivalWindow().ShowRival(rivalName, rivalGlory, myGlory, position)

def ShowOvertake(overtakenName, newPosition):
    """Mostra notifica sorpasso"""
    GetOvertakeWindow().ShowOvertake(overtakenName, newPosition)


# ═══════════════════════════════════════════════════════════════════════════════
#  RESET ALL HUNTER WINDOWS - Chiamato su cambio mappa/logout/relog
# ═══════════════════════════════════════════════════════════════════════════════
def ResetAllHunterWindows():
    """Resetta e nasconde tutte le finestre Hunter al cambio mappa/logout/relog"""
    global g_defenseWindow, g_speedKillWindow, g_hunterTipsWindow, g_hunterNotificationWindow
    global g_emergencyWindow, g_whatIfWindow, g_systemMsgWindow
    global g_eventWindow, g_rivalWindow, g_overtakeWindow
    global g_supremoAwakeningWindow, g_supremoChallengeWindow, g_supremoVictoryWindow
    global g_gloryDetailWindow

    # Reset FractureDefenseWindow
    if g_defenseWindow is not None:
        try:
            g_defenseWindow.isActive = False
            g_defenseWindow.endTime = 0
            g_defenseWindow.Hide()
        except:
            pass

    # Reset SpeedKillTimerWindow
    if g_speedKillWindow is not None:
        try:
            g_speedKillWindow.isActive = False
            g_speedKillWindow.endTime = 0
            g_speedKillWindow.lastUpdateTime = 0
            g_speedKillWindow.Hide()
        except:
            pass

    # Reset HunterTipsWindow
    if g_hunterTipsWindow is not None:
        try:
            g_hunterTipsWindow.currentTip = ""
            g_hunterTipsWindow.startTime = 0
            g_hunterTipsWindow.Hide()
        except:
            pass

    # Reset HunterNotificationWindow
    if g_hunterNotificationWindow is not None:
        try:
            g_hunterNotificationWindow.notificationQueue = []
            g_hunterNotificationWindow.currentNotification = None
            g_hunterNotificationWindow.startTime = 0
            g_hunterNotificationWindow.Hide()
        except:
            pass

    # Reset EmergencyWindow
    if g_emergencyWindow is not None:
        try:
            g_emergencyWindow.Hide()
        except:
            pass

    # Reset altri windows
    if g_whatIfWindow is not None:
        try:
            g_whatIfWindow.Hide()
        except:
            pass

    if g_systemMsgWindow is not None:
        try:
            g_systemMsgWindow.Hide()
        except:
            pass

    if g_eventWindow is not None:
        try:
            g_eventWindow.Hide()
        except:
            pass

    if g_rivalWindow is not None:
        try:
            g_rivalWindow.Hide()
        except:
            pass

    if g_overtakeWindow is not None:
        try:
            g_overtakeWindow.Hide()
        except:
            pass

    # Reset Supremo Windows
    if g_supremoAwakeningWindow is not None:
        try:
            g_supremoAwakeningWindow.endTime = 0
            g_supremoAwakeningWindow.Hide()
        except:
            pass

    if g_supremoChallengeWindow is not None:
        try:
            g_supremoChallengeWindow.endTime = 0
            g_supremoChallengeWindow.Hide()
        except:
            pass

    if g_supremoVictoryWindow is not None:
        try:
            g_supremoVictoryWindow.endTime = 0
            g_supremoVictoryWindow.Hide()
        except:
            pass

    if g_gloryDetailWindow is not None:
        try:
            g_gloryDetailWindow.ClearQueue()
        except:
            pass
