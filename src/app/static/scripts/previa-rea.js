document.addEventListener("DOMContentLoaded", function () {
    // Campos do formulário de reagente
    const nomeInput = document.querySelector('#reagente');
    const categoriaSelect = document.querySelector('#form-lab select:first-of-type');
    const quantidadeInput = document.querySelector('.qnt-uni input[type="number"]');
    const unidadeSelect = document.querySelector('.qnt-uni select');
    const fornecedorInput = document.querySelector('.for-dv input[type="text"]');
    const dataInput = document.querySelector('.for-dv input[type="date"]');
    const localSelect = document.querySelector('.local select');
    // Container da prévia
    const cardPrev = document.querySelector('.card-previa');

    // Campos da prévia
    const prevLocal = document.querySelector('.prev-local span');
    const prevNome = document.querySelector('.prev-nome');
    const prevCategoria = document.querySelector('.prev-categoria h4');
    const prevQuantidade = document.querySelector('.prev-quantidade');
    const prevUnidade = document.querySelector('.prev-unidade');
    const prevFornecedor = document.querySelector('.prev-fornecedor span');
    const prevVencimento = document.querySelector('.prev-vencimento span');

    // Verifica se todos os campos estão vazios
    function isFormEmpty() {
        return !(
            nomeInput.value.trim() ||
            categoriaSelect.value.trim() ||
            quantidadeInput.value.trim() ||
            unidadeSelect.value.trim() ||
            fornecedorInput.value.trim() ||
            dataInput.value.trim() || 
            localSelect.value.trim(
        ));
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
        prevQuantidade.textContent = quantidadeInput.value || '';
        prevUnidade.textContent = unidadeSelect.value || '';
        prevFornecedor.textContent = fornecedorInput.value || '';
        prevLocal.textContent = localSelect.options[localSelect.selectedIndex]?.text || '';
        // Formata a data para dd/mm/aaaa
        if (dataInput.value) {
            const [ano, mes, dia] = dataInput.value.split('-');
            prevVencimento.textContent = `${dia}/${mes}/${ano}`;
        } else {
            prevVencimento.textContent = '';
        }
    }

    // Monitora todos os campos
    [nomeInput, categoriaSelect, quantidadeInput, unidadeSelect, fornecedorInput, dataInput].forEach(el => {
        el.addEventListener("input", atualizarPrevia);
    });
});
