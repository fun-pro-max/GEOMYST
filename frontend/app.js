if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js");
}

/* ======================================
   STATE
====================================== */

const API = window.location.origin;

let seenStories = JSON.parse(localStorage.getItem("seenStories") || "[]");
let storyMarker = null;

const map = L.map("map", { zoomControl: false }).setView([20, 0], 2);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19
}).addTo(map);


/* ======================================
   AUTO LOAD EXPERIENCE
====================================== */

window.addEventListener("load", async () => {
    await safeStart();
});


async function safeStart() {
    try {
        await travelRandom();
    } catch (e) {
        console.error("Startup failed:", e);
        showError("Signal lost. Retrying connection...");
        setTimeout(safeStart, 2500);
    }
}


/* ======================================
   GET RANDOM LOCATION
====================================== */

async function travelRandom() {

    const res = await fetch(`${API}/random-location`);
    if (!res.ok) throw new Error("Backend sleeping");

    const data = await res.json();
    const { lat, lng, state } = data;

    map.flyTo([lat, lng], 6, { duration: 2.8 });

    if (storyMarker) {
        map.removeLayer(storyMarker);
    }

    storyMarker = L.marker([lat, lng]).addTo(map);

    await fetchStory(state);
}


/* ======================================
   FETCH STORY
====================================== */

async function fetchStory(state) {

    const card = document.getElementById("storyCard");
    card.classList.add("loading");

    const res = await fetch(`${API}/story`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            state: state,
            seen: seenStories
        })
    });

    if (!res.ok) throw new Error("Story fetch failed");

    const story = await res.json();

    if (!story || !story.id) {
        throw new Error("Invalid story payload");
    }

    seenStories.push(story.id);
    localStorage.setItem("seenStories", JSON.stringify(seenStories));

    showStory(story);
}


/* ======================================
   DISPLAY STORY + MINIMIZE MAP
====================================== */

function showStory(story) {

    document.body.classList.add("focus-mode");

    const title = document.getElementById("title");
    const content = document.getElementById("summary");

    title.innerText = story.heading;

    const formatted = `
        <div class="fact-block">${story.fact}</div>
        <div class="mystery-block">${story.mystery}</div>
        <div class="archive-tag">ARCHIVE TRACE · ${story.place}</div>
    `;

    typeWriter(content, formatted);
}


/* ======================================
   TYPEWRITER EFFECT (HTML SAFE)
====================================== */

function typeWriter(element, html, speed = 12) {
    element.innerHTML = "";
    let i = 0;

    function type() {
        if (i <= html.length) {
            element.innerHTML = html.substring(0, i++);
            setTimeout(type, speed);
        }
    }

    type();
}


/* ======================================
   ERROR DISPLAY
====================================== */

function showError(message) {
    const title = document.getElementById("title");
    const content = document.getElementById("summary");

    title.innerText = "Connection Disturbance";
    content.innerHTML = `<div class="fact-block">${message}</div>`;
}

/* ======================================
   BUTTON: LOAD NEW LOCATION
====================================== */

document.getElementById("newLocationBtn")
    .addEventListener("click", async () => {

        document.body.classList.remove("focus-mode");

        await travelRandom();
});
