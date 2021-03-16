import React from "react";
import Button from "@material-ui/core/Button";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import Paper from "@material-ui/core/Paper";
import "../stylesheets/styles-details.css"
import {IconButton} from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close";


export const ConfirmDialog = (props) => {
  const {onClose, open, title} = props;

  const handleClose = (confirmed) => {
    if (confirmed) {
      onClose(true);
    } else {
      onClose(false);
    }
  };

  return (
    <Dialog onClose={handleClose} open={open} fullWidth={true}
            className="medium-width-modal">
      <Paper className="column">
        <IconButton className="close-btn" onClick={() => handleClose()}>
          <CloseIcon/>
        </IconButton>
        <DialogTitle className={"dialog-title"}>{title}</DialogTitle>
        <div className="row">
          <Button
            variant="contained"
            className={'blue-button'}
            onClick={() => handleClose(true)}
          >
            Confirm
          </Button>
          <Button
            variant="contained"
            color="default"
            className="alternate-blue-btn"
            onClick={() => handleClose(false)}
          >
            Cancel
          </Button>
        </div>
      </Paper>
    </Dialog>
  );
}
