// --- Détection de l'environnement (Codespaces ou local) ---
const surCodespaces = window.location.hostname.endsWith(".app.github.dev");
function urlApi(port) {
  if (surCodespaces) {
    return "https://" + window.location.hostname.replace(/-\d+\.app\.github\.dev$/, `-${port}.app.github.dev`);
  }
  return `http://localhost:${port}`;
}
const API_LIVRES = urlApi(8001);
const API_UTILISATEURS = urlApi(8002);
const API_EMPRUNTS = urlApi(8003);

// --- Navigation par onglets ---
document.querySelectorAll(".onglet").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".onglet").forEach(b => b.classList.remove("actif"));
    document.querySelectorAll("section").forEach(s => s.classList.remove("visible"));
    btn.classList.add("actif");
    document.getElementById(btn.dataset.cible).classList.add("visible");
  });
});

// --- Petit utilitaire d'appel API ---
async function appeler(url, options = {}) {
  const reponse = await fetch(url, options);
  const donnees = await reponse.json().catch(() => ({}));
  if (!reponse.ok) throw new Error(donnees.detail || "Erreur " + reponse.status);
  return donnees;
}
const dateFr = d => new Date(d).toLocaleDateString("fr-FR");

// ================= LIVRES =================
async function chargerLivres(livres = null) {
  try {
    const donnees = livres ?? await appeler(`${API_LIVRES}/livres`);
    document.getElementById("liste-livres").innerHTML = donnees.map(l =>
      `<tr><td>${l.id}</td><td>${l.titre}</td><td>${l.auteur}</td><td>${l.isbn}</td><td>${l.quantite}</td>
       <td><button onclick="supprimerLivre(${l.id})">🗑️</button></td></tr>`).join("");
  } catch (e) { alert("Livres : " + e.message); }
}

document.getElementById("form-livre").addEventListener("submit", async ev => {
  ev.preventDefault();
  try {
    await appeler(`${API_LIVRES}/livres`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        titre: document.getElementById("livre-titre").value,
        auteur: document.getElementById("livre-auteur").value,
        isbn: document.getElementById("livre-isbn").value,
        quantite: parseInt(document.getElementById("livre-quantite").value),
      }),
    });
    ev.target.reset();
    chargerLivres();
  } catch (e) { alert(e.message); }
});

document.getElementById("recherche").addEventListener("input", async ev => {
  const q = ev.target.value.trim();
  if (!q) return chargerLivres();
  try { chargerLivres(await appeler(`${API_LIVRES}/livres/recherche?q=${encodeURIComponent(q)}`)); }
  catch (e) { alert(e.message); }
});

async function supprimerLivre(id) {
  if (!confirm("Supprimer ce livre ?")) return;
  try { await appeler(`${API_LIVRES}/livres/${id}`, { method: "DELETE" }); chargerLivres(); }
  catch (e) { alert(e.message); }
}

// ================= UTILISATEURS =================
async function chargerUtilisateurs() {
  try {
    const donnees = await appeler(`${API_UTILISATEURS}/utilisateurs`);
    document.getElementById("liste-utilisateurs").innerHTML = donnees.map(u =>
      `<tr><td>${u.id}</td><td>${u.nom}</td><td>${u.email}</td><td>${u.type_utilisateur}</td></tr>`).join("");
  } catch (e) { alert("Utilisateurs : " + e.message); }
}

document.getElementById("form-utilisateur").addEventListener("submit", async ev => {
  ev.preventDefault();
  try {
    await appeler(`${API_UTILISATEURS}/utilisateurs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nom: document.getElementById("util-nom").value,
        email: document.getElementById("util-email").value,
        type_utilisateur: document.getElementById("util-type").value,
      }),
    });
    ev.target.reset();
    chargerUtilisateurs();
  } catch (e) { alert(e.message); }
});

// ================= EMPRUNTS =================
function ligneEmprunt(e) {
  const statut = e.date_retour_effective
    ? `<span class="rendu">Rendu le ${dateFr(e.date_retour_effective)}</span>`
    : e.en_retard
      ? `<span class="retard">EN RETARD</span>`
      : `<span class="encours">En cours</span>`;
  const action = e.date_retour_effective ? "" :
    `<button onclick="retournerEmprunt(${e.id})">Retourner</button>`;
  return `<tr><td>${e.id}</td><td>${e.livre_id}</td><td>${e.utilisateur_id}</td>
    <td>${dateFr(e.date_emprunt)}</td><td>${dateFr(e.date_retour_prevue)}</td>
    <td>${statut}</td><td>${action}</td></tr>`;
}

async function chargerEmprunts(url = `${API_EMPRUNTS}/emprunts`) {
  try {
    const donnees = await appeler(url);
    document.getElementById("liste-emprunts").innerHTML = donnees.map(ligneEmprunt).join("");
  } catch (e) { alert("Emprunts : " + e.message); }
}

document.getElementById("form-emprunt").addEventListener("submit", async ev => {
  ev.preventDefault();
  try {
    await appeler(`${API_EMPRUNTS}/emprunts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        livre_id: parseInt(document.getElementById("emprunt-livre").value),
        utilisateur_id: parseInt(document.getElementById("emprunt-utilisateur").value),
      }),
    });
    ev.target.reset();
    chargerEmprunts();
  } catch (e) { alert(e.message); }
});

async function retournerEmprunt(id) {
  try { await appeler(`${API_EMPRUNTS}/emprunts/${id}/retour`, { method: "PUT" }); chargerEmprunts(); }
  catch (e) { alert(e.message); }
}

document.getElementById("btn-retards").addEventListener("click", () =>
  chargerEmprunts(`${API_EMPRUNTS}/emprunts/retards`));

// --- Chargement initial ---
chargerLivres();
chargerUtilisateurs();
chargerEmprunts();