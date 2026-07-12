document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOffcanvas = document.getElementById('sidebarOffcanvas');
    let bsOffcanvas = null;

    if (sidebarToggle && sidebarOffcanvas) {
        bsOffcanvas = new bootstrap.Offcanvas(sidebarOffcanvas);
        sidebarToggle.addEventListener('click', function () {
            bsOffcanvas.toggle();
        });
    }

    // Touch gestures: swipe right to open sidebar, swipe left to close
    let touchStartX = 0;
    let touchEndX = 0;
    const SWIPE_THRESHOLD = 80;

    document.addEventListener('touchstart', function (e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', function (e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const diff = touchEndX - touchStartX;
        if (!bsOffcanvas) return;
        if (diff > SWIPE_THRESHOLD && touchStartX < 40) {
            bsOffcanvas.show();
        } else if (diff < -SWIPE_THRESHOLD) {
            bsOffcanvas.hide();
        }
    }

    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });

    // Confirmation dialogs
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(btn.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss alerts after 5s
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add data-label attributes to responsive tables
    document.querySelectorAll('.table').forEach(function (table) {
        const headers = [];
        table.querySelectorAll('thead th').forEach(function (th) {
            headers.push(th.textContent.trim());
        });
        if (headers.length) {
            table.querySelectorAll('tbody tr').forEach(function (row) {
                row.querySelectorAll('td').forEach(function (td, idx) {
                    if (headers[idx]) {
                        td.setAttribute('data-label', headers[idx]);
                    }
                });
            });
        }
    });
});
