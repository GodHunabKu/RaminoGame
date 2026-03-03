# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - UI COMPONENTS
#  Componenti UI riutilizzabili stile Solo Leveling
# ═══════════════════════════════════════════════════════════════════════════════

import ui
import wndMgr
import app
import math

from hunter_core import (
    COLOR_BG_DARK, COLOR_TEXT_NORMAL, COLOR_TEXT_MUTED,
    COLOR_SCHEMES, DEFAULT_SCHEME, RANK_THEMES,
    GetColorScheme, GetRankColor, GetColorFromKey
)


# ═══════════════════════════════════════════════════════════════════════════════
#  ANIMATED PROGRESS BAR - Barra di progresso con effetto glow
# ═══════════════════════════════════════════════════════════════════════════════
class AnimatedProgressBar(ui.Window):
    """Barra di progresso animata con effetto glow - Riutilizzabile ovunque"""
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.width = 200
        self.height = 20
        self.progress = 0.0
        self.targetProgress = 0.0
        self.color = 0xFF00FF00
        self.glowPhase = 0
        
        self.__BuildUI()
    
    def __BuildUI(self):
        # Background - più profondo e scuro
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.width, self.height)
        self.bg.SetColor(0xFF080808)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Bordo completo a 4 lati (stile Solo Leveling)
        self.border = ui.Bar()  # Top
        self.border.SetParent(self)
        self.border.SetPosition(0, 0)
        self.border.SetSize(self.width, 1)
        self.border.SetColor(0xFF2A2A2A)
        self.border.AddFlag("not_pick")
        self.border.Show()

        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, self.height - 1)
        self.borderBottom.SetSize(self.width, 1)
        self.borderBottom.SetColor(0xFF1E1E1E)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()

        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(1, self.height)
        self.borderLeft.SetColor(0xFF222222)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(self.width - 1, 0)
        self.borderRight.SetSize(1, self.height)
        self.borderRight.SetColor(0xFF222222)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        # Angoli decorativi stile Solo Leveling (L-brackets)
        tickLen = 5
        tickColor = 0xFF444444
        self.ctlH = ui.Bar(); self.ctlH.SetParent(self); self.ctlH.SetPosition(0, 0); self.ctlH.SetSize(tickLen, 1); self.ctlH.SetColor(tickColor); self.ctlH.AddFlag("not_pick"); self.ctlH.Show()
        self.ctlV = ui.Bar(); self.ctlV.SetParent(self); self.ctlV.SetPosition(0, 0); self.ctlV.SetSize(1, tickLen); self.ctlV.SetColor(tickColor); self.ctlV.AddFlag("not_pick"); self.ctlV.Show()
        self.ctrH = ui.Bar(); self.ctrH.SetParent(self); self.ctrH.SetPosition(self.width - tickLen, 0); self.ctrH.SetSize(tickLen, 1); self.ctrH.SetColor(tickColor); self.ctrH.AddFlag("not_pick"); self.ctrH.Show()
        self.ctrV = ui.Bar(); self.ctrV.SetParent(self); self.ctrV.SetPosition(self.width - 1, 0); self.ctrV.SetSize(1, tickLen); self.ctrV.SetColor(tickColor); self.ctrV.AddFlag("not_pick"); self.ctrV.Show()
        self.cblH = ui.Bar(); self.cblH.SetParent(self); self.cblH.SetPosition(0, self.height - 1); self.cblH.SetSize(tickLen, 1); self.cblH.SetColor(tickColor); self.cblH.AddFlag("not_pick"); self.cblH.Show()
        self.cblV = ui.Bar(); self.cblV.SetParent(self); self.cblV.SetPosition(0, self.height - tickLen); self.cblV.SetSize(1, tickLen); self.cblV.SetColor(tickColor); self.cblV.AddFlag("not_pick"); self.cblV.Show()
        self.cbrH = ui.Bar(); self.cbrH.SetParent(self); self.cbrH.SetPosition(self.width - tickLen, self.height - 1); self.cbrH.SetSize(tickLen, 1); self.cbrH.SetColor(tickColor); self.cbrH.AddFlag("not_pick"); self.cbrH.Show()
        self.cbrV = ui.Bar(); self.cbrV.SetParent(self); self.cbrV.SetPosition(self.width - 1, self.height - tickLen); self.cbrV.SetSize(1, tickLen); self.cbrV.SetColor(tickColor); self.cbrV.AddFlag("not_pick"); self.cbrV.Show()

        # Progress fill
        self.fill = ui.Bar()
        self.fill.SetParent(self)
        self.fill.SetPosition(2, 2)
        self.fill.SetSize(0, self.height - 4)
        self.fill.SetColor(self.color)
        self.fill.AddFlag("not_pick")
        self.fill.Show()

        # Glow overlay esterno (lento, ampio)
        self.glow = ui.Bar()
        self.glow.SetParent(self)
        self.glow.SetPosition(2, 2)
        self.glow.SetSize(0, self.height - 4)
        self.glow.SetColor(0x00FFFFFF)
        self.glow.AddFlag("not_pick")
        self.glow.Show()

        # Highlight interno (riga brillante nella parte alta del fill)
        self.innerHL = ui.Bar()
        self.innerHL.SetParent(self)
        self.innerHL.SetPosition(2, 2)
        self.innerHL.SetSize(0, 2)
        self.innerHL.SetColor(0x20FFFFFF)
        self.innerHL.AddFlag("not_pick")
        self.innerHL.Show()

        # Shimmer (linea brillante che scorre lentamente nel fill)
        self.shimmer = ui.Bar()
        self.shimmer.SetParent(self)
        self.shimmer.SetPosition(2, 2)
        self.shimmer.SetSize(3, self.height - 4)
        self.shimmer.SetColor(0x00FFFFFF)
        self.shimmer.AddFlag("not_pick")
        self.shimmer.Show()

        # Text
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(self.width // 2, 2)
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("")
        self.text.SetPackedFontColor(0xFFFFFFFF)
        self.text.SetOutline()
        self.text.Show()

        self.shimmerPhase = 0.0
    
    def SetSize(self, w, h):
        ui.Window.SetSize(self, w, h)
        self.width = w
        self.height = h
        self.bg.SetSize(w, h)
        self.border.SetSize(w, 1)
        if hasattr(self, 'borderBottom'):
            self.borderBottom.SetSize(w, 1)
            self.borderBottom.SetPosition(0, h - 1)
            self.borderLeft.SetSize(1, h)
            self.borderRight.SetSize(1, h)
            self.borderRight.SetPosition(w - 1, 0)
        # Aggiorna corner ticks
        tickLen = 5
        if hasattr(self, 'ctrH'):
            self.ctrH.SetPosition(w - tickLen, 0)
            self.ctrV.SetPosition(w - 1, 0)
            self.cblH.SetPosition(0, h - 1)
            self.cblV.SetPosition(0, h - tickLen)
            self.cbrH.SetPosition(w - tickLen, h - 1)
            self.cbrV.SetPosition(w - 1, h - tickLen)
        self.text.SetPosition(w // 2, 2)
        self.__UpdateFill()
    
    def SetProgress(self, current, maximum):
        """Imposta progresso con testo"""
        if maximum > 0:
            self.targetProgress = min(1.0, float(current) / float(maximum))
        else:
            self.targetProgress = 0.0
        self.text.SetText(str(int(current)) + " / " + str(int(maximum)))
    
    def SetProgressNoText(self, current, maximum):
        """Imposta progresso senza mostrare il testo"""
        if maximum > 0:
            self.targetProgress = min(1.0, float(current) / float(maximum))
        else:
            self.targetProgress = 0.0
    
    def SetProgressPercent(self, percent):
        """Imposta progresso come percentuale (0-100)"""
        self.targetProgress = min(1.0, max(0.0, percent / 100.0))
    
    def HideText(self):
        """Nasconde il testo della barra"""
        self.text.Hide()
    
    def ShowText(self):
        """Mostra il testo della barra"""
        self.text.Show()
    
    def SetColor(self, color):
        """Imposta il colore della barra"""
        self.color = color
        self.fill.SetColor(color)
        # Corner ticks: versione attenuata del colore fill
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        tickColor = 0xFF000000 | ((r // 3) << 16) | ((g // 3) << 8) | (b // 3)
        if hasattr(self, 'ctlH'):
            self.ctlH.SetColor(tickColor); self.ctlV.SetColor(tickColor)
            self.ctrH.SetColor(tickColor); self.ctrV.SetColor(tickColor)
            self.cblH.SetColor(tickColor); self.cblV.SetColor(tickColor)
            self.cbrH.SetColor(tickColor); self.cbrV.SetColor(tickColor)

    def __UpdateFill(self):
        fillWidth = int((self.width - 4) * self.progress)
        self.fill.SetSize(max(0, fillWidth), self.height - 4)
        self.glow.SetSize(max(0, fillWidth), self.height - 4)
        if hasattr(self, 'innerHL'):
            self.innerHL.SetSize(max(0, fillWidth), 2)

    def OnUpdate(self):
        # Smooth animation
        if abs(self.progress - self.targetProgress) > 0.001:
            self.progress += (self.targetProgress - self.progress) * 0.1
            self.__UpdateFill()

        # Shimmer lento che scorre nel fill (non epilettico)
        if hasattr(self, 'shimmerPhase'):
            self.shimmerPhase += 0.009
            if self.shimmerPhase > 1.0:
                self.shimmerPhase -= 1.0
            fillW = int((self.width - 4) * self.progress)
            if fillW > 6:
                sx = 2 + int(self.shimmerPhase * (fillW - 4))
                self.shimmer.SetPosition(sx, 2)
                self.shimmer.SetColor(0x22FFFFFF)
            else:
                self.shimmer.SetColor(0x00FFFFFF)

        # Glow lento (0.4 Hz circa, alpha basso - non epilettico)
        self.glowPhase += 0.035
        glowAlpha = int((math.sin(self.glowPhase) * 0.5 + 0.5) * 22)
        self.glow.SetColor((glowAlpha << 24) | 0xFFFFFF)


# ═══════════════════════════════════════════════════════════════════════════════
#  SOLO LEVELING BUTTON - Bottone custom con bordi neon
# ═══════════════════════════════════════════════════════════════════════════════
class SoloLevelingButton(ui.Window):
    """Bottone stile Solo Leveling con bordi neon colorati"""
    
    def __init__(self):
        ui.Window.__init__(self)
        self.event = None
        self.eventArgs = []
        self.theme = None
        self.isDown = False
        self.isHover = False
    
    def Create(self, parent, x, y, width, height, text, theme):
        """Crea il bottone con i parametri specificati"""
        self.SetParent(parent)
        self.SetPosition(x, y)
        self.SetSize(width, height)
        self.theme = theme
        
        # Background
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(width, height)
        self.bgBar.SetColor(theme.get("btn_normal", 0xFF333333))
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi neon
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(width, 2)
        self.borderTop.SetColor(theme.get("border", 0xFF00CCFF))
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()
        
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, height - 2)
        self.borderBottom.SetSize(width, 2)
        self.borderBottom.SetColor(theme.get("border", 0xFF00CCFF))
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()
        
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(2, height)
        self.borderLeft.SetColor(theme.get("border", 0xFF00CCFF))
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()
        
        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(width - 2, 0)
        self.borderRight.SetSize(2, height)
        self.borderRight.SetColor(theme.get("border", 0xFF00CCFF))
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()
        
        # Left accent bar (barra verticale colorata sx - stile Solo Leveling)
        self.leftAccent = ui.Bar()
        self.leftAccent.SetParent(self)
        self.leftAccent.SetPosition(0, 0)
        self.leftAccent.SetSize(3, height)
        self.leftAccent.SetColor(theme.get("border", 0xFF00CCFF))
        self.leftAccent.AddFlag("not_pick")
        self.leftAccent.Show()

        # Corner ticks (angoli decorativi minimi)
        borderColor = theme.get("border", 0xFF00CCFF)
        accentDim = (borderColor & 0x00FFFFFF) | 0x55000000
        tickLen = 5
        self.btnCtlH = ui.Bar(); self.btnCtlH.SetParent(self); self.btnCtlH.SetPosition(3, 0); self.btnCtlH.SetSize(tickLen, 1); self.btnCtlH.SetColor(accentDim); self.btnCtlH.AddFlag("not_pick"); self.btnCtlH.Show()
        self.btnCtrH = ui.Bar(); self.btnCtrH.SetParent(self); self.btnCtrH.SetPosition(width - tickLen - 2, 0); self.btnCtrH.SetSize(tickLen, 1); self.btnCtrH.SetColor(accentDim); self.btnCtrH.AddFlag("not_pick"); self.btnCtrH.Show()
        self.btnCblH = ui.Bar(); self.btnCblH.SetParent(self); self.btnCblH.SetPosition(3, height - 1); self.btnCblH.SetSize(tickLen, 1); self.btnCblH.SetColor(accentDim); self.btnCblH.AddFlag("not_pick"); self.btnCblH.Show()
        self.btnCbrH = ui.Bar(); self.btnCbrH.SetParent(self); self.btnCbrH.SetPosition(width - tickLen - 2, height - 1); self.btnCbrH.SetSize(tickLen, 1); self.btnCbrH.SetColor(accentDim); self.btnCbrH.AddFlag("not_pick"); self.btnCbrH.Show()

        # Testo
        self.textLine = ui.TextLine()
        self.textLine.SetParent(self)
        self.textLine.SetPosition(width // 2 + 1, (height - 14) // 2)
        self.textLine.SetHorizontalAlignCenter()
        self.textLine.SetText(text)
        self.textLine.SetPackedFontColor(theme.get("text_title", 0xFFFFFFFF))
        self.textLine.SetOutline()
        self.textLine.Show()

        self.Show()
        return self
    
    def SetEvent(self, func, *args):
        """Imposta l'evento click"""
        self.event = func
        self.eventArgs = args
    
    def SetText(self, text):
        """Cambia il testo del bottone"""
        if hasattr(self, 'textLine'):
            self.textLine.SetText(text)
    
    def SetTextColor(self, color):
        """Cambia il colore del testo"""
        if hasattr(self, 'textLine'):
            self.textLine.SetPackedFontColor(color)
    
    def UpdateTheme(self, theme):
        """Aggiorna il tema colori"""
        self.theme = theme
        if hasattr(self, 'borderTop'):
            borderColor = theme.get("border", 0xFF00CCFF)
            self.borderTop.SetColor(borderColor)
            self.borderBottom.SetColor(borderColor)
            self.borderLeft.SetColor(borderColor)
            self.borderRight.SetColor(borderColor)
            self.bgBar.SetColor(theme.get("btn_normal", 0xFF333333))
            self.textLine.SetPackedFontColor(theme.get("text_title", 0xFFFFFFFF))
        if hasattr(self, 'leftAccent'):
            borderColor = theme.get("border", 0xFF00CCFF)
            self.leftAccent.SetColor(borderColor)
            accentDim = (borderColor & 0x00FFFFFF) | 0x55000000
            if hasattr(self, 'btnCtlH'):
                self.btnCtlH.SetColor(accentDim)
                self.btnCtrH.SetColor(accentDim)
                self.btnCblH.SetColor(accentDim)
                self.btnCbrH.SetColor(accentDim)
    
    def Down(self):
        """Stato premuto"""
        self.isDown = True
        if self.theme and hasattr(self, 'bgBar'):
            self.bgBar.SetColor(self.theme.get("btn_down", 0xFF555555))
        if hasattr(self, 'leftAccent') and self.theme:
            bc = self.theme.get("border", 0xFF00CCFF)
            r = min(255, ((bc >> 16) & 0xFF) + 50)
            g = min(255, ((bc >> 8) & 0xFF) + 50)
            b = min(255, (bc & 0xFF) + 50)
            self.leftAccent.SetColor(0xFF000000 | (r << 16) | (g << 8) | b)

    def SetUp(self):
        """Stato normale"""
        self.isDown = False
        if self.theme and hasattr(self, 'bgBar'):
            self.bgBar.SetColor(self.theme.get("btn_normal", 0xFF333333))
        if hasattr(self, 'leftAccent') and self.theme:
            self.leftAccent.SetColor(self.theme.get("border", 0xFF00CCFF))

    def OnMouseOverIn(self):
        self.isHover = True
        if self.theme and hasattr(self, 'bgBar'):
            self.bgBar.SetColor(self.theme.get("btn_hover", 0xFF444444))
        if hasattr(self, 'leftAccent') and self.theme:
            bc = self.theme.get("border", 0xFF00CCFF)
            r = min(255, ((bc >> 16) & 0xFF) + 30)
            g = min(255, ((bc >> 8) & 0xFF) + 30)
            b = min(255, (bc & 0xFF) + 30)
            self.leftAccent.SetColor(0xFF000000 | (r << 16) | (g << 8) | b)

    def OnMouseOverOut(self):
        self.isHover = False
        if not self.isDown and self.theme and hasattr(self, 'bgBar'):
            self.bgBar.SetColor(self.theme.get("btn_normal", 0xFF333333))
        if hasattr(self, 'leftAccent') and self.theme and not self.isDown:
            self.leftAccent.SetColor(self.theme.get("border", 0xFF00CCFF))
    
    def OnMouseLeftButtonDown(self):
        self.Down()
    
    def OnMouseLeftButtonUp(self):
        self.SetUp()
        if self.event:
            if self.eventArgs:
                self.event(*self.eventArgs)
            else:
                self.event()


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM BUTTON - Bottone stile Sistema (flat con hover glow)
# ═══════════════════════════════════════════════════════════════════════════════
class SystemButton(ui.Window):
    """Bottone stile System (Flat con hover glow) - Versione semplificata"""
    
    def __init__(self, parent, x, y, width, text, color_scheme, event):
        ui.Window.__init__(self)
        self.SetParent(parent)
        self.SetPosition(x, y)
        self.SetSize(width, 30)
        
        self.color_scheme = color_scheme
        self.event = event
        
        # Sfondo bottone
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetSize(width, 30)
        self.bg.SetColor(0x66000000)
        self.bg.AddFlag("not_pick")
        self.bg.Show()
        
        # Bordo inferiore
        self.border = ui.Bar()
        self.border.SetParent(self)
        self.border.SetPosition(0, 29)
        self.border.SetSize(width, 1)
        self.border.SetColor(color_scheme.get("border", 0xFF00CCFF))
        self.border.AddFlag("not_pick")
        self.border.Show()
        
        # Testo
        self.textLine = ui.TextLine()
        self.textLine.SetParent(self)
        self.textLine.SetPosition(width // 2, 8)
        self.textLine.SetHorizontalAlignCenter()
        self.textLine.SetText(text)
        self.textLine.SetPackedFontColor(color_scheme.get("title", 0xFFFFFFFF))
        self.textLine.Show()
        
        self.Show()
        
    def OnMouseOverIn(self):
        self.bg.SetColor(self.color_scheme.get("glow", 0x44FFFFFF))
        
    def OnMouseOverOut(self):
        self.bg.SetColor(0x66000000)
        
    def OnMouseLeftButtonUp(self):
        if self.event:
            self.event()


# ═══════════════════════════════════════════════════════════════════════════════
#  SOLO LEVELING WINDOW - Finestra base con bordi colorati
# ═══════════════════════════════════════════════════════════════════════════════
class SoloLevelingWindow(ui.ScriptWindow):
    """Finestra base con stile System (Sfondo scuro + Bordi colorati)"""
    
    def __init__(self, width, height, color_scheme=None):
        ui.ScriptWindow.__init__(self)
        self.color_scheme = color_scheme if color_scheme else DEFAULT_SCHEME
        self.SetSize(width, height)
        self.__BuildInterface(width, height)
        
    def __BuildInterface(self, w, h):
        # Sfondo profondo
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(w, h)
        self.bg.SetColor(COLOR_BG_DARK)
        self.bg.Show()

        # Inner shadow (sottile ombra interna per profondità)
        self.innerShadow = ui.Bar()
        self.innerShadow.SetParent(self)
        self.innerShadow.SetPosition(2, 2)
        self.innerShadow.SetSize(w - 4, 4)
        self.innerShadow.SetColor(0x18000000)
        self.innerShadow.AddFlag("not_pick")
        self.innerShadow.Show()

        # Bordi (Top, Bottom, Left, Right)
        self.borders = []
        # Top
        b1 = ui.Bar(); b1.SetParent(self); b1.SetPosition(0, 0); b1.SetSize(w, 2); b1.Show()
        # Bottom
        b2 = ui.Bar(); b2.SetParent(self); b2.SetPosition(0, h-2); b2.SetSize(w, 2); b2.Show()
        # Left
        b3 = ui.Bar(); b3.SetParent(self); b3.SetPosition(0, 0); b3.SetSize(2, h); b3.Show()
        # Right
        b4 = ui.Bar(); b4.SetParent(self); b4.SetPosition(w-2, 0); b4.SetSize(2, h); b4.Show()

        self.borders = [b1, b2, b3, b4]

        # Corner ticks - marchi angolari stile Solo Leveling (L-brackets)
        self.cornerTicks = []
        tickLen = 8
        for (cx, cy, cw, ch) in [
            (2, 0, tickLen, 1), (0, 2, 1, tickLen),              # TL
            (w - tickLen - 2, 0, tickLen, 1), (w - 1, 2, 1, tickLen),  # TR
            (2, h - 1, tickLen, 1), (0, h - tickLen - 2, 1, tickLen),  # BL
            (w - tickLen - 2, h - 1, tickLen, 1), (w - 1, h - tickLen - 2, 1, tickLen),  # BR
        ]:
            ct = ui.Bar()
            ct.SetParent(self)
            ct.SetPosition(cx, cy)
            ct.SetSize(cw, ch)
            ct.AddFlag("not_pick")
            ct.Show()
            self.cornerTicks.append(ct)

        self.UpdateColors()
            
    def SetColorScheme(self, scheme):
        """Cambia lo schema colori"""
        self.color_scheme = scheme
        self.UpdateColors()
        
    def UpdateColors(self):
        """Aggiorna i colori dei bordi e degli angoli decorativi"""
        borderColor = self.color_scheme.get("border", 0xFFFFFFFF)
        for bar in self.borders:
            bar.SetColor(borderColor)
        # Corner ticks: versione più scura del colore border
        r = (borderColor >> 16) & 0xFF
        g = (borderColor >> 8) & 0xFF
        b = borderColor & 0xFF
        tickColor = 0xFF000000 | ((r * 2 // 3) << 16) | ((g * 2 // 3) << 8) | (b * 2 // 3)
        if hasattr(self, 'cornerTicks'):
            for ct in self.cornerTicks:
                ct.SetColor(tickColor)


# ═══════════════════════════════════════════════════════════════════════════════
#  SYSTEM POPUP - Popup unificato per notifiche e messaggi
# ═══════════════════════════════════════════════════════════════════════════════
class SystemPopup(ui.Window):
    """
    Popup unificato per notifiche - Usabile per:
    - Messaggi di sistema
    - Progresso missioni
    - Notifiche trial/gate
    - Qualsiasi popup temporaneo
    """
    
    def __init__(self):
        ui.Window.__init__(self)
        
        self.width = 300
        self.height = 60
        self.SetSize(self.width, self.height)
        self.AddFlag("not_pick")
        self.AddFlag("float")
        
        self.messageQueue = []
        self.currentMessage = None
        self.endTime = 0
        self.messageDelay = 3.0
        self.currentColor = 0xFF00CCFF
        
        self.__BuildUI()
    
    def __BuildUI(self):
        screenWidth = wndMgr.GetScreenWidth()
        self.SetPosition((screenWidth - self.width) // 2, 320)
        
        # Background
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(self.width, self.height)
        self.bgBar.SetColor(0xDD0A0A0A)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()
        
        # Bordi
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(self.width, 2)
        self.borderTop.SetColor(self.currentColor)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, self.height - 2)
        self.borderBottom.SetSize(self.width, 2)
        self.borderBottom.SetColor(self.currentColor)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()

        # Left accent bar (spessa barra colorata sx - stile Sistema Solo Leveling)
        self.leftAccent = ui.Bar()
        self.leftAccent.SetParent(self)
        self.leftAccent.SetPosition(0, 2)
        self.leftAccent.SetSize(4, self.height - 4)
        self.leftAccent.SetColor(self.currentColor)
        self.leftAccent.AddFlag("not_pick")
        self.leftAccent.Show()

        # Right accent bar (sottile, speculare)
        self.rightAccent = ui.Bar()
        self.rightAccent.SetParent(self)
        self.rightAccent.SetPosition(self.width - 2, 2)
        self.rightAccent.SetSize(2, self.height - 4)
        self.rightAccent.SetColor((self.currentColor & 0x00FFFFFF) | 0x55000000)
        self.rightAccent.AddFlag("not_pick")
        self.rightAccent.Show()

        # Separatore interno (linea tra titolo e messaggio)
        self.separator = ui.Bar()
        self.separator.SetParent(self)
        self.separator.SetPosition(8, self.height // 2)
        self.separator.SetSize(self.width - 16, 1)
        self.separator.SetColor(0x22FFFFFF)
        self.separator.AddFlag("not_pick")
        self.separator.Show()

        # Titolo
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(self.width // 2, 10)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(self.currentColor)
        self.titleText.SetOutline()
        self.titleText.Show()

        # Messaggio
        self.messageText = ui.TextLine()
        self.messageText.SetParent(self)
        self.messageText.SetPosition(self.width // 2, 33)
        self.messageText.SetHorizontalAlignCenter()
        self.messageText.SetText("")
        self.messageText.SetPackedFontColor(0xFFEEEEEE)
        self.messageText.Show()

        self.Hide()
    
    def SetColor(self, color):
        """Imposta il colore del popup"""
        self.currentColor = color
        self.borderTop.SetColor(color)
        self.borderBottom.SetColor(color)
        self.titleText.SetPackedFontColor(color)
        if hasattr(self, 'leftAccent'):
            self.leftAccent.SetColor(color)
        if hasattr(self, 'rightAccent'):
            self.rightAccent.SetColor((color & 0x00FFFFFF) | 0x55000000)
    
    def SetColorFromScheme(self, colorCode):
        """Imposta colore da codice schema (GREEN, BLUE, etc.)"""
        scheme = GetColorScheme(colorCode)
        self.SetColor(scheme.get("border", 0xFFFFFFFF))
    
    def ShowPopup(self, title, message, colorCode=None, duration=3.0):
        """Mostra un popup (aggiunge alla coda se già visibile)"""
        if colorCode:
            scheme = GetColorScheme(colorCode)
            color = scheme.get("border", self.currentColor)
        else:
            color = self.currentColor
        
        # Aggiungi alla coda
        self.messageQueue.append({
            "title": title.replace("+", " "),
            "message": message.replace("+", " "),
            "color": color,
            "duration": duration
        })
        
        # Se non c'è messaggio corrente, mostra subito
        if not self.currentMessage:
            self.__ShowNext()
    
    def ShowProgress(self, title, current, target, colorCode=None):
        """Mostra popup con progresso"""
        message = "%d / %d" % (current, target)
        self.ShowPopup(title, message, colorCode, 3.0)
    
    def __ShowNext(self):
        """Mostra il prossimo messaggio in coda"""
        if len(self.messageQueue) > 0:
            data = self.messageQueue.pop(0)
            
            self.SetColor(data["color"])
            self.titleText.SetText(data["title"])
            self.messageText.SetText(data["message"])
            
            self.currentMessage = data
            self.endTime = app.GetTime() + data["duration"]
            
            self.Show()
            self.SetTop()
        else:
            self.currentMessage = None
    
    def OnUpdate(self):
        if self.endTime > 0 and app.GetTime() > self.endTime:
            self.Hide()
            self.endTime = 0
            self.currentMessage = None
            # Mostra il prossimo se c'è
            self.__ShowNext()
    
    def ClearQueue(self):
        """Svuota la coda messaggi"""
        self.messageQueue = []
        self.Hide()
        self.currentMessage = None
        self.endTime = 0


# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL POPUP INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════
g_systemPopup = None

def GetSystemPopup():
    """Ritorna l'istanza globale del popup"""
    global g_systemPopup
    if g_systemPopup is None:
        g_systemPopup = SystemPopup()
    return g_systemPopup

def ShowSystemPopup(title, message, colorCode=None, duration=3.0):
    """Mostra un popup di sistema"""
    GetSystemPopup().ShowPopup(title, message, colorCode, duration)

def ShowProgressPopup(title, current, target, colorCode=None):
    """Mostra un popup di progresso"""
    GetSystemPopup().ShowProgress(title, current, target, colorCode)

def HideSystemPopup():
    """Nasconde il popup corrente e svuota la coda"""
    GetSystemPopup().ClearQueue()
