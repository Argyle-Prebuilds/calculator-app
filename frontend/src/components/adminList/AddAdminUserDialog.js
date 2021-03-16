import React, {useState} from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import Paper from "@material-ui/core/Paper";
import {IconButton, TextField} from "@material-ui/core";
import CloseIcon from '@material-ui/icons/Close';
import {onEnterPressed} from "../utils/general";


export const AddAdminUserDialog = (props) => {
  const {onClose, open, errors} = props;
  const [email, setEmail] = useState("");

  const handleClose = (confirmed = false) => {
    if (confirmed) {
      onClose(email);
    } else {
      onClose("");
    }
    setEmail("");
  };

  const handleChange = (evt) => {
    setEmail(evt.target.value);
  };

  return (
    <Dialog onClose={() => handleClose()} open={open} fullWidth={true}
            className="medium-width-modal">
      <Paper className="column">
        <IconButton className="close-btn" onClick={handleClose}>
          <CloseIcon/>
        </IconButton>

        <TextField
          className='grey-font full-width-input medium-width-input'
          placeholder="Enter email"
          id="email"
          value={email}
          error={!!errors.email}
          helperText={errors.email}
          onChange={handleChange}
          onKeyPress={(evt) => onEnterPressed(evt, () => {
            handleClose(true)
          })}
        />
        <div className='margin-top-20'>
          <Button
            variant="contained"
            className="blue-btn"
            color="primary"

            disabled={!email}
            onClick={() => handleClose(true)}
          >
            Submit
          </Button>
        </div>
      </Paper>
    </Dialog>
  );
}
