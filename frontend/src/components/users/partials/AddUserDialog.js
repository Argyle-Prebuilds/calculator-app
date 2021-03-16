import React, {useEffect, useState} from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import Paper from "@material-ui/core/Paper";
import {IconButton, TextField} from "@material-ui/core";
import CloseIcon from '@material-ui/icons/Close';
import {onEnterPressed} from "../../utils/general";

export const AddUserDialog = ({onClose, open}) => {

  const [token, setToken] = useState('')
  const [error, setError] = useState('')

  const handleClose = (addUser = false) => {
    if (addUser){
      if (!token) {
        setError('This field cannot be empty.')
      } else {
        onClose(addUser, token);
        setToken('')
      }
    } else {
      onClose(false, token)
      setToken('')
    }
  };

  const resetToken = () => {
    setToken('')
  }
  const updateState = (e) => {
    setToken(e.target.value)
    setError('')
  }
  useEffect(resetToken, [])

  return (
    <Dialog onClose={() => handleClose()} open={open} fullWidth={true}
            className="medium-width-modal">
      <Paper className="column">
        <IconButton className="close-btn" onClick={() => handleClose(false)}>
          <CloseIcon/>
        </IconButton>
        <TextField
          className='grey-font full-width-input medium-width-input'
          onChange={updateState}
          placeholder="Enter User Token"
          value={token}
          name='token'
          multiline={true}
          error={!!error}
          helperText={error}
            onKeyPress={(evt) => onEnterPressed(evt, () => {
            handleClose(true)
          })}
        />
        <div className='margin-top-20'>
          <Button
            className="blue-btn"
            variant="contained"
            color="primary"
            onClick={() => handleClose(true)}
          >
            Connect
          </Button>
        </div>
      </Paper>
    </Dialog>
  );
}
