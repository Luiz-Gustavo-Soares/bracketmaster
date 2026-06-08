/*helpers globais, alerts auto-dismiss*/

document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA DO LIVE SEARCH (BUSCA GLOBAL) ---
    const searchInput = document.getElementById('globalSearchInput');
    const searchDropdown = document.getElementById('searchDropdown');
    const searchItems = document.querySelectorAll('.search-item'); // Pega todos os jogadores da lista
    const viewAllBtn = document.querySelector('.search-item-view-all');

    if (searchInput && searchDropdown) {
        
        // Dispara toda vez que o usuário digita ou apaga uma letra
        searchInput.addEventListener('input', function() {
            // Pega o que foi digitado e converte para minúsculo para facilitar a busca
            const termo = this.value.toLowerCase().trim();

            if (termo.length > 0) {
                // Se digitou algo, mostra a caixinha
                searchDropdown.classList.add('is-active');
                
                let encontrouAlguem = false;

                // Passa por cada jogador da lista para ver se o nome bate
                searchItems.forEach(item => {
                    const nick = item.querySelector('.search-item-nick').textContent.toLowerCase();
                    
                    if (nick.includes(termo)) {
                        item.style.display = 'flex'; // Mostra o jogador
                        encontrouAlguem = true;
                    } else {
                        item.style.display = 'none'; // Esconde o jogador
                    }
                });

                // Se não achou ninguém, esconde o botão de "Ver todos" para não ficar solto
                if (viewAllBtn) {
                    viewAllBtn.style.display = encontrouAlguem ? 'block' : 'none';
                }

            } else {
                // Se apagou tudo, esconde a caixinha inteira
                searchDropdown.classList.remove('is-active');
            }
        });

        // Esconde o dropdown se o usuário clicar fora dele
        document.addEventListener('click', (event) => {
            if (!searchInput.contains(event.target) && !searchDropdown.contains(event.target)) {
                searchDropdown.classList.remove('is-active');
            }
        });
    }

});

// --- MENU MOBILE ---
const hamburger = document.getElementById('navHamburger');
const mobileMenu = document.getElementById('navMobileMenu');

if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('is-active');
        mobileMenu.classList.toggle('is-open');
    });

    // Fecha ao clicar em um link
    mobileMenu.querySelectorAll('.nav-mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('is-active');
            mobileMenu.classList.remove('is-open');
        });
    });
}