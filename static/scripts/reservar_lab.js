function alternardivData() {
    const tipoReserva = document.getElementById('tipo-reserva').value;
    const divData = document.getElementById('div-data');
    const labelInicio = document.getElementById('label-inicio')
    const inputData = document.getElementById('data-reserva');

    if (tipoReserva === 'extraordinaria') {
        divData.style.display = 'none'; // 
        labelInicio.textContent = 'Data da reserva:';
    } else {
        divData.style.display = 'flex'; 
        labelInicio.textContent = 'Data de início:';
    }
}

document.addEventListener('DOMContentLoaded', alternardivData); //executa a função ao documento ser carregado para não haver erros