export const verifyFingerprint = async (file1, file2) => {
  const formData = new FormData();
  formData.append("file1", file1);
  formData.append("file2", file2);

  const res = await fetch("http://127.0.0.1:8000/verify-fingerprint", {
    method: "POST",
    body: formData,
  });

  return await res.json();
};