// Efecto de caída de emojis personalizable
// Cambia el valor de emoji para el efecto que desees

// Edita aquí el emoji y la opacidad deseada:
let emoji = '💻'; // Cambia este emoji por el que quieras
let emojiOpacity = 0.3; // Cambia la opacidad (0.0 a 1.0)



function createEmojiFall() {
    const el = document.createElement('div');
    el.classList.add('emoji-fall');
    el.textContent = emoji;

    const startLeft = Math.random() * (window.innerWidth - 40);
    const duration = Math.random() * 3 + 2;
    const size = Math.random() * 24 + 18;
    // Usa la opacidad definida arriba
    const opacity = emojiOpacity;

    el.style.left = startLeft + 'px';
    el.style.fontSize = (size + 10) + 'px';
    el.style.setProperty('--emoji-fall-opacity', opacity);
    el.style.opacity = opacity;
    el.style.position = 'fixed';
    el.style.top = '-40px';
    el.style.pointerEvents = 'none';
    el.style.zIndex = 9999;
    el.style.willChange = 'transform, opacity';
    el.style.animation = `emoji-fall-fx ${duration}s linear forwards`;
    // el.style.border = '1px solid red'; // descomenta para debug visual

    document.body.appendChild(el);

    setTimeout(() => {
        el.remove();
    }, duration * 1000);
}

setInterval(createEmojiFall, 120);

// Permite cambiar el emoji desde la consola o código:
// localStorage.setItem('fall_emoji', '❤️'); location.reload();
