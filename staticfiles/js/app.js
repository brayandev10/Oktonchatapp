// Sélecteur pour le statut réseau
const statusIndicator = document.getElementById('network-status');
const form = document.getElementById('offline-form');

// Fonction de mise à jour du statut
function updateNetworkStatus() {
    if (navigator.onLine) {
        statusIndicator.textContent = "En ligne";
        statusIndicator.style.color = "green";
    } else {
        statusIndicator.textContent = "Hors ligne";
        statusIndicator.style.color = "red";
    }
}

window.addEventListener('load', updateNetworkStatus);
window.addEventListener('online', updateNetworkStatus);
window.addEventListener('offline', updateNetworkStatus);

// Notification à l’arrivée sur la page
if ("Notification" in window && Notification.permission !== "denied") {
    Notification.requestPermission().then(permission => {
        if (permission === "granted") {
            new Notification("Bienvenue dans notre PWA Django !");
        }
    });
}

// Gestion d'un formulaire en mode hors-ligne
if (form) {
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const data = new FormData(form);
        const values = Object.fromEntries(data.entries());

        if (!navigator.onLine) {
            // Stockage local si hors-ligne
            localStorage.setItem('pendingForm', JSON.stringify(values));
            alert("Formulaire enregistré localement. Il sera soumis dès que la connexion sera rétablie.");
        } else {
            form.submit(); // Soumission classique
        }
    });

    // Envoi automatique du formulaire quand on revient en ligne
    window.addEventListener('online', () => {
        const saved = localStorage.getItem('pendingForm');
        if (saved) {
            const values = JSON.parse(saved);
            // Simuler une soumission AJAX ici si tu veux
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(values)
            }).then(response => {
                if (response.ok) {
                    alert("Formulaire soumis automatiquement !");
                    localStorage.removeItem('pendingForm');
                    form.reset();
                }
            });
        }
    });
}
