import React, {useEffect, useState} from "react";
import {Button, InputAdornment, Paper, TextField} from "@material-ui/core";
import jwt_decode from "jwt-decode";
import {UsersService} from "../../services/UsersService";
import {
  displayErrorNotifications,
  renderNotification
} from "../utils/notifications";
import {UsersTable} from "./partials/UsersTable";
import {Search} from "@material-ui/icons";
import {API_KEYS_INITIAL_STATE, PAGINATION_INITIAL_STATE} from "../../consts";
import {AddUserDialog} from "./partials/AddUserDialog";
import {ConfirmationDialog} from "./partials/ConfirmationDialog";
import {useHistory} from "react-router-dom";
import {ProgressContainer} from "../common/ProgressContainer";
import {getAPIKeys} from "../../services/SettingService";
import Typography from "@material-ui/core/Typography";

export const UsersList = () => {

  const [userList, setUserList] = useState([])
  const [filteredUserList, setFilteredUserList] = useState([])
  const [paginationState, setPaginationState] = useState(PAGINATION_INITIAL_STATE)
  const [addUserOpen, setAddUserOpen] = useState(false);
  const [successDialogOpen, setSuccessDialogOpen] = useState(false);
  const [errorDialogOpen, setErrorDialogOpen] = useState(false);
  const [argyleId, setArgyleId] = useState(false);
  const [argyleKeys, setArgyleKeys] = useState(API_KEYS_INITIAL_STATE)

  const history = useHistory()
  const updateState = (data) => {
    setUserList(data.results)
    const {count, next, previous} = data
    setFilteredUserList(data.results)
    setPaginationState({count, next, previous})
  }

  const getKeys = () => {
    getAPIKeys().then((response) => {
      setArgyleKeys(response.data)
      if (response.data.client_id && response.data.client_secret) {
        loadUserList()
      }
    }).catch((error) => {
      displayErrorNotifications(error)
    })
  }

  const loadUserList = (url = null) => {
    const action = url ? UsersService.fetchUsersListByUrl(url) : UsersService.fetchUsersList()
    action.then(response => {
      updateState(response.data)
    }).catch(error => displayErrorNotifications(error))
  }

  const deleteUser = (argyle_id) => {
    UsersService.deleteUser(argyle_id).then(res => {
        renderNotification('User successfully deleted.')
        loadUserList()
      }
    ).catch(err =>
      displayErrorNotifications(err)
    )
  }

  const loadNextPage = () => {
    loadUserList(paginationState.next)

  }
  const loadPrevPage = () => {
    loadUserList(paginationState.previous)
  }

  const addNewUser = (token) => {
    try {
      const decodedToken = jwt_decode(token);
      const {user_id, exp} = decodedToken
      UsersService.createUser({
        argyle_id: user_id,
        token_expiry: exp
      }).then(res => {
        setArgyleId(user_id)
        setSuccessDialogOpen(true)
        loadUserList()
      }).catch(error => {
        setErrorDialogOpen(true)
      })
    } catch {
      setErrorDialogOpen(true)
    }
  }

  const filterList = (e) => {
    const value = e.target.value.toLowerCase()
    let filteredList = userList.filter(el => el.full_name.toLowerCase().includes(value))
    setFilteredUserList(filteredList)
  }

  const onCloseAddUser = (addUser, token) => {
    setAddUserOpen(false)
    if (addUser && token) {
      addNewUser(token)
    }
  }

  const onCloseSuccess = (redirect) => {
    setSuccessDialogOpen(false)
    if (redirect) {
      history.push(`/details/${argyleId}`)
    }
  }

  const onCloseError = (redirect) => {
    setErrorDialogOpen(false)

    if (redirect) {
      setAddUserOpen(true)
    }
  }

  const areArgyleKeysExist = () => {
    if(!argyleKeys){
      return false
    }
    return argyleKeys.client_id && argyleKeys.client_secret
  }

  useEffect(getKeys, []);

  if (!userList) {
    return <ProgressContainer/>
  }
  return (
    <Paper className="medium-paper-container">
      <div>
        <TextField
          onChange={filterList}
          className='grey-font full-width-input'
          placeholder="Enter Full Name"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search className="grey-font"/>
              </InputAdornment>
            ),
          }}
        />

        <Button className="blue-btn float-right add-user-btn "
                variant="contained"
                disabled={!areArgyleKeysExist()}

                onClick={() => setAddUserOpen(true)}>Add User</Button>
      </div>
      {!areArgyleKeysExist() && <div className={"no-keys-container"}>
        <Typography>
        No results found - Set Argyle API Keys
      </Typography>
      </div>}
      {areArgyleKeysExist() &&
      <UsersTable data={filteredUserList} count={paginationState.count}
                  loadNextPage={loadNextPage} loadPrevPage={loadPrevPage}
                  deleteUser={deleteUser}/>}
      <AddUserDialog
        open={addUserOpen}
        onClose={onCloseAddUser}
      />
      <ConfirmationDialog
        open={successDialogOpen}
        onClose={onCloseSuccess}
        message='User has been successfully connected!'
        rightBtnText='View User Details'
        success={true}
      />
      <ConfirmationDialog
        open={errorDialogOpen}
        onClose={onCloseError}
        message={`Couldn't add this User.\nPlease try again.`}
        rightBtnText='Retry Connection'
        success={false}
      />

    </Paper>
  )
}
