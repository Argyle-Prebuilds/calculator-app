import {api, API_URL} from "./APIService";


export const getAPIKeys = () => {
  return api.get(`${API_URL}/integrations/api-keys/`);
};

export const updateAPIKey = (id, data = {}) => {
  return api.put(`${API_URL}/integrations/api-keys/${id}/`, data);
};

export const addAPIKey = (data = {}) => {
  return api.post(`${API_URL}/integrations/api-keys/`, data);
};
