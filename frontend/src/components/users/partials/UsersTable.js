import React, {useState} from "react";
import {useHistory} from "react-router-dom";

import {
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableFooter,
  TableHead,
  TablePagination,
  TableRow
} from "@material-ui/core";
import DeleteIcon from '@material-ui/icons/Delete';
import {PAGE_LIMIT} from "../../../consts";


export const UsersTable = ({
                             data,
                             count,
                             loadNextPage,
                             loadPrevPage,
                             deleteUser
                           }) => {

  const [page, setPage] = useState(0)
  const history = useHistory()

  const showUserDetails = (argyle_id) =>{
    history.push(`/details/${argyle_id}`)
  }

  const onChangePage = (e, newPage) => {
    if (newPage > page) {
      loadNextPage()
    } else {
      loadPrevPage()
    }
    setPage(newPage)

  }


  return <TableContainer className='table-container'>
    <Table>
      <TableHead>
        <TableRow className='table-head-row'>
          <TableCell className="users-table-head">Full Name</TableCell>
          <TableCell className="users-table-head">Token Status</TableCell>
          <TableCell className="users-table-head"></TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map(element => {
          return (
            <TableRow key={element.argyle_id} onClick={() => showUserDetails(element.argyle_id)} className='table-row users-table'>
              <TableCell>{element.full_name}</TableCell>
              <TableCell>{element.token_status}</TableCell>
              <TableCell align="right">
                <IconButton
                  className="delete-btn"
                  onClick={(e) => {
                    deleteUser(element.argyle_id)
                      e.stopPropagation()
                  }}
                >
                  <DeleteIcon/>
                </IconButton>
              </TableCell>
            </TableRow>
          )
        })
        }
      </TableBody>
      <TableFooter>
        <TableRow>
          <TablePagination rowsPerPageOptions={[PAGE_LIMIT]} count={count}
                           onChangePage={onChangePage} page={page}
                           rowsPerPage={PAGE_LIMIT}/>
        </TableRow>
      </TableFooter>
    </Table>
  </TableContainer>
}
