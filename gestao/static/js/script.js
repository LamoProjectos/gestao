document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOffcanvas = document.getElementById('sidebarOffcanvas');

    if (sidebarToggle && sidebarOffcanvas) {
        const bsOffcanvas = new bootstrap.Offcanvas(sidebarOffcanvas);
        sidebarToggle.addEventListener('click', function () {
            bsOffcanvas.toggle();
        });
    }

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });

    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(btn.getAttribute('data-confirm'))) {
                e.preventDefault();
            }
        });
    });
});
