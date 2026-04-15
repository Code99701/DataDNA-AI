const BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

const handleResponse = async (res) => {
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  return res.json();
};

// --- Upload / Watermark ---
export const embedWatermark = async (file, userId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  const res = await fetch(`${BASE_URL}/embed-watermark`, { method: 'POST', body: formData });
  return handleResponse(res);
};

// --- Verify / Detect Leak ---
export const verifyFingerprint = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${BASE_URL}/verify-fingerprint`, { method: 'POST', body: formData });
  return handleResponse(res);
};

// --- Identity Registration ---
export const registerIdentity = async (payload) => {
  const res = await fetch(`${BASE_URL}/register-identity`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
};

// --- Identity Identification ---
export const identifyUser = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${BASE_URL}/identify`, { method: 'POST', body: formData });
  return handleResponse(res);
};

// --- Dashboard Stats ---
export const getDashboardStats = async () => {
  const res = await fetch(`${BASE_URL}/stats`);
  return handleResponse(res);
};