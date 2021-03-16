import React from 'react'
import {Container} from '@material-ui/core'

export const BasicContainer = ({extraCssClass, children}) => {

  return <Container
    className={`basic-container ${extraCssClass ? extraCssClass : ''}`}
  >
    <div className="width-100">
      {children}
    </div>
  </Container>
}
