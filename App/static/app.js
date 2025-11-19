const API_BASE = ""; // same origin as FastAPI

const state = {
    chart: null,
    dataPoints: [],   // { t: Date, price: number }
    streamTimer: null,
    smaWindow: 10
};

function log(message) {
    const logEl = document.getElementById("log");
    const timestamp = new Date().toLocaleTimeString();
    logEl.textContent = `[${timestamp}] ${message}\n` + logEl.textContent;
}

// --- API calls ---

async function fetchAllowedSymbols() {
    const res = await fetch(`${API_BASE}/allowed-symbols`);
    if (!res.ok) {
        throw new Error(`Failed to load symbols: ${res.status}`);
    }
    return res.json(); // { symbols: [...] }
}

async function fetchDashboardData(symbol, window = 10, limit = 100) {
    const url = `${API_BASE}/dashboard-data` +
        `?symbol=${encodeURIComponent(symbol)}` +
        `&window=${encodeURIComponent(window)}` +
        `&limit=${encodeURIComponent(limit)}`;

    const res = await fetch(url);
    if (!res.ok) {
        // Try to read FastAPI HTTPException detail
        let detail = `status ${res.status}`;
        try {
            const body = await res.json();
            if (body && body.detail) {
                detail = body.detail;
            }
        } catch (_) {
            // ignore
        }
        throw new Error(`Failed to fetch dashboard data: ${detail}`);
    }
    return res.json(); // { price, timeseries, sma, fundamentals, ... }
}

// --- UI helpers ---

async function initSymbolDropdown() {
    const select = document.getElementById("symbol-select");
    try {
        const data = await fetchAllowedSymbols();
        const symbols = data.symbols || [];

        select.innerHTML = "";
        symbols.forEach(sym => {
            const opt = document.createElement("option");
            opt.value = sym;
            opt.textContent = sym;
            select.appendChild(opt);
        });

        if (symbols.length > 0) {
            select.value = symbols[0];
        }

        log(`Loaded ${symbols.length} allowed stock symbols.`);
    } catch (err) {
        log(`Error loading symbols: ${err.message}`);
    }
}

function setCurrentPriceDisplay(price) {
    const el = document.getElementById("current-price");
    if (price == null) {
        el.textContent = "$—";
    } else {
        el.textContent = `$${price.toFixed(2)}`;
    }
}

function setSMADisplay(smaObj) {
    const windowEl = document.getElementById("sma-window");
    const resultEl = document.getElementById("sma-result");

    if (!smaObj || smaObj.error || smaObj.sma == null) {
        resultEl.textContent = smaObj && smaObj.error ? smaObj.error : "N/A";
        return;
    }

    if (smaObj.window != null) {
        windowEl.textContent = smaObj.window.toString();
    }
    resultEl.textContent = `$${smaObj.sma.toFixed(2)}`;
}

function setFundamentalsDisplay(f) {
    // If backend reported an error, show placeholders
    if (!f || f.error) {
        document.getElementById("fund-longName").textContent = f && f.error ? f.error : "N/A";
        document.getElementById("fund-marketCap").textContent = "—";
        document.getElementById("fund-pe").textContent = "—";
        document.getElementById("fund-divYield").textContent = "—";
        document.getElementById("fund-52wLow").textContent = "—";
        document.getElementById("fund-52wHigh").textContent = "—";
        return;
    }

    const fmtNumber = (n) => {
        if (n == null) return "—";
        if (typeof n === "number") {
            // basic pretty formatting for large numbers
            if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
            if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
            if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
            return n.toLocaleString();
        }
        return String(n);
    };

    document.getElementById("fund-longName").textContent = f.longName || f.symbol || "—";
    document.getElementById("fund-marketCap").textContent = fmtNumber(f.marketCap);
    document.getElementById("fund-pe").textContent = f.trailingPE != null ? f.trailingPE.toFixed(2) : "—";

    if (f.dividendYield != null) {
        // yfinance dividendYield is typically a fraction (e.g., 0.01 for 1%)
        document.getElementById("fund-divYield").textContent = (f.dividendYield * 100).toFixed(2) + "%";
    } else {
        document.getElementById("fund-divYield").textContent = "—";
    }

    document.getElementById("fund-52wLow").textContent =
        f.fiftyTwoWeekLow != null ? f.fiftyTwoWeekLow.toFixed(2) : "—";
    document.getElementById("fund-52wHigh").textContent =
        f.fiftyTwoWeekHigh != null ? f.fiftyTwoWeekHigh.toFixed(2) : "—";
}

// --- Chart.js setup/update ---

function initChart() {
    const ctx = document.getElementById("price-chart");
    state.chart = new Chart(ctx, {
        type: "line",
        data: {
            datasets: [
                {
                    label: "Price",
                    data: [], // { x: time, y: price }
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: "time",
                    time: {
                        tooltipFormat: "HH:mm:ss",
                        displayFormats: {
                            second: "HH:mm:ss",
                            minute: "HH:mm"
                        }
                    },
                    title: {
                        display: true,
                        text: "Time"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Price (USD)"
                    }
                }
            },
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
}

function replaceDataSeries(points) {
    // points: [{ timestamp, price }, ...]
    state.dataPoints = points.map(p => ({
        t: new Date(p.timestamp),
        price: p.price
    }));

    if (!state.chart) return;
    const dataset = state.chart.data.datasets[0];
    dataset.data = state.dataPoints.map(dp => ({
        x: dp.t,
        y: dp.price
    }));
    state.chart.update("none");
}

function appendLatestPricePoint(price) {
    const now = new Date();
    const dp = { t: now, price };
    state.dataPoints.push(dp);

    if (!state.chart) return;
    const dataset = state.chart.data.datasets[0];
    dataset.data.push({ x: dp.t, y: dp.price });

    if (dataset.data.length > 200) {
        dataset.data.shift();
        state.dataPoints.shift();
    }

    state.chart.update("none");
}

// --- Main dashboard update from backend ---

async function fetchAndRenderDashboardOnce() {
    const select = document.getElementById("symbol-select");
    const symbol = select.value;
    if (!symbol) {
        log("No symbol selected.");
        return;
    }

    try {
        const data = await fetchDashboardData(symbol, state.smaWindow, 100);

        // 1) Current price
        if (data.price && data.price.price != null) {
            setCurrentPriceDisplay(data.price.price);
        } else {
            setCurrentPriceDisplay(null);
        }

        // 2) Timeseries (replace local chart data with backend data if available)
        let points = null;
        if (data.timeseries && Array.isArray(data.timeseries.points)) {
            points = data.timeseries.points;
        }

        if (points && points.length > 0) {
            // Backend has real history → use it
            replaceDataSeries(points);
        } else if (data.price && data.price.price != null) {
            // No history yet → at least plot the latest price
            appendLatestPricePoint(data.price.price);
        }

        // 3) SMA from backend
        setSMADisplay(data.sma);

        // 4) Fundamentals
        setFundamentalsDisplay(data.fundamentals);

        log(`Dashboard updated for ${symbol}.`);
    } catch (err) {
        log(`Dashboard fetch error: ${err.message}`);
    }
}

// --- Live update loop ---

function startLiveUpdates() {
    if (state.streamTimer) return;

    // For the real project, 5 minutes (300000) matches the backend polling interval.
    // For demo/testing, 5000 ms is nicer
    const intervalMs = 5000;

    state.streamTimer = setInterval(fetchAndRenderDashboardOnce, intervalMs);

    document.getElementById("start-stream-btn").disabled = true;
    document.getElementById("stop-stream-btn").disabled = false;

    log("Live updates started.");
}

function stopLiveUpdates() {
    if (!state.streamTimer) return;

    clearInterval(state.streamTimer);
    state.streamTimer = null;

    document.getElementById("start-stream-btn").disabled = false;
    document.getElementById("stop-stream-btn").disabled = true;

    log("Live updates stopped.");
}

// --- Initialization ---

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("sma-window").textContent = state.smaWindow.toString();

    initChart();

    initSymbolDropdown().then(() => {
        fetchAndRenderDashboardOnce();
    });

    document.getElementById("fetch-once-btn")
        .addEventListener("click", fetchAndRenderDashboardOnce);

    document.getElementById("start-stream-btn")
        .addEventListener("click", startLiveUpdates);

    document.getElementById("stop-stream-btn")
        .addEventListener("click", stopLiveUpdates);
});

