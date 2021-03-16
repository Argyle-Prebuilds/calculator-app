import {api, API_URL} from "./APIService";
import {baseAPI} from "./BaseAPIService";

export const loginService = (data) => {
  return baseAPI.post(`${API_URL}/auth/login/`, data)
}

export const validateTokenService = (data) => {
  return api.post(`${API_URL}/auth/validate-token/`, data)
}

export const passwordResetService = (data) => {
  return api.post(`${API_URL}/auth/password-reset/`, data)
}

export const passwordUpdateService = (data) => {
  return api.post(`${API_URL}/auth/password-update/`, data)
}

export const activateAccountService = (user_id, data) => {
  return baseAPI.put(`${API_URL}/admin-users/activate/${user_id}/`, data);
};
