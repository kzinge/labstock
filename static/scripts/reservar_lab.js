function alternardivData() {
    const tipoReserva = document.getElementById('tipo-reserva').value;
    const divData = document.getElementById('div-data');
    const inputData = document.getElementById('data-reserva');

    if (tipoReserva === 'extraordinaria') {
        divData.style.display = 'flex'; // 
        inputData.setAttribute('required', true); // Torna o input obrigatório
    } else {
        divData.style.display = 'none'; 
        inputData.removeAttribute('required'); // Remove a obrigatoriedade
    }
}

document.addEventListener('DOMContentLoaded', alternardivData); //executa a função ao documento ser carregado para não haver erros