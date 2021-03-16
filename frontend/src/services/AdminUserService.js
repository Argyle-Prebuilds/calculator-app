import {api, API_URL} from "./APIService";
import {PAGE_LIMIT} from "../consts";


export const fetchAdminUsersService = (page = 1, limit = PAGE_LIMIT,) => {
  return api.get(`${API_URL}/admin-users/list/`, {params: {limit, page}});
};

export const fetchAdminUsersServiceByUrl = (url) => {
  return api.get(url)
}

export const removeAdminUserService = (id) => {
  return api.delete(`${API_URL}/admin-users/delete/${id}/`);
};

export const addAdminUserService = (data) => {
  return api.post(`${API_URL}/admin-users/create/`, data);
};
