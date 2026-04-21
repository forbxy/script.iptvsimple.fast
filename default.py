import xbmc
import xbmcgui
import xbmcvfs
import xml.etree.ElementTree as ET

SETTINGS_PATH = "special://userdata/addon_data/pvr.iptvsimple/instance-settings-1.xml"
TARGET_SETTINGS = {
    "defaultInputstream": "inputstream.ffmpegdirect",
    "defaultMimeType": "application/vnd.apple.mpegurl",
}

INTRO_MSG = (
    "原理：在 IPTV Simple Client 设置-高级 中写入以下两项，\n"
    "让播放时跳过流类型探测，直接用 ffmpegdirect 播放，切台更快：\n"
    "  defaultInputstream = inputstream.ffmpegdirect\n"
    "  defaultMimeType = application/vnd.apple.mpegurl\n"
)


def modify_xml(values):
    """将 TARGET_SETTINGS 的各项写入或清除（values 为 None 时清除）。"""
    real_path = xbmcvfs.translatePath(SETTINGS_PATH)

    if not xbmcvfs.exists(SETTINGS_PATH):
        xbmcgui.Dialog().notification(
            "IPTV Simple Fast Play",
            "找不到 instance-settings-1.xml，请先配置 IPTV Simple。",
            xbmcgui.NOTIFICATION_ERROR,
        )
        return

    tree = ET.parse(real_path)
    root = tree.getroot()

    changed = {}
    for setting_id in TARGET_SETTINGS:
        target_value = TARGET_SETTINGS[setting_id] if values else ""
        elem = root.find("./setting[@id='{}']".format(setting_id))
        if elem is None:
            if not values:
                continue
            elem = ET.SubElement(root, "setting")
            elem.set("id", setting_id)
        old = elem.text or ""
        if old != target_value:
            changed[setting_id] = (old, target_value)
        elem.text = target_value
        if values:
            if "default" in elem.attrib:
                del elem.attrib["default"]
        else:
            elem.set("default", "true")

    if not changed:
        xbmcgui.Dialog().notification(
            "IPTV Simple Fast Play",
            "设置已是目标设置，无需修改。",
            xbmcgui.NOTIFICATION_INFO,
        )
        return

    tree.write(real_path, encoding="utf-8", xml_declaration=True)

    action = "已设置" if values else "已清除"
    lines = ["{}: {}".format(sid, new) for sid, (old, new) in changed.items()]
    xbmcgui.Dialog().ok(
        "IPTV Simple Fast Play",
        "{}以下设置（重启 Kodi 生效）：\n\n{}".format(action, "\n".join(lines)),
    )


if __name__ == "__main__":
    # yesnocustom 返回值: 0=No(清除设置), 1=Yes(写入设置), 2=Custom(退出), -1=返回键
    choice = xbmcgui.Dialog().yesnocustom(
        "IPTV Simple Fast Play",
        INTRO_MSG,
        customlabel="退出",
        yeslabel="写入设置",
        nolabel="清除设置",
    )
    if choice == 1:
        modify_xml(TARGET_SETTINGS)
    elif choice == 0:
        modify_xml(None)
