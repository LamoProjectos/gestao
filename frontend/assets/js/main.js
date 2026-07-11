/* ============ GALLERY DATA ============ */
const galleryData = {
    'katembe': {
        title: 'Moradia Tipo 05 — Katembe',
        images: [
            'assets/images/projeto-katembe.jpg',
            'assets/images/projeto-katembe-2.jpg',
            'assets/images/projeto-katembe-3.jpg',
            'assets/images/projeto-katembe-4.jpg',
        ]
    },
    'guava-ampliacao': {
        title: 'Ampliação Tipo 03 — Guava (2 Pisos)',
        images: [
            'assets/images/projeto-guava-ampliacao.png',
            'assets/images/projeto-guava-tipo04-2.png',
            'assets/images/projeto-guava-tipo04-3.png',
            'assets/images/projeto-guava-tipo04-4.png',
        ]
    },
    'rotunda': {
        title: 'Renovação Tipo 03 — 2ª Rotunda',
        images: [
            'assets/images/projeto-rotunda.jpg',
            'assets/images/projeto-rotunda-2.jpg',
            'assets/images/projeto-rotunda-3.jpg',
            'assets/images/projeto-rotunda-4.jpg',
        ]
    },
    'pool': {
        title: 'Pool Familiar — Guava',
        images: [
            'assets/images/projeto-pool.jpg',
            'assets/images/projeto-pool-2.jpg',
            'assets/images/projeto-pool-3.jpg',
            'assets/images/projeto-pool-4.jpg',
        ]
    },
    'matlemele': {
        title: 'Reforma Tipo 03 — Matlemele',
        images: [
            'assets/images/projeto-matlemele.jpg',
            'assets/images/projeto-matlemele-2.jpg',
            'assets/images/projeto-matlemele-3.jpg',
            'assets/images/projeto-matlemele-4.jpg',
        ]
    },
    'salao': {
        title: 'Salão de Eventos — Muhalaze',
        images: [
            'assets/images/projeto-salao.jpg',
            'assets/images/projeto-salao-2.jpg',
            'assets/images/projeto-salao-3.jpg',
            'assets/images/projeto-salao-4.jpg',
        ]
    }
};

/* ============ GALLERY / LIGHTBOX ============ */
let currentGallery = null;
let currentIndex = 0;

function openGallery(projectId) {
    const data = galleryData[projectId];
    if (!data || !data.images.length) return;

    currentGallery = data;
    currentIndex = 0;
    document.getElementById('galleryModal').classList.add('open');
    document.body.style.overflow = 'hidden';
    showGalleryImage();
}

function showGalleryImage() {
    const img = document.getElementById('galleryImage');
    const counter = document.getElementById('galleryCounter');
    const caption = document.getElementById('galleryCaption');

    img.src = currentGallery.images[currentIndex];
    img.alt = currentGallery.title;
    counter.textContent = `${currentIndex + 1} / ${currentGallery.images.length}`;
    caption.textContent = currentGallery.title;
}

function closeGallery() {
    document.getElementById('galleryModal').classList.remove('open');
    document.body.style.overflow = '';
    currentGallery = null;
}

function closeGalleryOutside(e) {
    if (e.target === e.currentTarget) closeGallery();
}

function navigateGallery(dir) {
    if (!currentGallery) return;
    currentIndex += dir;
    if (currentIndex < 0) currentIndex = currentGallery.images.length - 1;
    if (currentIndex >= currentGallery.images.length) currentIndex = 0;
    showGalleryImage();
}

document.addEventListener('keydown', (e) => {
    if (!document.getElementById('galleryModal').classList.contains('open')) return;
    if (e.key === 'Escape') closeGallery();
    if (e.key === 'ArrowLeft') navigateGallery(-1);
    if (e.key === 'ArrowRight') navigateGallery(1);
});

/* ============ PROJECT FILTER ============ */
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.dataset.filter;
        document.querySelectorAll('#portfolioGrid .col-md-4').forEach(card => {
            if (filter === 'all' || card.dataset.category === filter) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

/* ============ SCROLL ANIMATIONS (Intersection Observer) ============ */
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            if (el.classList.contains('animate-on-scroll')) {
                el.classList.add('visible');
            }
            if (el.querySelector('.counter')) {
                animateCounter(el);
            }
            observer.unobserve(el);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

/* ============ COUNTER ANIMATION ============ */
function animateCounter(container) {
    const counters = container.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.target);
        const step = Math.max(1, Math.floor(target / 60));
        let current = 0;

        const update = () => {
            current += step;
            if (current >= target) {
                counter.textContent = target;
                return;
            }
            counter.textContent = current;
            requestAnimationFrame(update);
        };
        requestAnimationFrame(update);
    });
}

/* ============ NAVBAR SCROLL EFFECT ============ */
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});

/* ============ BACK TO TOP ============ */
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    backToTop.classList.toggle('visible', window.scrollY > 500);
});
backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ============ SMOOTH SCROLL ============ */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const top = target.getBoundingClientRect().top + window.scrollY - 70;
            window.scrollTo({ top, behavior: 'smooth' });
        }
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
});

/* ============ ACTIVE NAV LINK ============ */
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        if (window.scrollY >= section.offsetTop - 150) {
            current = section.getAttribute('id');
        }
    });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
    });
});

/* ============ CONTACT FORM ============ */
document.querySelectorAll('.contact-form form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const btn = this.querySelector('button[type="submit"]');
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Mensagem Enviada!';
        btn.style.background = 'linear-gradient(135deg, #16a34a, #15803d)';
        setTimeout(() => {
            btn.innerHTML = original;
            btn.style.background = '';
        }, 3000);
    });
});
