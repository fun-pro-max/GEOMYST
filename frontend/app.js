let seenStories = JSON.parse(localStorage.getItem("seenStories") || "[]");

let storyMarker = null;

const map = L.map('map', { zoomControl: false }).setView([20, 0], 2);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);


/* ======================================
   AUTO SELECT A RANDOM LOCATION ON LOAD
====================================== */

window.addEventListener("load", async () => {
    await travelRandom();
});


/* ======================================
   FETCH RANDOM LOCATION FROM BACKEND
====================================== */

async function travelRandom() {
    const res = await fetch("http://127.0.0.1:8000/random-location");
    const data = await res.json();

    const { lat, lng, state } = data;

    map.flyTo([lat, lng], 6, { duration: 3 });

    if (storyMarker) map.removeLayer(storyMarker);
    storyMarker = L.marker([lat, lng]).addTo(map);

    await fetchStory(state, lat, lng);
}


/* ======================================
   FETCH STORY
====================================== */

async function fetchStory(state, lat, lng) {

    const card = document.getElementById("storyCard");
    card.classList.add("loading");

    const res = await fetch("http://127.0.0.1:8000/story", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            state: state,
            lat: lat,
            lng: lng,
            seen: seenStories
        })
    });

    const story = await res.json();

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
   TYPEWRITER EFFECT
====================================== */

function typeWriter(element, html, speed = 8) {
    element.innerHTML = "";
    let i = 0;

    function type() {
        if (i < html.length) {
            element.innerHTML = html.slice(0, i++);
            requestAnimationFrame(type);
        }
    }
    type();
}
