import React, {useEffect, useState} from "react";
import {
  addAdminUserService,
  fetchAdminUsersService,
  fetchAdminUsersServiceByUrl,
  removeAdminUserService,
} from "../../services/AdminUserService";
import DeleteIcon from '@material-ui/icons/Delete';
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import TableBody from "@material-ui/core/TableBody";
import {
  IconButton,
  Paper,
  TableCell,
  TableContainer,
  TableFooter,
  TablePagination
} from "@material-ui/core";
import CircularProgress from '@material-ui/core/CircularProgress';
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications"
import {AddAdminUserDialog} from "./AddAdminUserDialog";
import {ConfirmDialog} from "../common/ConfirmDialog";
import {ProgressContainer} from "../common/ProgressContainer";
import {PAGE_LIMIT, PAGINATION_INITIAL_STATE} from "../../consts";

export const AdminUserList = () => {
  const INITIAL_STATE = {
    email: "",
  };
  const [userList, setUserList] = useState([]);
  const [inputFormErrors, setInputFormErrors] = useState(INITIAL_STATE);
  const [confirmationOpen, setConfirmationOpen] = useState(false);
  const [addUserOpen, setAddUserOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState("");
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(0)
  const [paginationState, setPaginationState] = useState(PAGINATION_INITIAL_STATE)
  const logged_in_user_id = localStorage.getItem('user_id')

  const loadNextPage = () => {
    fetchUsers(paginationState.next)

  }
  const loadPrevPage = () => {
    fetchUsers(paginationState.previous)
  }

  const fetchUsers = (url = null) => {
    const action = url ? fetchAdminUsersServiceByUrl(url) : fetchAdminUsersService()

    action.then((response) => {
      setUserList(response.data.results)
      const {count, next, previous} = response.data
      setPaginationState({count, next, previous})
    })
      .catch((error) => {
        displayErrorNotifications(error)
      })
  };

  const removeUser = (confirmed) => {
    setConfirmationOpen(false);
    if (confirmed) {
      setLoading(true)
      removeAdminUserService(selectedUser.id)
        .then((response) => {
          renderNotification('User removed.')
          fetchUsers();
          setLoading(false)
        })
        .catch((error) => {
          setLoading(false)
          displayErrorNotifications(error)
        });
    }
  };

  const onChangePage = (e, newPage) => {
    if (newPage > page) {
      loadNextPage()
    } else {
      loadPrevPage()
    }
    setPage(newPage)
  }

  const addUser = (email) => {
    setAddUserOpen(false);
    setInputFormErrors(INITIAL_STATE);
    if (email) {
      setLoading(true)
      addAdminUserService({
        email: email,
      })
        .then((response) => {
          setLoading(false)
          renderNotification('User successfully added.')
          fetchUsers();
        })
        .catch((error) => {
          setLoading(false)
          setAddUserOpen(true)
          displayErrorNotifications(error, Object.keys(INITIAL_STATE))
          if (error.response !== undefined) {
            setInputFormErrors(error.response.data)
          }
        });
    }
  };

  const generateTable = () => (
    <TableContainer className='table-container'>
      <Table>
        <TableHead>
          <TableRow className='table-head-row'>
            <TableCell className="users-table-head">Email</TableCell>
            <TableCell className="users-table-head">Status</TableCell>
            <TableCell className="users-table-head"></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {userList.map((elem) => {
            return (
              <TableRow key={elem.email}>
                <TableCell>{elem.email}</TableCell>
                {elem.is_active ?
                  <TableCell className="text-green">Active</TableCell>
                  : <TableCell className="text-greyed">Inactive</TableCell>
                }

                <TableCell align="right">
                  {logged_in_user_id !== elem.id &&
                  <IconButton
                    variant="text"
                    className="delete-btn"
                    onClick={() => {
                      setConfirmationOpen(true);
                      setSelectedUser(elem);
                    }}
                  >
                    <DeleteIcon/>
                  </IconButton>
                  }
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination rowsPerPageOptions={[PAGE_LIMIT]}
                             count={paginationState.count}
                             onChangePage={onChangePage} page={page}
                             rowsPerPage={PAGE_LIMIT}/>
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  )

  useEffect(fetchUsers, []);
  if (!userList) {
    return <ProgressContainer/>
  }
  return (
    <Paper className="medium-paper-container">
      <div>
        <div className={"right-flex-container margin-bottom-25"}>
          <Button
            className="blue-btn add-user-btn "
            variant="contained"
            onClick={() => {
              setAddUserOpen(true);
            }}
          >
            {loading ? <CircularProgress size={30}
                                         color="inherit"/> : "Add Admin User"}
          </Button>
        </div>

        <div>
          {!userList.length && (
            <Typography variant="h6" align="center"
                        className="margin-bottom-25">
              Empty list
            </Typography>
          )}
          {userList && generateTable()}
        </div>
        <ConfirmDialog
          open={confirmationOpen}
          onClose={removeUser}
          title="Are you sure you want to delete this account?"
        />
        <AddAdminUserDialog
          open={addUserOpen}
          onClose={addUser}
          errors={inputFormErrors}
        />
      </div>
    </Paper>
  );
}
