import {useEffect} from "react";
import {useHistory} from "react-router-dom";

export const Logout = () => {
  const history = useHistory()

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    history.push("/");
  };

  useEffect(() => {
    handleLogout();
  }, []);

  return null
};
