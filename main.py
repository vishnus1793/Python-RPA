import re
import time
import pyautogui
import pygetwindow as gw

# Safety: Move mouse rapidly to any screen corner to abort immediately
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

def extract_notification_count(title: str) -> int:
    """Extracts notification count like '(3)' from a window title."""
    match = re.search(r"\((\d+)\)", title)
    return int(match.group(1)) if match else 0

def wait_for_edge_window(timeout: int = 15):
    """Waits until a Microsoft Edge window appears and brings it to focus."""
    start = time.time()
    while time.time() - start < timeout:
        windows = [w for w in gw.getWindowsWithTitle("Edge") if w.title.strip()]
        if windows:
            win = windows[0]
            try:
                if win.isMinimized:
                    win.restore()
                win.activate()
            except Exception:
                pass
            return win
        time.sleep(0.5)
    return None

def main():
    print("Starting UI RPA bot in 3 seconds... Keep your hands off the mouse/keyboard.")
    time.sleep(3)

    # Step 1: Press Windows key, type 'edge', and press Enter
    print("[1/5] Pressing Windows key and launching Microsoft Edge...")
    pyautogui.press("win")
    time.sleep(1.0)  # Give Start Menu animation time to open
    pyautogui.write("edge", interval=0.08)
    time.sleep(1.0)  # Wait for Windows Search to highlight Microsoft Edge
    pyautogui.press("enter")

    # Wait until Edge actually opens on screen instead of guessing a fixed sleep
    print("      Waiting for Edge window to appear...")
    edge_win = wait_for_edge_window(timeout=15)
    if not edge_win:
        print("[ERROR] Edge window did not open in time.")
        return
    time.sleep(1.0)

    # Step 2: Focus address bar (Ctrl + L) and open YouTube
    print("[2/5] Opening YouTube in Tab 1...")
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.3)
    pyautogui.write("https://www.youtube.com", interval=0.03)
    pyautogui.press("enter")
    time.sleep(1.5)

    # Step 3: Press Ctrl + T to open a second tab
    print("[3/5] Opening a new tab (Ctrl + T)...")
    pyautogui.hotkey("ctrl", "t")
    time.sleep(0.8)

    # Step 4: Type web.whatsapp.com and press Enter
    print("[4/5] Opening WhatsApp Web in Tab 2...")
    pyautogui.write("https://web.whatsapp.com", interval=0.03)
    pyautogui.press("enter")
    time.sleep(2.0)

    # Step 5: Monitor both tabs by cycling Ctrl + Tab every 4 seconds
    print("\n[5/5] Monitoring Edge tabs for notifications (auto-switching tabs every 4s)...")
    print(" -> Slam mouse into top-left corner or press Ctrl+C in terminal to stop.\n")

    last_notified = {}

    try:
        while True:
            edge_windows = [w for w in gw.getWindowsWithTitle("Edge") if w.title.strip()]
            if not edge_windows:
                print("\n[STOPPED] Microsoft Edge window was closed.")
                break

            active_title = edge_windows[0].title
            count = extract_notification_count(active_title)

            # Identify which site is currently active
            site = "WhatsApp" if "WhatsApp" in active_title else ("YouTube" if "YouTube" in active_title else "Other")

            if site in ["WhatsApp", "YouTube"]:
                prev_count = last_notified.get(site, 0)
                if count != prev_count:
                    if count > 0:
                        print(f"[{time.strftime('%H:%M:%S')}] 🔔 {site.upper()} ALERT: {count} new notification(s)! ({active_title})")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] ✅ {site} notifications cleared.")
                    last_notified[site] = count

            time.sleep(4)

            # Switch to the other tab if Edge is currently the active foreground window
            active_win = gw.getActiveWindow()
            if active_win and "Edge" in active_win.title:
                pyautogui.hotkey("ctrl", "tab")
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[STOPPED] Monitoring ended by user.")
    except pyautogui.FailSafeException:
        print("\n[STOPPED] Failsafe triggered (mouse moved to screen corner).")

if __name__ == "__main__":
    main()