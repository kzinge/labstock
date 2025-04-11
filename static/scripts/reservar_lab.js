function alternarCampoData() {
    const tipoReserva = document.getElementById('tipo-reserva').value;
    const labelInicio = document.getElementById('label-inicio')
    const labelFinal = document.getElementById('label-final')
    const inputData = document.getElementById('data-final');

    if (tipoReserva === 'extraordinaria') {
        inputData.style.display = 'none'; 
        labelFinal.style.display = 'none';
        labelInicio.textContent = 'Data da reserva';
        inputData.removeAttribute('required');
    } else {
        inputData.style.display = 'block'; 
        labelFinal.style.display = 'block';
        labelInicio.textContent = 'Data inicial';
        inputData.setAttribute('required', '');
    }
}

document.addEventListener('DOMContentLoaded', alternardivData); //executa a função ao documento ser carregado para não haver erros