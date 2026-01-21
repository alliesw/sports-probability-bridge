# Sports-Betting-Chrome-Extension

(1) Tool that integrates directly with major books like Kalshi, FanDuel, and Draftkings. It allows you to analyze player props, while showing you where the best odds are currently live and links your sports books accounts to track your ROI from several sports betting apps - providing insight into how much money and time your spending and means to stop sports betting if it's a problem.  


Requirements: 
Extensions will need to handle both WebSockets (for Kalshi's rapid updates) and REST APIs or DOM Scraping (for FanDuel).
Implementation Checklist

Check Selectors: Verify that .team-name-class is the actual class FanDuel is currently using (these change frequently).

Debouncing: If the page is very active, the observer might fire too often. You can "debounce" the performMatch function to limit it to running once every 500ms.

Permissions: Ensure your manifest.json has host_permissions for both Kalshi and FanDuel.

PROJECT ARCHITECTURE: 
Component         Responsibility
-----------------------------------------------------------------------------------------
Manifest (v3),    Declares permissions (host_permissions) for kalshi.com and fanduel.com.
Service Worker,   Maintains the WebSocket connection to Kalshi and fetches FanDuel data.
Content Script,   Injects the UI (stats overlay) directly onto the betting pages.
Popup UI,         Allows the user to toggle specific leagues or markets on/off.

