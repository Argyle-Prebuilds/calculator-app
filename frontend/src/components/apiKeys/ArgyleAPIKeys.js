import {Button, Paper} from "@material-ui/core";
import React, {useEffect, useState} from "react";
import TextField from "@material-ui/core/TextField";
import CircularProgress from "@material-ui/core/CircularProgress";
import Switch from "@material-ui/core/Switch";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import {addAPIKey, getAPIKeys} from "../../services/SettingService";
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications";
import {onEnterPressed} from "../utils/general";
import "../stylesheets/styles-api-keys.css";
import Typography from "@material-ui/core/Typography";
import {API_KEYS_INITIAL_STATE} from "../../consts";

export const ArgyleAPIKeys = () => {

  const [inputForm, setInputForm] = useState(API_KEYS_INITIAL_STATE)
  const [errorState, setErrorState] = useState(API_KEYS_INITIAL_STATE)
  const [loading, setLoading] = useState(false)

  const updateFormState = (event) => {
    setInputForm({
      ...inputForm,
      [event.target.name]: event.target.type === 'checkbox' ? event.target.checked : event.target.value,
    });
    setErrorState({
      ...errorState,
      [event.target.name]: ''
    })
  }

  const updateErrors = (errors) => {
    let errorList = {...API_KEYS_INITIAL_STATE};
    for (let key of Object.keys(errors)) {
      errorList[key] = errors[key];
    }
    setErrorState(errorList);
  }

  const getKeys = () => {
    getAPIKeys().then((response) => {
      setInputForm(response.data)
    }).catch((error) => {
      displayErrorNotifications(error)
    })
  }

  useEffect(getKeys, [])
  const saveChanges = () => {
    setLoading(true)

    addAPIKey(inputForm).then(response => {
      renderNotification('Keys successfully saved.')
      setLoading(false)
    }).catch(error => {
        setLoading(false)
        let ignoreKeys = Object.keys(API_KEYS_INITIAL_STATE)
        ignoreKeys.push('pay_distribution_data')
        displayErrorNotifications(error, ignoreKeys)
        if (error.response !== undefined) {
          updateErrors(error.response.data)
        }
      }
    )
  }

  const {client_id, client_secret, plugin_key, is_sandbox_mode} = inputForm

  return <Paper className="medium-paper-container">

    <div className="paper-child-container">
      <Typography variant='h6'>Set Argyle API credentials</Typography>
      <div className='padded-input'>

        <TextField
          value={plugin_key}
          name='plugin_key'
          label='plugin_key'
          onChange={updateFormState}
          onKeyPress={(evt) => onEnterPressed(evt, saveChanges)}
          required
          error={!!errorState.plugin_key}
          helperText={errorState.plugin_key}
          variant={'standard'}
          fullWidth
        /></div>
      <div className='padded-input'>
        <TextField
          value={client_id}
          name='client_id'
          label='client_id'
          onChange={updateFormState}
          onKeyPress={(evt) => onEnterPressed(evt, saveChanges)}
          required
          error={!!errorState.client_id}
          helperText={errorState.client_id}
          fullWidth

        />
      </div>
      <div className='padded-input'>
        <TextField
          value={client_secret}
          name='client_secret'
          label='client_secret'
          onChange={updateFormState}
          onKeyPress={(evt) => onEnterPressed(evt, saveChanges)}
          required
          error={!!errorState.client_secret}
          helperText={errorState.client_secret}
          fullWidth

        />
      </div>

      <FormControlLabel className="switch-box margin-top-15" control={
        <Switch
          checked={is_sandbox_mode}
          onChange={(event) => updateFormState(event)}
          color="primary"
          name="is_sandbox_mode"
        />} label="Is sandbox mode?">
      </FormControlLabel>

      <div className="add-key-pair-btn">
        <Button onClick={saveChanges} className="blue-btn"
                variant="contained">
          {loading ?
            <CircularProgress size={30} color='inherit'/> : "Save keys"}
        </Button>
      </div>
    </div>
  </Paper>
}
