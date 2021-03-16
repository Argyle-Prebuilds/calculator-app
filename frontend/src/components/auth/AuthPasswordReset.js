import React, {useState} from "react";
import {Button, Card, TextField, Typography} from "@material-ui/core";
import SettingsBackupRestoreIcon
  from '@material-ui/icons/SettingsBackupRestore';
import CircularProgress from '@material-ui/core/CircularProgress';
import {passwordResetService} from "../../services/AuthService";
import {PASSWORD_RESET_INITIAL_STATE} from "../../consts";
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications"
import {onEnterPressed} from "../utils/general"
import "../stylesheets/styles-auth.css";

export const PasswordReset = () => {

  const [formData, setFormData] = useState(PASSWORD_RESET_INITIAL_STATE);
  const [formErrors, setFormErrors] = useState(PASSWORD_RESET_INITIAL_STATE);
  const [loading, setLoading] = useState(false)

  const handleChange = (evt) => {
    setFormErrors({...formErrors, [evt.target.name]: ""});
    setFormData({...formData, [evt.target.name]: evt.target.value});
  };

  const handleSubmit = async () => {
    setLoading(true)
    await passwordResetService(formData)
      .then(() => {
        setLoading(false)
        renderNotification('Check your email for a message from us.')
      })
      .catch((error) => {
        setLoading(false)
        displayErrorNotifications(error, Object.keys(PASSWORD_RESET_INITIAL_STATE))
        if (error.response !== undefined) {
          setFormErrors(error.response.data)
        }
      });
  };

  return (
    <Card className="card-auth margin-top-25">
      <SettingsBackupRestoreIcon className="login-icon"/>
      <Typography className="margin-top-25" variant="h5" align="center">
        Password Reset
      </Typography>
      <div className="input-container">
        <TextField
          label="Email"
          name="email"
          variant="standard"
          margin="normal"
          type="email"
          fullWidth
          required
          value={formData.email}
          onChange={handleChange}
          error={!!formErrors.email}
          helperText={formErrors.email}
          onKeyPress={(evt) => onEnterPressed(evt, handleSubmit)}
        />
      </div>
      <div className="input-container margin-top-25">
        <Button
          variant="contained"
          color="primary"
          className="blue-btn spinner-container"
          type="submit"
          fullWidth
          onClick={handleSubmit}
        >
          {loading ? <CircularProgress size={30}
                                       color='inherit'/> : "Reset Password"}
        </Button>
      </div>
    </Card>
  );
};
