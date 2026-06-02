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