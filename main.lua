local o = {
    fetch_aot = 5,
}
local utils = require "mp.utils"
local options = require 'mp.options'
local chat_sid
local is_running
local channelname
local timer
local ON_WINDOWS = package.config:sub(1,1) ~= "/"
local python_path = ON_WINDOWS and "python" or "python3"
local ircdump = utils.join_path(mp.get_script_directory(), "ircdump.py")
options.read_options(o)

if not mp.get_script_directory() then
    mp.msg.error("This script requires to be placed in a script directory")
    return
end

local function timer_callback()
    mp.command_native({"sub-remove", chat_sid})
    mp.command_native({
        name = "sub-add",
        url = utils.join_path(mp.get_script_directory(), channelname .. ".txt"),
        title = "Twitch Chat"
    })
    chat_sid = mp.get_property_native("sid")

    local fetch_delay = o.fetch_aot
    timer = mp.add_timeout(fetch_delay, function()
        timer_callback()
    end)
end

local function handle_track_change(name, sid)
    if timer and sid then
        timer:resume()
        chat_sid = sid
    elseif timer and not sid then
        timer:stop()
    end
end

local function init()
    channelname = string.match(mp.get_property("path"), "^https://w?w?w?%.?twitch%.tv/([^/]-)$")
    if not channelname then
        return
    end
    local args = {
        python_path,
        ircdump,
        channelname,
        mp.get_script_directory(),
    }
    mp.command_native_async({
        name = "subprocess", 
        capture_stdout = false, 
        playback_only = false, 
        args = args,
    })
    -- enable subtitles button
    mp.command_native({
        name = "sub-add",
        url = "memory://" .. "1\n0:0:0,0 --> 999:0:0,0\nloading...",
        title = "Twitch Chat",
    })
    chat_sid = mp.get_property_native("sid")
    timer_callback()
end

mp.register_event("start-file", init)
mp.observe_property("current-tracks/sub/id", "native", handle_track_change)