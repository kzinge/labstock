function change_menu(choice) {
    div_reagentes = document.getElementById('form_reagentes')
    div_materiais = document.getElementById('form_materiais')
    div_nova_cat = document.getElementById('nova_cat')
    div_cat_exist = document.getElementById('cat_existente')
    input_nova_cat = document.getElementsByName('tipo_reagente_novo')[0]
    input_cat = document.getElementsByName('tipo_reagente')[0]
    // A página inicia com o de reagentes ativo

    if (choice == 'reagentes') { // Aparece o form dos reagentes e some com o de materiais
        div_reagentes.style.display = 'flex'; 
        div_materiais.style.display = 'none';
    } 
    else if (choice == 'materiais') { // Aparece o form de materiais e some com o de reagentes
        div_reagentes.style.display = 'none';
        div_materiais.style.display = 'flex';
    }

    // Bloco de escolha da categoria do form de reagentes
    else if (choice == 'nova_categoria') {
        div_cat_exist.style.display = 'none';
        input_cat.value = null;
        input_cat.required = false;
        input_nova_cat.required = true;
        div_nova_cat.style.display = 'inline';
    }
    else if (choice == 'categoria_existente') {
        div_cat_exist.style.display = 'inline';
        input_nova_cat.value = null;
        input_cat.required = true;
        input_nova_cat.required = false;
        div_nova_cat.style.display = 'none';
    }
}
