import React, {useState} from "react";
import {useHistory, useParams} from "react-router-dom";
import {activateAccountService} from "../../services/AuthService";
import {
  Box,
  Button,
  Card,
  Container,
  TextField,
  Typography,
} from "@material-ui/core";
import CircularProgress from '@material-ui/core/CircularProgress';
import PowerSettingsNewIcon from '@material-ui/icons/PowerSettingsNew';
import {displayErrorNotifications} from "../utils/notifications"
import {onEnterPressed} from "../utils/general"
import {PASSWORD_INITIAL_STATE} from "../../consts";

export const AccountActivate = () => {
  const history = useHistory();
  const params = useParams()

  const [inputForm, setInputForm] = useState(PASSWORD_INITIAL_STATE);
  const [inputFormErrors, setInputFormErrors] = useState(PASSWORD_INITIAL_STATE);
  const [loading, setLoading] = useState(false)

  const submitForm = () => {
    setLoading(true)
    activateAccountService(params.user_id, inputForm)
      .then((response) => {
        history.push("/auth/login");
      })
      .catch((error) => {
        setLoading(false)
        displayErrorNotifications(error, Object.keys(PASSWORD_INITIAL_STATE))
        if (error.response !== undefined) {
          const errors = error.response.data
          setInputFormErrors({
            ...PASSWORD_INITIAL_STATE,
            ...errors,
          })
        }
      });
  };

  const handleChange = (evt) => {
    setInputFormErrors(PASSWORD_INITIAL_STATE);
    setInputForm({
      ...inputForm,
      [evt.target.id]: evt.target.value,
    });
  };

  return (
    <Box>
      <Container>
        <Card className="card-auth margin-top-25">
          <PowerSettingsNewIcon className="login-icon"/>
          <Typography className="margin-top-25" variant="h5" align="center">
            Activate Account
          </Typography>
          <div className="input-container">
            <TextField
              id="password"
              label="New password"
              value={inputForm.password}
              error={!!inputFormErrors.password}
              helperText={inputFormErrors.password}
              onChange={handleChange}
              onKeyPress={(evt) => onEnterPressed(evt, submitForm)}
              variant="standard"
              margin="normal"
              fullWidth
              type="password"
            />
          </div>
          <div className="input-container">
            <TextField
              id="password_confirmed"
              label="Confirm your password"
              value={inputForm.password_confirmed}
              error={!!inputFormErrors.password_confirmed}
              helperText={inputFormErrors.password_confirmed}
              onChange={handleChange}
              onKeyPress={(evt) => onEnterPressed(evt, submitForm)}
              variant="standard"
              margin="normal"
              fullWidth
              type="password"
            />
          </div>
          <div className="input-container margin-top-25">
            <Button
              variant="contained"
              color="primary"
              className="button-auth spinner-container"
              type="submit"
              fullWidth
              onClick={submitForm}
            >
              {loading ?
                <CircularProgress size={30} color='inherit'/> : "Submit"}
            </Button>
          </div>
        </Card>
      </Container>
    </Box>
  );
}
