import {Box} from "@material-ui/core";
import React from "react";

export const GreyBorderedBox = ({
                                  borderTop = 0,
                                  borderBottom = 0,
                                  children
                                }) => {
  return <Box style={{width: '100%', borderColor: '#e8e8e8'}}
              borderTop={borderTop}
              borderBottom={borderBottom}>
    {children}
  </Box>
}
