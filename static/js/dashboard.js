const STATUS_ENDPOINT = "/api/status";
const REFRESH_INTERVAL_MS = 5000;

const metricElements = {
    statusMessage: document.getElementById("status-message"),
    lastUpdated: document.getElementById("last-updated"),
    hostname: document.getElementById("metric-hostname"),
    localIp: document.getElementById("metric-local-ip"),
    cpu: document.getElementById("metric-cpu"),
    cpuBar: document.getElementById("metric-cpu-bar"),
    cpuDetail: document.getElementById("metric-cpu-detail"),
    memory: document.getElementById("metric-memory"),
    memoryBar: document.getElementById("metric-memory-bar"),
    memoryDetail: document.getElementById("metric-memory-detail"),
    disk: document.getElementById("metric-disk"),
    diskBar: document.getElementById("metric-disk-bar"),
    diskDetail: document.getElementById("metric-disk-detail"),
    uptime: document.getElementById("metric-uptime"),
};

let hasLoadedMetrics = false;
let isRefreshing = false;

function setStatusMessage(message, state) {
    metricElements.statusMessage.textContent = message;
    metricElements.statusMessage.className = `status-message status-message--${state}`;
}

function setCardState(state) {
    document.querySelectorAll("[data-metric-card]").forEach((card) => {
        card.classList.remove("metric-card--loading", "metric-card--error", "metric-card--ready");
        card.classList.add(`metric-card--${state}`);
    });
}

function formatText(value) {
    if (typeof value !== "string" || value.trim() === "") {
        return "Unavailable";
    }

    return value;
}

function getPercent(value) {
    const percent = Number(value);

    if (!Number.isFinite(percent)) {
        return null;
    }

    return Math.min(100, Math.max(0, percent));
}

function formatPercent(value) {
    const percent = getPercent(value);

    if (percent === null) {
        return "Unavailable";
    }

    return `${percent.toLocaleString(undefined, { maximumFractionDigits: 1 })}%`;
}

function formatBytes(value) {
    const bytes = Number(value);

    if (!Number.isFinite(bytes) || bytes < 0) {
        return "Unavailable";
    }

    const units = ["B", "KB", "MB", "GB", "TB"];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex += 1;
    }

    const precision = unitIndex === 0 ? 0 : 1;
    return `${size.toLocaleString(undefined, { maximumFractionDigits: precision })} ${units[unitIndex]}`;
}

function setBar(barElement, percent) {
    const safePercent = getPercent(percent);
    barElement.style.width = `${safePercent === null ? 0 : safePercent}%`;
}

function updateUsageMetric(valueElement, barElement, detailElement, usage, detailLabel) {
    const total = Number(usage?.total);
    const used = Number(usage?.used);
    const percent = getPercent(usage?.percent);

    if (percent === null || !Number.isFinite(total) || total <= 0 || !Number.isFinite(used) || used < 0) {
        valueElement.textContent = "Unavailable";
        detailElement.textContent = `Could not read ${detailLabel} data`;
        setBar(barElement, 0);
        return;
    }

    valueElement.textContent = formatPercent(percent);
    detailElement.textContent = `${formatBytes(used)} of ${formatBytes(total)} used`;
    setBar(barElement, percent);
}

function updateCpuMetric(cpuUsage) {
    const percent = getPercent(cpuUsage);

    metricElements.cpu.textContent = formatPercent(cpuUsage);
    metricElements.cpuDetail.textContent = percent === null ? "Could not read CPU data" : "Current processor load";
    setBar(metricElements.cpuBar, percent);
}

function updateLastUpdated() {
    const timestamp = new Date().toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });

    metricElements.lastUpdated.textContent = `Last updated: ${timestamp}`;
}

function updateDashboard(data) {
    metricElements.hostname.textContent = formatText(data.hostname);
    metricElements.localIp.textContent = formatText(data.local_ip);
    metricElements.uptime.textContent = formatText(data.uptime?.formatted);

    updateCpuMetric(data.cpu_usage);
    updateUsageMetric(
        metricElements.memory,
        metricElements.memoryBar,
        metricElements.memoryDetail,
        data.memory_usage,
        "RAM",
    );
    updateUsageMetric(
        metricElements.disk,
        metricElements.diskBar,
        metricElements.diskDetail,
        data.disk_usage,
        "disk",
    );

    updateLastUpdated();
    setCardState("ready");
    setStatusMessage("Metrics loaded successfully.", "success");
    hasLoadedMetrics = true;
}

function showInitialError() {
    setCardState("error");
    metricElements.hostname.textContent = "Unavailable";
    metricElements.localIp.textContent = "Unavailable";
    metricElements.cpu.textContent = "Unavailable";
    metricElements.memory.textContent = "Unavailable";
    metricElements.disk.textContent = "Unavailable";
    metricElements.uptime.textContent = "Unavailable";
    metricElements.cpuDetail.textContent = "Could not read CPU data";
    metricElements.memoryDetail.textContent = "Could not read RAM data";
    metricElements.diskDetail.textContent = "Could not read disk data";
    setBar(metricElements.cpuBar, 0);
    setBar(metricElements.memoryBar, 0);
    setBar(metricElements.diskBar, 0);
}

async function refreshMetrics() {
    if (isRefreshing) {
        return;
    }

    isRefreshing = true;

    try {
        const response = await fetch(STATUS_ENDPOINT, {
            headers: { Accept: "application/json" },
            cache: "no-store",
        });

        if (!response.ok) {
            throw new Error(`Status request failed with HTTP ${response.status}`);
        }

        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error(error);

        if (!hasLoadedMetrics) {
            showInitialError();
        }

        setStatusMessage("Unable to load server metrics from /api/status. Check that the Flask app is running.", "error");
    } finally {
        isRefreshing = false;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setCardState("loading");
    refreshMetrics();
    window.setInterval(refreshMetrics, REFRESH_INTERVAL_MS);
});
