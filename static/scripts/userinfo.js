function getUserCookie() {
    const keys = ['username', 'user_foto', 'usertype'];
    const cookieMap = Object.fromEntries(
        document.cookie
            .split('; ')
            .map(cookie => cookie.split('='))
            .map(([key, val]) => [key, decodeURIComponent(val)])
    );
    return keys.map(key => cookieMap[key] || "");
}

document.addEventListener("DOMContentLoaded", () => {
    const cookies = getUserCookie();

    const usernameElement = document.getElementById('username');
    if (usernameElement) {
        usernameElement.textContent = cookies[0].replace(/"/g, "");
    }

    const userFotoElement = document.getElementById('user_foto');
    if (userFotoElement) {
        userFotoElement.src = cookies[1];
    }

    const usertypeElement = document.getElementById('usertype');
    if (usertypeElement) {
        usertypeElement.textContent = cookies[2];
    }
});
