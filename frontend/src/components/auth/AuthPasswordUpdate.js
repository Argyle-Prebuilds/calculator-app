import React, {useState} from "react";
import {Button, Card, TextField, Typography,} from "@material-ui/core";
import CircularProgress from '@material-ui/core/CircularProgress';
import {useHistory, useParams} from "react-router-dom";
import EditIcon from '@material-ui/icons/Edit';
import {passwordUpdateService} from "../../services/AuthService";
import "../stylesheets/styles-auth.css";
import {PASSWORD_INITIAL_STATE} from "../../consts";
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications"
import {onEnterPressed} from "../utils/general"

export const PasswordUpdate = () => {
  const history = useHistory()
  const [formData, setFormData] = useState({
    ...PASSWORD_INITIAL_STATE,
    ...useParams(),
  });
  const [formErrors, setFormErrors] = useState(PASSWORD_INITIAL_STATE);
  const [loading, setLoading] = useState(false)

  const handleChange = (evt) => {
    setFormErrors({...formErrors, [evt.target.name]: ""});
    setFormData({...formData, [evt.target.name]: evt.target.value});
  };

  const handleSubmit = async () => {
    setLoading(true)
    await passwordUpdateService(formData)
      .then(() => {
        setLoading(false)
        renderNotification('Password successfully changed.')
        setTimeout(() => {
          history.push("/auth/login")
        }, 3000);
      })
      .catch((error) => {
        setLoading(false)
        displayErrorNotifications(error, Object.keys(PASSWORD_INITIAL_STATE))
        if (error.response !== undefined) {
          setFormErrors(error.response.data)
        }
      });
  };

  return (
    <Card className="card-auth margin-top-25">
      <EditIcon className="login-icon"/>
      <Typography className="margin-top-25" variant="h5" align="center">
        Change Password
      </Typography>
      <div className="input-container margin-top-25">
        <TextField
          label="New password"
          name="password"
          type="password"
          variant="standard"
          margin="normal"
          fullWidth
          autoFocus
          value={formData.password}
          onChange={handleChange}
          error={!!formErrors.password}
          helperText={formErrors.password}
          onKeyPress={(evt) => onEnterPressed(evt, handleSubmit)}
        />
      </div>
      <div className="input-container margin-top-25">
        <TextField
          label="Repeat password"
          name="password_confirmed"
          type="password"
          variant="standard"
          fullWidth
          required
          value={formData.password_confirmed}
          onChange={handleChange}
          error={!!formErrors.password_confirmed}
          helperText={formErrors.password_confirmed}
          onKeyPress={(evt) => onEnterPressed(evt, handleSubmit)}
        />
      </div>
      <div className="input-container margin-top-25">
        <Button
          variant="contained"
          color="primary"
          className="blue-btn spinner-container"
          fullWidth
          onClick={handleSubmit}
        >
          {loading ?
            <CircularProgress size={30} color='inherit'/> : "Set Password"}
        </Button>
      </div>
    </Card>
  );
};
