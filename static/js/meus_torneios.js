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