//Creating a Mapping Table

//Since team names don't change often, hard-coding a "Lookup Table" for edge cases (like "NYK" vs "Knicks") will save your CPU from doing fuzzy math on every page scroll.

const TEAM_ALIASES = {
  "NYK": "New York Knicks",
  "GSW": "Golden State Warriors",
  "MAN UTD": "Manchester United",
  // Add more as you find them
};

function resolveTeamName(input) {
  const upper = input.toUpperCase();
  return TEAM_ALIASES[upper] || input;
}
