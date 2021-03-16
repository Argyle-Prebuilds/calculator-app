import React, {useState} from 'react'
import {formatDate, formatRate} from '../../utils/formatting'
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TablePagination,
  TableRow,
} from '@material-ui/core'
import {PAGE_LIMIT} from "../../../consts";

export const EmploymentsTable = ({
                                   data, count, loadNextPage,
                                   loadPrevPage,
                                 }) => {

  const [page, setPage] = useState(0)

  const onChangePage = (e, newPage) => {
    if (newPage > page) {
      loadNextPage()
    } else {
      loadPrevPage()
    }
    setPage(newPage)
  }

  return <Table className="border-top-gray">
    <TableHead>
      <TableRow className='table-head-row'>
        <TableCell className="small-table-head">Employer</TableCell>
        <TableCell className="small-table-head">Job Title</TableCell>
        <TableCell className="small-table-head">Job Type</TableCell>
        <TableCell className="small-table-head">Base Pay Rate</TableCell>
        <TableCell className="small-table-head">Hire Date</TableCell>
        <TableCell className="small-table-head">Termination
          Date</TableCell>
        <TableCell className="small-table-head">Termination
          Reason</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {data.map(element => {
        return <TableRow key={element.id}>
          <TableCell
            className="small-table-row">{element.employer}</TableCell>
          <TableCell
            className="small-table-row">{element.job_title}</TableCell>
          <TableCell
            className="small-table-row">{element.job_type}</TableCell>
          <TableCell
            className="small-table-row">{formatRate(element.base_pay)}</TableCell>
          <TableCell
            className="small-table-row">{element.hire_date ? formatDate(element.hire_date) : '-'}</TableCell>
          <TableCell
            className="small-table-row">{element.termination_date ? formatDate(element.termination_date) : '-'}</TableCell>
          <TableCell
            className="small-table-row">{element.termination_reason}</TableCell>
        </TableRow>
      })}
    </TableBody>
    <TableFooter>
      <TableRow>
        <TablePagination rowsPerPageOptions={[PAGE_LIMIT]} count={count}
                         onChangePage={onChangePage} page={page}
                         rowsPerPage={PAGE_LIMIT}/>
      </TableRow>
    </TableFooter>
  </Table>
}
