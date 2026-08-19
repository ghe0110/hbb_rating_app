const state = {
  ratingType: "current",
  season: "all",
  factor: "overall",
  page: 1,
  pageSize: 50,
};

async function loadRatings() {
  const path = state.ratingType === "historical"
    ? "./data/historical/historical_rating.csv"
    : state.ratingType === "live"
      ? "./data/current/live_rating.csv"
      : "./data/current/current_rating.csv";

  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } catch {
    return "";
  }
}

function render() {
  // UI implementation can be expanded without changing the data model.
}

window.addEventListener("DOMContentLoaded", render);
