// Mock API service for the application
export const fetchResults = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ data: "Mock API Result" });
    }, 1000);
  });
};
