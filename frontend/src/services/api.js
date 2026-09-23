import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
});

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/resume/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const extractSkills = async (filename) => {
  const response = await api.post("/resume/extract-skills", {
    filename,
  });

  return response.data;
};

export const analyzeResume = async (filename) => {
  const response = await api.post("/ai/ai/analysis", {
    filename,
  });

  return response.data;
};

export const matchJob = async (filename, jobDescription) => {
  const response = await api.post("/job/match-job", {
    filename,
    job_description: jobDescription,
  });

  return response.data;
};

export default api;