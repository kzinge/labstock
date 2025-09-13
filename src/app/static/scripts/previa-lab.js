document.addEventListener("DOMContentLoaded", () => {
    // Inputs do formulário
    const nomeInput = document.querySelector('#form-lab input[type="text"]:first-of-type');
    const categoriaSelect = document.querySelector('#form-lab select');
    const blocoInput = document.getElementById("bloco");
    const salaInput = document.getElementById("sala");
    const capacidadeInput = document.querySelector('#form-lab input[type="number"]');
    const prefixoSala = document.getElementById("prefixo-sala");

    // Campos da prévia
    const cardPrevia = document.querySelector(".card-previa");
    const prevNome = document.querySelector(".prev-nome");
    const prevCategoria = document.querySelector(".prev-categoria h4");
    const prevBloco = document.querySelector(".prev-bloco span");
    const prevSala = document.querySelector(".prev-sala span");
    const prevCapacidade = document.querySelector(".prev-capacidade span");

    // Função para atualizar a prévia
    function atualizarPrevia() {
        // Mostra a prévia se ainda estiver escondida
        if (!cardPrevia.classList.contains("show")) {
            cardPrevia.classList.add("show");
        }

        // Nome do laboratório
        prevNome.textContent = nomeInput.value || "Nome do laboratório";

        // Categoria
        const categoriaSelecionada = categoriaSelect.options[categoriaSelect.selectedIndex]?.text || "Selecione";
        prevCategoria.textContent = categoriaSelecionada;

        // Bloco e Sala
        const bloco = blocoInput.value.trim();
        const sala = salaInput.value.trim();
        prevBloco.textContent = bloco || "";
        prevSala.textContent = bloco && sala ? bloco + "-" + sala : sala || "";

        // Capacidade
        prevCapacidade.textContent = capacidadeInput.value || "";
    }

    // Atualiza prefixo da sala
    blocoInput.addEventListener("input", () => {
        const valorBloco = blocoInput.value.trim();
        prefixoSala.textContent = valorBloco ? valorBloco + "-" : "";
        atualizarPrevia();
    });

    // Eventos para atualizar prévia em tempo real
    nomeInput.addEventListener("input", atualizarPrevia);
    categoriaSelect.addEventListener("change", atualizarPrevia);
    salaInput.addEventListener("input", atualizarPrevia);
    capacidadeInput.addEventListener("input", atualizarPrevia);
});
