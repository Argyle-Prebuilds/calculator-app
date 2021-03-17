import React, {useState, useEffect} from 'react';
import {BasicContainer} from '../common/BasicContainer';
import "../stylesheets/styles-details.css"
import "../stylesheets/styles-global.css"
import {PAGINATION_INITIAL_STATE} from "../../consts"
import {
  Grid,
  Typography
} from '@material-ui/core';
import {CollapsableTable} from './partials/CollapsableTable';
import {EmploymentsTable} from './partials/EmploymentsTable';
import {Chart} from './partials/Chart';
import {useHistory, useParams} from "react-router-dom";
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications";
import {UsersService} from "../../services/UsersService";
import {SmallBackBtnBasicContainer} from "../common/SmallBackBtnBasicContainer";
import {formatMoney} from "../utils/formatting";
import {ProgressContainer} from "../common/ProgressContainer";
import {GreyBorderedBox} from "../common/GreyBorderedBox";

export const DetailsView = () => {
  const [userProfileData, setUserProfileData] = useState(null)
  const [userEmploymentsData, setEmploymentsData] = useState(null)
  const [userIncomeMetrics, setUserIncomeMetrics] = useState(null)
  const [paginationState, setPaginationState] = useState(PAGINATION_INITIAL_STATE)
  const [monthMetrics, setMonthMetrics] = useState(null) // data for chart
  const {argyle_id} = useParams();
  const history = useHistory()

  const loadUserData = () => {

    UsersService.fetchUserProfileData(argyle_id).then(response => {
      setUserProfileData(response.data)
      loadEmploymentsList()
      loadMetrics()
    }).catch(error => {
      history.push("/users/")

      if (error?.response?.status === 404) {
        renderNotification('No data.', 'error');
        history.push("/users/")
        return
      }
      displayErrorNotifications(error)
    })

  }

  const loadMetrics = () => {
    UsersService.fetchUserKeyMetricsData(argyle_id).then(response => {
      const {income_metrics, month_metrics} = response.data
      setUserIncomeMetrics(income_metrics)
      setMonthMetrics(month_metrics)
    }).catch(error => displayErrorNotifications(error))
  }

  const loadEmploymentsList = (url = null) => {
    const action = url ? UsersService.fetchUserEmploymentsDataByUrl(url) : UsersService.fetchUserEmploymentsData(argyle_id)

    action.then(response => {
      const {count, next, previous, results} = response.data
      setPaginationState({count, next, previous})
      setEmploymentsData(results)
    }).catch(error => displayErrorNotifications(error))
  }

  const loadNextPage = () => {
    loadEmploymentsList(paginationState.next)

  }
  const loadPrevPage = () => {
    loadEmploymentsList(paginationState.previous)
  }

  useEffect(loadUserData, [])

  if (!userProfileData || !userEmploymentsData || !userIncomeMetrics) {
    return <ProgressContainer/>
  }
  return (
    <div className="details-container">

      <Grid container spacing={2}>
        <Grid item sm={12} xs={12} md={7}>
          <SmallBackBtnBasicContainer>
            <span className="font-bold">
              {userProfileData.full_name}
            </span>
            <span className="font-grey float-right">
              <span
                style={{color: "#989898"}}>DOB:</span> {userProfileData.birth_date}
              <span className="spacing"/>
              {userProfileData.email}
              <span className="spacing"/>
              {userProfileData.phone_number}
            </span>
          </SmallBackBtnBasicContainer>
          <BasicContainer>
            <Chart data={monthMetrics}/>
          </BasicContainer>
          <BasicContainer>
            <Typography variant="h5" className="font-bold container-title">
              Employment History
            </Typography>
            <EmploymentsTable
              data={userEmploymentsData}
              count={paginationState.count}
              loadNextPage={loadNextPage} loadPrevPage={loadPrevPage}
            />
          </BasicContainer>
        </Grid>
        <Grid item sm={12} xs={12} md={5}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <div className={"center-flex-container"}>
                <div
                  className="font-size-mini text-align-center ">
                  Last Year Total Income
                </div>
                <div
                  className="font-size-large font-bold text-align-center ">
                  {formatMoney(userIncomeMetrics.gross_pay.last_year_total)}
                </div>
              </div>
            </Grid>
            <Grid item xs={6}>
              <div className={"center-flex-container"}>
                <div
                  className="font-size-mini text-align-center ">
                  Current Year Projected Income
                </div>
                <div
                  className="font-size-large font-bold text-align-center ">
                  {formatMoney(userIncomeMetrics.gross_pay.projected_total)}
                </div>
              </div>
            </Grid>
          </Grid>
          <BasicContainer>
            <Typography variant="h5"
                        className="font-bold container-title">
              Income Metrics
            </Typography>
            <GreyBorderedBox borderTop={1} borderBottom={1}>
              <Grid container
                    className="smaller-font font-bold "
                    spacing={0}>
                <Grid item xs={5}>
                  <span>Calculations</span>
                </Grid>
                <Grid item xs={2}>
                  <span>Last Year</span>
                </Grid>
                <Grid item xs={3} className='padding-left-20'>
                  <span>YTD</span>
                </Grid>
                <Grid item xs={2}>
                  <span>Projected</span>
                </Grid>
              </Grid>
            </GreyBorderedBox>
            <CollapsableTable
              header="Total days with employer"
              data={userIncomeMetrics.total_days}
              dataKey="total_days"
            />
            <CollapsableTable
              header="Hours worked per week"
              data={userIncomeMetrics.hours_per_week}
              dataKey="hours_per_week"
            />
            <CollapsableTable
              header="Pay frequency"
              data={userIncomeMetrics.pay_frequency}
              dataKey="pay_frequency"
            />
            <CollapsableTable
              header="Rate of pay"
              data={userIncomeMetrics.rate_of_pay}
              dataKey="rate_of_pay"
            />
            <CollapsableTable
              header="Base pay"
              data={userIncomeMetrics.base_pay}
              dataKey="base_pay"
            />
            <CollapsableTable
              header="Overtime pay"
              data={userIncomeMetrics.overtime}
              dataKey="overtime"
            />
            <CollapsableTable
              header="Commission pay"
              data={userIncomeMetrics.commission}
              dataKey="commission"
            />
            <CollapsableTable
              header="Bonus pay"
              data={userIncomeMetrics.bonuses}
              dataKey="bonuses"
            />
            <CollapsableTable
              header="Other pay"
              data={userIncomeMetrics.reimbursements}
              dataKey="reimbursements"
            />
            <CollapsableTable
              header="Total gross pay"
              data={userIncomeMetrics.gross_pay}
              dataKey="gross_pay"
            />
            <CollapsableTable
              header="Gross Monthly Income"
              data={userIncomeMetrics.gross_monthly}
              dataKey="gross_monthly"
            />
            <CollapsableTable
              header="Gross Monthly Income + 1 Year Avg"
              data={userIncomeMetrics.gross_monthly_with_last_year}
              dataKey="gross_monthly_with_last_year"
            />
            <CollapsableTable
              header="Total taxes"
              data={userIncomeMetrics.taxes}
              dataKey="taxes"
            />
            <CollapsableTable
              header="Other deductions"
              dataKey="deductions"
              data={userIncomeMetrics.deductions}
            />
            <CollapsableTable
              header="Total net pay"
              data={userIncomeMetrics.net_pay}
              dataKey="net_pay"
            />
          </BasicContainer>
        </Grid>
      </Grid>
    </div>
  )
}
