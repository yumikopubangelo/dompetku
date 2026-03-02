function getApiBaseUrl() {
  return (window.API_BASE_URL || "http://localhost:5000/api").replace(/\/$/, "");
}

function buildApiUrl(path) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${getApiBaseUrl()}${normalizedPath}`;
}

function getAccessToken() {
  return localStorage.getItem("access_token");
}

function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

function saveSession(authPayload) {
  localStorage.setItem("access_token", authPayload.access_token || "");
  localStorage.setItem("refresh_token", authPayload.refresh_token || "");
  localStorage.setItem("auth_user", JSON.stringify(authPayload.user || {}));
}

function clearSession() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("auth_user");
}

function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem("auth_user") || "{}");
  } catch (_e) {
    return {};
  }
}

function isTokenExpired(token) {
  if (!token) return true;
  const parts = token.split(".");
  if (parts.length < 2) return true;

  try {
    const b64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = b64 + "=".repeat((4 - (b64.length % 4 || 4)) % 4);
    const payload = JSON.parse(atob(padded));
    if (!payload.exp) return false;
    return Date.now() >= payload.exp * 1000;
  } catch (_e) {
    return true;
  }
}

function isAuthenticated() {
  const token = getAccessToken();
  return Boolean(token) && !isTokenExpired(token);
}

function redirectToLogin() {
  if (window.location.pathname !== "/login") {
    window.location.href = "/login";
  }
}

function redirectToDashboard() {
  if (window.location.pathname === "/login" || window.location.pathname === "/register") {
    window.location.href = "/dashboard";
  }
}

function requireAuth() {
  if (!isAuthenticated()) {
    clearSession();
    redirectToLogin();
  }
}

function requireGuest() {
  if (isAuthenticated()) {
    redirectToDashboard();
  }
}

async function loginWithCredentials(username, password) {
  const response = await fetch(buildApiUrl("/auth/login"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Login gagal");
  }

  saveSession(payload);
  return payload;
}

async function registerWithCredentials(username, password, confirmPassword) {
  const response = await fetch(buildApiUrl("/auth/register"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username,
      password,
      confirm_password: confirmPassword,
    }),
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Registrasi gagal");
  }

  saveSession(payload);
  return payload;
}

async function logoutSession() {
  const token = getAccessToken();
  try {
    if (token) {
      await fetch(buildApiUrl("/auth/logout"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
    }
  } finally {
    clearSession();
    redirectToLogin();
  }
}

function formatRupiah(value) {
  const amount = Number(value || 0);
  return `Rp ${new Intl.NumberFormat("id-ID").format(amount)}`;
}

async function apiFetch(path, options = {}) {
  const token = getAccessToken();
  const headers = {
    ...(options.headers || {}),
  };

  if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(buildApiUrl(path), {
    ...options,
    headers,
  });

  if (response.status === 401) {
    clearSession();
    if (typeof showAlert === "function" && window.location.pathname !== "/login") {
      showAlert("Sesi login tidak valid. Silakan login ulang.", "warning");
    }
    redirectToLogin();
  }

  return response;
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.IS_AUTH_PAGE) {
    requireGuest();
  } else {
    requireAuth();
  }
});
