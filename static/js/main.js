/*helpers globais, alerts auto-dismiss*/

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. LÓGICA DO LIVE SEARCH (BUSCA GLOBAL)
    // ==========================================
    const searchInput = document.getElementById('globalSearchInput');
    const searchDropdown = document.getElementById('searchDropdown');
    const searchItems = document.querySelectorAll('.search-item');
    const viewAllBtn = document.querySelector('.search-item-view-all');

    if (searchInput && searchDropdown) {
        searchInput.addEventListener('input', function() {
            const termo = this.value.toLowerCase().trim();

            if (termo.length > 0) {
                searchDropdown.classList.add('is-active');
                let encontrouAlguem = false;

                searchItems.forEach(item => {
                    const nick = item.querySelector('.search-item-nick').textContent.toLowerCase();
                    if (nick.includes(termo)) {
                        item.style.display = 'flex';
                        encontrouAlguem = true;
                    } else {
                        item.style.display = 'none';
                    }
                });

                if (viewAllBtn) {
                    viewAllBtn.style.display = encontrouAlguem ? 'block' : 'none';
                }
            } else {
                searchDropdown.classList.remove('is-active');
            }
        });

        document.addEventListener('click', (event) => {
            if (!searchInput.contains(event.target) && !searchDropdown.contains(event.target)) {
                searchDropdown.classList.remove('is-active');
            }
        });
    }

    // ==========================================
    // 2. MENU MOBILE UNIFICADO
    // ==========================================
    const hamburgerBtn = document.getElementById("navHamburgerBtn");
    const mobileMenu = document.getElementById("mobileMenu");
    const mobileOverlay = document.getElementById("mobileOverlay");
    const mobileCloseBtn = document.getElementById("mobileCloseBtn");

    if (hamburgerBtn && mobileMenu && mobileOverlay && mobileCloseBtn) {
        
        hamburgerBtn.addEventListener("click", () => {
            mobileMenu.classList.add("is-open");
            mobileOverlay.classList.add("is-active");
            document.body.style.overflow = "hidden"; // Trava o scroll da página
        });

        mobileOverlay.addEventListener("click", () => {
            mobileMenu.classList.remove("is-open");
            mobileOverlay.classList.remove("is-active");
            document.body.style.overflow = "auto";
        });

        mobileCloseBtn.addEventListener("click", () => {
            mobileMenu.classList.remove("is-open");
            mobileOverlay.classList.remove("is-active");
            document.body.style.overflow = "auto";
        });
    }
});