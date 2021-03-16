import {CircularProgress} from "@material-ui/core";
import React from "react";

export const ProgressContainer = () => {
  return <div className='loader-div'>
    Loading data...
    <CircularProgress size={50}/>
  </div>
}
