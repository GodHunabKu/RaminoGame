##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chat
import app
import player
import uiTaskBar
import net
import uiCharacter
import uiInventory
#BONUS CHANGER
import uiBonusChanger
#END OF BONUS CHANGER
import uiDragonSoul
import uiChat
import uiMessenger
import guild
if app.ENABLE_AURA_SYSTEM:
	import uiaura
if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendar
if app.ENABLE_LRN_BATTLE_PASS:
	import uibattlepass

if app.ENABLE_ODLAMKI_SYSTEM:
	import uiOdlamki

if app.ENABLE_LOADING_PERFORMANCE:
	import uiWarpShower

if app.ENABLE_VS_SHOP_SEARCH:
	import uiShopSearch

import uiIkonki
import uibotcontrol

if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
	import uiLegendDamageWindow

# import uiWeeklyRank
import ui
import uiHelp
import uiWhisper
import uiPointReset
import grp
if constInfo.GIFT_CODE_SYSTEM:
	import uigiftcodewindow
import uiShop
import uiBonus
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiWonExchange
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiSelectItem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale
import event
import localeInfo
import uiremoveitem
import uiMarbleShop
import uiCollectWindow
import uiBlend
# ============================================================
# 1. AGGIUNGI QUESTO IMPORT ALL'INIZIO DEL FILE
# ============================================================
import uihunterlevel
import hunter_windows
if app.ENABLE_MOUNT_COSTUME_SYSTEM:
	import uiMount
if app.ENABLE_RESP_SYSTEM:
	import uiresp
if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
	import uiBuffNPC
import uiItemShop
if app.ENABLE_LRN_LOCATION_SYSTEM:
	import uilocation
if app.ENABLE_OFFLINE_SHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop
if app.ENABLE_ACCE_COSTUME_SYSTEM:
	import uiacce
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
import uimapasw
import new_uiWeeklyRank
if app.ENABLE_DUNGEON_INFO_SYSTEM:
	import uiDungeonInfo
if app.ENABLE_NEW_PET_SYSTEM:
	import _Pety
if app.ENABLE_ARTEFAKT_SYSTEM:
	import uiartefaktsystem
if app.ENABLE_MINIMAP_DUNGEONINFO:
	import uiminimapdungeoninfo
if app.__BL_CHEST_DROP_INFO__:
	import uiChestDropInfo
import uiCards
if app.ENABLE_COLLECTIONS_SYSTEM:
	import uiCollections
if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
	import uiPrivateShop
	import uiPrivateShopSearch
import chr

import emoji

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	class NewGoldChat(ui.Window):
		def __init__(self, parent = None, x = 0, y = 0):
			ui.Window.__init__(self)
			self.texts = {}
			self.before_close = app.GetTime() + 5
			self.parent = parent
			self.SpaceBet = 14
			self.maxY = 0
			self.x = x-745
			self.y = y+1
			self.ColorValue = 0xFFFFFFFF
			self.Show()
			
		def GetMaxY(self):
			return self.maxY

		def AddGoldValue(self, text):
			for i in xrange(len(self.texts)):
				if len(self.texts) == 5 and i == 0:
					self.texts[i].Hide()
				x, y = self.texts[i].GetLocalPosition()
				self.texts[i].SetPosition(x, y-self.SpaceBet)

			i = 0
			if len(self.texts) == 5:
				for i in xrange(len(self.texts)-1):
					self.texts[i] = self.texts[i+1]
				i = 4
			else:
				i = len(self.texts)
			
			self.texts[i] = ui.TextLine()
			if self.parent != None:
				self.texts[i].SetParent(self.parent)
			self.texts[i].SetPosition(self.x, self.y)
			self.texts[i].SetPackedFontColor(grp.GenerateColor(255./255, 215./255, 76./255, 1))
			self.texts[i].SetHorizontalAlignLeft()
			self.texts[i].SetOutline(TRUE)
			self.texts[i].SetText(text)
			
			self.texts[i].Show()
			self.before_close = app.GetTime() + 10

			#if self.hide.IsShow():
				#x, y = self.texts[0].GetLocalPosition()
				#x2, y2 = self.hide.GetLocalPosition()
				#self.hide.SetPosition(x2, y+20)

		def ClearAll(self):
			self.Hide()
			self.texts = {}

		def OnRender(self):
			if len(self.texts) > 0:
				x, y = self.texts[0].GetGlobalPosition()
				w, h = self.texts[0].GetTextSize()
				grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
				# grp.RenderBar(x, y+h-6, 108, h*len(self.texts)+5)
				self.BOARD_START_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.0)
				self.BOARD_END_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.8)
				grp.RenderGradationBar(x, y+h-50, 150, h*8, self.BOARD_START_COLOR, self.BOARD_END_COLOR)
				# if len(self.texts) == 0:
				# 	self.Hide()
				
		def OnUpdate(self):
			if app.GetTime() >= self.before_close:
				for i in xrange(len(self.texts)):
					if len(self.texts) > 0 and i == 0:
						self.texts[i].Hide()
						self.texts = {}
					if i == 0:
						return
					x, y = self.texts[i].GetLocalPosition()
					self.texts[i].SetPosition(x, y-self.SpaceBet)

				i = 0
				if len(self.texts) == 5:
					for i in xrange(len(self.texts)-1):
						self.texts[i] = self.texts[i+1]
					i = 4
				else:
					i = len(self.texts)
				
				# self.texts[i] = ui.TextLine()
				# if self.parent != None:
				# 	self.texts[i].SetParent(self.parent)
				# self.texts[i].SetPosition(self.x, self.y)
				# self.texts[i].SetPackedFontColor(grp.GenerateColor(255./255, 200./255, 200./255, 1))
				# self.texts[i].SetHorizontalAlignLeft()
				# self.texts[i].SetOutline(TRUE)
				# self.texts[i].SetText("")

				# self.texts[i].Hide()

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.onTopWindow = player.ON_TOP_WND_NONE
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None
		self.wndWeb = None
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.wndCubeRenewal = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.yangText = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = None
		if app.ENABLE_COLLECTIONS_SYSTEM:
			self.wndCollections = None
		self.wndGuildBuilding = None
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = None
		self.wndRemoveItem = None
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory = None
		if app.ENABLE_RESP_SYSTEM:
			self.wndResp = None
		self.wndMapaSw = None
		self.wndMarbleShopWindow = None
		self.wndBonus = None
		self.wndBlend = None
		self.wndCollectWindow = None
		# ============================================================
		# 2. NELLA CLASSE Interface, nel metodo __init__()
		#    Aggiungi questa riga (vicino a self.wndCollectWindow = None, ecc)
		# ============================================================
		self.wndHunterLevel = None
		self.wndWeeklyRankWindow_New = None
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None
		
		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		# 	self.wndHorseShoe = None

		if app.ENABLE_ODLAMKI_SYSTEM:
			self.wndOdlamki = None
		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			self.wndLegendDamageWindow = None

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.wndOfflineShopAdminPanel = None
			self.wndOfflineShopLogPanel = None
			self.offlineShopAdvertisementBoardDict = {}
		if app.ENABLE_LRN_LOCATION_SYSTEM:
			self.wndLocationWindow = None
		if app.ENABLE_LRN_BATTLE_PASS:
			self.wndBattlePassDialog = None
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel		= None
			self.wndPrivateShopSearch		= None
			self.privateShopTitleBoardDict = {}
		self.wndBotControl = None
		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			self.wndMiniMapDungeonInfo = None
		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = None
			self.wndBuffNPCCreateWindow = None

		if app.ENABLE_VS_SHOP_SEARCH:
			self.wndOfflineShopSearch = None

		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		if app.ENABLE_LOADING_PERFORMANCE:
			self.wndWarpShower = None
		
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyTaskBar = None

		event.SetInterfaceWindow(self)

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	def AppendQueue(self, vnum, value):
		name = chr.GetNameByVID(vnum)
		if value == 1:
			self.yangText.AddGoldValue("|cFFe4ec98"+emoji.AppendEmoji("icon/emoji/sell.png")+" "+str(name))
		elif value == 0:
			self.yangText.AddGoldValue("|cFFf8a6a6"+emoji.AppendEmoji("icon/emoji/buy.png")+" "+str(name))

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		yangText = self.NewGoldChat(None, wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2 + 540, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37 + 9)
		self.yangText = yangText

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def OnPickMoneyNew(self, money):
		self.yangText.AddGoldValue("|cFFffd74c"+emoji.AppendEmoji("icon/emoji/money_icon_small.png")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def OnPickChequeNew(self, money):
		self.yangText.AddGoldValue("|cFFb8b8b8"+emoji.AppendEmoji("icon/emoji/cheque_icon.png")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def OnPickPktOsiagNew(self, money):
		self.yangText.AddGoldValue("|cFFFF0000"+emoji.AppendEmoji("d:/ymir work/ui/stone_point/stone_point.tga")+" "+"+%s"%(localeInfo.NumberToGoldNotText(money)))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))

		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None
		import app
		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
			
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_OFFLINE_SHOP, ui.__mem_func__(self.TogglePrivateShopPanelWindowCheck))

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		# wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		# wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			wndExtendedInventory = uiInventory.ExtendedInventoryWindow()
			wndExtendedInventory.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoul.BindInterfaceClass(self)
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None

		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			wndSafebox.BindInterface(self)
		wndSafebox.BindInterface(self)
		wndMapaSw = uimapasw.MapaSwWindow()
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		self.wndMarbleShopWindow = uiMarbleShop.MarbleShopWindow()
		self.wndBonus = uiBonus.BonusWindow()
		self.wndWeeklyRankWindow_New = new_uiWeeklyRank.WeeklyRankWindow()
		self.wndCollectWindow = uiCollectWindow.CollectWindow()
		self.wndBlend = uiBlend.AutoDopalacze()
		# ITEM_MALL
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		self.wndWonExchange = uiWonExchange.WonExchangeWindow()
		self.wndWonExchange.BindInterface(self)
		
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			wndOfflineShopAdminPanel = uiOfflineShop.OfflineShopAdminPanelWindow()
			wndOfflineShopAdminPanel.BindInterfaceClass(self)
			self.wndOfflineShopAdminPanel = wndOfflineShopAdminPanel

			wndOfflineShopLogPanel = uiOfflineShop.OfflineShopLogsWindow()
			wndOfflineShopLogPanel.BindInterfaceClass(self)
			self.wndOfflineShopLogPanel = wndOfflineShopLogPanel

		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		# 	wndHorseShoe = uiMount.HorseShoeWindow()
		# 	wndHorseShoe.BindInterfaceClass(self)
		# 	self.wndHorseShoe = wndHorseShoe

		if app.ENABLE_ODLAMKI_SYSTEM:
			wndOdlamki = uiOdlamki.OdlamkiWindow()
			wndOdlamki.BindInterfaceClass(self)
			self.wndOdlamki = wndOdlamki

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndBotControl = uibotcontrol.BotControlWindow()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory = wndExtendedInventory
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog
		if app.ENABLE_LOADING_PERFORMANCE:
			self.wndWarpShower = uiWarpShower.WarpShowerWindow()
		if app.ENABLE_COLLECTIONS_SYSTEM:
			self.wndCollections = uiCollections.CollectionsWindow()
		if app.__BL_CHEST_DROP_INFO__:
			self.wndChestDropInfo = uiChestDropInfo.ChestDropInfoWindow()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfoWindow()
			self.wndMiniMap.BindInterfaceClass(self)
		self.wndMapaSw = wndMapaSw
		# self.wndPety = wndPety

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_NEW_PET_SYSTEM:
			self.pets_window = _Pety.Pety(self.wndInventory)
			self.pets_window.Hide()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = uiBuffNPC.BuffNPCWindow()
			self.wndBuffNPCCreateWindow = uiBuffNPC.BuffNPCCreateWindow()

		if app.ENABLE_VS_SHOP_SEARCH:
			self.wndOfflineShopSearch = uiShopSearch.SearchWindow()

		if app.ENABLE_ARTEFAKT_SYSTEM:
			self.wndArtefaktWindow = uiartefaktsystem.ArtefaktWindow()
			self.wndArtefaktWindow.Hide()
		
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			self.wndMount = uiMount.MountWindow()
			self.wndMount.Hide()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			self.wndLegendDamageWindow = uiLegendDamageWindow.LegendDamageWindow()
			self.wndLegendDamageWindow.Hide()
			self.wndLegendDamageWindow.BindInterfaceClass(self)
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel = uiPrivateShop.PrivateShopPanel()
			self.wndPrivateShopPanel.BindInterfaceClass(self)
			self.wndPrivateShopPanel.BindInventoryClass(self.wndInventory)
			self.wndPrivateShopPanel.BindDragonSoulInventoryClass(self.wndDragonSoul)

			self.wndDragonSoul.BindPrivateShopClass(self.wndPrivateShopPanel)
			self.wndDragonSoul.BindPrivateShopSearchClass(self.wndPrivateShopSearch)
			
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSeachWindow()
			self.wndPrivateShopSearch.BindInterfaceClass(self)
			
			self.wndInventory.BindWindow(self.wndPrivateShopPanel)
			self.wndInventory.BindPrivateShopClass(self.wndPrivateShopPanel)
			self.wndInventory.BindPrivateShopSearchClass(self.wndPrivateShopSearch)

	if app.ENABLE_NEW_PET_SYSTEM:
		def pet_refresh(self):
			if self.pets_window:
				self.pets_window.PetReload()
				
		def pet_window_open(self):
			_obj = self.pets_window
			if not _obj:
				return
				
			_obj.Show() if not _obj.IsShow() else _obj.Close()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()
		
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.dlgOfflineShop = uiOfflineShop.OfflineShopDialog()
			self.dlgOfflineShop.LoadDialog()
			self.dlgOfflineShop.BindInterfaceClass(self)
			self.dlgOfflineShop.Hide()

			self.offlineShopBuilder = uiOfflineShopBuilder.OfflineShopBuilder()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.offlineShopBuilder.BindInterface(self)
				self.offlineShopBuilder.SetInven(self.wndInventory)
				self.wndInventory.BindWindow(self.offlineShopBuilder)
			self.offlineShopBuilder.Hide()	

		if app.ENABLE_MINIMAP_DUNGEONINFO:
			self.wndMiniMapDungeonInfo = uiminimapdungeoninfo.MiniMapDungeonInfo()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()
		
		self.wndRemoveItem = uiremoveitem.RemoveItemDialog()
		self.wndRemoveItem.Hide()
		
		if app.ENABLE_RESP_SYSTEM:
			self.wndResp = uiresp.RespDialog()
			self.wndResp.Hide()

		self.wndItemShop = uiItemShop.ItemShopWindow()
		self.wndItemShop.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	if constInfo.GIFT_CODE_SYSTEM:
		def __MakeGiftCodeWindow(self):
			self.wndGiftCodeWindow = uigiftcodewindow.UiGiftCodeWindow()
			self.wndGiftCodeWindow.LoadWindow()
			self.wndGiftCodeWindow.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()
		
	#BONUS CHANGER
	def __MakeChangerWindow(self):
		self.wndChangerWindow = uiBonusChanger.ChangerWindow()
		self.wndChangerWindow.LoadWindow()
		self.wndChangerWindow.Hide()
	#END OF BONUS CHANGER

	def __MakeCardsInfoWindow(self):
		self.wndCardsInfo = uiCards.CardsInfoWindow()
		self.wndCardsInfo.LoadWindow()
		self.wndCardsInfo.Hide()
		
	def __MakeCardsWindow(self):
		self.wndCards = uiCards.CardsWindow()
		self.wndCards.LoadWindow()
		self.wndCards.Hide()
		
	def __MakeCardsIconWindow(self):
		self.wndCardsIcon = uiCards.IngameWindow()
		self.wndCardsIcon.LoadWindow()
		self.wndCardsIcon.Hide()

	def __MakeIsIconWindow(self):
		self.wndIsIcon = uiIkonki.IsIngameIcon()
		self.wndIsIcon.BindInterfaceClass(self)
		self.wndIsIcon.LoadWindow()
		self.wndIsIcon.Show()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def __MakeAcceWindow(self):
			self.wndAcceCombine = uiacce.CombineWindow()
			self.wndAcceCombine.LoadWindow()
			self.wndAcceCombine.Hide()

			self.wndAcceAbsorption = uiacce.AbsorbWindow()
			self.wndAcceAbsorption.LoadWindow()
			self.wndAcceAbsorption.Hide()

			if self.wndInventory:
				self.wndInventory.SetAcceWindow(self.wndAcceCombine, self.wndAcceAbsorption)

		def AcceMaterials(self, id, vnum, count):
			self.wndAcceCombine.SendMaterials(id, vnum, count)

	if app.ENABLE_AURA_SYSTEM:
		def __MakeAuraWindow(self):
			self.wndAuraRefine = uiaura.RefineWindow(self.wndInventory, self)
			self.wndAuraRefine.LoadWindow()
			self.wndAuraRefine.Hide()
	
			self.wndAuraAbsorption = uiaura.AbsorbWindow(self.wndInventory, self)
			self.wndAuraAbsorption.LoadWindow()
			self.wndAuraAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetAuraWindow(self.wndAuraAbsorption, self.wndAuraRefine)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiSelectItem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.Hide()

	if app.ENABLE_LRN_LOCATION_SYSTEM:
		def __MakeLocationWindow(self):
			self.wndLocationWindow = uilocation.UiLocationWindow()
			self.wndLocationWindow.LoadWindow()
			self.wndLocationWindow.Hide()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def RefreshVisibleCostume(self):
			self.wndInventory.RefreshVisibleCostume()

	if app.ENABLE_LRN_BATTLE_PASS:
		def __MakeBattlePassWindow(self):
			self.wndBattlePassDialog = uibattlepass.BattlePassDialog()
			self.wndBattlePassDialog.LoadWindow()
			self.wndBattlePassDialog.Hide()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		
		self.__MakeIsIconWindow()

		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.__MakeCubeRenewal()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		if constInfo.GIFT_CODE_SYSTEM:
			self.__MakeGiftCodeWindow()
		#BONUS CHANGER
		self.__MakeChangerWindow()
		#END OF BONUS CHANGER
		self.__MakeCardsInfoWindow()
		self.__MakeCardsWindow()
		self.__MakeCardsIconWindow()
		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.__MakeAcceWindow()
		if app.ENABLE_AURA_SYSTEM:
			self.__MakeAuraWindow()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		if app.ENABLE_LRN_BATTLE_PASS:
			self.__MakeBattlePassWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		if app.ENABLE_LRN_LOCATION_SYSTEM:
			self.__MakeLocationWindow()

		# Hunter Level Window
		self.wndHunterLevel = uihunterlevel.HunterLevelWindow()
		self.wndHunterLevel.LoadWindow()
		self.wndHunterLevel.Hide()
		uihunterlevel.SetWindowManager(self.wndHunterLevel)

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			self.wndAcceCombine.SetItemToolTip(self.tooltipItem)
			self.wndAcceAbsorption.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_SYSTEM:
			self.wndAuraAbsorption.SetItemToolTip(self.tooltipItem)
			self.wndAuraRefine.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.SetSkillToolTip(self.tooltipSkill)

		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		# 	self.wndMount.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel.SetItemToolTip(self.tooltipItem)
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)
			self.privateShopTitleBoardDict = {}
		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		self.wndRemoveItem.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_ODLAMKI_SYSTEM:
			self.wndOdlamki.SetItemToolTip(self.tooltipItem)
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_RESP_SYSTEM:
			self.wndResp.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			self.dlgOfflineShop.SetItemToolTip(self.tooltipItem)
			self.offlineShopBuilder.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "sussurrare" == type:	
				self.OpenWhisperDialog(str(tokens[1]))

	## Make Windows & Dialogs
	################################

	def Close(self):
		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				self.wndEventManager = None

			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				self.wndEventIcon = None

		# Hunter Level Window - Deregistra prima di distruggere
		uihunterlevel.SetWindowManager(None)
		if self.wndHunterLevel:
			self.wndHunterLevel.Destroy()
			self.wndHunterLevel = None
				
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()

		if self.wndBotControl:
			self.wndBotControl.Hide()

		if self.yangText:
			self.yangText.ClearAll()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Destroy()

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				self.wndExtendedInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndBotControl:
			self.wndBotControl.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if self.wndCardsInfo:
			self.wndCardsInfo.Destroy()

		if self.wndCards:
			self.wndCards.Destroy()

		if self.wndCardsIcon:
			self.wndCardsIcon.Destroy()
				
		if app.ENABLE_ARTEFAKT_SYSTEM:
			if self.wndArtefaktWindow:
				self.wndArtefaktWindow.Destroy()
				del self.wndArtefaktWindow

		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			if self.wndMount:
				self.wndMount.Destroy()
				del self.wndMount

		if self.wndCube:
			self.wndCube.Destroy()

		if constInfo.GIFT_CODE_SYSTEM:
			if self.wndGiftCodeWindow:
				self.wndGiftCodeWindow.Destroy()

		if self.wndMapaSw:
			self.wndMapaSw.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceCombine:
			self.wndAcceCombine.Destroy()

		if app.ENABLE_ACCE_COSTUME_SYSTEM and self.wndAcceAbsorption:
			self.wndAcceAbsorption.Destroy()

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAuraAbsorption:
				self.wndAuraAbsorption.Destroy()

			if self.wndAuraRefine:
				self.wndAuraRefine.Destroy()

		if app.ENABLE_LOADING_PERFORMANCE:
			if self.wndWarpShower:
				self.wndWarpShower.Destroy()
				del self.wndWarpShower

		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()
		
		if app.ENABLE_NEW_PET_SYSTEM and self.pets_window:
			self.pets_window.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		#BONUS CHANGER
		if self.wndChangerWindow:
			self.wndChangerWindow.Destroy()
		#END OF BONUS CHANGER

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if app.ENABLE_COLLECTIONS_SYSTEM:
			if self.wndCollections:
				self.wndCollections.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Hide()
				self.wndPrivateShopPanel.Destroy()
				
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Hide()
				self.wndPrivateShopSearch.Destroy()

			del self.wndPrivateShopPanel
			del self.wndPrivateShopSearch
			self.privateShopTitleBoardDict = {}
			
		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				del self.wndChestDropInfo

		# if self.eventIcon:
		# 	self.eventIcon.Destroy()

		# if self.rankingIcon:
		# 	self.rankingIcon.Destroy()
			
		if self.wndIsIcon:
			self.wndIsIcon.Destroy()

		# if self.wndPromoicon:
		# 	self.wndPromoicon.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				self.wndMiniMapDungeonInfo.Destroy()

		if self.wndRemoveItem:
			self.wndRemoveItem.Destroy()
			del self.wndRemoveItem

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Destroy()
				self.wndCubeRenewal.Close()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Destroy()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Destroy()

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				self.wndOfflineShopSearch.Destroy()

		if app.ENABLE_RESP_SYSTEM:
			if self.wndResp:
				self.wndResp.Destroy()

				del self.wndResp

		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			if (self.dlgOfflineShop):
				self.dlgOfflineShop.Destroy()
				
			if (self.offlineShopBuilder):
				self.offlineShopBuilder.Destroy()

			if (self.wndOfflineShopAdminPanel):
				self.wndOfflineShopAdminPanel.Destroy()
			
			if (self.wndOfflineShopLogPanel):
				self.wndOfflineShopLogPanel.Destroy()

		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		# 	if (self.wndHorseShoe):
		# 		self.wndHorseShoe.Destroy()

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.wndOdlamki:
				self.wndOdlamki.Destroy()

		if self.wndItemShop:
			self.wndItemShop.Destroy()
			del self.wndItemShop

		if app.ENABLE_LRN_LOCATION_SYSTEM:
			if self.wndLocationWindow:
				self.wndLocationWindow.Destroy()
				
		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()

		if self.wndMarbleShopWindow:
			self.wndMarbleShopWindow.Destroy()

		if self.wndBonus:
			self.wndBonus.Destroy()
		
		if self.wndCollectWindow:
			self.wndCollectWindow.Destroy()

		if self.wndWeeklyRankWindow_New:
			self.wndWeeklyRankWindow_New.Destroy()
			
		if self.wndBlend:
			self.wndBlend.Destroy()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Destroy()

		if app.ENABLE_LRN_BATTLE_PASS:
			if self.wndBattlePassDialog:
				self.wndBattlePassDialog.Destroy()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				self.wndLegendDamageWindow.Destroy()
				del self.wndLegendDamageWindow

		self.wndChatLog.Destroy()
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Destroy()
				del self.wndDungeonInfo

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL
		
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			del self.wndMiniMapDungeonInfo

		del self.wndMapaSw
		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.yangText
		del self.wndTaskBar
		del self.wndWonExchange
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			del self.wndCubeRenewal
		del self.wndCharacter
		del self.wndInventory
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndBotControl
		del self.wndHelp

		del self.wndCardsInfo
		del self.wndCards
		del self.wndCardsIcon

		del self.wndCube
		del self.wndCubeResult
		if constInfo.GIFT_CODE_SYSTEM:
			del self.wndGiftCodeWindow
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		if app.ENABLE_NEW_PET_SYSTEM and self.pets_window:
			del self.pets_window
		del self.wndGameButton
		# del self.eventIcon
		del self.wndIsIcon
		# del self.wndPromoicon
		# del self.rankingIcon
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect
		if app.ENABLE_LRN_BATTLE_PASS:
			del self.wndBattlePassDialog
		if app.ENABLE_COLLECTIONS_SYSTEM:
			del self.wndCollections
		#BONUS CHANGER
		del self.wndChangerWindow
		#END OF BONUS CHANGER
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				del self.wndExtendedInventory
		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot	
		del self.wndMarbleShopWindow
		del self.wndBonus
		del self.wndCollectWindow
		del self.wndWeeklyRankWindow_New
		if self.wndHunterLevel: # PULIZIA AGGIUNTA
			del self.wndHunterLevel
		del self.wndBlend
		if app.ENABLE_LRN_LOCATION_SYSTEM:
			del self.wndLocationWindow
		if app.ENABLE_OFFLINE_SHOP_SYSTEM:
			del self.dlgOfflineShop
			del self.wndOfflineShopAdminPanel
			del self.wndOfflineShopLogPanel
			self.offlineShopAdvertisementBoardDict = {}

		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		# 	del self.wndHorseShoe

		if app.ENABLE_ODLAMKI_SYSTEM:
			del self.wndOdlamki

		if app.ENABLE_ACCE_COSTUME_SYSTEM:
			del self.wndAcceCombine
			del self.wndAcceAbsorption

		if app.ENABLE_AURA_SYSTEM:
			del self.wndAuraAbsorption
			del self.wndAuraRefine

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			del self.wndBuffNPCWindow
			del self.wndBuffNPCCreateWindow

		if app.ENABLE_VS_SHOP_SEARCH:
			del self.wndOfflineShopSearch

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				del self.wndExpandedMoneyTaskBar

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	# ============================================================
	# HUNTER SYSTEM - GATE & TRIAL UI HANDLERS
	# ============================================================
	
	def HunterGateTrialOpen(self):
		"""Apre la finestra principale del sistema Gate/Trial"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OpenGateTrialWindow()

	def HunterGateStatus(self, gateId, gateName, remainingSeconds, colorCode):
		"""Aggiorna lo stato del Gate disponibile"""
		if self.wndHunterLevel:
			self.wndHunterLevel.UpdateGateStatus(gateId, gateName, remainingSeconds, colorCode)

	def HunterGateEnter(self, gateId, duration):
		"""Chiamato quando il player entra nel Gate"""
		if self.wndHunterLevel:
			self.wndHunterLevel.HideGateTimer()
		chat.AppendChat(chat.CHAT_TYPE_INFO, "[GATE] Sei entrato! Hai %d minuti per completare." % duration)

	def HunterGateComplete(self, success, gloriaChange):
		"""Chiamato quando il Gate viene completato o fallito"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnGateComplete(success, gloriaChange)
		if success:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[GATE] COMPLETATO! +%d Gloria" % gloriaChange)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "[GATE] FALLITO! -%d Gloria" % gloriaChange)

	def HunterTrialStart(self, trialId, trialName, toRank, colorCode):
		"""Chiamato quando una Trial inizia"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnTrialStart(trialId, trialName, toRank, colorCode)

	def HunterTrialStatus(self, trialId, trialName, toRank, colorCode, remainingSeconds,
						  bossKills, bossReq, metinKills, metinReq,
						  fractureSeals, fractureReq, chestOpens, chestReq,
						  dailyMissions, dailyReq):
		"""Aggiorna lo stato completo della Trial in corso"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnTrialStatus(
				trialId, trialName, toRank, colorCode, remainingSeconds,
				bossKills, bossReq, metinKills, metinReq,
				fractureSeals, fractureReq, chestOpens, chestReq,
				dailyMissions, dailyReq
			)

	def HunterTrialProgress(self, trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions):
		"""Aggiorna solo il progresso della Trial (update leggero)"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnTrialProgress(trialId, bossKills, metinKills, fractureSeals, chestOpens, dailyMissions)

	def HunterTrialComplete(self, newRank, gloriaReward, trialName):
		"""Chiamato quando la Trial viene completata"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnTrialComplete(newRank, gloriaReward, trialName)

	# ============================================================
	# END OF HUNTER GATE & TRIAL HANDLERS
	# ============================================================
	
	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()
		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			if self.wndPrivateShopPanel.IsShow():
				self.wndPrivateShopPanel.Refresh()
	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		#BONUS CHANGER
		if constInfo.IS_BONUS_CHANGER:
			self.UpdateBonusChanger()
		#END OF BONUS CHANGER
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.RefreshEquipSlotWindow()
		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			self.wndExtendedInventory.RefreshItemSlot()
		if app.ENABLE_ARTEFAKT_SYSTEM:
			self.wndArtefaktWindow.RefreshSlot()
		if app.ENABLE_MOUNT_COSTUME_SYSTEM:
			self.wndMount.RefreshSlots()


	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenBotControl(self):
		if self.wndBotControl.IsShow():
			self.wndBotControl.Close()
		else:
			self.wndBotControl.Open()

	if app.ENABLE_ARTEFAKT_SYSTEM:
		def OpenArtefaktWindow(self):
			if self.wndArtefaktWindow.IsShow():
				self.wndArtefaktWindow.Hide()
			else:
				self.wndArtefaktWindow.Open()

	if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		def ToggleMountWindow(self):
			if self.wndMount.IsShow():
				self.wndMount.Hide()
			else:
				self.wndMount.Open()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	# ShopOffline
	if app.ENABLE_OFFLINE_SHOP_SYSTEM:
		def OpenOfflineShopDialog(self, vid):
			self.wndInventory.Show()
			self.wndInventory.SetTop()
			self.dlgOfflineShop.Open(vid)
			self.dlgOfflineShop.SetTop()

			if self.wndOfflineShopAdminPanel:
				if self.wndOfflineShopAdminPanel.wndOfflineShopAddItem:
					self.wndOfflineShopAdminPanel.wndOfflineShopAddItem.Close()
					
				if self.wndOfflineShopAdminPanel.wndOfflineShopRemoveItem:
					self.wndOfflineShopAdminPanel.wndOfflineShopRemoveItem.Close()
			
		def CloseOfflineShopDialog(self):	
			self.dlgOfflineShop.Close()
			
		def RefreshOfflineShopDialog(self):
			self.dlgOfflineShop.Refresh()

		def ToggleOfflineShopAdminPanelWindow(self, info):
			if (self.wndOfflineShopAdminPanel.IsShow() == True):
				self.wndOfflineShopAdminPanel.Close()
			else:
				self.wndOfflineShopAdminPanel.SetAdditionalInfo(info)
				self.wndOfflineShopAdminPanel.Show()	

		def ToggleOfflineShopLogWindow(self):
			self.wndOfflineShopLogPanel.Open()

		def OpenOfflineShopInputNameDialog(self):
			inputDialog = uiOfflineShop.OfflineShopInputDialog()
			inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenOfflineShopBuilder))
			inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseOfflineShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog
			
		def CloseOfflineShopInputNameDialog(self):
			self.inputDialog = None
			return True
		
		def OpenOfflineShopBuilder(self):	
			self.offlineShopBuilder.Open(player.GetName())
			self.CloseOfflineShopInputNameDialog()
			return True
		
		def AppearOfflineShop(self, vid, text):
			board = uiOfflineShopBuilder.OfflineShopAdvertisementBoard()
			board.Open(vid, text)
			
			self.offlineShopAdvertisementBoardDict[vid] = board
			
		def DisappearOfflineShop(self, vid):
			if (not self.offlineShopAdvertisementBoardDict.has_key(vid)):
				return
				
			del self.offlineShopAdvertisementBoardDict[vid]
			uiOfflineShopBuilder.DeleteADBoard(vid)

	if app.ENABLE_VS_SHOP_SEARCH:
		def ToggleOfflineShopSearch(self):
			if self.wndOfflineShopSearch.IsShow():
				self.wndOfflineShopSearch.Close()
			else:
				self.wndOfflineShopSearch.Open()
				self.wndOfflineShopSearch.SetTop()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
			self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, cost2, cost3, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if constInfo.ZAPAMIETAJ_OKNO_ZAPISU == True:
			self.wndLocationWindow.Show()
		if constInfo.ZAPAMIETAJ_OKNO_TPMETKIBOSSY == True:
			self.wndResp.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndMapaSw.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.yangText.Show()
		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndWonExchange:
			self.wndWonExchange.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
		if app.ENABLE_LRN_LOCATION_SYSTEM:
			if self.wndLocationWindow:
				self.wndLocationWindow.Hide()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if app.ENABLE_COLLECTIONS_SYSTEM:
			if self.wndCollections:
				self.wndCollections.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Hide()

		if self.wndWonExchange:
			self.wndWonExchange.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				self.wndExtendedInventory.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()
			
		if self.wndMapaSw:
			self.wndMapaSw.Hide()

		if self.wndChat:
			self.wndChat.Hide()

		if self.yangText:
			self.yangText.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()
			
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				self.wndMiniMapDungeonInfo.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			self.wndPrivateShopPanel.Hide()
			self.wndPrivateShopSearch.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			
		if app.__BL_CHEST_DROP_INFO__:
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Hide()
			
		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()
	
		if self.wndRemoveItem:
			self.wndRemoveItem.Hide()

		if app.ENABLE_RESP_SYSTEM:
			if self.wndResp:
				self.wndResp.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
		
		if self.wndMarbleShopWindow:
			self.wndMarbleShopWindow.Hide()

		if self.wndBonus:
			self.wndBonus.Hide()

		if self.wndCollectWindow:
			self.wndCollectWindow.Hide()

		if self.wndWeeklyRankWindow_New:
			self.wndWeeklyRankWindow_New.Hide()

		if self.wndHunterLevel: # PULIZIA AGGIUNTA
			self.wndHunterLevel.Close()

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				self.wndLegendDamageWindow.Close()

		if self.wndBlend:
			self.wndBlend.Hide()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Hide()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Hide()

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				self.wndOfflineShopSearch.Hide()

	def IsShowDlgQuestionWindow(self):
		if self.wndDragonSoul.IsDlgQuestionShow():
			return True
		elif self.dlgShop.IsDlgQuestionShow():
			return True
		elif self.wndWonExchange.IsDlgQuestionShow():
			return True
		else:
			return False

	def CloseDlgQuestionWindow(self):
		if self.wndDragonSoul.IsDlgQuestionShow():
			self.wndDragonSoul.ExternQuestionDialog_Close()
		if self.dlgShop.IsDlgQuestionShow():
			self.dlgShop.ExternQuestionDialog_Close()
		if self.wndWonExchange.IsDlgQuestionShow():
			self.wndWonExchange.ExternQuestionDialog_Close()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	if app.ENABLE_MINIMAP_DUNGEONINFO:
		def SetMiniMapDungeonInfo(self, state):
			import dbg
			# dbg.TraceError("SetMiniMapDungeonInfo %d" % (state))
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "SetMiniMapDungeonInfo %d" % (state))
			if state == 1:
				self.wndMiniMap.HideMiniMap()
				self.wndMiniMap.Hide()
				self.wndMiniMapDungeonInfo.Show()
			else:
				self.wndMiniMap.Show()
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMapDungeonInfo.Hide()
	
		def SetMiniMapDungeonInfoStage(self, cur_stage, max_stage):
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "SetMiniMapDungeonInfoStage %d %d" % (cur_stage, max_stage))
			self.wndMiniMapDungeonInfo.SetStage(cur_stage, max_stage)
		
		def SetMiniMapDungeonInfoGauge(self, gauge_type, value1, value2):
			#chat.AppendChat(chat.CHAT_TYPE_INFO, "SetMiniMapDungeonInfoGauge %d %d %d" % (gauge_type, value1, value2))
			self.wndMiniMapDungeonInfo.SetGauge(gauge_type, value1, value2)
		
		def SetMiniMapDungeonInfoNotice(self, notice):
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "SetMiniMapDungeonInfoNotice %s" % (notice))
			self.wndMiniMapDungeonInfo.SetNotice(notice)

		def SetMiniMapDungeonInfoButton(self, status):
			self.wndMiniMapDungeonInfo.SetButton(status)

		def SetMiniMapDungeonInfoTimer(self, status, time):
			self.wndMiniMapDungeonInfo.SetTimer(status, time)

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def ToggleMapaSwWindow(self):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndMapaSw.IsShow():
				self.wndMapaSw.Laduj()
				self.wndMapaSw.SetTop()
			else:
				self.wndMapaSw.Laduj()
		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				if 1 == constInfo.EnvanterAcilsinmi:
					if not self.wndExtendedInventory.IsShow():
						self.wndExtendedInventory.Show()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				if 1 == constInfo.EnvanterAcilsinmi:
					if self.wndExtendedInventory.IsShow():
						self.wndExtendedInventory.Close()

	# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
	# 	def Mount_SetEXPInfo(self, level, cur_exp, exp):
	# 		if self.wndMount:
	# 			self.wndMount.SetEXPInfo(level, cur_exp, exp)

	# 	def MountNPC_Clear(self):
	# 		if self.wndMount:
	# 			self.wndMount.SetClear()

	# 	def MountNPC_SetSkillInfo(self, skillpoints, skilldata):
	# 		if self.wndMount:
	# 			self.wndMount.SetSkillInfo(skillpoints, skilldata)

		# def ToggleHorseshoePanel(self):
		# 	if (self.wndHorseShoe.IsShow() == True):
		# 		self.wndHorseShoe.Close()
		# 	else:
		# 		self.wndHorseShoe.Show()	

	if app.ENABLE_ODLAMKI_SYSTEM:
		def OpenOdlamkiWindow(self):
			if self.wndOdlamki.IsShow():
				self.wndOdlamki.Hide()
			else:
				self.wndOdlamki.Open()

		# if app.ENABLE_COLLECT_WINDOW:
	# 	def ToggleQuest(self, id):
	# 		self.wndCollectWindow.UpdateQuest(str(id))

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def BuffNPC_OpenCreateWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCCreateWindow.IsShow():
					self.wndBuffNPCCreateWindow.Show()
					self.wndBuffNPCCreateWindow.SetTop()
				
		def BuffNPCOpenWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCWindow.IsShow():
					self.wndBuffNPCWindow.Show()
					self.wndBuffNPCWindow.SetTop()
				else:
					self.wndBuffNPCWindow.Close()
				
		def BuffNPC_Summon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSummon()
				# self.wndBuffNPCWindow.Show()
				# self.wndBuffNPCWindow.SetTop()
				
		def BuffNPC_Unsummon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetUnsummon()
				
		def BuffNPC_Clear(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetClear()
				
		def BuffNPC_SetBasicInfo(self, name, sex, intvalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetBasicInfo(name, sex, intvalue)
				
		def BuffNPC_SetSkillInfo(self, skill1, skill2, skill3):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillInfo(skill1, skill2, skill3)
				
		def BuffNPC_SetSkillCooltime(self, slot, timevalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillCooltime(slot, timevalue)
		
		def BuffNPC_CreatePopup(self, type, value0, value1):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.CreatePopup(type, value0, value1)

	if app.WJ_SPLIT_INVENTORY_SYSTEM:
		def ToggleExtendedInventoryWindow(self):
			if FALSE == player.IsObserverMode():
				if self.wndExtendedInventory.IsShow():
					# constInfo.EXTENDED_INVENTORY_IS_OPEN = 0
					self.wndExtendedInventory.OverOutItem()
					self.wndExtendedInventory.Close()
				else:
					# constInfo.EXTENDED_INVENTORY_IS_OPEN = 1
					self.wndExtendedInventory.Show()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()

	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)

		elif app.ENABLE_HIGHLIGHT_NEW_ITEM and player.SLOT_TYPE_INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
			self.wndExtendedInventory.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		if (self.wndExpandedTaskBar): # Just call SetToolTipText If self.wndExpandedTaskbar is not None
			self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()


	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def ToggleMarmurShopWindow(self):
		if self.wndMarbleShopWindow.IsShow():
			self.wndMarbleShopWindow.Close()
		else:
			self.wndMarbleShopWindow.Open()

	def ToggleBonusWindow(self):
		if self.wndBonus.IsShow():
			self.wndBonus.Close()
		else:
			self.wndBonus.Open()

	def OpenBlendWindow(self):
		if self.wndBlend.IsShow():
			self.wndBlend.Close()
		else:
			self.wndBlend.Open()

	def ToggleCollectWindow(self):
		if self.wndCollectWindow.IsShow():
			self.wndCollectWindow.Close()
		else:
			self.wndCollectWindow.Open()

	def ToggleWeeklyRankWindow(self):
		if self.wndWeeklyRankWindow_New.IsShow():
			self.wndWeeklyRankWindow_New.Close()
		else:
			self.wndWeeklyRankWindow_New.Open()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	def OpenRemoveItem(self, inventory):
		if self.wndRemoveItem.IsShow():
			self.wndRemoveItem.Hide()
		else:
			self.wndRemoveItem.OpenWindow(inventory)

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	# def __OnClickSkillPlusButton(self):
		# self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	if app.ENABLE_KEYCHANGE_SYSTEM:
		def ToggleHelpWindow(self):
			if self.wndHelp.IsShow():
				self.CloseHelpWindow()
			else:
				self.OpenHelpWindow()

	# def __OnClickHelpButton(self):
	# 	player.SetPlayTime(1)
	# 	self.CheckGameButton()
	# 	self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)

		self.wndChat.CloseChat()

	if constInfo.GIFT_CODE_SYSTEM:
		def OpenGiftCodeWindow(self):
			if self.wndGiftCodeWindow.IsShow():
				self.wndGiftCodeWindow.Hide()
			else:
				self.wndGiftCodeWindow.Show()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()
		
	def OpenCardsInfoWindow(self):
		self.wndCardsInfo.Open()
		
	def OpenCardsWindow(self, safemode):
		self.wndCards.Open(safemode)
		
	def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsShowIcon(self):
		self.wndCardsIcon.Show()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		if 0:
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	if app.ENABLE_ACCE_COSTUME_SYSTEM:
		def ActAcce(self, iAct, bWindow):
			board = (self.wndAcceAbsorption,self.wndAcceCombine)[int(bWindow)]
			if iAct == 1:
				self.ActAcceOpen(board)
			elif iAct == 2:
				self.ActAcceClose(board)
			elif iAct == 3 or iAct == 4:
				self.ActAcceRefresh(board, iAct)

		def ActAcceOpen(self,board):
			if not board.IsOpened():
				board.Open()
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceClose(self,board):
			if board.IsOpened():
				board.Close()
			self.wndInventory.RefreshBagSlotWindow()

		def ActAcceRefresh(self,board,iAct):
			if board.IsOpened():
				board.Refresh(iAct)
			self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_AURA_SYSTEM:
		def ActAura(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Open()
				else:
					if not self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Open()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Close()
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndAuraRefine.IsOpened():
						self.wndAuraRefine.Refresh(iAct)
				else:
					if self.wndAuraAbsorption.IsOpened():
						self.wndAuraAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_LRN_LOCATION_SYSTEM:
		def OpenLocationWindowInstantly(self):
			self.wndLocationWindow.Show()

		def OpenLocationWindow(self):
			self.wndLocationWindow.OnCloseBoardSaveWindow()
			
			if self.wndLocationWindow.IsShow():
				self.wndLocationWindow.Hide()
			else:
				self.wndLocationWindow.Show()

	if app.ENABLE_RESP_SYSTEM:
		def OpenRespWindow(self):
			if self.wndResp.IsShow():
				self.wndResp.Hide()
			else:
				self.wndResp.Show()

		def ClearLocationWindow(self):
			self.wndLocationWindow.ClearData()

		def UpdateLocationWindowPos(self, position, index, posx, posy):
			self.wndLocationWindow.AppendPosition(position, index, posx, posy)

		def UpdateLocationWindowName(self, name):
			self.wndLocationWindow.AppendName(name)

	if app.ENABLE_DUNGEON_INFO_SYSTEM:
		def ToggleDungeonInfoWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndDungeonInfo.IsShow():
					self.wndDungeonInfo.Open()
				else:
					self.wndDungeonInfo.Close()

		def DungeonInfoOpen(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnOpen()

		def DungeonRankingRefresh(self):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnRefreshRanking()

		def DungeonInfoReload(self, onReset):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.OnReload(onReset)

	if app.ENABLE_LRN_BATTLE_PASS:
		def ClearBattlePassQuest(self):
			self.wndBattlePassDialog.ClearPageQuest()
			self.wndBattlePassDialog.ClearQuest()

		def AppendBattlePassQuest(self, *data):
			self.wndBattlePassDialog.AppendQuest(*data)

			self.wndBattlePassDialog.WindowRebuild("quest")
			self.wndBattlePassDialog.RefreshPageQuest()

		def AppendBattlePassQuestData(self, index, count, status):
			self.wndBattlePassDialog.AppendQuestData(index, count, status)
			self.wndBattlePassDialog.RefreshPageQuest()

		def ClearBattlePassReward(self):
			self.wndBattlePassDialog.ClearPageReward()
			self.wndBattlePassDialog.ClearReward()

		def AppendBattlePassReward(self, *data):
			self.wndBattlePassDialog.AppendReward(*data)

			self.wndBattlePassDialog.WindowRebuild("reward")
			self.wndBattlePassDialog.RefreshPageReward()

		def AppendBattlePassRewardData(self, level, status_free, status_premium):
			self.wndBattlePassDialog.AppendRewardData(level, status_free, status_premium)
			self.wndBattlePassDialog.RefreshPageReward()

		def AppendBattlePassLevel(self, level, exp, exp_max):
			self.wndBattlePassDialog.AppendLevel(level, exp, exp_max)
			self.wndBattlePassDialog.RefreshLevel()

		def BattlePassManager(self):
			if self.wndBattlePassDialog.IsShow():
				self.wndBattlePassDialog.Hide()
			else:
				self.wndBattlePassDialog.Show()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.yangText,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndWonExchange:
			hideWindows += self.wndWonExchange,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_COLLECTIONS_SYSTEM:
			hideWindows += self.wndCollections,

		if self.wndRemoveItem:
			hideWindows += self.wndRemoveItem,

		if app.ENABLE_ODLAMKI_SYSTEM:
			if self.wndOdlamki:
				hideWindows += self.wndOdlamki,

		if app.WJ_SPLIT_INVENTORY_SYSTEM:
			if self.wndExtendedInventory:
				hideWindows += self.wndExtendedInventory,

		if app.ENABLE_RESP_SYSTEM and self.wndResp:
			hideWindows += self.wndResp,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		if app.ENABLE_LRN_LOCATION_SYSTEM:
			hideWindows += self.wndLocationWindow,

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if self.wndMarbleShopWindow:
			hideWindows += self.wndMarbleShopWindow,

		if self.wndHunterLevel: # AGGIUNTA
			hideWindows += self.wndHunterLevel,

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				hideWindows += self.wndBuffNPCWindow,
			if self.wndBuffNPCCreateWindow:
				hideWindows += self.wndBuffNPCCreateWindow,

		if app.ENABLE_VS_SHOP_SEARCH:
			if self.wndOfflineShopSearch:
				hideWindows += self.wndOfflineShopSearch,

		if app.ENABLE_DUNGEON_INFO_SYSTEM:
			if self.wndDungeonInfo:
				hideWindows += self.wndDungeonInfo,
				
		if app.ENABLE_MINIMAP_DUNGEONINFO:
			if self.wndMiniMapDungeonInfo:
				hideWindows += self.wndMiniMapDungeonInfo,

		if constInfo.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,
                
		if app.ENABLE_LRN_BATTLE_PASS:
			hideWindows += self.wndBattlePassDialog,

		if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
			if self.wndLegendDamageWindow:
				hideWindows += self.wndLegendDamageWindow,

		if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
			hideWindows += self.wndPrivateShopPanel,\
						self.wndPrivateShopSearch

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def ToggleWonExchangeWindow(self):
		if player.IsObserverMode():
			return

		if False == self.wndWonExchange.IsShow():
			self.wndWonExchange.SetPage(uiWonExchange.WonExchangeWindow.PAGE_SELL)
			self.wndWonExchange.Show()
			self.wndWonExchange.SetTop()
		else:
			self.wndWonExchange.Hide()

	def __ShowWindows(self, wnds):
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	if app.ENABLE_COLLECTIONS_SYSTEM:
		def ToggleCollectionWindow(self):
			if self.wndCollections.IsShow():
				self.wndCollections.Hide()
			else:
				self.wndCollections.Show()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#####################################################################################
	### Private Shop ###

	def OpenPrivateShopInputNameDialog(self):
		#if player.IsInSafeArea():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
		#	return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#BONUS CHANGER
	def UpdateBonusChanger(self):
		if self.wndChangerWindow:
			self.wndChangerWindow.OnUpdate()
	
	def AddToBonusChange(self, item1, item2):
		if self.wndChangerWindow:
			self.wndChangerWindow.AddItems(item1, item2)
	#END OF BONUS CHANGER

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.Ʈ_̹_ü
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			if localeInfo.IsEUROPE():
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.iteritems():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)

		if not app.ENABLE_QUEST_RENEWAL:
			if localeInfo.IsARABIC():
				btn.SetToolTipText(name, -20, 55)
				btn.ToolTipText.SetHorizontalAlignRight()
			else:
				btn.SetToolTipText(name, -20, 55)
				btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.Ʈ_ġ_
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
		
			if app.ENABLE_QUEST_RENEWAL:
				btn.SetToolTipText(str(len(self.questButtonList)))
				btn.ToolTipText.SetPosition(13, 37)


			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if app.ENABLE_QUEST_RENEWAL and count > 0:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_RENEWAL:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_RENEWAL:
				break
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name):
		# if not self.whisperDialogDict.has_key(name):
		dlg = self.__MakeWhisperDialog(name)
		dlg.OpenWithTarget(name)
		dlg.chatLine.SetFocus()
		dlg.Show()

		self.__CheckGameMaster(name)
		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	if app.TAKE_LEGEND_DAMAGE_BOARD_SYSTEM:
		def OpenLegendDamageWindow(self, vid):
			import dbg
			dbg.TraceError("OpenLegendDamageWindow: %d ", vid)
			self.wndLegendDamageWindow.Show(vid)

		def SendLegendDamageData(self, vid, pos, name, level, race, empire, damage):
			if vid not in constInfo.LEGEND_DAMAGE_DATA:
				constInfo.LEGEND_DAMAGE_DATA[vid] = {
					"NAME": [None] * 15,
					"LEVEL": [None] * 15,
					"RACE": [None] * 15,
					"EMPIRE": [None] * 15,
					"DAMAGE": [None] * 15
				}

			damage_data = constInfo.LEGEND_DAMAGE_DATA[vid]
			damage_data["NAME"][pos] = name
			damage_data["LEVEL"][pos] = level
			damage_data["RACE"][pos] = race
			damage_data["EMPIRE"][pos] = empire
			damage_data["DAMAGE"][pos] = damage

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()
		
	if app.__BL_CHEST_DROP_INFO__:
		def OpenChestDropWindow(self, itemVnum, isMain):
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Open(itemVnum, isMain)

	#####################################################################################
	def RequestOpenItemShop(self):
		self.wndItemShop.RequestOpen()

	def TombolaStart(self, pos, to_pos, to_spin, time):
		self.wndItemShop.StartSpinning(pos, to_pos, to_spin, time)

	def TombolaSetSpinningItem(self, pos, vnum, count):
		self.wndItemShop.SetSpinningItem(pos, vnum, count)

	def TombolaOpen(self):
		self.wndItemShop.Show()

	def TombolaSetPrice(self, group, price, price_type):
		self.wndItemShop.SetPrice(group, price, price_type)

	def TombolaSetItem(self, group, vnum, count, chance):
		self.wndItemShop.SetItem(group, vnum, count, chance)

	def TombolaClear(self):
		self.wndItemShop.TombolaClear()

	def IsEditLineFocus(self):
		if self.wndChat.chatLine.IsFocus():
			return 1

		if self.wndChat.chatToLine.IsFocus():
			return 1

		return 0

	def ActiveTileNow(self, id):
		self.wndWeeklyRankWindow_New.Active(id)

	def GetActiveTitleNow(self):
		self.wndWeeklyRankWindow_New.GetActiveNow()

	def TitleEnable(self, id, val):
		self.wndWeeklyRankWindow_New.Enable(id, val)

	def OfflineShopLogs(self, id, item, count, price, price2, date, action):
		self.wndOfflineShopLogPanel.SendLogs(id, item, count, price, price2, date, action)

	def SelectPage(self, page, season):
		self.wndWeeklyRankWindow_New.PutPage(page, season)

	def SendWeeklyInfo(self, pos, name, points, empire, job):
		self.wndWeeklyRankWindow_New.LoadPage(pos, name, points, empire, job)


	if app.BL_MOVE_CHANNEL:
		def RefreshServerInfo(self, channelNumber):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo(channelNumber)

### EFEKT ALCHEMIA
	def UseDSSButtonEffect(self, enable):
		if self.wndInventory:
			self.wndInventory.UseDSSButtonEffect(enable)
	
	def EmptyFunction(self):
		pass

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetOnTopWindow(self, onTopWnd):
			self.onTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.onTopWindow

		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshMarkSlots()

	if app.ENABLE_LOADING_PERFORMANCE:
		def OpenWarpShowerWindow(self):
			if self.wndMiniMap and self.wndMiniMap.IsShowingAtlas():
				self.wndMiniMap.ToggleAtlasWindow()

			if self.dlgSystem:
				self.dlgSystem.Close()
				self.dlgSystem.Destroy()

			self.HideAllQuestButton()
			self.HideAllWhisperButton()

			self.HideAllWindows()

			self.wndWarpShower.Open()

		def CloseWarpShowerWindow(self):
			if self.wndWarpShower:
				self.wndWarpShower.Close()

	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendar.MovableImage()
				self.wndEventIcon.Show()
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendar.EventCalendarWindow()
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if eventendTime != 0:
				eventendTime += app.GetGlobalTimeStamp()
			uiEventCalendar.SetEventStatus(eventID, eventStatus, eventendTime, eventEndTimeText)
			self.RefreshEventManager()
		def ClearEventManager(self):
			uiEventCalendar.server_event_data={}
		def RefreshEventManager(self):
			if self.wndEventManager:
				self.wndEventManager.Refresh()
			if self.wndEventIcon:
				self.wndEventIcon.Refresh()
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			self.MakeEventIcon()
			if startRealTime != 0:
				startRealTime += app.GetGlobalTimeStamp()
			if endRealTime != 0:
				endRealTime += app.GetGlobalTimeStamp()
			uiEventCalendar.SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP_OFFICIAL:
		def OpenPrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Open()
				
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
				
		def ClosePrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Close(False)
				
		def RefreshPrivateShopWindow(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Refresh()
				self.wndPrivateShopPanel.RefreshWindow()
				
		def TogglePrivateShopPanelWindow(self):
			if False == player.IsObserverMode():
				if not self.wndPrivateShopPanel.RequestOpen():
					self.wndPrivateShopPanel.Close()
					
		def TogglePrivateShopPanelWindowCheck(self):
			if False == player.IsObserverMode():
				if not self.wndPrivateShopPanel.RequestOpen(True):
					self.wndPrivateShopPanel.Close()

		def OpenPrivateShopSearch(self, mode):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Open(mode)
				
		def PrivateShopSearchUpdate(self, index, state):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.UpdateResult(index, state)

		def PrivateShopSearchRefresh(self):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.RefreshPage()
				
		def AppendMarketItemPrice(self, gold, cheque):
			if self.wndPrivateShopPanel and self.wndPrivateShopPanel.IsShow():
				self.wndPrivateShopPanel.AppendMarketItemPrice(gold, cheque)
				
			elif self.self.privateShopBuilder and self.self.privateShopBuilder.IsShow():
				self.privateShopBuilder.AppendMarketItemPrice(gold, cheque)
				
		def AddPrivateShopTitleBoard(self, vid, text, type):

			board = uiPrivateShop.PrivateShopTitleBoard(type)
			board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board

		def RemovePrivateShopTitleBoard(self, vid):

			if not self.privateShopAdvertisementBoardDict.has_key(vid):
				return

			del self.privateShopAdvertisementBoardDict[vid]
			uiPrivateShop.DeleteTitleBoard(vid)
			
		def SetPrivateShopPremiumBuild(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.SetPremiumBuildMode()
				self.wndPrivateShopPanel.RefreshWindow()
				
		def PrivateShopStateUpdate(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.OnStateUpdate()

# ============================================================
# 4. AGGIUNGI QUESTI METODI NELLA CLASSE Interface
#    (mettili dove preferisci, io suggerisco alla fine)
# ============================================================

# --- COPIA DA QUI ---

# ==================== HUNTER LEVEL SYSTEM ====================
	def GetHunterLevelWindow(self):
		"""Ritorna la finestra Hunter Level."""
		return self.wndHunterLevel

# ==================== HUNTER SYSTEM BRIDGES ====================
	def HunterSystemSpeak(self, msg, rankKey="E"):
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowSystemMessage(msg, rankKey)

	def HunterWelcome(self, rankKey, name, points):
		"""Mostra il messaggio di benvenuto epico basato sul rank"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowWelcomeMessage(rankKey, name, points)

	def HunterEmergency(self, title, seconds, vnums, count, description="", difficulty="NORMAL", penalty=0):
		if self.wndHunterLevel:
			self.wndHunterLevel.StartEmergencyQuest(title, seconds, vnums, count, description, difficulty, penalty)

	def HunterEmergencyUpdate(self, current):
		if self.wndHunterLevel:
			self.wndHunterLevel.UpdateEmergencyCount(current)

	def HunterEmergencyClose(self, status):
		if self.wndHunterLevel:
			self.wndHunterLevel.EndEmergencyQuest(status == "SUCCESS")

	def HunterRivalUpdate(self, name, points, label="Gloria", mode="VICINO"):
		if self.wndHunterLevel:
			self.wndHunterLevel.UpdateRival(name, points, label, mode)

	def HunterWhatIf(self, qid, text, opt1, opt2, opt3, colorCode):
		if self.wndHunterLevel:
			self.wndHunterLevel.OpenWhatIf(qid, text, opt1, opt2, opt3, colorCode)

	def HunterBossAlert(self, bossName):
		"""Mostra ALERT a schermo intero quando spawna un BOSS"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowBossAlert(bossName)

	def HunterSystemInit(self):
		"""Mostra effetto inizializzazione sistema"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowSystemInit()

	def HunterAwakening(self, playerName):
		"""Mostra effetto risveglio al Lv 5"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowAwakening(playerName)

	def HunterActivation(self, playerName):
		"""Mostra effetto attivazione Hunter al Lv 30"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowHunterActivation(playerName)

	def HunterRankUp(self, oldRank, newRank):
		"""Mostra effetto salita di rank"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowRankUp(oldRank, newRank)

	def HunterOvertake(self, overtakenName, newPosition):
		"""Mostra effetto sorpasso in classifica"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowOvertake(overtakenName, newPosition)

	def HunterSysMsg(self, msg, color="PURPLE"):
		"""Mostra messaggio di sistema con colore rank"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowSystemMessage(msg, color)

	def HunterEventStatus(self, eventName, duration, eventType="default", desc="", reward=""):
		"""Mostra finestra stato evento"""
		if self.wndHunterLevel:
			self.wndHunterLevel.ShowEventStatus(eventName, duration, eventType, desc, reward)

	def HunterEventClose(self):
		"""Chiude la finestra stato evento"""
		if self.wndHunterLevel:
			self.wndHunterLevel.CloseEventStatus()

	# ============================================================
	# DAILY MISSIONS SYSTEM
	# ============================================================
	
	def HunterMissionsCount(self, count):
		"""Imposta numero missioni"""
		if self.wndHunterLevel:
			self.wndHunterLevel.SetMissionsCount(count)
	
	def HunterMissionData(self, missionData):
		"""Aggiunge dati missione"""
		if self.wndHunterLevel:
			self.wndHunterLevel.AddMissionData(missionData)
	
	def HunterMissionProgress(self, missionId, current, target):
		"""Aggiorna progresso missione"""
		if self.wndHunterLevel:
			self.wndHunterLevel.UpdateMissionProgress(missionId, current, target)
	
	def HunterMissionComplete(self, missionId, name, reward):
		"""Notifica missione completata"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnMissionComplete(missionId, name, reward)
	
	def HunterAllMissionsComplete(self, bonus, hasFractureBonus=False):
		"""Notifica tutte missioni complete + bonus fratture attivato"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnAllMissionsComplete(bonus, hasFractureBonus)
	
	def HunterMissionsOpen(self):
		"""Apre pannello missioni"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OpenMissionsPanel()
	
	def HunterOpenRankUp(self):
		"""Apre pannello Rank Up dalla finestra Trial"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OpenRankUpPanel()
	
	# ============================================================
	# EVENTS SYSTEM
	# ============================================================
	
	def HunterEventsCount(self, count):
		"""Imposta numero eventi"""
		if self.wndHunterLevel:
			self.wndHunterLevel.SetEventsCount(count)
	
	def HunterEventData(self, eventData):
		"""Aggiunge dati evento"""
		if self.wndHunterLevel:
			self.wndHunterLevel.AddEventData(eventData)
	
	def HunterEventJoined(self, eventId, name, glory):
		"""Conferma partecipazione evento"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnEventJoined(eventId, name, glory)
	
	def HunterEventsOpen(self):
		"""Apre pannello eventi"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OpenEventsPanel()

	def HunterNewDay(self):
		"""E' passata la mezzanotte - resetta cache eventi"""
		if self.wndHunterLevel:
			self.wndHunterLevel.OnNewDay()

	# ============================================================
	# FRACTURE DEFENSE SYSTEM - Usa finestra dedicata
	# ============================================================

	def HunterFractureDefenseStart(self, fractureName, duration, rank, totalMobs=0):
		"""Inizia difesa frattura con finestra dedicata"""
		defenseWnd = hunter_windows.GetDefenseWindow()
		if defenseWnd:
			defenseWnd.StartDefense(fractureName, rank, duration, totalMobs)

	def HunterFractureDefenseUpdate(self, killed, required, wave=0):
		"""Aggiorna progresso difesa"""
		defenseWnd = hunter_windows.GetDefenseWindow()
		if defenseWnd:
			defenseWnd.UpdateProgress(killed, required, wave)

	def HunterFractureDefenseTimer(self, remainingSeconds):
		"""Retrocompatibilita' - vecchio formato timer"""
		pass  # Non piu' necessario, il timer e' gestito dalla finestra

	def HunterFractureDefenseComplete(self, success, message=""):
		"""Completa difesa frattura"""
		defenseWnd = hunter_windows.GetDefenseWindow()
		if defenseWnd:
			defenseWnd.EndDefense(success == 1 or success == "1")

	# ============================================================
	# SPEED KILL SYSTEM
	# ============================================================

	def HunterSpeedKillStart(self, mobType, duration, mobName):
		"""Inizia speed kill challenge con UI dedicata"""
		speedKillWnd = hunter_windows.GetSpeedKillWindow()
		if speedKillWnd:
			# Determina il tipo di mob per i colori
			mobTypeKey = "DEFAULT"
			mobTypeStr = str(mobType).upper()
			mobNameStr = str(mobName).upper()
			if "METIN" in mobNameStr:
				mobTypeKey = "SUPER_METIN"
			elif "BOSS" in mobTypeStr or mobTypeStr.isdigit():
				mobTypeKey = "BOSS"
			speedKillWnd.StartSpeedKill(mobName, duration, mobTypeKey)

	def HunterSpeedKillTimer(self, remainingSeconds):
		"""Aggiorna timer speed kill"""
		speedKillWnd = hunter_windows.GetSpeedKillWindow()
		if speedKillWnd:
			speedKillWnd.UpdateTimer(remainingSeconds)

	def HunterSpeedKillEnd(self, isSuccess):
		"""Termina speed kill"""
		speedKillWnd = hunter_windows.GetSpeedKillWindow()
		if speedKillWnd:
			speedKillWnd.EndSpeedKill(isSuccess == 1 or isSuccess == "1")

	def HunterShowTip(self, tipText):
		"""Mostra un tip nella finestra Hunter Tips"""
		tipsWnd = hunter_windows.GetHunterTipsWindow()
		if tipsWnd:
			tipsWnd.AddTip(tipText)

# ==============================================================

	def ToggleHunterLevelWindow(self):
		if self.wndHunterLevel:
			if self.wndHunterLevel.IsShow():
				self.wndHunterLevel.Close()
			else:
				self.wndHunterLevel.Open()

	def OpenHunterLevelWindow(self):
		if self.wndHunterLevel:
			self.wndHunterLevel.Open()

	def CloseHunterLevelWindow(self):
		if self.wndHunterLevel:
			self.wndHunterLevel.Close()
# ==================== FINE HUNTER LEVEL SYSTEM ====================

# --- FINE COPIA ---


import ui, net, chat

class CaptchaDialog(ui.ScriptWindow):
    def __init__(self, code):
        ui.ScriptWindow.__init__(self)
        self.code = code
        self.BuildWindow()

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(250, 120)
        self.Board.SetCenterPosition()
        self.Board.AddFlag("movable")
        self.Board.AddFlag("float")
        self.Board.SetTitleName("Captcha Sicurezza")
        self.Board.Show()

        self.inputSlot = ui.EditLine()
        self.inputSlot.SetParent(self.Board)
        self.inputSlot.SetPosition(20, 50)
        self.inputSlot.SetSize(210, 20)
        self.inputSlot.SetMax(6)
        self.inputSlot.SetNumberMode()
        self.inputSlot.Show()

        self.btnSubmit = ui.Button()
        self.btnSubmit.SetParent(self.Board)
        self.btnSubmit.SetPosition(75, 80)
        self.btnSubmit.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
        self.btnSubmit.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
        self.btnSubmit.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
        self.btnSubmit.SetText("Conferma")
        self.btnSubmit.SetEvent(ui.__mem_func__(self.SubmitCaptcha))
        self.btnSubmit.Show()

    def SubmitCaptcha(self):
        inputCode = self.inputSlot.GetText()
        if len(inputCode) == 6:
            net.SendQuestInputStringPacket(inputCode)
            self.Board.Hide()
        else:
            chat.AppendChat(chat.CHAT_TYPE_INFO, "Il codice deve essere di 6 cifre!")

def OpenCaptchaDialog(self, code):
    self.captchaDlg = CaptchaDialog(code)

def OnRecvWhisper(self, name, line):
    if line.startswith("ShowCaptcha"):
        code = line.split()[1]
        self.OpenCaptchaDialog(code)