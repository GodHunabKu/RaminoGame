# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════════════════
#  HUNTER SYSTEM - MAIN MODULE
#  Import unificato per tutto il sistema Hunter stile Solo Leveling
# ═══════════════════════════════════════════════════════════════════════════════
#
#  STRUTTURA MODULI:
#  -----------------
#  hunter_core.py        - Configurazioni, costanti, colori, DraggableMixin
#  hunter_components.py  - Componenti UI riutilizzabili (progress bar, popup)
#  hunter_windows.py     - Finestre principali (WhatIf, SystemMessage, etc)
#  hunter_effects.py     - Effetti fullscreen (BossAlert, Awakening, RankUp)
#  hunter_missions.py    - Sistema missioni ed eventi
#  hunter.py             - QUESTO FILE: import unificato
#
#  USO:
#  ----
#  from hunter import ShowSystemMessage, OpenDailyMissions, ShowAwakening
#
# ═══════════════════════════════════════════════════════════════════════════════

# =============================================================================
# CORE - Configurazioni e Utility
# =============================================================================
from hunter_core import (
    # Costanti
    WINDOW_POSITIONS,
    RANK_COLORS,
    RANK_NAMES,
    RANK_TITLES,
    RANK_QUOTES,
    COLOR_SCHEMES,
    FRACTURE_ID_MAP,
    RANK_THEMES,
    AWAKENING_CONFIG,
    
    # Mixin
    DraggableMixin,
    
    # Utility
    FormatTime,
    FormatNumber,
    GetRankKey,
    GetColorScheme,
    GetAwakeningConfig,
    IsAwakeningLevel,
    GetRankTheme,
)

# =============================================================================
# COMPONENTS - Componenti UI Riutilizzabili
# =============================================================================
from hunter_components import (
    AnimatedProgressBar,
    SoloLevelingButton,
    SystemButton,
    SoloLevelingWindow,
    SystemPopup,
    
    # Public API components
    ShowSystemPopup,
    HideSystemPopup,
)

# =============================================================================
# WINDOWS - Finestre Principali
# =============================================================================
from hunter_windows import (
    # Classi
    WhatIfChoiceWindow,
    SystemMessageWindow,
    EmergencyQuestWindow,
    EventStatusWindow,
    RivalTrackerWindow,
    OvertakeWindow,
    
    # Getter istanze
    GetWhatIfChoiceWindow,
    GetSystemMessageWindow,
    GetEmergencyQuestWindow,
    GetEventStatusWindow,
    GetRivalTrackerWindow,
    GetOvertakeWindow,
    
    # Public API windows
    ShowSystemMessage,
    ShowEmergencyQuest,
    ShowEventStatus,
    ShowRivalTracker,
    ShowOvertake,
    OpenWhatIfChoice,
)

# =============================================================================
# EFFECTS - Effetti Fullscreen
# =============================================================================
from hunter_effects import (
    # Classi
    BossAlertWindow,
    SystemInitWindow,
    AwakeningEffect,
    RankUpEffect,
    
    # Getter istanze
    GetBossAlertWindow,
    GetSystemInitWindow,
    GetAwakeningEffect,
    GetRankUpEffect,
    
    # Public API effects
    ShowBossAlert,
    ShowSystemInit,
    ShowAwakening,
    ShowRankUp,
    CheckAndShowAwakening,
)

# =============================================================================
# MISSIONS - Sistema Missioni ed Eventi
# =============================================================================
from hunter_missions import (
    # Classi
    DailyMissionsWindow,
    MissionProgressPopup,
    MissionCompleteWindow,
    AllMissionsCompleteWindow,
    EventSlotHoverArea,
    EventsScheduleWindow,
    
    # Getter istanze
    GetDailyMissionsWindow,
    GetMissionProgressPopup,
    GetMissionCompleteWindow,
    GetAllMissionsCompleteWindow,
    GetEventsScheduleWindow,
    
    # Public API missions
    OpenDailyMissions,
    ShowMissionProgress,
    ShowMissionComplete,
    ShowAllMissionsComplete,
    OpenEventsSchedule,
)


# =============================================================================
# CONVENIENCE API - Funzioni di alto livello
# =============================================================================

def InitHunterSystem(callback=None):
    """
    Inizializza il sistema Hunter con animazione.
    Da chiamare al login del giocatore.
    
    Args:
        callback: Funzione da chiamare quando l'inizializzazione e' completa
    """
    ShowSystemInit(callback)


def ShowLevelUp(level):
    """
    Gestisce il level up con eventuale awakening.
    
    Args:
        level: Nuovo livello raggiunto
        
    Returns:
        True se e' stato mostrato un awakening, False altrimenti
    """
    return CheckAndShowAwakening(level)


def NotifyRankUp(oldRank, newRank):
    """
    Notifica una promozione di rango.
    
    Args:
        oldRank: Rango precedente (es. "E", "D", "C", ...)
        newRank: Nuovo rango
    """
    ShowRankUp(oldRank, newRank)


def NotifyMissionProgress(missionName, current, target, theme=None):
    """
    Notifica progresso di una missione.
    
    Args:
        missionName: Nome della missione
        current: Progresso attuale
        target: Obiettivo
        theme: Tema colori (opzionale)
    """
    ShowMissionProgress(missionName, current, target, theme)


def NotifyMissionComplete(missionName, reward, theme=None):
    """
    Notifica completamento di una missione.
    
    Args:
        missionName: Nome della missione completata
        reward: Gloria guadagnata
        theme: Tema colori (opzionale)
    """
    ShowMissionComplete(missionName, reward, theme)


def NotifyAllMissionsComplete(bonusGlory, theme=None, hasFractureBonus=False):
    """
    Notifica completamento di tutte le missioni giornaliere.
    
    Args:
        bonusGlory: Gloria bonus guadagnata
        theme: Tema colori (opzionale)
        hasFractureBonus: Se attivo il bonus fratture +50%
    """
    ShowAllMissionsComplete(bonusGlory, theme, hasFractureBonus)


def NotifyBossSpawn(bossName=""):
    """
    Notifica spawn di un boss.
    
    Args:
        bossName: Nome del boss (opzionale)
    """
    ShowBossAlert(bossName)


# =============================================================================
# VERSION INFO
# =============================================================================
HUNTER_VERSION = "2.0.0"
HUNTER_STYLE = "Solo Leveling"


def GetVersion():
    """Ritorna la versione del sistema Hunter"""
    return HUNTER_VERSION


def GetStyle():
    """Ritorna lo stile grafico (Solo Leveling)"""
    return HUNTER_STYLE
