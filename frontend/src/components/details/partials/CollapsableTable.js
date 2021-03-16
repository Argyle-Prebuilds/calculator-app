import React, {useState, useEffect} from 'react'
import {
  CALCULATION_TOOLTIPS,
  FORMAT_MONEY_FIELDS,
  RATE_FIELDS
} from '../../../consts'
import {formatMoney, formatRate} from "../../utils/formatting"
import {Grid} from '@material-ui/core'
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import {GreyBorderedBox} from "../../common/GreyBorderedBox";
import {CalculationsTooltip} from "../../common/CalculationsTooltip";


export const CollapsableTable = ({
                                   data,
                                   dataKey,
                                   header
                                 }) => {
  const [showDetails, setShowDetails] = useState(false)


  useEffect(() => {
  }, [])


  const toggleDetails = () => {
    setShowDetails(!showDetails)
  }

  return <GreyBorderedBox borderBottom={1}>
    <Grid container className="smaller-font" spacing={0}
          alignItems={"center"}>

      <Grid container spacing={0} onClick={toggleDetails} alignItems={"center"}
            className='toggle-row'>
        <Grid item xs={5} className='expand-col'>{showDetails ?
          <ExpandLessIcon/> : <ExpandMoreIcon/>}{header}
        </Grid>
        <CalculationsTooltip style={{top: "25px !important"}}
                             title={CALCULATION_TOOLTIPS[dataKey]?.last_year_total}
                             placement="top">

          <Grid item xs={2}>{formatData(data.last_year_total, dataKey)}</Grid>
        </CalculationsTooltip>
        <CalculationsTooltip title={CALCULATION_TOOLTIPS[dataKey]?.ytd_total}
                             placement="top">
          <Grid item xs={3}
                className='padding-left-20'>{formatData(data.ytd_total, dataKey)}</Grid>
        </CalculationsTooltip>
        <CalculationsTooltip
          title={CALCULATION_TOOLTIPS[dataKey]?.projected_total}
          placement="top">
          <Grid item xs={2}>{formatData(data.projected_total, dataKey)}</Grid>
        </CalculationsTooltip>

      </Grid>
      {
        showDetails && Object.keys(data.companies).map(key => {
          const rowData = data.companies[key];
          return <GreyBorderedBox borderTop={1} key={key}>
            <Grid container spacing={0}
                  className=' grey-background'
                  alignItems={"center"}>
              <Grid item xs={5} className="padding-left-35">{key}</Grid>
              {Object.keys(rowData).map((key) => {
                // column with 'ytd_total' key needs to have bigger left padding
                return <CalculationsTooltip key={key}
                  title={CALCULATION_TOOLTIPS[dataKey]?.companies?.[key]}
                  placement="top">
                  <Grid item xs={key === 'ytd_total' ? 3 : 2}
                        className={key === 'ytd_total' ? 'padding-left-20' : ''}>{formatData(rowData[key], dataKey)}</Grid>
                </CalculationsTooltip>
              })}
            </Grid>
          </GreyBorderedBox>
        })
      }
    </Grid>
  </GreyBorderedBox>
}

const formatData = (value, dataKey) => {
  let retValue = '-';
  if (!!value) {
    if (FORMAT_MONEY_FIELDS.includes(dataKey)) {
      retValue = formatMoney(value)
    } else if (RATE_FIELDS.includes(dataKey)) {
      retValue = formatRate(value)
    } else if (dataKey === 'hours_per_week') {
      retValue = value
    } else if (Array.isArray(value)) {
      if(value.length) retValue = value.join(', ')
    } else {
      retValue = value
    }
  }
  return retValue;
}
