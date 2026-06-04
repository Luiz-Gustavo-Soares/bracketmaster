/*helpers globais, alerts auto-dismiss*/
window.addEventListener('scroll', function() { //VAi ficar esperando um evento, no caso mexer no scroll se acontecer chama a função
    const scrollIndicator = document.getElementById('scrollIndicator'); // pega o id na nossa linha
    
    if (scrollIndicator) { 
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop; // quantos pixels rodou 
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight; //maximo de pixels antes de bater no rodape da tela
        const scrolled = (winScroll / height) * 100; //descobrir a porcentagem usando a posição atual e o restante total
        scrollIndicator.style.width = scrolled + "%"; // pega a % e taca na linha, especificamente na largura, assim ela cresce igual a rosca do calabreso
    }
});

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