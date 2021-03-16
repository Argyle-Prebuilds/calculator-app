import {BasicContainer} from "./BasicContainer";
import React from "react";
import KeyboardArrowLeftIcon from "@material-ui/icons/KeyboardArrowLeft";
import {useHistory} from "react-router-dom";

export const SmallBackBtnBasicContainer = ({children}) => {
  const history = useHistory()

  const goBack = () => {
    history.push("/users/")
  }

  return <BasicContainer
    extraCssClass="small-container padding-left-0 padding-bottom-0">
    <div className="back-icon-container cursor-btn" onClick={goBack}>
      <KeyboardArrowLeftIcon className="vertical-center"/>
    </div>
    <div className="width-100">
      {children}
    </div>
  </BasicContainer>
}
