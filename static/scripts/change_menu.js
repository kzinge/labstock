function change_menu(menu) {
    div_reagentes = document.getElementById('form_reagentes')
    div_materiais = document.getElementById('form_materiais')
    console.log(div_materiais,div_reagentes)
    if (menu == 'reagentes') {
        div_reagentes.style.display = 'flex';
        div_materiais.style.display = 'none';
    } else if (menu == 'materiais') {
        div_reagentes.style.display = 'none';
        div_materiais.style.display = 'flex';
    }
}