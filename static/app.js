const grid = document.getElementById("grid");
const searchInput = document.getElementById("search");
const countEl = document.getElementById("count");
const errorEl = document.getElementById("error");

let allCars = [];

// Skeletons while loading
const skels = document.getElementById("skeletons");
for (let i = 0; i < 8; i++) {
  skels.innerHTML += `<div class="skel">
    <div class="skel-img"></div>
    <div class="skel-line"></div>
    <div class="skel-line short"></div>
    <div class="skel-line btn"></div>
  </div>`;
}

function formatPrice(price) {
  if (!price) return "Price on request";
  const krw = price * 10000;
  if (krw >= 100000000) return `₩${(krw / 100000000).toFixed(1)}억`;
  return `₩${Math.round(krw / 10000).toLocaleString()}만`;
}

function formatMileage(km) {
  if (!km) return "—";
  return Math.round(km).toLocaleString() + " km";
}

function formatYear(year) {
  if (!year) return "—";
  const y = String(Math.round(year));
  return y.length >= 6 ? y.slice(0, 4) + "." + y.slice(4, 6) : y;
}

function renderCard(car) {
  return `<div class="card" onclick="window.open('${car.url}','_blank')">
    <div class="card-img-wrap">
      <img
        class="card-img"
        src="${car.photo || ''}"
        alt="${car.name}"
        loading="lazy"
        onerror="this.parentElement.innerHTML='<div class=card-img-placeholder>🚗</div>'"
      >
    </div>
    <div class="card-body">
      <div class="card-name">${car.name}</div>
      <div class="card-meta">
        <span>📅 ${formatYear(car.year)}</span>
        <span>🛣 ${formatMileage(car.mileage)}</span>
      </div>
      <div class="card-price">${formatPrice(car.price)}</div>
      <a class="card-btn" href="${car.url}" target="_blank" onclick="event.stopPropagation()">View on Encar →</a>
    </div>
  </div>`;
}

function render(cars) {
  grid.innerHTML = cars.map(renderCard).join("");
  countEl.textContent = `${cars.length} cars`;
}

function filter(query) {
  const q = query.toLowerCase();
  return allCars.filter(c =>
    c.name.toLowerCase().includes(q) ||
    (c.manufacturer || "").toLowerCase().includes(q) ||
    (c.model || "").toLowerCase().includes(q)
  );
}

searchInput.addEventListener("input", () => render(filter(searchInput.value)));

fetch("/api/cars")
  .then(r => r.json())
  .then(data => {
    if (data.error) throw new Error(data.error);
    allCars = data.cars || [];
    render(allCars);
  })
  .catch(err => {
    grid.innerHTML = "";
    errorEl.textContent = "⚠️ " + err.message;
    errorEl.classList.remove("hidden");
  });
