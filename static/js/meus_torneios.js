/**
 * Gerenciador de Estados Assíncronos - Meus Torneios
 */
function switchState(stateId) {
    // 1. Oculta todos os blocos de visualização
    document.querySelectorAll('.state-view').forEach(view => {
        view.classList.remove('active');
    });

    // 2. Regra Especial para reaproveitamento do Formulário (Criar vs Editar)
    if (stateId === 'state-form-create') {
        document.getElementById('state-form').classList.add('active');
        document.getElementById('form-main-title').innerText = "Criar Torneio";
        document.getElementById('btn-form-submit').innerText = "SALVAR";
        clearFormFields();
    } 
    else if (stateId === 'state-form-edit') {
        document.getElementById('state-form').classList.add('active');
        document.getElementById('form-main-title').innerText = "Editar Torneio";
        document.getElementById('btn-form-submit').innerText = "ATUALIZAR TORNEIO";
        injectMockDataIntoForm();
    } 
    // 3. Fluxo nativo para os demais estados (como Vazio, Lista e Inscrições)
    else {
        const targetView = document.getElementById(stateId);
        if (targetView) {
            targetView.classList.add('active');
        }
    }
}

/**
 * Preenche o formulário com dados mockados simulando a ação de Edição
 */
function injectMockDataIntoForm() {
    document.getElementById('f-titulo').value = "Mix Diamantina";
    document.getElementById('f-desc').value = "Boas-vindas ao melhor campeonato de Commander do mundo, e até de Diamantina!";
    document.getElementById('f-mod').value = "Presencial";
    document.getElementById('f-cid').value = "Diamantina";
    document.getElementById('f-est').value = "MG";
    document.getElementById('f-jog').value = "16";
    document.getElementById('f-formato').value = "Draft";
    document.getElementById('f-estrat').value = "Suíço";
    document.getElementById('f-rodadas').value = "3";
    document.getElementById('f-tipo').value = "Competitivo";
    document.getElementById('f-val').value = "25,00";
    document.getElementById('f-pra').value = "2026-06-15";
    document.getElementById('f-prem').value = "1º Lugar: 400,00 + Troféu\n2º Lugar: 200,00\n3º Lugar: 100,00";
}

/**
 * Reseta todos os campos limpando os inputs para uma nova criação limpa
 */
function clearFormFields() {
    document.querySelectorAll('.form-control').forEach(input => {
        input.value = "";
        if(input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        }
    });
}

function toggleModalidade() {
    const mod = document.getElementById('f-mod').value;
    const wrapPlataforma = document.getElementById('wrap-plataforma');
    const wrapLocalizacao = document.getElementById('wrap-localizacao');

    if (mod === 'Remoto') {
        wrapPlataforma.style.display = 'flex'; // Mostra Plataforma
        wrapLocalizacao.style.display = 'none'; // Esconde Endereço
    } else {
        wrapPlataforma.style.display = 'none';  // Esconde Plataforma
        wrapLocalizacao.style.display = 'block'; // Mostra Endereço
    }
}

function clearFormFields() {
    document.querySelectorAll('.form-control').forEach(input => {
        input.value = "";
        if(input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        }
    });
    // Garante que volta a mostrar a localização e esconder a plataforma ao limpar
    toggleModalidade(); 
}