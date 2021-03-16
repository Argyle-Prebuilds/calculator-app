import {withStyles} from "@material-ui/core/styles";
import {Tooltip} from "@material-ui/core";

export const CalculationsTooltip = withStyles((theme) => ({
  tooltip: {
    maxWidth: 220,
    fontSize: theme.typography.pxToRem(12),
    border: '1px solid #dadde9',
  },
}))(Tooltip);
