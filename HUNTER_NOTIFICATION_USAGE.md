# Hunter Notification System - Usage Guide

## Overview

The Hunter Notification System replaces chat spam with an elegant notification UI window. It features:

- **Queue system** - Multiple notifications display one after another
- **5 notification types** with distinct color schemes
- **Auto fade-in/fade-out** animations
- **No chat spam** - Clean UI that doesn't clutter the chat

## Notification Types

| Type | Color | Icon | Use Case |
|------|-------|------|----------|
| `winner` | Gold | [*] | Event winners, lottery wins |
| `achievement` | Green | [+] | Achievement/Trial completions |
| `rank` | Purple | [^] | Rank/Grade changes |
| `system` | Blue | [!] | System messages |
| `event` | Orange | [E] | Event announcements |

## Lua Functions

### Send notification to single player

```lua
hg_lib.send_notification(player_pid, notification_type, message)
```

**Parameters:**
- `player_pid` - Player ID (use `0` for current player)
- `notification_type` - One of: "winner", "achievement", "rank", "system", "event"
- `message` - Text message to display

**Examples:**

```lua
-- Achievement completion
hg_lib.send_notification(0, "achievement", "Hai completato il traguardo: Cacciatore Esperto!")

-- Event winner
local pid = pc.get_player_id()
hg_lib.send_notification(pid, "winner", "Hai vinto l'evento Elite Hunt con 150 punti!")

-- Rank upgrade
hg_lib.send_notification(0, "rank", "Sei salito al grado S! Gloria: 500.000")

-- System message
hg_lib.send_notification(0, "system", "Il tuo party ha completato la frattura!")
```

### Send notification to entire party

```lua
hg_lib.send_notification_to_party(notification_type, message)
```

**Example:**

```lua
-- Notify entire party
hg_lib.send_notification_to_party("event", "Il party ha completato la Frattura Aurea!")
```

## Where to Use Notifications

### ✅ Replace chat spam for:

1. **Event Winners** - Lines 2183-2185, 2122
   ```lua
   -- OLD: notice_all(...)
   -- NEW: hg_lib.send_notification(winner_id, "winner", "Hai vinto l'evento con +" .. glory_prize .. " Gloria!")
   ```

2. **Achievement Completions** - Line 5947
   ```lua
   -- OLD: syschat("[TRAGUARDO] completato!")
   -- NEW: hg_lib.send_notification(0, "achievement", ach_name .. " completato!")
   ```

3. **Rank Changes** - Lines 2301-2318
   ```lua
   -- OLD: Multiple syschat lines
   -- NEW: hg_lib.send_notification(0, "rank", "Sei salito al grado " .. rank_key .. "!")
   ```

4. **Event Announcements** - Lines 2259-2260
   ```lua
   -- OLD: notice_all for event start/end
   -- NEW: Use "event" type notification
   ```

### ❌ Keep using chat for:
- Combat messages
- Error messages
- Debug output
- Quick status updates

## Implementation Example

Here's a complete example replacing event winner announcement:

### Before (chat spam):
```lua
notice_all("|cffFFD700[HUNTER ESTRAZIONE]|r " .. winner_name .. " ha vinto +" .. glory_prize .. " Gloria!")
notice_all("|cff00FF00Congratulazioni al vincitore dell'evento " .. event_name .. "!|r")

if current_pid == winner_id then
    syschat("|cffFFD700=============================================|r")
    syschat("[!!!] HAI VINTO L'ESTRAZIONE! [!!!]")
    syschat("|cffFFD700=============================================|r")
    syschat("Premio Gloria: +" .. glory_prize)
    -- ... more syschat lines
end
```

### After (notification UI):
```lua
-- Send notification only to winner
if current_pid == winner_id then
    local msg = "Hai vinto l'evento " .. event_name .. " con +" .. glory_prize .. " Gloria!"
    hg_lib.send_notification(winner_id, "winner", msg)
end
```

## Benefits

1. **No chat spam** - Chat remains clean and readable
2. **Better visibility** - Colored notifications stand out
3. **Queue system** - Multiple notifications display sequentially
4. **Professional look** - Animated, polished UI
5. **Flexible positioning** - Draggable window

## Technical Details

- Notifications auto-dismiss after **8 seconds**
- Fade in/out duration: **1.5 seconds**
- Queue processes notifications sequentially
- Window can be repositioned by dragging
- Reset on map change/logout automatically

## Files Modified

- `hunter_windows.py` - Added `HunterNotificationWindow` class
- `interfacemodule.py` - Added `HunterNotification` command handler
- `hunterlib.lua` - Added `send_notification` and `send_notification_to_party` functions
