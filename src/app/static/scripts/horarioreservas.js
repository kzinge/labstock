const selectTipo = document.getElementById('tipo');
const divHorario = document.getElementById('reserva-horario');

function atualizarHorario() {
    const valor = selectTipo.value;

    if (valor === 'Anual' || valor === 'Semestral') {
        divHorario.innerHTML = `
            <p>Selecione os dias da semana:</p>
            <div id="dias-checkboxes">
                ${['segunda','terça','quarta','quinta','sexta'].map(dia => `
                    <label>
                        <input type="checkbox" name="dias" value="${dia}"> ${dia.charAt(0).toUpperCase() + dia.slice(1)}
                    </label><br>
                `).join('')}
            </div>
            <div id="horarios-por-dia"></div>
        `;

        const checkboxes = divHorario.querySelectorAll('input[name="dias"]');
        const horariosContainer = divHorario.querySelector('#horarios-por-dia');

        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                const dia = checkbox.value;
                const id = `horario-${dia}`;

                if (checkbox.checked) {
                    // horários
                    const div = document.createElement('div');
                    div.id = id;
                    div.innerHTML = `
                        <p>${dia.charAt(0).toUpperCase() + dia.slice(1)}:</p>
                        <label>Das <input type="time" name="inicio_${dia}"> até <input type="time" name="fim_${dia}"></label>
                    `;
                    horariosContainer.appendChild(div);
                } else {

                    const div = document.getElementById(id);
                    if (div) div.remove();
                }
            });
        });

    } else if (valor === 'Extraordinária') {
        divHorario.innerHTML = `
            <p>Selecione a data no calendário:</p>
            <input type="date" name="data_extraordinaria">
            <label>Das <input type="time" name="inicio"> até <input type="time" name="fim"></label>
        `;
    } else {
        divHorario.innerHTML = '';
    }
}

selectTipo.addEventListener('change', atualizarHorario);
atualizarHorario();

