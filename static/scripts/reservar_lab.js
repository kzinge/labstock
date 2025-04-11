function alternardivData() {
    const tipoReserva = document.getElementById('tipo-reserva').value;
    const divData = document.getElementById('div-data');
    const labelInicio = document.getElementById('label-inicio')
    const labelFinal = document.getElementById('label-final')
    const inputData = document.getElementById('data-final');

    if (tipoReserva === 'extraordinaria') {
        inputData.style.display = 'none'; // 
        labelInicio.textContent = 'Data da reserva:';
        labelFinal.style.display = 'none';
        inputData.removeAttribute('required');
    } else {
        inputData.style.display = 'block'; 
        labelFinal.style.display = 'block';
        labelInicio.textContent = 'Data de início:';
        inputData.setAttribute('required', '');
    }
}

document.addEventListener('DOMContentLoaded', alternardivData); //executa a função ao documento ser carregado para não haver erros