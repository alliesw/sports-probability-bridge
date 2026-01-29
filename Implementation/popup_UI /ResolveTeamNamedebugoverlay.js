//Updated resolveTeamName

//We’ll update this function to check the dictionary and expand any abbreviations it finds.

function resolveTeamName(name) {
  if (!name) return "";
  let cleanName = name.toLowerCase().trim();

  // Split the name into words and check if any word is in our alias map
  // Example: "NY Knicks" becomes "new york knicks"
  const words = cleanName.split(' ');
  const expandedWords = words.map(word => TEAM_ALIASES[word] || word);
  
  return expandedWords.join(' ');
}

//------------------------------------------------------------------
//Consolidated Logic with Debugging

//This version tracks the highest score found during the loop and displays it in the overlay.

const TEAM_ALIASES = {
  "ny": "new york", "la": "los angeles", "gs": "golden state",
  "warriors": "golden state warriors", "philly": "philadelphia",
  "phx": "phoenix", "lv": "las vegas", "usa": "united states"
};

function resolveTeamName(name) {
  if (!name) return "";
  let cleanName = name.toLowerCase().trim();
  const words = cleanName.split(/\s+/);
  return words.map(word => TEAM_ALIASES[word] || word).join(' ');
}

function getSimilarity(s1, s2) {
  const str1 = resolveTeamName(s1);
  const str2 = resolveTeamName(s2);
  const longer = str1.length > str2.length ? str1 : str2;
  const shorter = str1.length > str2.length ? str2 : str1;
  if (longer.length === 0) return 1.0;

  const costs = [];
  for (let i = 0; i <= str1.length; i++) {
    let lastValue = i;
    for (let j = 0; j <= str2.length; j++) {
      if (i === 0) costs[j] = j;
      else if (j > 0) {
        let newValue = costs[j - 1];
        if (str1.charAt(i - 1) !== str2.charAt(j - 1)) {
          newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
        }
        costs[j - 1] = lastValue;
        lastValue = newValue;
      }
    }
    if (i > 0) costs[str2.length] = lastValue;
  }
  return (longer.length - costs[str2.length]) / longer.length;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "KALSHI_UPDATE") {
    const kalshiMarket = message.payload.title;
    const teamElements = document.querySelectorAll('.team-name-class'); // Update per site
    const debugDiv = document.getElementById('debug-info');
    
    let bestMatch = { name: "None", score: 0 };

    Array.from(teamElements).forEach(el => {
      const teamName = el.innerText;
      const score = getSimilarity(teamName, kalshiMarket);

      if (score > bestMatch.score) {
        bestMatch = { name: teamName, score: score };
      }
    });

    // Update Debug UI
    if (debugDiv) {
      debugDiv.innerHTML = `
        Best Match: ${bestMatch.name}<br>
        Score: ${(bestMatch.score * 100).toFixed(1)}%
      `;
    }

    // Update Main UI if threshold met
    if (bestMatch.score > 0.7) {
      document.getElementById('live-val').innerText = `${message.payload.price}¢`;
    }
  }
  return true;
});
//3. How to use this for fine-tuning

//Watch the Score: If you see "Lakers" matching at 65%, you'll know you need to either lower your threshold to 0.6 or add "lakers" to your TEAM_ALIASES.

//Verify Selectors: If the "Best Match" consistently says "None," it means your .team-name-class selector isn't finding the text on the page.
