function getUserCookie() {
    const username = 'username'
    const user_foto = 'user_foto'
    return document.cookie
        .split('; ') 
        .map(cookie => cookie.split('=')) 
        .filter(([chave]) => chave === username || chave === user_foto)
        .map(([, valor]) => decodeURIComponent(valor));
    
}

document.addEventListener("DOMContentLoaded", getUserCookie);
cookies = getUserCookie()
username_element = document.getElementById('username')
username_element.textContent = cookies[0].replace(/"/g,"")
user_foto_element = document.getElementById('user_foto')
user_foto_element.src = cookies[1]