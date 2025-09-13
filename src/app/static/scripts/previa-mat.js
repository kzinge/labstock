document.addEventListener("DOMContentLoaded", function () {
    // Campos do formulário de material
    const nomeInput = document.querySelector('#form-lab input[type="text"]:first-of-type');
    const categoriaSelect = document.querySelector('#form-lab select:first-of-type');
    const descricaoInput = document.querySelector('#descricao');
    const fornecedorInput = document.querySelector('#form-lab .column-inputs .col:nth-child(2) input[type="text"]');
    const dataInput = document.querySelector('#form-lab input[type="date"]');
    const quantidadeInput = document.querySelector('#quantidade-form');

    // Container da prévia
    const cardPrev = document.querySelector('.card-previa');

    // Campos da prévia
    const prevNome = document.querySelector('.prev-nome');
    const prevCategoria = document.querySelector('.prev-categoria h4');
    const prevDescricao = document.querySelector('.prev-descricao p');
    const prevFornecedor = document.querySelector('.prev-fornecedor span');
    const prevVencimento = document.querySelector('.prev-vencimento span');
    const prevQuantidade = document.querySelector('.prev-quantidade span');

    // Verifica se todos os campos estão vazios
    function isFormEmpty() {
        return !(
            nomeInput.value.trim() ||
            categoriaSelect.value.trim() ||
            descricaoInput.value.trim() ||
            fornecedorInput.value.trim() ||
            dataInput.value.trim() ||
            quantidadeInput.value.trim()
        );
    }


    // Atualiza a prévia
    function atualizarPrevia() {
        if (isFormEmpty()) {
            cardPrev.classList.remove("show");
            return;
        }

        cardPrev.classList.add("show");
        prevNome.textContent = nomeInput.value || '';
        prevCategoria.textContent = categoriaSelect.options[categoriaSelect.selectedIndex]?.text || '';
        prevDescricao.textContent = descricaoInput.value || '';
        prevFornecedor.textContent = fornecedorInput.value || '';
        prevVencimento.textContent = dataInput.value || '';
        prevQuantidade.textContent = quantidadeInput.value || '';

        if (dataInput.value) {
            const [ano, mes, dia] = dataInput.value.split('-');
            prevVencimento.textContent = `${dia}/${mes}/${ano}`;
        } else {
            prevVencimento.textContent = '';
        }
    }


    // Monitora todos os campos
    [nomeInput, categoriaSelect, descricaoInput, fornecedorInput, dataInput, quantidadeInput].forEach(el => {
        el.addEventListener("input", atualizarPrevia);
    });
});
