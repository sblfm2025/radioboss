/* ==========================================================================
   LOGIKA INTERAKTIF JAVASCRIPT - GAYA INDUSTRI OBS / GRAFANA
   Mengelola: Navigasi Tab, AJAX Polling asinkron, Live Progress Worker, & Toasts
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Inisialisasi awal dashboard stats
    loadDashboardStats();
    
    // 2. Setup Navigasi Tab Sidebar
    const menuItems = document.querySelectorAll(".menu-item");
    const tabPanes = document.querySelectorAll(".tab-pane");
    const tabTitle = document.getElementById("current-tab-title");
    const tabSubtitle = document.getElementById("current-tab-subtitle");
    
    const tabHeaders = {
        "dashboard": { title: "Dashboard Utama", subtitle: "Pantau kesehatan pustaka siaran dan status kelayakan on-air Radio SBL." },
        "scanner": { title: "Pindai & Audit Drive", subtitle: "Pindai file musik stasiun radio secara aman untuk mendeteksi ancaman playback." },
        "playlists": { title: "Hasil Audit Playlist", subtitle: "Laporan file playlist stasiun radio yang rusak (Error Code 2) atau bermasalah." },
        "scheduler": { title: "Hasil Audit Scheduler", subtitle: "Pemilahan grup scheduler Ramadhan, waktu adzan, dan random source mentah." },
        "cartwall": { title: "Penataan Cart Wall", subtitle: "Rencana penempatan jingle program, sweeper, spot ILM stasiun ke tab steril." },
        "migration": { title: "Folder & Copier", subtitle: "Bangun folder steril baru dan salin aset approved secara aman (Dry-Run + Fisik)." },
        "reports": { title: "Laporan & Dokumen", subtitle: "Semua ekspor laporan CSV dan dokumen panduan manual administrator." },
        "settings": { title: "Pengaturan Sistem", subtitle: "Ubah direktori target fresh reset stasiun radio dan konfigurasi SQLite." }
    };

    menuItems.forEach(item => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            const targetTab = item.getAttribute("data-tab");
            
            // Perbarui class active navigasi
            menuItems.forEach(m => m.classList.remove("active"));
            item.classList.add("active");
            
            // Tampilkan panel tab yang tepat
            tabPanes.forEach(pane => pane.classList.remove("active"));
            const activePane = document.getElementById(`tab-${targetTab}`);
            if (activePane) activePane.classList.add("active");
            
            // Perbarui teks header tab
            const headerInfo = tabHeaders[targetTab];
            if (headerInfo) {
                tabTitle.textContent = headerInfo.title;
                tabSubtitle.textContent = headerInfo.subtitle;
            }
            
            // Muat data dinamis khusus per tab yang dipilih
            if (targetTab === "playlists") loadPlaylistAuditData();
            if (targetTab === "scheduler") loadSchedulerAuditData();
            if (targetTab === "cartwall") loadCartWallPlanData();
        });
    });
});

// 3. Menampilkan Pesan Toast Notifikasi
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    const toastMessage = document.getElementById("toast-message");
    const toastIcon = document.getElementById("toast-icon");
    
    toastMessage.textContent = message;
    
    // Pilih icon yang sesuai
    toastIcon.className = "fa-solid";
    if (type === "success") {
        toastIcon.classList.add("fa-circle-check");
        toast.style.borderColor = "var(--success)";
    } else if (type === "error") {
        toastIcon.classList.add("fa-circle-xmark");
        toast.style.borderColor = "var(--danger)";
    } else {
        toastIcon.classList.add("fa-circle-info");
        toast.style.borderColor = "var(--accent)";
    }
    
    toast.classList.remove("hidden");
    
    // Sembunyikan otomatis setelah 4 detik
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 4000);
}

// 4. Memuat Statistik Dashboard Utama
async function loadDashboardStats() {
    try {
        const res = await fetch("/api/stats");
        const stats = await res.json();
        
        // Perbarui widget angka dashboard
        document.getElementById("stat-total-files").textContent = stats.total_files;
        document.getElementById("stat-total-playlists").textContent = stats.playlist_files;
        document.getElementById("stat-broken-playlists").textContent = stats.broken_playlists;
        document.getElementById("stat-missing-paths").textContent = stats.missing_paths;
        
        // Perbarui rincian risiko panel kanan
        document.getElementById("stat-ramadhan").textContent = stats.ramadhan_files;
        document.getElementById("stat-adzan").textContent = stats.adzan_files;
        document.getElementById("stat-dirty").textContent = stats.dirty_metadata_files;
        document.getElementById("stat-high-scheduler").textContent = stats.emergency_scheduler_count;
        
        // Perbarui indikator kesiapan siaran stasiun radio SBL
        const readinessIndicator = document.getElementById("readiness-indicator");
        const indicatorIcon = readinessIndicator.querySelector("i");
        const indicatorText = readinessIndicator.querySelector("span");
        
        if (stats.readiness_status === "READY") {
            readinessIndicator.className = "readiness-badge ready";
            indicatorIcon.className = "fa-solid fa-circle-check";
            indicatorText.textContent = "SIARAN STERIL & SIAP ON-AIR";
        } else {
            readinessIndicator.className = "readiness-badge dangerous";
            indicatorIcon.className = "fa-solid fa-circle-exclamation";
            indicatorText.textContent = "SIARAN BELUM STERIL";
        }
        
        // Perbarui path input
        document.getElementById("migration-fresh-root").value = stats.fresh_root;
        document.getElementById("setting-fresh-root").value = stats.fresh_root;
        
    } catch (err) {
        console.error("Gagal memuat statistik dashboard:", err);
    }
}

// --- POLLING ASINKRON TASK QUEUE WORKER ---
function pollTaskStatus(taskId) {
    const taskBanner = document.getElementById("async-task-banner");
    const taskName = document.getElementById("task-banner-name");
    const taskPercentage = document.getElementById("task-banner-percentage");
    const taskProgressBar = document.getElementById("task-banner-progress-bar");
    const taskMessage = document.getElementById("task-banner-message");
    
    taskBanner.classList.remove("hidden");
    
    const interval = setInterval(async () => {
        try {
            const res = await fetch(`/api/task/status/${taskId}`);
            if (res.status === 404) {
                clearInterval(interval);
                taskBanner.classList.add("hidden");
                showToast("Tugas tidak ditemukan.", "error");
                return;
            }
            
            const task = await res.json();
            
            taskName.textContent = task.name;
            taskPercentage.textContent = `${task.progress}%`;
            taskProgressBar.style.width = `${task.progress}%`;
            taskMessage.textContent = task.message;
            
            if (task.status === "SUCCESS") {
                clearInterval(interval);
                showToast(`${task.name} sukses selesai!`);
                setTimeout(() => {
                    taskBanner.classList.add("hidden");
                }, 2000);
                loadDashboardStats();
            } else if (task.status === "FAILED") {
                clearInterval(interval);
                showToast(task.message, "error");
                setTimeout(() => {
                    taskBanner.classList.add("hidden");
                }, 2000);
                loadDashboardStats();
            }
        } catch (err) {
            clearInterval(interval);
            taskBanner.classList.add("hidden");
            showToast("Koneksi ke Task Queue stasiun radio terputus.", "error");
        }
    }, 800);
}

// 5. Memicu Pemindaian Filesystem stasiun radio
async function triggerScan() {
    const scanFolderInput = document.getElementById("scan-path-input").value;
    if (!scanFolderInput) {
        showToast("Mohon isi path folder musik stasiun radio!", "error");
        return;
    }

    try {
        const response = await fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ folder: scanFolderInput })
        });
        
        const res = await response.json();
        
        if (res.status === "PENDING") {
            showToast("Tugas pemindaian pustaka didaftarkan ke antrean.");
            pollTaskStatus(res.task_id);
        } else {
            showToast(res.message, "error");
        }
    } catch (err) {
        showToast("Koneksi gagal saat memicu scan stasiun radio.", "error");
    }
}

// 6. Memuat Hasil Audit Playlist Lama (Tab Playlists)
async function loadPlaylistAuditData() {
    const tableBody = document.querySelector("#playlists-table tbody");
    tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted"><i class="fa-solid fa-spinner fa-spin"></i> Memuat data audit playlist...</td></tr>`;
    
    try {
        const res = await fetch("/api/playlist-audit-list");
        const list = await res.json();
        
        if (list.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">Belum ada data. Silakan jalankan Scan stasiun radio terlebih dahulu.</td></tr>`;
            return;
        }
        
        tableBody.innerHTML = "";
        list.forEach(row => {
            const tr = document.createElement("tr");
            
            // Tentukan badge status kelayakan
            let statusBadge = "ready";
            if (row.status === "BROKEN" || row.status === "DANGEROUS") statusBadge = "dangerous";
            else if (row.status === "NEEDS_RELINK") statusBadge = "review";
            
            tr.innerHTML = `
                <td><strong>${row.playlist_name}</strong></td>
                <td><small class="text-muted">${row.playlist_path}</small></td>
                <td>${row.total_items}</td>
                <td class="${row.missing_items > 0 ? 'text-danger font-bold' : ''}">${row.missing_items}</td>
                <td>${row.dangerous_items}</td>
                <td><span class="badge ${statusBadge}">${row.status}</span></td>
                <td><small>${row.recommendation}</small></td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Gagal mengambil data audit playlist stasiun radio.</td></tr>`;
    }
}

// 7. Memuat Hasil Audit Scheduler Lama (Tab Scheduler)
async function loadSchedulerAuditData() {
    const tableBody = document.querySelector("#scheduler-table tbody");
    tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted"><i class="fa-solid fa-spinner fa-spin"></i> Mengaudit event scheduler...</td></tr>`;
    
    try {
        const res = await fetch("/api/scheduler-list");
        const list = await res.json();
        
        if (list.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">Belum ada data scheduler terdaftar. Jalankan scan stasiun radio.</td></tr>`;
            return;
        }
        
        tableBody.innerHTML = "";
        list.forEach(row => {
            const tr = document.createElement("tr");
            
            // Tentukan badge risiko
            let statusBadge = "ready";
            if (row.status === "SEASONAL_RAMADHAN_ARCHIVE") statusBadge = "dangerous";
            else if (row.status === "ADZAN_REVIEW" || row.status === "DANGEROUS_RANDOM_SOURCE") statusBadge = "review";
            
            tr.innerHTML = `
                <td><strong>${row.event_group}</strong></td>
                <td>${row.event_name}</td>
                <td><code>${row.time}</code></td>
                <td><span class="badge archive">${row.command_type}</span></td>
                <td><small class="text-muted">${row.target_path}</small></td>
                <td><span class="badge ${row.risk_level === 'CRITICAL' ? 'dangerous' : (row.risk_level === 'HIGH' ? 'review' : 'ready')}">${row.risk_level}</span></td>
                <td><span class="badge ${statusBadge}">${row.status}</span></td>
                <td><small>${row.recommended_action}</small></td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Gagal mengambil data audit scheduler stasiun radio.</td></tr>`;
    }
}

// 8. Memuat Rencana Cart Wall Baru (Tab Cart Wall)
async function loadCartWallPlanData() {
    const tableBody = document.querySelector("#cartwall-table tbody");
    tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted"><i class="fa-solid fa-spinner fa-spin"></i> Menyusun rencana cart wall...</td></tr>`;
    
    try {
        const res = await fetch("/api/cartwall-list");
        const list = await res.json();
        
        if (list.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">Belum ada data. Silakan jalankan scan pustaka musik.</td></tr>`;
            return;
        }
        
        tableBody.innerHTML = "";
        list.forEach(row => {
            const tr = document.createElement("tr");
            
            let statusBadge = "ready";
            if (row.status === "ARCHIVE") statusBadge = "archive";
            
            tr.innerHTML = `
                <td><span class="badge archive">${row.current_tab}</span></td>
                <td>slot ${row.slot}</td>
                <td><strong>${row.label}</strong></td>
                <td>${row.duration_seconds}s</td>
                <td><small class="text-muted">${row.detected_type}</small></td>
                <td><strong>${row.new_tab}</strong></td>
                <td><small class="text-muted">${row.new_folder}</small></td>
                <td><span class="badge ${statusBadge}">${row.status}</span></td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Gagal memuat rencana cart wall stasiun radio.</td></tr>`;
    }
}

// 9. Memicu Pembangunan Folder Steril stasiun radio
async function triggerBuildStructure() {
    try {
        const response = await fetch("/api/build-structure", { method: "POST" });
        const res = await response.json();
        
        if (res.status === "SUCCESS") {
            showToast(`Struktur folder steril stasiun radio sukses dibuat di: ${res.fresh_root}`);
            loadDashboardStats();
        } else {
            showToast(res.message, "error");
        }
    } catch (err) {
        showToast("Koneksi gagal saat membangun struktur folder.", "error");
    }
}

// 10. Memicu Penyalinan Berkas APPROVED ke Folder Steril stasiun radio SBL
async function triggerCopyFiles() {
    try {
        const response = await fetch("/api/copy-files", { method: "POST" });
        const res = await response.json();
        
        if (res.status === "PENDING") {
            showToast("Tugas migrasi Safe Copy didaftarkan ke antrean.");
            pollTaskStatus(res.task_id);
        } else {
            showToast(res.message, "error");
        }
    } catch (err) {
        showToast("Koneksi gagal saat proses salin file stasiun radio.", "error");
    }
}

// 11. Memicu Pembuatan Playlist Baru .m3u8 stasiun radio
async function triggerBuildPlaylists() {
    showToast("Menyusun playlist .m3u8 baru & Scheduler plan...", "info");
    
    try {
        // Susun Playlist baru
        const plRes = await fetch("/api/generate-playlists", { method: "POST" });
        const plData = await plRes.json();
        
        // Susun Scheduler Plan baru
        const scRes = await fetch("/api/generate-scheduler-plan", { method: "POST" });
        const scData = await scRes.json();
        
        if (plData.status === "SUCCESS" && scData.status === "SUCCESS") {
            showToast("Sukses menyusun 4 playlist steril dan 5 event scheduler siaran baru!");
            loadDashboardStats();
        } else {
            showToast("Penyusunan playlist/scheduler mengalami kendala.", "error");
        }
    } catch (err) {
        showToast("Gagal koneksi saat menyusun playlist siaran stasiun radio.", "error");
    }
}

// 12. Memicu Ekspor Seluruh Laporan CSV/MD
async function triggerGenerateReports() {
    try {
        const response = await fetch("/api/generate-reports", { method: "POST" });
        const res = await response.json();
        
        if (res.status === "PENDING") {
            showToast("Tugas ekspor laporan didaftarkan ke antrean.");
            pollTaskStatus(res.task_id);
        } else {
            showToast(res.message, "error");
        }
    } catch (err) {
        showToast("Koneksi gagal mengekspor laporan stasiun radio.", "error");
    }
}

// 13. Mereset Seluruh Database SQLite
async function triggerResetData() {
    if (!confirm("Apakah Anda yakin ingin mengosongkan seluruh indeks database? Indeks file scan dan audit lama akan hilang!")) {
        return;
    }
    
    try {
        const response = await fetch("/api/reset-data", { method: "POST" });
        const res = await response.json();
        
        if (res.status === "SUCCESS") {
            showToast("Database SQLite berhasil dikosongkan.");
            loadDashboardStats();
        } else {
            showToast(res.message, "error");
        }
    } catch (err) {
        showToast("Koneksi gagal mereset database.", "error");
    }
}
