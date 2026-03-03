# -*- coding: utf-8 -*-
# ============================================================
# HUNTER SYSTEM - RANK UP & SUPREMO UI v2.1 (Compatta)
# ============================================================

import ui
import wndMgr
import app
import math

# ============================================================
# COLORI PER RANK
# ============================================================
RANK_COLORS = {
    "E": 0xFF707070,
    "D": 0xFF00FF00,
    "C": 0xFF00FFFF,
    "B": 0xFF4499FF,
    "A": 0xFFCC44FF,
    "S": 0xFFFFAA00,
    "N": 0xFFFF2222,
}

COLOR_CODES = {
    "GREEN": 0xFF00FF00,
    "BLUE": 0xFF0099FF,
    "CYAN": 0xFF00FFFF,
    "ORANGE": 0xFFFF6600,
    "RED": 0xFFFF0000,
    "GOLD": 0xFFFFD700,
    "PURPLE": 0xFF9900FF,
    "WHITE": 0xFFFFFFFF,
    "GRAY": 0xFF808080,
}

def GetRankColor(rank):
    return RANK_COLORS.get(rank, 0xFFFFFFFF)

def GetColorCode(code):
    return COLOR_CODES.get(code, RANK_COLORS.get(code, 0xFFFFFFFF))


# ============================================================
# MEMORIA POSIZIONI FINESTRE
# ============================================================
_WINDOW_POSITIONS = {}

def SaveWindowPosition(name, x, y):
    _WINDOW_POSITIONS[name] = (x, y)

def GetWindowPosition(name, defaultX, defaultY):
    return _WINDOW_POSITIONS.get(name, (defaultX, defaultY))


# ============================================================
# BARRA DI PROGRESSO COMPATTA
# ============================================================
class ProgressBar(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.width = 150
        self.height = 14
        self.progress = 0.0
        self.targetProgress = 0.0
        self.color = 0xFF00FF00
        self.current = 0
        self.maximum = 0
        self.showText = True
        self.__BuildUI()
    
    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.width, self.height)
        self.bg.SetColor(0xFF1a1a1a)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        self.fill = ui.Bar()
        self.fill.SetParent(self)
        self.fill.SetPosition(1, 1)
        self.fill.SetSize(0, self.height - 2)
        self.fill.SetColor(self.color)
        self.fill.AddFlag("not_pick")
        self.fill.Show()
        
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(self.width // 2, 0)
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("")
        self.text.SetPackedFontColor(0xFFFFFFFF)
        self.text.SetOutline()
        self.text.Show()
    
    def SetSize(self, w, h):
        ui.Window.SetSize(self, w, h)
        self.width = w
        self.height = h
        self.bg.SetSize(w, h)
        self.text.SetPosition(w // 2, 0)
        self.__UpdateFill()
    
    def SetProgress(self, current, maximum):
        self.current = current
        self.maximum = maximum
        if maximum > 0:
            self.targetProgress = min(1.0, float(current) / float(maximum))
        else:
            self.targetProgress = 0.0
        if self.showText:
            self.text.SetText(str(int(current)) + "/" + str(int(maximum)))
        if current >= maximum and maximum > 0:
            self.fill.SetColor(0xFF00FF00)
        else:
            self.fill.SetColor(self.color)
    
    def SetColor(self, color):
        self.color = color
        if self.current < self.maximum:
            self.fill.SetColor(color)
    
    def HideText(self):
        self.showText = False
        self.text.Hide()
    
    def __UpdateFill(self):
        fillWidth = int((self.width - 2) * self.progress)
        self.fill.SetSize(max(0, fillWidth), self.height - 2)
    
    def OnUpdate(self):
        if abs(self.progress - self.targetProgress) > 0.001:
            self.progress += (self.targetProgress - self.progress) * 0.2
            self.__UpdateFill()


# ============================================================
# TOOLTIP OBIETTIVI
# ============================================================
_g_objectiveTooltip = None

def GetObjectiveTooltip():
    global _g_objectiveTooltip
    if _g_objectiveTooltip is None:
        _g_objectiveTooltip = ObjectiveTooltip()
    return _g_objectiveTooltip


class ObjectiveTooltip(ui.Window):
    """Tooltip premium per i dettagli degli obiettivi della Prova Rank."""

    MAX_WIDTH = 340
    LINE_H = 14
    POOL_SIZE = 40
    BAR_POOL = 12
    HEADER_H = 28

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
        # Main background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.MAX_WIDTH, 50)
        self.bg.SetColor(0xF2080812)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Header background bar (colored)
        self.headerBg = ui.Bar()
        self.headerBg.SetParent(self)
        self.headerBg.SetPosition(0, 0)
        self.headerBg.SetSize(self.MAX_WIDTH, self.HEADER_H)
        self.headerBg.SetColor(0xCC1a0a2a)
        self.headerBg.AddFlag("not_pick")
        self.headerBg.Show()

        # 4-side border
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.MAX_WIDTH, 2)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        self.borderBot = ui.Bar()
        self.borderBot.SetParent(self)
        self.borderBot.SetPosition(0, 48)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)
        self.borderBot.SetColor(0xFFFFD700)
        self.borderBot.AddFlag("not_pick")
        self.borderBot.Show()

        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, 50)
        self.borderLeft.SetColor(0xFFFFD700)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, 50)
        self.borderRight.SetColor(0xFFFFD700)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        # Header accent line under header
        self.headerLine = ui.Bar()
        self.headerLine.SetParent(self)
        self.headerLine.SetPosition(2, self.HEADER_H)
        self.headerLine.SetSize(self.MAX_WIDTH - 4, 1)
        self.headerLine.SetColor(0xFFFFD700)
        self.headerLine.AddFlag("not_pick")
        self.headerLine.Show()

        # Title text (in header)
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.MAX_WIDTH // 2, 6)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(0xFFFFFFFF)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()

        # Progress bar inside tooltip
        self.progBg = ui.Bar()
        self.progBg.SetParent(self)
        self.progBg.SetPosition(14, 0)
        self.progBg.SetSize(self.MAX_WIDTH - 28, 12)
        self.progBg.SetColor(0xFF0d0d1a)
        self.progBg.AddFlag("not_pick")
        self.progBg.Hide()

        self.progFill = ui.Bar()
        self.progFill.SetParent(self)
        self.progFill.SetPosition(15, 1)
        self.progFill.SetSize(0, 10)
        self.progFill.SetColor(0xFF00FF00)
        self.progFill.AddFlag("not_pick")
        self.progFill.Hide()

        self.progText = ui.TextLine()
        self.progText.SetParent(self)
        self.progText.SetPosition(self.MAX_WIDTH // 2, 0)
        self.progText.SetHorizontalAlignCenter()
        self.progText.SetText("")
        self.progText.SetPackedFontColor(0xFFFFFFFF)
        self.progText.SetOutline()
        self.progText.AddFlag("not_pick")
        self.progText.Hide()

        # Status badge
        self.statusBadge = ui.Bar()
        self.statusBadge.SetParent(self)
        self.statusBadge.SetPosition(0, 0)
        self.statusBadge.SetSize(80, 16)
        self.statusBadge.SetColor(0xCC222222)
        self.statusBadge.AddFlag("not_pick")
        self.statusBadge.Hide()

        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(0, 0)
        self.statusText.SetHorizontalAlignCenter()
        self.statusText.SetText("")
        self.statusText.SetPackedFontColor(0xFFFFFFFF)
        self.statusText.SetOutline()
        self.statusText.AddFlag("not_pick")
        self.statusText.Hide()

    def __BuildPool(self):
        for i in range(self.POOL_SIZE):
            tl = ui.TextLine()
            tl.SetParent(self)
            tl.AddFlag("not_pick")
            tl.Hide()
            self.linePool.append(tl)
        for i in range(self.BAR_POOL):
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

    def __PutSep(self, y, color=0xFF333355):
        if self.usedBars < len(self.barPool):
            b = self.barPool[self.usedBars]
            b.SetPosition(14, y)
            b.SetSize(self.MAX_WIDTH - 28, 1)
            b.SetColor(color)
            b.Show()
            self.usedBars += 1

    def __PutDot(self, x, y, color):
        """Piccolo quadrato 4x4 come bullet point."""
        if self.usedBars < len(self.barPool):
            b = self.barPool[self.usedBars]
            b.SetPosition(x, y + 4)
            b.SetSize(4, 4)
            b.SetColor(color)
            b.Show()
            self.usedBars += 1

    def ShowTooltip(self, title, titleColor, fullNames, current, required, descLines, tipLine=""):
        """Mostra il tooltip premium con header, barra, target, descrizione e suggerimento."""
        self.__ResetPool()

        # ===== HEADER =====
        self.titleText.SetText(title)
        self.titleText.SetPackedFontColor(titleColor)
        self.headerBg.SetColor(self.__DimColor(titleColor, 0.15))

        y = self.HEADER_H + 6

        # ===== STATUS BADGE =====
        if required > 0:
            if current >= required:
                badgeText = " COMPLETATO "
                badgeColor = 0xCC004400
                badgeTextColor = 0xFF00FF00
            else:
                pct = int(100.0 * current / required)
                badgeText = " " + str(pct) + "% "
                if pct >= 75:
                    badgeColor = 0xCC003300
                    badgeTextColor = 0xFF88FF00
                elif pct >= 50:
                    badgeColor = 0xCC333300
                    badgeTextColor = 0xFFFFCC00
                elif pct >= 25:
                    badgeColor = 0xCC332200
                    badgeTextColor = 0xFFFF8800
                else:
                    badgeColor = 0xCC330000
                    badgeTextColor = 0xFFFF4444

            badgeW = len(badgeText) * 7 + 10
            badgeX = self.MAX_WIDTH - badgeW - 14
            self.statusBadge.SetPosition(badgeX, y)
            self.statusBadge.SetSize(badgeW, 16)
            self.statusBadge.SetColor(badgeColor)
            self.statusBadge.Show()
            self.statusText.SetPosition(badgeX + badgeW // 2, y + 1)
            self.statusText.SetText(badgeText)
            self.statusText.SetPackedFontColor(badgeTextColor)
            self.statusText.Show()

            # Progress text
            progStr = str(current) + " / " + str(required)
            progColor = 0xFF00FF00 if current >= required else 0xFFFFCC00
            self.__PutLine("Progresso:  " + progStr, progColor, 14, y)
            y += 20

            # Progress bar
            barW = self.MAX_WIDTH - 28
            self.progBg.SetPosition(14, y)
            self.progBg.SetSize(barW, 10)
            self.progBg.Show()

            fillW = max(0, int(barW * min(1.0, float(current) / float(required))))
            fillColor = 0xFF00FF00 if current >= required else titleColor
            self.progFill.SetPosition(14, y)
            self.progFill.SetSize(fillW, 10)
            self.progFill.SetColor(fillColor)
            self.progFill.Show()

            self.progText.Hide()
            y += 16
        else:
            self.statusBadge.Hide()
            self.statusText.Hide()
            self.progBg.Hide()
            self.progFill.Hide()
            self.progText.Hide()

        self.__PutSep(y, self.__DimColor(titleColor, 0.4))
        y += 8

        # ===== TARGET LIST =====
        if fullNames:
            self.__PutLine("TARGET RICHIESTI", 0xFFFFD700, 14, y, True)
            y += 18
            nameList = [n.strip() for n in fullNames.split(",") if n.strip()]
            for name in nameList:
                self.__PutDot(18, y, titleColor)
                self.__PutLine(name, 0xFFFFFFFF, 28, y)
                y += self.LINE_H + 2
            y += 2
        else:
            self.__PutLine("Nessun target specifico", 0xFF666666, 14, y)
            y += 18

        self.__PutSep(y, 0xFF333355)
        y += 8

        # ===== DOVE / COME =====
        if descLines:
            self.__PutLine("DOVE / COME", 0xFF55BBFF, 14, y, True)
            y += 18
            for line in descLines:
                if line.startswith("  "):
                    self.__PutLine(line, 0xFFAAAAAA, 14, y)
                else:
                    self.__PutLine(line, 0xFFCCCCCC, 14, y)
                y += self.LINE_H

        # ===== SUGGERIMENTO =====
        if tipLine:
            y += 4
            self.__PutSep(y, 0xFF444422)
            y += 6
            self.__PutLine("SUGGERIMENTO", 0xFFFFAA00, 14, y, True)
            y += 16
            self.__PutLine(tipLine, 0xFFFFDD88, 14, y)
            y += self.LINE_H

        y += 12

        # ===== RESIZE & POSITION =====
        self.tooltipH = y
        self.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.bg.SetSize(self.MAX_WIDTH, self.tooltipH)
        self.borderLeft.SetSize(2, self.tooltipH)
        self.borderRight.SetPosition(self.MAX_WIDTH - 2, 0)
        self.borderRight.SetSize(2, self.tooltipH)
        self.borderBot.SetPosition(0, self.tooltipH - 2)
        self.borderBot.SetSize(self.MAX_WIDTH, 2)

        # Apply accent color to borders
        self.borderLeft.SetColor(titleColor)
        self.borderRight.SetColor(self.__DimColor(titleColor, 0.5))
        self.borderTop.SetColor(titleColor)
        self.borderBot.SetColor(self.__DimColor(titleColor, 0.5))
        self.headerLine.SetColor(self.__DimColor(titleColor, 0.6))

        # Posizione vicino al mouse
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

    def __DimColor(self, color, factor):
        """Riduce la luminosita' di un colore mantenendo l'alfa."""
        a = (color >> 24) & 0xFF
        r = int(((color >> 16) & 0xFF) * factor)
        g = int(((color >> 8) & 0xFF) * factor)
        b = int((color & 0xFF) * factor)
        return (a << 24) | (min(255, r) << 16) | (min(255, g) << 8) | min(255, b)

    def HideTooltip(self):
        self.statusBadge.Hide()
        self.statusText.Hide()
        self.progBg.Hide()
        self.progFill.Hide()
        self.progText.Hide()
        self.Hide()


# ============================================================
# RIGA OBIETTIVO COMPATTA
# ============================================================
class ObjectiveRow(ui.Window):
    def __init__(self, label, color):
        ui.Window.__init__(self)
        self.SetSize(280, 32)
        self.label = label
        self.color = color
        self.current = 0
        self.required = 0
        self.targetNames = ""
        self.tooltipDesc = []
        self.tooltipTip = ""
        self.__BuildUI()
    
    def __BuildUI(self):
        self.labelText = ui.TextLine()
        self.labelText.SetParent(self)
        self.labelText.SetPosition(0, 2)
        self.labelText.SetText(self.label)
        self.labelText.SetPackedFontColor(self.color)
        self.labelText.SetOutline()
        self.labelText.AddFlag("not_pick")
        self.labelText.Show()
        
        # Sottotitolo con nomi target (inizialmente nascosto)
        self.namesText = ui.TextLine()
        self.namesText.SetParent(self)
        self.namesText.SetPosition(8, 14)
        self.namesText.SetText("")
        self.namesText.SetPackedFontColor(0xFFAAAAAA)
        self.namesText.AddFlag("not_pick")
        self.namesText.Hide()
        
        self.progressBar = ProgressBar()
        self.progressBar.SetParent(self)
        self.progressBar.SetPosition(0, 28)
        self.progressBar.SetSize(230, 14)
        self.progressBar.SetColor(self.color)
        self.progressBar.AddFlag("not_pick")
        self.progressBar.Show()
        
        self.statusText = ui.TextLine()
        self.statusText.SetParent(self)
        self.statusText.SetPosition(240, 28)
        self.statusText.SetText("")
        self.statusText.SetPackedFontColor(0xFF888888)
        self.statusText.AddFlag("not_pick")
        self.statusText.Show()
    
    def SetTargetNames(self, names):
        """Imposta i nomi dei target sotto il titolo dell'obiettivo."""
        self.targetNames = names if names else ""
        if self.targetNames:
            # Tronca se troppo lungo per la finestra
            displayNames = self.targetNames
            if len(displayNames) > 40:
                displayNames = displayNames[:37] + "..."
            self.namesText.SetText(displayNames)
            self.namesText.Show()
            # Riga piu' alta con subtitle: riposiziona bar e status
            self.progressBar.SetPosition(0, 28)
            self.statusText.SetPosition(240, 28)
            self.SetSize(280, 44)
        else:
            self.namesText.Hide()
            # Riga standard senza subtitle
            self.progressBar.SetPosition(0, 16)
            self.statusText.SetPosition(240, 16)
            self.SetSize(280, 32)
    
    def GetRowHeight(self):
        """Ritorna l'altezza della riga in base alla presenza di nomi target."""
        if self.targetNames:
            return 48
        return 36
    
    def SetProgress(self, current, required):
        self.current = current
        self.required = required
        self.progressBar.SetProgress(current, required)
        
        if required <= 0:
            self.statusText.SetText("N/R")
            self.statusText.SetPackedFontColor(0xFF555555)
            self.Hide()
        elif current >= required:
            self.statusText.SetText("OK")
            self.statusText.SetPackedFontColor(0xFF00FF00)
            self.Show()
        else:
            self.statusText.SetText("-" + str(required - current))
            self.statusText.SetPackedFontColor(0xFFFF8800)
            self.Show()

    def SetTooltipDescription(self, descLines, tipLine=""):
        """Imposta le linee di descrizione e suggerimento per il tooltip hover."""
        self.tooltipDesc = descLines if descLines else []
        self.tooltipTip = tipLine

    def OnMouseOverIn(self):
        if self.required > 0:
            tooltip = GetObjectiveTooltip()
            tooltip.ShowTooltip(
                self.label, self.color, self.targetNames,
                self.current, self.required, self.tooltipDesc,
                self.tooltipTip
            )

    def OnMouseOverOut(self):
        tooltip = GetObjectiveTooltip()
        tooltip.HideTooltip()


# ============================================================
# FINESTRA PRINCIPALE COMPATTA
# ============================================================
class TrialStatusWindow(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.screenHeight = wndMgr.GetScreenHeight()
        
        self.windowWidth = 320
        self.windowHeight = 450
        
        self.SetSize(self.windowWidth, self.windowHeight)
        
        defaultX = self.screenWidth - self.windowWidth - 10
        defaultY = 150
        savedX, savedY = GetWindowPosition("TrialStatusWindow", defaultX, defaultY)
        self.SetPosition(savedX, savedY)
        
        self.AddFlag("movable")
        self.AddFlag("float")
        
        self.isDragging = False
        self.dragOffsetX = 0
        self.dragOffsetY = 0
        
        self.trialData = None
        self.gateData = None
        self.currentRank = "E"
        self.targetRank = "E"
        self.lastUpdateTime = 0
        
        self.__BuildUI()
        self.Hide()
    
    def OnMouseLeftButtonDown(self):
        self.isDragging = True
        mouseX, mouseY = wndMgr.GetMousePosition()
        winX, winY = self.GetGlobalPosition()
        self.dragOffsetX = mouseX - winX
        self.dragOffsetY = mouseY - winY
        return True
    
    def OnMouseLeftButtonUp(self):
        if self.isDragging:
            self.isDragging = False
            x, y = self.GetGlobalPosition()
            SaveWindowPosition("TrialStatusWindow", x, y)
        return True
    
    def OnMouseDrag(self, x, y):
        if self.isDragging:
            mouseX, mouseY = wndMgr.GetMousePosition()
            newX = mouseX - self.dragOffsetX
            newY = mouseY - self.dragOffsetY
            newX = max(0, min(newX, self.screenWidth - self.windowWidth))
            newY = max(0, min(newY, self.screenHeight - self.windowHeight))
            self.SetPosition(newX, newY)
        return True
    
    def __BuildUI(self):
        # Background
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.windowWidth, self.windowHeight)
        self.bg.SetColor(0xEE080810)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Border top
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.windowWidth, 2)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        # Header
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.windowWidth // 2, 8)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("HUNTER TRIAL")
        self.titleText.SetPackedFontColor(0xFFFFD700)
        self.titleText.SetOutline()
        self.titleText.AddFlag("not_pick")
        self.titleText.Show()
        
        # Close button (ui.Window con area cliccabile reale)
        self.closeBtn = ui.Window()
        self.closeBtn.SetParent(self)
        self.closeBtn.SetPosition(self.windowWidth - 25, 5)
        self.closeBtn.SetSize(20, 18)
        self.closeBtn.Show()
        
        self.closeBtnBg = ui.Bar()
        self.closeBtnBg.SetParent(self.closeBtn)
        self.closeBtnBg.SetPosition(0, 0)
        self.closeBtnBg.SetSize(20, 18)
        self.closeBtnBg.SetColor(0x88FF0000)
        self.closeBtnBg.AddFlag("not_pick")
        self.closeBtnBg.Show()
        
        self.closeBtnText = ui.TextLine()
        self.closeBtnText.SetParent(self.closeBtn)
        self.closeBtnText.SetPosition(10, 1)
        self.closeBtnText.SetHorizontalAlignCenter()
        self.closeBtnText.SetText("X")
        self.closeBtnText.SetPackedFontColor(0xFFFFFFFF)
        self.closeBtnText.SetOutline()
        self.closeBtnText.AddFlag("not_pick")
        self.closeBtnText.Show()
        
        self.closeBtn.OnMouseLeftButtonUp = ui.__mem_func__(self.Close)
        self.closeBtn.OnMouseOverIn = lambda: self.closeBtnBg.SetColor(0xCCFF0000)
        self.closeBtn.OnMouseOverOut = lambda: self.closeBtnBg.SetColor(0x88FF0000)
        
        # ===== SUPREMO SECTION =====
        yPos = 28
        
        self.supremoTitle = ui.TextLine()
        self.supremoTitle.SetParent(self)
        self.supremoTitle.SetPosition(15, yPos)
        self.supremoTitle.SetText("[ SUPREMO ]")
        self.supremoTitle.SetPackedFontColor(0xFFFF0000)
        self.supremoTitle.SetOutline()
        self.supremoTitle.AddFlag("not_pick")
        self.supremoTitle.Show()
        
        yPos += 18
        
        self.supremoStatusText = ui.TextLine()
        self.supremoStatusText.SetParent(self)
        self.supremoStatusText.SetPosition(20, yPos)
        self.supremoStatusText.SetText("Nessun invito attivo")
        self.supremoStatusText.SetPackedFontColor(0xFF666666)
        self.supremoStatusText.AddFlag("not_pick")
        self.supremoStatusText.Show()
        
        yPos += 16
        
        self.supremoTimerText = ui.TextLine()
        self.supremoTimerText.SetParent(self)
        self.supremoTimerText.SetPosition(20, yPos)
        self.supremoTimerText.SetText("")
        self.supremoTimerText.SetPackedFontColor(0xFFFFD700)
        self.supremoTimerText.AddFlag("not_pick")
        self.supremoTimerText.Show()
        
        yPos += 20
        
        self.supremoBar = ProgressBar()
        self.supremoBar.SetParent(self)
        self.supremoBar.SetPosition(20, yPos)
        self.supremoBar.SetSize(self.windowWidth - 40, 12)
        self.supremoBar.SetColor(0xFFFF0000)
        self.supremoBar.HideText()
        self.supremoBar.AddFlag("not_pick")
        self.supremoBar.Hide()
        
        yPos += 18
        
        # Divider
        self.div1 = ui.Bar()
        self.div1.SetParent(self)
        self.div1.SetPosition(15, yPos)
        self.div1.SetSize(self.windowWidth - 30, 1)
        self.div1.SetColor(0xFF333333)
        self.div1.AddFlag("not_pick")
        self.div1.Show()
        
        yPos += 8
        
        # ===== RANK TRIAL SECTION =====
        self.trialTitle = ui.TextLine()
        self.trialTitle.SetParent(self)
        self.trialTitle.SetPosition(15, yPos)
        self.trialTitle.SetText("[ PROVA RANK ]")
        self.trialTitle.SetPackedFontColor(0xFFAA00FF)
        self.trialTitle.SetOutline()
        self.trialTitle.AddFlag("not_pick")
        self.trialTitle.Show()
        
        yPos += 18
        
        # Rank display
        self.rankLine = ui.TextLine()
        self.rankLine.SetParent(self)
        self.rankLine.SetPosition(20, yPos)
        self.rankLine.SetText("E-RANK >>> D-RANK")
        self.rankLine.SetPackedFontColor(0xFFFFFFFF)
        self.rankLine.SetOutline()
        self.rankLine.AddFlag("not_pick")
        self.rankLine.Show()
        
        yPos += 18
        
        # Trial status
        self.trialStatusText = ui.TextLine()
        self.trialStatusText.SetParent(self)
        self.trialStatusText.SetPosition(20, yPos)
        self.trialStatusText.SetText("Nessuna prova attiva")
        self.trialStatusText.SetPackedFontColor(0xFF666666)
        self.trialStatusText.AddFlag("not_pick")
        self.trialStatusText.Show()
        
        yPos += 16
        
        self.trialTimerText = ui.TextLine()
        self.trialTimerText.SetParent(self)
        self.trialTimerText.SetPosition(20, yPos)
        self.trialTimerText.SetText("")
        self.trialTimerText.SetPackedFontColor(0xFFFF8800)
        self.trialTimerText.AddFlag("not_pick")
        self.trialTimerText.Show()
        
        yPos += 22
        
        # Divider
        self.div2 = ui.Bar()
        self.div2.SetParent(self)
        self.div2.SetPosition(15, yPos)
        self.div2.SetSize(self.windowWidth - 30, 1)
        self.div2.SetColor(0xFF333333)
        self.div2.AddFlag("not_pick")
        self.div2.Show()
        
        yPos += 8
        
        # ===== OBJECTIVES =====
        self.objTitle = ui.TextLine()
        self.objTitle.SetParent(self)
        self.objTitle.SetPosition(15, yPos)
        self.objTitle.SetText("[ OBIETTIVI ]")
        self.objTitle.SetPackedFontColor(0xFFFFD700)
        self.objTitle.SetOutline()
        self.objTitle.AddFlag("not_pick")
        self.objTitle.Show()
        
        yPos += 20
        
        self.objBaseY = yPos
        
        self.bossRow = ObjectiveRow("Boss Fratture", 0xFFFF6666)
        self.bossRow.SetParent(self)
        self.bossRow.SetPosition(20, yPos)
        self.bossRow.Show()
        yPos += 36
        
        self.metinRow = ObjectiveRow("Metin Fratture", 0xFF66FFFF)
        self.metinRow.SetParent(self)
        self.metinRow.SetPosition(20, yPos)
        self.metinRow.Show()
        yPos += 36
        
        self.fractureRow = ObjectiveRow("Fratture Conquistate", 0xFFCC66FF)
        self.fractureRow.SetParent(self)
        self.fractureRow.SetPosition(20, yPos)
        self.fractureRow.Show()
        yPos += 36
        
        self.chestRow = ObjectiveRow("Bauli Fratture", 0xFFFFDD66)
        self.chestRow.SetParent(self)
        self.chestRow.SetPosition(20, yPos)
        self.chestRow.Show()
        yPos += 36
        
        self.missionRow = ObjectiveRow("Missioni Giornaliere", 0xFF66FF66)
        self.missionRow.SetParent(self)
        self.missionRow.SetPosition(20, yPos)
        self.missionRow.Show()
        yPos += 40
        
        self.objectiveRows = [self.bossRow, self.metinRow, self.fractureRow, self.chestRow, self.missionRow]
        
        # ===== TOOLTIP DESCRIPTIONS =====
        self.bossRow.SetTooltipDescription([
            "Spawnano dai PORTALI delle fratture.",
            "Completa la fase di difesa per aprire il portale.",
            "Il portale genera casualmente: Boss, Metin,",
            "  Super Metin, o Baule.",
            "Le fratture appaiono dopo ~500 kill",
            "  su qualsiasi mappa non-dungeon.",
        ])
        self.metinRow.SetTooltipDescription([
            "Supermetin speciali dai portali frattura.",
            "Spawn casuale dal portale (come i Boss).",
            "Completa la difesa della frattura per",
            "  generare il portale.",
            "I Super Metin hanno 300 secondi di",
            "  possesso esclusivo per chi li claima.",
        ])
        self.fractureRow.SetTooltipDescription([
            "Avvicinati a una frattura e conquistala!",
            "Entra, completa la difesa e ottieni Gloria.",
            "Puoi anche scegliere di sigillarla",
            "  (costa Coraggio, variabile per Rank).",
            "I colori indicano il grado della frattura:",
            "  BLU=facile, ARANCIO=medio, ROSSO=duro.",
        ])
        self.chestRow.SetTooltipDescription([
            "Bauli che appaiono dai portali frattura.",
            "Uno dei 4 tipi di spawn possibili dal portale.",
            "Contengono ricompense e oggetti Hunter.",
            "Apri fratture e completa la difesa",
            "  per spawnare il portale.",
        ])
        self.missionRow.SetTooltipDescription([
            "3 missioni al giorno (reset a mezzanotte).",
            "Bonus +50% Gloria se completi tutte e 3!",
            "Tipi: kill mob, metin, boss, raccolta.",
            "",
            "NOVITA': PROGRESSO CONDIVISO!",
            "Se sei in gruppo o vicino a un altro player",
            "  che completa una missione, ottieni il",
            "  progresso anche tu automaticamente!",
            "Gioca vicino agli altri per progredire",
            "  molto piu' velocemente!",
        ])
        
        # Footer
        self.div3 = ui.Bar()
        self.div3.SetParent(self)
        self.div3.SetPosition(15, yPos)
        self.div3.SetSize(self.windowWidth - 30, 1)
        self.div3.SetColor(0xFF333333)
        self.div3.AddFlag("not_pick")
        self.div3.Show()
        
        yPos += 6
        
        self.footerText = ui.TextLine()
        self.footerText.SetParent(self)
        self.footerText.SetPosition(self.windowWidth // 2, yPos)
        self.footerText.SetHorizontalAlignCenter()
        self.footerText.SetText("NPC: Traditore Balso (Capitale)")
        self.footerText.SetPackedFontColor(0xFF888888)
        self.footerText.AddFlag("not_pick")
        self.footerText.Show()
        
        yPos += 14
        
        self.footerText2 = ui.TextLine()
        self.footerText2.SetParent(self)
        self.footerText2.SetPosition(self.windowWidth // 2, yPos)
        self.footerText2.SetHorizontalAlignCenter()
        self.footerText2.SetText("Progressi individuali (anche in party)")
        self.footerText2.SetPackedFontColor(0xFF666666)
        self.footerText2.AddFlag("not_pick")
        self.footerText2.Show()
    
    def Show(self):
        ui.Window.Show(self)
        self.SetTop()
    
    def Close(self):
        # Nascondi tooltip obiettivi se visibile
        try:
            tooltip = GetObjectiveTooltip()
            tooltip.HideTooltip()
        except:
            pass
        self.Hide()
    
    def OnPressEscapeKey(self):
        self.Close()
        return True
    
    def SetCurrentRank(self, rank):
        self.currentRank = rank
        self.__UpdateRankLine()
    
    def SetTargetRank(self, rank):
        self.targetRank = rank
        self.__UpdateRankLine()
        self.borderTop.SetColor(GetRankColor(rank))
    
    def __UpdateRankLine(self):
        self.rankLine.SetText(self.currentRank + "-RANK >>> " + self.targetRank + "-RANK")
    
    def UpdateGateStatus(self, gateId, gateName, remainingSeconds, colorCode):
        """Aggiorna lo stato del Supremo (World Boss)"""
        gateName = gateName.replace("+", " ") if gateName else ""
        
        self.gateData = {
            "id": gateId,
            "name": gateName,
            "remaining": remainingSeconds,
            "maxTime": remainingSeconds,
            "color": colorCode
        }
        
        if gateId > 0 and remainingSeconds > 0:
            self.supremoStatusText.SetText("Supremo: " + gateName)
            self.supremoStatusText.SetPackedFontColor(GetColorCode(colorCode))
            self.supremoTimerText.SetText("Tempo: " + self.__FormatTime(remainingSeconds))
            self.supremoTimerText.SetPackedFontColor(0xFFFFD700)
            self.supremoBar.SetProgress(remainingSeconds, remainingSeconds)
            self.supremoBar.Show()
            self.supremoTitle.SetPackedFontColor(0xFFFF4444)
        else:
            self.supremoStatusText.SetText("Nessun invito attivo")
            self.supremoStatusText.SetPackedFontColor(0xFF666666)
            self.supremoTimerText.SetText("")
            self.supremoBar.Hide()
            self.supremoTitle.SetPackedFontColor(0xFFFF0000)
            self.gateData = None
    
    def _RepositionObjectives(self):
        """Riposiziona dinamicamente le righe obiettivo visibili e ridimensiona la finestra."""
        yPos = self.objBaseY
        for row in self.objectiveRows:
            if row.required > 0:
                row.SetPosition(20, yPos)
                yPos += row.GetRowHeight()
        
        if yPos > self.objBaseY:
            yPos += 4
        
        self.div3.SetPosition(15, yPos)
        yPos += 6
        self.footerText.SetPosition(self.windowWidth // 2, yPos)
        yPos += 14
        self.footerText2.SetPosition(self.windowWidth // 2, yPos)
        yPos += 14
        
        self.windowHeight = yPos
        self.SetSize(self.windowWidth, self.windowHeight)
        self.bg.SetSize(self.windowWidth, self.windowHeight)
    
    def UpdateTrialStatus(self, trialId, trialName, toRank, colorCode, remaining,
                          bossKills, reqBoss, metinKills, reqMetin,
                          fractureSeals, reqFracture, chestOpens, reqChest,
                          dailyMissions, reqMissions,
                          bossNames="", metinNames="", fractureNames="", chestNames=""):
        
        trialName = trialName.replace("+", " ") if trialName else ""
        
        self.trialData = {
            "id": trialId,
            "name": trialName,
            "toRank": toRank,
            "color": colorCode,
            "remaining": remaining,
        }
        
        self.SetTargetRank(toRank)
        
        if trialId > 0:
            self.trialStatusText.SetText(trialName if trialName != "NONE" else "Prova per " + toRank)
            self.trialStatusText.SetPackedFontColor(GetColorCode(colorCode))
            
            if remaining and remaining > 0:
                self.trialTimerText.SetText("Tempo: " + self.__FormatTime(remaining))
            else:
                self.trialTimerText.SetText("Tempo: ILLIMITATO")
                self.trialTimerText.SetPackedFontColor(0xFF00FF00)
            
            self.trialTitle.SetPackedFontColor(0xFFAA00FF)
        else:
            self.trialStatusText.SetText("Nessuna prova attiva")
            self.trialStatusText.SetPackedFontColor(0xFF666666)
            self.trialTimerText.SetText("Parla con Traditore Balso")
            self.trialTimerText.SetPackedFontColor(0xFF555555)
            self.trialTitle.SetPackedFontColor(0xFF666666)
        
        # Update objectives
        self.bossRow.SetProgress(bossKills, reqBoss)
        self.bossRow.SetTargetNames(bossNames)
        self.metinRow.SetProgress(metinKills, reqMetin)
        self.metinRow.SetTargetNames(metinNames)
        self.fractureRow.SetProgress(fractureSeals, reqFracture)
        self.fractureRow.SetTargetNames(fractureNames)
        self.chestRow.SetProgress(chestOpens, reqChest)
        self.chestRow.SetTargetNames(chestNames)
        self.missionRow.SetProgress(dailyMissions, reqMissions)
        
        # Riposiziona solo le righe con requisito > 0
        self._RepositionObjectives()
        
        # Check completion
        allComplete = True
        if reqBoss > 0 and bossKills < reqBoss:
            allComplete = False
        if reqMetin > 0 and metinKills < reqMetin:
            allComplete = False
        if reqFracture > 0 and fractureSeals < reqFracture:
            allComplete = False
        if reqChest > 0 and chestOpens < reqChest:
            allComplete = False
        if reqMissions > 0 and dailyMissions < reqMissions:
            allComplete = False
        
        if allComplete and trialId > 0:
            self.trialStatusText.SetText("COMPLETATA!")
            self.trialStatusText.SetPackedFontColor(0xFF00FF00)
            self.trialTimerText.SetText("Torna da Traditore Balso!")
            self.trialTimerText.SetPackedFontColor(0xFFFFD700)
    
    def __FormatTime(self, seconds):
        if not seconds or seconds <= 0:
            return "SCADUTO"
        if seconds >= 86400:
            d = seconds // 86400
            h = (seconds % 86400) // 3600
            return str(d) + "g " + str(h) + "h"
        if seconds >= 3600:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return str(h) + "h " + str(m) + "m"
        m = seconds // 60
        s = seconds % 60
        return "%02d:%02d" % (m, s)
    
    def OnUpdate(self):
        currentTime = app.GetTime()
        
        if currentTime - self.lastUpdateTime >= 1.0:
            self.lastUpdateTime = currentTime
            
            # Trial timer
            if self.trialData and self.trialData.get("remaining") and self.trialData["remaining"] > 0:
                self.trialData["remaining"] -= 1
                self.trialTimerText.SetText("Tempo: " + self.__FormatTime(self.trialData["remaining"]))
            
            # Supremo timer
            if self.gateData and self.gateData.get("remaining") and self.gateData["remaining"] > 0:
                self.gateData["remaining"] -= 1
                self.supremoTimerText.SetText("Tempo: " + self.__FormatTime(self.gateData["remaining"]))
                if self.gateData.get("maxTime"):
                    self.supremoBar.SetProgress(self.gateData["remaining"], self.gateData["maxTime"])


# ============================================================
# SISTEMA MESSAGGI
# ============================================================
class SystemSpeakWindow(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        
        self.screenWidth = wndMgr.GetScreenWidth()
        self.SetSize(500, 50)
        self.SetPosition((self.screenWidth - 500) // 2, 30)
        self.AddFlag("not_pick")
        
        self.messageQueue = []
        self.currentMessage = None
        self.startTime = 0
        self.duration = 3.0
        
        self.__BuildUI()
        self.Hide()
    
    def __BuildUI(self):
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(500, 50)
        self.bg.SetColor(0xDD000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(500, 2)
        self.borderTop.SetColor(0xFFFFD700)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.messageText = ui.TextLine()
        self.messageText.SetParent(self)
        self.messageText.SetPosition(250, 18)
        self.messageText.SetHorizontalAlignCenter()
        self.messageText.SetText("")
        self.messageText.SetPackedFontColor(0xFFFFFFFF)
        self.messageText.SetOutline()
        self.messageText.AddFlag("not_pick")
        self.messageText.Show()
    
    def AddMessage(self, colorCode, message):
        message = message.replace("+", " ")
        color = GetColorCode(colorCode) if colorCode else 0xFFFFFFFF
        
        self.messageQueue.append({"color": color, "message": message})
        # Anti-leak: limita coda messaggi
        if len(self.messageQueue) > 20:
            self.messageQueue.pop(0)
        
        if not self.IsShow():
            self.__ShowNext()
    
    def __ShowNext(self):
        if not self.messageQueue:
            self.Hide()
            return
        
        self.currentMessage = self.messageQueue.pop(0)
        self.startTime = app.GetTime()
        
        self.messageText.SetText(self.currentMessage["message"])
        self.messageText.SetPackedFontColor(self.currentMessage["color"])
        self.borderTop.SetColor(self.currentMessage["color"])
        
        self.Show()
        self.SetTop()
    
    def OnUpdate(self):
        if not self.IsShow():
            return
        
        elapsed = app.GetTime() - self.startTime
        if elapsed >= self.duration:
            self.__ShowNext()


# ============================================================
# GLOBAL INSTANCES
# ============================================================
g_trialStatusWindow = None
g_systemSpeakWindow = None

def GetTrialStatusWindow():
    global g_trialStatusWindow
    if g_trialStatusWindow is None:
        g_trialStatusWindow = TrialStatusWindow()
    return g_trialStatusWindow

def GetSystemSpeakWindow():
    global g_systemSpeakWindow
    if g_systemSpeakWindow is None:
        g_systemSpeakWindow = SystemSpeakWindow()
    return g_systemSpeakWindow


# ============================================================
# API FUNCTIONS
# ============================================================

def OpenGateTrialWindow():
    wnd = GetTrialStatusWindow()
    wnd.Show()

def CloseGateTrialWindow():
    wnd = GetTrialStatusWindow()
    wnd.Close()

def UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode):
    wnd = GetTrialStatusWindow()
    wnd.UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode)

def UpdateTrialStatus(trialId, trialName, toRank, colorCode, remaining,
                      bossKills, reqBoss, metinKills, reqMetin,
                      fractureSeals, reqFracture, chestOpens, reqChest,
                      dailyMissions, reqMissions, fromRank=None,
                      bossNames="", metinNames="", fractureNames="", chestNames=""):
    wnd = GetTrialStatusWindow()
    # FIX: Se fromRank è fornito, aggiorna il rank corrente
    if fromRank:
        wnd.SetCurrentRank(fromRank)
    wnd.UpdateTrialStatus(trialId, trialName, toRank, colorCode, remaining,
                          bossKills, reqBoss, metinKills, reqMetin,
                          fractureSeals, reqFracture, chestOpens, reqChest,
                          dailyMissions, reqMissions,
                          bossNames, metinNames, fractureNames, chestNames)

def UpdateTrialProgress(trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions,
                        bossReq=0, metinReq=0, fractureReq=0, chestReq=0, dailyReq=0):
    wnd = GetTrialStatusWindow()
    if not wnd:
        return
    # FIX: Se trialData non e' mai stato popolato (finestra mai aperta),
    # inizializzalo con i dati del pacchetto leggero cosi' la UI funziona comunque
    if not wnd.trialData or not wnd.trialData.get("id"):
        if trialId > 0:
            wnd.trialData = {"id": trialId, "name": "", "toRank": "", "color": "NONE", "remaining": -1}
    if wnd.trialData and wnd.trialData.get("id") == trialId:
        # Guard: se le righe obiettivo non sono ancora state create, skip
        if not hasattr(wnd, 'bossRow') or not wnd.bossRow:
            return
        # Usa i req dal pacchetto se > 0, altrimenti fallback ai valori memorizzati
        bReq = bossReq if bossReq > 0 else wnd.bossRow.required
        mReq = metinReq if metinReq > 0 else wnd.metinRow.required
        fReq = fractureReq if fractureReq > 0 else wnd.fractureRow.required
        cReq = chestReq if chestReq > 0 else wnd.chestRow.required
        dReq = dailyReq if dailyReq > 0 else wnd.missionRow.required
        wnd.bossRow.SetProgress(bossKills, bReq)
        wnd.metinRow.SetProgress(metinKills, mReq)
        wnd.fractureRow.SetProgress(fractureSeals, fReq)
        wnd.chestRow.SetProgress(chestOpens, cReq)
        wnd.missionRow.SetProgress(dailyMissions, dReq)

def SetCurrentRank(rank):
    wnd = GetTrialStatusWindow()
    wnd.SetCurrentRank(rank)

def ShowSystemMessage(colorCode, message):
    wnd = GetSystemSpeakWindow()
    wnd.AddMessage(colorCode, message)
