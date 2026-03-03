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
# FRACTURE PORTAL - Sistema Preview Fratture con UI Immersiva
# =============================================================================
from hunter_fracture_portal import (
    FracturePortalWindow,
    ParseFracturePreviewData,
    RANK_CONFIG as FRACTURE_RANK_CONFIG,
    FRACTURE_COLORS,
)

# Singleton istanza
_fracturePortalWindow = None

def GetFracturePortalWindow():
    global _fracturePortalWindow
    if _fracturePortalWindow is None:
        _fracturePortalWindow = FracturePortalWindow()
    return _fracturePortalWindow

def ShowFracturePortal(data):
    """
    Mostra la finestra preview frattura.
    data = dict con: name, rank, color, vnum, req_glory, req_power_rank,
                     can_enter, can_force, player_glory, party_power_rank,
                     rewards, seal_bonus
    """
    wnd = GetFracturePortalWindow()
    wnd.ShowPortal(data)

def ShowFracturePortalFromCmd(cmdData):
    """
    Parsa e mostra la finestra da una stringa comando.
    Format: name|rank|color|vnum|req_glory|req_power_rank|can_enter|can_force|player_glory|party_power_rank|seal_bonus|rewards
    """
    data = ParseFracturePreviewData(cmdData)
    if data:
        ShowFracturePortal(data)

def HideFracturePortal():
    """Nasconde la finestra preview frattura"""
    wnd = GetFracturePortalWindow()
    if wnd.IsShow():
        wnd.Hide()

def RestoreGameInterface():
    """
    Ripristina la UI del gioco (taskbar, minimap, etc).
    Chiamata quando la finestra portale si chiude.
    
    IMPORTANTE: Questa funzione deve gestire il caso in cui la FracturePortalWindow
    ha intercettato l'input di una QuestDialog con setskin(NOWINDOW), lasciando
    il QuestCurtain in uno stato inconsistente.
    """
    try:
        import dbg
        
        # STEP 1: Forza chiusura QuestCurtain se esiste
        try:
            import uiQuest
            if hasattr(uiQuest, 'QuestDialog') and hasattr(uiQuest.QuestDialog, 'QuestCurtain'):
                curtain = uiQuest.QuestDialog.QuestCurtain
                if curtain:
                    # Forza chiusura immediata
                    curtain.CurtainMode = -1
                    curtain.Close()
        except Exception as e:
            dbg.TraceError("RestoreGameInterface QuestCurtain cleanup: " + str(e))
        
        # STEP 2: Ripristina la UI del gioco
        global _gameInterface
        if _gameInterface:
            # Mostra le finestre base
            if hasattr(_gameInterface, 'ShowDefaultWindows'):
                _gameInterface.ShowDefaultWindows()
            
            # Mostra i pulsanti quest e whisper che potrebbero essere stati nascosti
            if hasattr(_gameInterface, 'ShowAllQuestButton'):
                try:
                    _gameInterface.ShowAllQuestButton()
                except:
                    pass
            
            if hasattr(_gameInterface, 'ShowAllWhisperButton'):
                try:
                    _gameInterface.ShowAllWhisperButton()
                except:
                    pass
                    
    except Exception as e:
        import dbg
        dbg.TraceError("RestoreGameInterface error: " + str(e))

# Riferimento all'interfaccia di gioco (settato da game.py)
_gameInterface = None

def SetGameInterface(interface):
    """Salva il riferimento all'interfaccia di gioco"""
    global _gameInterface
    _gameInterface = interface
