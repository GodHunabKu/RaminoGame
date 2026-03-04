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
    COLOR_BG_DARK, COLOR_BG_DARK2, COLOR_BG_INNER,
    COLOR_TEXT_NORMAL, COLOR_TEXT_MUTED, COLOR_TEXT_DIM,
    COLOR_SEPARATOR, COLOR_SEPARATOR_BRIGHT,
    COLOR_GOLD, COLOR_GOLD_DIM, COLOR_SYSTEM_BLUE, COLOR_SYSTEM_CYAN,
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
        # Background scuro profondo con bordo interno
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(self.width, self.height)
        self.bg.SetColor(0xFF060610)
        self.bg.AddFlag("not_pick")
        self.bg.Show()

        # Inner bg (per effetto profondità)
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(1, 1)
        self.bgInner.SetSize(self.width - 2, self.height - 2)
        self.bgInner.SetColor(0xFF040408)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # Bordi esterni – colore dinamico
        self.border = ui.Bar()
        self.border.SetParent(self)
        self.border.SetPosition(0, 0)
        self.border.SetSize(self.width, 1)
        self.border.SetColor(0xFF333355)
        self.border.AddFlag("not_pick")
        self.border.Show()

        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, self.height - 1)
        self.borderBottom.SetSize(self.width, 1)
        self.borderBottom.SetColor(0xFF222233)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()

        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(1, self.height)
        self.borderLeft.SetColor(0xFF282838)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(self.width - 1, 0)
        self.borderRight.SetSize(1, self.height)
        self.borderRight.SetColor(0xFF282838)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        # Angoli decorativi stile Solo Leveling (L-brackets lunghi e doppi)
        tickLen = 8
        tickColor = 0xFF444466
        # Outer corners
        self.ctlH = ui.Bar(); self.ctlH.SetParent(self); self.ctlH.SetPosition(0, 0); self.ctlH.SetSize(tickLen, 1); self.ctlH.SetColor(tickColor); self.ctlH.AddFlag("not_pick"); self.ctlH.Show()
        self.ctlV = ui.Bar(); self.ctlV.SetParent(self); self.ctlV.SetPosition(0, 0); self.ctlV.SetSize(1, tickLen); self.ctlV.SetColor(tickColor); self.ctlV.AddFlag("not_pick"); self.ctlV.Show()
        self.ctrH = ui.Bar(); self.ctrH.SetParent(self); self.ctrH.SetPosition(self.width - tickLen, 0); self.ctrH.SetSize(tickLen, 1); self.ctrH.SetColor(tickColor); self.ctrH.AddFlag("not_pick"); self.ctrH.Show()
        self.ctrV = ui.Bar(); self.ctrV.SetParent(self); self.ctrV.SetPosition(self.width - 1, 0); self.ctrV.SetSize(1, tickLen); self.ctrV.SetColor(tickColor); self.ctrV.AddFlag("not_pick"); self.ctrV.Show()
        self.cblH = ui.Bar(); self.cblH.SetParent(self); self.cblH.SetPosition(0, self.height - 1); self.cblH.SetSize(tickLen, 1); self.cblH.SetColor(tickColor); self.cblH.AddFlag("not_pick"); self.cblH.Show()
        self.cblV = ui.Bar(); self.cblV.SetParent(self); self.cblV.SetPosition(0, self.height - tickLen); self.cblV.SetSize(1, tickLen); self.cblV.SetColor(tickColor); self.cblV.AddFlag("not_pick"); self.cblV.Show()
        self.cbrH = ui.Bar(); self.cbrH.SetParent(self); self.cbrH.SetPosition(self.width - tickLen, self.height - 1); self.cbrH.SetSize(tickLen, 1); self.cbrH.SetColor(tickColor); self.cbrH.AddFlag("not_pick"); self.cbrH.Show()
        self.cbrV = ui.Bar(); self.cbrV.SetParent(self); self.cbrV.SetPosition(self.width - 1, self.height - tickLen); self.cbrV.SetSize(1, tickLen); self.cbrV.SetColor(tickColor); self.cbrV.AddFlag("not_pick"); self.cbrV.Show()

        # Progress fill con padding raffinato
        self.fill = ui.Bar()
        self.fill.SetParent(self)
        self.fill.SetPosition(2, 2)
        self.fill.SetSize(0, self.height - 4)
        self.fill.SetColor(self.color)
        self.fill.AddFlag("not_pick")
        self.fill.Show()

        # Highlight interno top (riga luminosa nella parte alta – depth effect)
        self.innerHL = ui.Bar()
        self.innerHL.SetParent(self)
        self.innerHL.SetPosition(2, 2)
        self.innerHL.SetSize(0, 2)
        self.innerHL.SetColor(0x30FFFFFF)
        self.innerHL.AddFlag("not_pick")
        self.innerHL.Show()

        # Bottom shadow del fill (effetto 3D)
        self.fillShadow = ui.Bar()
        self.fillShadow.SetParent(self)
        self.fillShadow.SetPosition(2, self.height - 4)
        self.fillShadow.SetSize(0, 2)
        self.fillShadow.SetColor(0x20000000)
        self.fillShadow.AddFlag("not_pick")
        self.fillShadow.Show()

        # Glow overlay (pulsing – alpha basso, non epilettico)
        self.glow = ui.Bar()
        self.glow.SetParent(self)
        self.glow.SetPosition(2, 2)
        self.glow.SetSize(0, self.height - 4)
        self.glow.SetColor(0x00FFFFFF)
        self.glow.AddFlag("not_pick")
        self.glow.Show()

        # Shimmer (linea brillante che scorre nel fill da sx a dx)
        self.shimmer = ui.Bar()
        self.shimmer.SetParent(self)
        self.shimmer.SetPosition(2, 2)
        self.shimmer.SetSize(4, self.height - 4)
        self.shimmer.SetColor(0x00FFFFFF)
        self.shimmer.AddFlag("not_pick")
        self.shimmer.Show()

        # Text overlay centrato
        self.text = ui.TextLine()
        self.text.SetParent(self)
        self.text.SetPosition(self.width // 2, 2)
        self.text.SetHorizontalAlignCenter()
        self.text.SetText("")
        self.text.SetPackedFontColor(0xFFDDDDFF)
        self.text.SetOutline()
        self.text.Show()

        self.shimmerPhase = 0.0
    
    def SetSize(self, w, h):
        ui.Window.SetSize(self, w, h)
        self.width = w
        self.height = h
        self.bg.SetSize(w, h)
        self.border.SetSize(w, 1)
        if hasattr(self, 'bgInner'):
            self.bgInner.SetSize(w - 2, h - 2)
        if hasattr(self, 'borderBottom'):
            self.borderBottom.SetSize(w, 1)
            self.borderBottom.SetPosition(0, h - 1)
            self.borderLeft.SetSize(1, h)
            self.borderRight.SetSize(1, h)
            self.borderRight.SetPosition(w - 1, 0)
        # Aggiorna corner ticks
        tickLen = 8
        if hasattr(self, 'ctrH'):
            self.ctrH.SetPosition(w - tickLen, 0)
            self.ctrV.SetPosition(w - 1, 0)
            self.cblH.SetPosition(0, h - 1)
            self.cblV.SetPosition(0, h - tickLen)
            self.cbrH.SetPosition(w - tickLen, h - 1)
            self.cbrV.SetPosition(w - 1, h - tickLen)
        if hasattr(self, 'fillShadow'):
            self.fillShadow.SetPosition(2, h - 4)
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
        """Imposta il colore della barra aggiornando fill, bordi e corner ticks"""
        self.color = color
        self.fill.SetColor(color)
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        tickColor = 0xFF000000 | ((r // 3) << 16) | ((g // 3) << 8) | (b // 3)
        borderColor = 0xFF000000 | ((r // 5) << 16) | ((g // 5) << 8) | (b // 5)
        if hasattr(self, 'border'):
            self.border.SetColor(borderColor)
            self.borderBottom.SetColor(borderColor)
            self.borderLeft.SetColor(borderColor)
            self.borderRight.SetColor(borderColor)
        if hasattr(self, 'ctlH'):
            self.ctlH.SetColor(tickColor); self.ctlV.SetColor(tickColor)
            self.ctrH.SetColor(tickColor); self.ctrV.SetColor(tickColor)
            self.cblH.SetColor(tickColor); self.cblV.SetColor(tickColor)
            self.cbrH.SetColor(tickColor); self.cbrV.SetColor(tickColor)

    def __UpdateFill(self):
        fillWidth = int((self.width - 4) * self.progress)
        fw = max(0, fillWidth)
        fh = self.height - 4
        self.fill.SetSize(fw, fh)
        self.glow.SetSize(fw, fh)
        if hasattr(self, 'innerHL'):
            self.innerHL.SetSize(fw, 2)
        if hasattr(self, 'fillShadow'):
            self.fillShadow.SetSize(fw, 2)

    def OnUpdate(self):
        # Smooth animation
        if abs(self.progress - self.targetProgress) > 0.001:
            self.progress += (self.targetProgress - self.progress) * 0.1
            self.__UpdateFill()

        # Shimmer elegante che scorre nel fill da sx a dx
        if hasattr(self, 'shimmerPhase'):
            self.shimmerPhase += 0.007
            if self.shimmerPhase > 1.0:
                self.shimmerPhase -= 1.0
            fillW = int((self.width - 4) * self.progress)
            if fillW > 8:
                sx = 2 + int(self.shimmerPhase * (fillW - 6))
                self.shimmer.SetPosition(sx, 2)
                shimmerAlpha = int((math.sin(self.shimmerPhase * math.pi) * 0.7 + 0.3) * 40)
                self.shimmer.SetColor((shimmerAlpha << 24) | 0xFFFFFF)
            else:
                self.shimmer.SetColor(0x00FFFFFF)

        # Glow pulsante lento (0.3 Hz circa – non epilettico, alpha massimo 28)
        self.glowPhase += 0.028
        glowAlpha = int((math.sin(self.glowPhase) * 0.5 + 0.5) * 28)
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

        borderColor = theme.get("border", 0xFF00CCFF)
        accentDim = (borderColor & 0x00FFFFFF) | 0x44000000
        accentDimmer = (borderColor & 0x00FFFFFF) | 0x22000000

        # Background scuro principale
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(width, height)
        self.bgBar.SetColor(theme.get("btn_normal", 0xFF0E0E1A))
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()

        # Inner background (gradiente simulato – più chiaro in cima)
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(3, 2)
        self.bgInner.SetSize(width - 6, height // 2)
        self.bgInner.SetColor(0x08FFFFFF)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # Bordo superiore (2px - più spesso, più visibile)
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(width, 2)
        self.borderTop.SetColor(borderColor)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        # Bordo inferiore (1px - più sottile, effetto profondità)
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, height - 1)
        self.borderBottom.SetSize(width, 1)
        self.borderBottom.SetColor(accentDim)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()

        # Bordi laterali (1px sottili)
        self.borderLeft = ui.Bar()
        self.borderLeft.SetParent(self)
        self.borderLeft.SetPosition(0, 0)
        self.borderLeft.SetSize(1, height)
        self.borderLeft.SetColor(accentDim)
        self.borderLeft.AddFlag("not_pick")
        self.borderLeft.Show()

        self.borderRight = ui.Bar()
        self.borderRight.SetParent(self)
        self.borderRight.SetPosition(width - 1, 0)
        self.borderRight.SetSize(1, height)
        self.borderRight.SetColor(accentDim)
        self.borderRight.AddFlag("not_pick")
        self.borderRight.Show()

        # Left accent bar (barra verticale neon sx – iconica stile Solo Leveling)
        self.leftAccent = ui.Bar()
        self.leftAccent.SetParent(self)
        self.leftAccent.SetPosition(0, 0)
        self.leftAccent.SetSize(4, height)
        self.leftAccent.SetColor(borderColor)
        self.leftAccent.AddFlag("not_pick")
        self.leftAccent.Show()

        # Corner ticks decorativi (più lunghi, più eleganti)
        tickLen = 8
        self.btnCtlH = ui.Bar(); self.btnCtlH.SetParent(self); self.btnCtlH.SetPosition(4, 0); self.btnCtlH.SetSize(tickLen, 1); self.btnCtlH.SetColor(borderColor); self.btnCtlH.AddFlag("not_pick"); self.btnCtlH.Show()
        self.btnCtrH = ui.Bar(); self.btnCtrH.SetParent(self); self.btnCtrH.SetPosition(width - tickLen - 1, 0); self.btnCtrH.SetSize(tickLen, 1); self.btnCtrH.SetColor(borderColor); self.btnCtrH.AddFlag("not_pick"); self.btnCtrH.Show()
        self.btnCtrV = ui.Bar(); self.btnCtrV.SetParent(self); self.btnCtrV.SetPosition(width - 1, 0); self.btnCtrV.SetSize(1, tickLen); self.btnCtrV.SetColor(borderColor); self.btnCtrV.AddFlag("not_pick"); self.btnCtrV.Show()
        self.btnCblH = ui.Bar(); self.btnCblH.SetParent(self); self.btnCblH.SetPosition(4, height - 1); self.btnCblH.SetSize(tickLen, 1); self.btnCblH.SetColor(accentDim); self.btnCblH.AddFlag("not_pick"); self.btnCblH.Show()
        self.btnCbrH = ui.Bar(); self.btnCbrH.SetParent(self); self.btnCbrH.SetPosition(width - tickLen - 1, height - 1); self.btnCbrH.SetSize(tickLen, 1); self.btnCbrH.SetColor(accentDim); self.btnCbrH.AddFlag("not_pick"); self.btnCbrH.Show()
        self.btnCbrV = ui.Bar(); self.btnCbrV.SetParent(self); self.btnCbrV.SetPosition(width - 1, height - tickLen); self.btnCbrV.SetSize(1, tickLen); self.btnCbrV.SetColor(accentDim); self.btnCbrV.AddFlag("not_pick"); self.btnCbrV.Show()

        # Testo centrato con outline
        self.textLine = ui.TextLine()
        self.textLine.SetParent(self)
        self.textLine.SetPosition(width // 2 + 2, (height - 14) // 2)
        self.textLine.SetHorizontalAlignCenter()
        self.textLine.SetText(text)
        self.textLine.SetPackedFontColor(theme.get("text_title", 0xFFEEEEFF))
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
        """Aggiorna il tema colori di tutti gli elementi del bottone"""
        self.theme = theme
        borderColor = theme.get("border", 0xFF00CCFF)
        accentDim = (borderColor & 0x00FFFFFF) | 0x44000000
        if hasattr(self, 'borderTop'):
            self.borderTop.SetColor(borderColor)
            self.borderBottom.SetColor(accentDim)
            self.borderLeft.SetColor(accentDim)
            self.borderRight.SetColor(accentDim)
            self.bgBar.SetColor(theme.get("btn_normal", 0xFF0E0E1A))
            self.textLine.SetPackedFontColor(theme.get("text_title", 0xFFEEEEFF))
        if hasattr(self, 'leftAccent'):
            self.leftAccent.SetColor(borderColor)
        if hasattr(self, 'btnCtlH'):
            self.btnCtlH.SetColor(borderColor)
            self.btnCtrH.SetColor(borderColor)
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
        # Sfondo principale – profondo blu-nero
        self.bg = ui.Bar()
        self.bg.SetParent(self)
        self.bg.SetPosition(0, 0)
        self.bg.SetSize(w, h)
        self.bg.SetColor(COLOR_BG_DARK)
        self.bg.Show()

        # Layer interno più chiaro (profondità e texture)
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(2, 2)
        self.bgInner.SetSize(w - 4, h - 4)
        self.bgInner.SetColor(0x0C0808FF)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # Top highlight (effetto gradiente cima)
        self.topHighlight = ui.Bar()
        self.topHighlight.SetParent(self)
        self.topHighlight.SetPosition(3, 3)
        self.topHighlight.SetSize(w - 6, 2)
        self.topHighlight.SetColor(0x12FFFFFF)
        self.topHighlight.AddFlag("not_pick")
        self.topHighlight.Show()

        # Bordi principali (Top spesso 2px, altri 1px per asimmetria elegante)
        self.borders = []
        # Top (2px – più visibile)
        b1 = ui.Bar(); b1.SetParent(self); b1.SetPosition(0, 0); b1.SetSize(w, 2); b1.Show()
        # Bottom (2px)
        b2 = ui.Bar(); b2.SetParent(self); b2.SetPosition(0, h - 2); b2.SetSize(w, 2); b2.Show()
        # Left (2px)
        b3 = ui.Bar(); b3.SetParent(self); b3.SetPosition(0, 0); b3.SetSize(2, h); b3.Show()
        # Right (1px – più sottile, asimmetrico)
        b4 = ui.Bar(); b4.SetParent(self); b4.SetPosition(w - 1, 0); b4.SetSize(1, h); b4.Show()
        self.borders = [b1, b2, b3, b4]

        # Corner ticks DOPPI – stile Solo Leveling definitivo (L-brackets grandi)
        self.cornerTicks = []
        tickOuter = 12  # Bracket esterno (lungo)
        tickInner = 6   # Bracket interno (corto, offset)
        for (cx, cy, cw, ch) in [
            # Top-Left outer L
            (2, 0, tickOuter, 1), (0, 2, 1, tickOuter),
            # Top-Left inner L (offset di 3px – doppio bracket)
            (5, 3, tickInner, 1), (3, 5, 1, tickInner),
            # Top-Right outer L
            (w - tickOuter - 2, 0, tickOuter, 1), (w - 1, 2, 1, tickOuter),
            # Top-Right inner L
            (w - tickInner - 5, 3, tickInner, 1), (w - 4, 5, 1, tickInner),
            # Bottom-Left outer L
            (2, h - 1, tickOuter, 1), (0, h - tickOuter - 2, 1, tickOuter),
            # Bottom-Left inner L
            (5, h - 4, tickInner, 1), (3, h - tickInner - 5, 1, tickInner),
            # Bottom-Right outer L
            (w - tickOuter - 2, h - 1, tickOuter, 1), (w - 1, h - tickOuter - 2, 1, tickOuter),
            # Bottom-Right inner L
            (w - tickInner - 5, h - 4, tickInner, 1), (w - 4, h - tickInner - 5, 1, tickInner),
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
        """Aggiorna i colori di bordi, angoli e highlight"""
        borderColor = self.color_scheme.get("border", 0xFFFFFFFF)
        r = (borderColor >> 16) & 0xFF
        g = (borderColor >> 8) & 0xFF
        b = borderColor & 0xFF
        # Bordi con asimmetria: top/left brillanti, bottom/right attenuati
        outerBright = borderColor
        outerDim = 0xFF000000 | ((r * 3 // 4) << 16) | ((g * 3 // 4) << 8) | (b * 3 // 4)
        if hasattr(self, 'borders') and len(self.borders) == 4:
            self.borders[0].SetColor(outerBright)   # Top
            self.borders[1].SetColor(outerDim)      # Bottom
            self.borders[2].SetColor(outerBright)   # Left
            self.borders[3].SetColor(outerDim)      # Right
        # Corner ticks: alternati outer=brillante, inner=attenuato
        innerTickColor = 0xFF000000 | ((r // 2) << 16) | ((g // 2) << 8) | (b // 2)
        if hasattr(self, 'cornerTicks'):
            for i, ct in enumerate(self.cornerTicks):
                # Outer brackets (indici 0,1,4,5,8,9,12,13) = brillanti
                # Inner brackets (indici 2,3,6,7,10,11,14,15) = attenuati
                if i % 4 < 2:
                    ct.SetColor(outerBright)
                else:
                    ct.SetColor(innerTickColor)


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
        w = self.width
        h = self.height

        # Background principale profondo
        self.bgBar = ui.Bar()
        self.bgBar.SetParent(self)
        self.bgBar.SetPosition(0, 0)
        self.bgBar.SetSize(w, h)
        self.bgBar.SetColor(0xF0040410)
        self.bgBar.AddFlag("not_pick")
        self.bgBar.Show()

        # Inner background (per profondità)
        self.bgInner = ui.Bar()
        self.bgInner.SetParent(self)
        self.bgInner.SetPosition(5, 2)
        self.bgInner.SetSize(w - 10, h - 4)
        self.bgInner.SetColor(0x10060618)
        self.bgInner.AddFlag("not_pick")
        self.bgInner.Show()

        # Top highlight sottile
        self.topHL = ui.Bar()
        self.topHL.SetParent(self)
        self.topHL.SetPosition(6, 3)
        self.topHL.SetSize(w - 12, 1)
        self.topHL.SetColor(0x15FFFFFF)
        self.topHL.AddFlag("not_pick")
        self.topHL.Show()

        # Bordo superiore (2px – principale)
        self.borderTop = ui.Bar()
        self.borderTop.SetParent(self)
        self.borderTop.SetPosition(0, 0)
        self.borderTop.SetSize(w, 2)
        self.borderTop.SetColor(self.currentColor)
        self.borderTop.AddFlag("not_pick")
        self.borderTop.Show()

        # Bordo inferiore (1px – più sottile)
        self.borderBottom = ui.Bar()
        self.borderBottom.SetParent(self)
        self.borderBottom.SetPosition(0, h - 1)
        self.borderBottom.SetSize(w, 1)
        self.borderBottom.SetColor((self.currentColor & 0x00FFFFFF) | 0x66000000)
        self.borderBottom.AddFlag("not_pick")
        self.borderBottom.Show()

        # Left accent bar (barra neon sx – 5px, iconica)
        self.leftAccent = ui.Bar()
        self.leftAccent.SetParent(self)
        self.leftAccent.SetPosition(0, 2)
        self.leftAccent.SetSize(5, h - 4)
        self.leftAccent.SetColor(self.currentColor)
        self.leftAccent.AddFlag("not_pick")
        self.leftAccent.Show()

        # Right accent bar (1px sottile speculare)
        self.rightAccent = ui.Bar()
        self.rightAccent.SetParent(self)
        self.rightAccent.SetPosition(w - 1, 2)
        self.rightAccent.SetSize(1, h - 4)
        self.rightAccent.SetColor((self.currentColor & 0x00FFFFFF) | 0x44000000)
        self.rightAccent.AddFlag("not_pick")
        self.rightAccent.Show()

        # Corner ticks decorativi (4 angoli)
        tickLen = 8
        c = self.currentColor
        self.popCorners = []
        for (cx, cy, cw, ch) in [
            (5, 0, tickLen, 1), (0, 2, 1, tickLen),           # TL
            (w - tickLen - 1, 0, tickLen, 1), (w - 1, 2, 1, tickLen), # TR
            (5, h - 1, tickLen, 1), (0, h - tickLen - 2, 1, tickLen), # BL
            (w - tickLen - 1, h - 1, tickLen, 1), (w - 1, h - tickLen - 2, 1, tickLen), # BR
        ]:
            ct = ui.Bar(); ct.SetParent(self); ct.SetPosition(cx, cy); ct.SetSize(cw, ch); ct.SetColor(c); ct.AddFlag("not_pick"); ct.Show()
            self.popCorners.append(ct)

        # Separatore orizzontale (linea tra titolo e messaggio)
        self.separator = ui.Bar()
        self.separator.SetParent(self)
        self.separator.SetPosition(8, h // 2)
        self.separator.SetSize(w - 16, 1)
        self.separator.SetColor(0x28FFFFFF)
        self.separator.AddFlag("not_pick")
        self.separator.Show()

        # Titolo (colore dinamico basato sul rank/tipo)
        self.titleText = ui.TextLine()
        self.titleText.SetParent(self)
        self.titleText.SetPosition(w // 2, 9)
        self.titleText.SetHorizontalAlignCenter()
        self.titleText.SetText("")
        self.titleText.SetPackedFontColor(self.currentColor)
        self.titleText.SetOutline()
        self.titleText.Show()

        # Messaggio (bianco-blu elegante)
        self.messageText = ui.TextLine()
        self.messageText.SetParent(self)
        self.messageText.SetPosition(w // 2, 33)
        self.messageText.SetHorizontalAlignCenter()
        self.messageText.SetText("")
        self.messageText.SetPackedFontColor(0xFFEEEEEE)
        self.messageText.Show()

        self.Hide()
    
    def SetColor(self, color):
        """Imposta il colore del popup aggiornando tutti gli elementi"""
        self.currentColor = color
        colorDim = (color & 0x00FFFFFF) | 0x55000000
        colorFaint = (color & 0x00FFFFFF) | 0x33000000
        self.borderTop.SetColor(color)
        self.borderBottom.SetColor(colorDim)
        self.titleText.SetPackedFontColor(color)
        if hasattr(self, 'leftAccent'):
            self.leftAccent.SetColor(color)
        if hasattr(self, 'rightAccent'):
            self.rightAccent.SetColor(colorFaint)
        if hasattr(self, 'popCorners'):
            for ct in self.popCorners:
                ct.SetColor(colorDim)
        if hasattr(self, 'separator'):
            self.separator.SetColor((color & 0x00FFFFFF) | 0x22000000)
    
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
#  FRAME BUILDER HELPERS - Riduce drasticamente il numero di ui.Bar() per finestra
#  Ogni finestra usava 20-50 barre individuali. Ora ne usa 8-12.
# ═══════════════════════════════════════════════════════════════════════════════

def BuildFrame(parent, w, h, borderColor, cornerLen=10):
    """
    Costruisce un frame completo Solo Leveling style con elementi minimi.
    Ritorna un dict con tutti gli elementi per aggiornamento colori successivo.

    Elementi creati: bg(1) + borders(4) + corners(4) + accent(1) = 10 totali
    vs i precedenti 20-40 per finestra.
    """
    frame = {"bars": [], "corners": []}

    # Background scuro profondo
    bg = ui.Bar()
    bg.SetParent(parent)
    bg.SetPosition(0, 0)
    bg.SetSize(w, h)
    bg.SetColor(0xF0030310)
    bg.AddFlag("not_pick")
    bg.Show()
    frame["bg"] = bg

    # Bordi: top(2px) + left(2px) brillanti, bottom(1px) + right(1px) attenuati
    dimColor = _DimColor(borderColor, 0.5)

    bTop = ui.Bar(); bTop.SetParent(parent); bTop.SetPosition(0, 0); bTop.SetSize(w, 2); bTop.SetColor(borderColor); bTop.AddFlag("not_pick"); bTop.Show()
    bBot = ui.Bar(); bBot.SetParent(parent); bBot.SetPosition(0, h-1); bBot.SetSize(w, 1); bBot.SetColor(dimColor); bBot.AddFlag("not_pick"); bBot.Show()
    bLeft = ui.Bar(); bLeft.SetParent(parent); bLeft.SetPosition(0, 0); bLeft.SetSize(2, h); bLeft.SetColor(borderColor); bLeft.AddFlag("not_pick"); bLeft.Show()
    bRight = ui.Bar(); bRight.SetParent(parent); bRight.SetPosition(w-1, 0); bRight.SetSize(1, h); bRight.SetColor(dimColor); bRight.AddFlag("not_pick"); bRight.Show()
    frame["borders"] = [bTop, bBot, bLeft, bRight]

    # Left accent bar (3px, colore pieno - signature Solo Leveling)
    accent = ui.Bar()
    accent.SetParent(parent)
    accent.SetPosition(0, 2)
    accent.SetSize(3, h - 3)
    accent.SetColor(borderColor)
    accent.AddFlag("not_pick")
    accent.Show()
    frame["accent"] = accent

    # Corner L-brackets (solo 4 angoli, puliti e precisi)
    cL = cornerLen
    cornerDim = _DimColor(borderColor, 0.6)
    for (cx, cy, cw, ch) in [
        (3, 2, cL, 1), (w-cL-1, 2, cL, 1),       # Top-L, Top-R
        (3, h-2, cL, 1), (w-cL-1, h-2, cL, 1),    # Bot-L, Bot-R
    ]:
        ct = ui.Bar(); ct.SetParent(parent); ct.SetPosition(cx, cy); ct.SetSize(cw, ch); ct.SetColor(cornerDim); ct.AddFlag("not_pick"); ct.Show()
        frame["corners"].append(ct)

    return frame


def BuildFrameWithHeader(parent, w, h, borderColor, headerText, headerH=24, cornerLen=10):
    """
    Frame completo + header bar con titolo.
    Ritorna frame dict + headerBg + headerLabel.
    """
    frame = BuildFrame(parent, w, h, borderColor, cornerLen)

    # Header background
    hBg = ui.Bar()
    hBg.SetParent(parent)
    hBg.SetPosition(2, 2)
    hBg.SetSize(w - 3, headerH)
    hBg.SetColor(_DimColor(borderColor, 0.15) | 0xAA000000)
    hBg.AddFlag("not_pick")
    hBg.Show()
    frame["headerBg"] = hBg

    # Header text
    hText = ui.TextLine()
    hText.SetParent(parent)
    hText.SetPosition(w // 2, (headerH - 14) // 2 + 2)
    hText.SetHorizontalAlignCenter()
    hText.SetText(headerText)
    hText.SetPackedFontColor(borderColor)
    hText.SetOutline()
    hText.AddFlag("not_pick")
    hText.Show()
    frame["headerText"] = hText

    # Separator sotto header
    sep = ui.Bar()
    sep.SetParent(parent)
    sep.SetPosition(6, headerH + 3)
    sep.SetSize(w - 12, 1)
    sep.SetColor(_DimColor(borderColor, 0.3))
    sep.AddFlag("not_pick")
    sep.Show()
    frame["headerSep"] = sep

    return frame


def UpdateFrameColors(frame, borderColor):
    """Aggiorna tutti i colori di un frame costruito con BuildFrame."""
    dimColor = _DimColor(borderColor, 0.5)
    cornerDim = _DimColor(borderColor, 0.6)

    if "borders" in frame:
        borders = frame["borders"]
        if len(borders) == 4:
            borders[0].SetColor(borderColor)   # Top
            borders[1].SetColor(dimColor)       # Bottom
            borders[2].SetColor(borderColor)    # Left
            borders[3].SetColor(dimColor)       # Right

    if "accent" in frame:
        frame["accent"].SetColor(borderColor)

    if "corners" in frame:
        for ct in frame["corners"]:
            ct.SetColor(cornerDim)

    if "headerBg" in frame:
        frame["headerBg"].SetColor(_DimColor(borderColor, 0.15) | 0xAA000000)

    if "headerText" in frame:
        frame["headerText"].SetPackedFontColor(borderColor)

    if "headerSep" in frame:
        frame["headerSep"].SetColor(_DimColor(borderColor, 0.3))


def BuildProgressBar(parent, x, y, w, h, barColor):
    """
    Progress bar compatta Solo Leveling style.
    Ritorna dict con bg, fill, text per aggiornamento.
    Solo 3 elementi vs i precedenti 12+.
    """
    bar = {}

    # Background
    bg = ui.Bar()
    bg.SetParent(parent)
    bg.SetPosition(x, y)
    bg.SetSize(w, h)
    bg.SetColor(0xFF060614)
    bg.AddFlag("not_pick")
    bg.Show()
    bar["bg"] = bg

    # Fill
    fill = ui.Bar()
    fill.SetParent(parent)
    fill.SetPosition(x + 1, y + 1)
    fill.SetSize(0, h - 2)
    fill.SetColor(barColor)
    fill.AddFlag("not_pick")
    fill.Show()
    bar["fill"] = fill

    # Text overlay
    text = ui.TextLine()
    text.SetParent(parent)
    text.SetPosition(x + w // 2, y + (h - 14) // 2)
    text.SetHorizontalAlignCenter()
    text.SetText("")
    text.SetPackedFontColor(0xFFEEEEFF)
    text.SetOutline()
    text.AddFlag("not_pick")
    text.Show()
    bar["text"] = text

    bar["width"] = w - 2
    bar["color"] = barColor
    return bar


def UpdateProgressBar(bar, current, maximum, showText=True):
    """Aggiorna fill e testo di una progress bar."""
    if maximum > 0:
        ratio = min(1.0, float(current) / float(maximum))
    else:
        ratio = 0.0
    fillW = int(bar["width"] * ratio)
    bar["fill"].SetSize(max(0, fillW), bar["fill"].GetHeight() if hasattr(bar["fill"], 'GetHeight') else 18)
    if showText:
        bar["text"].SetText("%d / %d" % (int(current), int(maximum)))


def BuildSectionLabel(parent, x, y, text, color):
    """Crea una label di sezione stile Solo Leveling (testo + lineetta)."""
    label = ui.TextLine()
    label.SetParent(parent)
    label.SetPosition(x, y)
    label.SetText(text)
    label.SetPackedFontColor(color)
    label.AddFlag("not_pick")
    label.Show()
    return label


def BuildValueRow(parent, x, y, w, labelText, valueText, labelColor=0xFF888899, valueColor=0xFFFFFFFF):
    """Crea una riga label: valore (label a sinistra, valore allineato a destra)."""
    row = {}

    label = ui.TextLine()
    label.SetParent(parent)
    label.SetPosition(x, y)
    label.SetText(labelText)
    label.SetPackedFontColor(labelColor)
    label.AddFlag("not_pick")
    label.Show()
    row["label"] = label

    value = ui.TextLine()
    value.SetParent(parent)
    value.SetPosition(x + w, y)
    value.SetHorizontalAlignRight()
    value.SetText(valueText)
    value.SetPackedFontColor(valueColor)
    value.SetOutline()
    value.AddFlag("not_pick")
    value.Show()
    row["value"] = value

    return row


def _DimColor(color, factor):
    """Attenua un colore mantenendo l'alpha a 0xFF."""
    r = int(((color >> 16) & 0xFF) * factor)
    g = int(((color >> 8) & 0xFF) * factor)
    b = int((color & 0xFF) * factor)
    return 0xFF000000 | (min(255, r) << 16) | (min(255, g) << 8) | min(255, b)


def _BrightenColor(color, amount):
    """Schiarisce un colore aggiungendo un valore fisso a R,G,B."""
    r = min(255, ((color >> 16) & 0xFF) + amount)
    g = min(255, ((color >> 8) & 0xFF) + amount)
    b = min(255, (color & 0xFF) + amount)
    return 0xFF000000 | (r << 16) | (g << 8) | b


def PulseBorderColor(borderColor, phase, intensity=0.3):
    """Calcola colore pulsante per bordi. Ritorna il colore modulato."""
    pulse = (math.sin(phase) + 1.0) / 2.0
    r = ((borderColor >> 16) & 0xFF)
    g = ((borderColor >> 8) & 0xFF)
    b = (borderColor & 0xFF)
    factor = (1.0 - intensity) + (pulse * intensity)
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return 0xFF000000 | (r << 16) | (g << 8) | b


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
