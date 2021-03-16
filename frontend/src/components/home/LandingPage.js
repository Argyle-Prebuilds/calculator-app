import {Box, Button, Divider, Typography} from "@material-ui/core";
import React from "react";
import {useHistory} from "react-router-dom";

export const LandingPage = () => {

  const history = useHistory()

  const redirectToLogin = () => {
    history.push('/auth/login')
  }
  return <Box className='homepage-container'>

    <div className="logo-box">
      <img src='/assets/argyle.svg' width={90}/>
    </div>
    <Box className='shadowed-box under-logo margin-bottom-30'>
      <Typography variant={'h5'} className='box-header'>Argyle
        Calculator</Typography>
      <Divider className='box-divider'/>
      <Typography variant={'h6'} className='box-text'>
        The app is the quickest way to connect, verify and control employment
        data
        from Argyle API. The Admin can log in to the app and add employers that
        he
        wants to control.
        The new employer can be added by providing his Argyle token.
        After adding the new employer, the admin can retrieve information about
        a
        given User, and view data visualizations/calculations on the User's
        Argyle
        data.</Typography>
    </Box>

    <Box className='shadowed-box margin-bottom-30'>
      <img src='/assets/chart.png' style={{width: '100%'}}/>
    </Box>
    <Box className='inline-boxes-container margin-bottom-30'>
      <Box className='shadowed-box'>
        <Typography variant={'h5'} className='box-header'>Lorem ipsum
          1</Typography>
        <Divider className='box-divider'/>

        <Typography variant={'h6'} className='box-text'>
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut..</Typography>
      </Box>
      <Box className='shadowed-box'>
        <Typography variant={'h5'} className='box-header'>Lorem ipsum
          2</Typography>
        <Divider className='box-divider'/>

        <Typography variant={'h6'} className='box-text'>
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut .</Typography>
      </Box>
      <Box className='shadowed-box'>
        <Typography variant={'h5'} className='box-header'>Lorem ipsum
          3</Typography>
        <Divider className='box-divider'/>

        <Typography variant={'h6'} className='box-text'>
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut </Typography>
      </Box>
      <Box className='shadowed-box'>
        <Typography variant={'h5'} className='box-header'>Lorem ipsum
          3</Typography>
        <Divider className='box-divider'/>

        <Typography variant={'h6'} className='box-text'>
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut .</Typography>
      </Box>
    </Box>
    <div className="">
      <Button
        variant="contained"
        color="primary"
        className="homepage-login-btn"
        type="submit"
        fullWidth
        onClick={redirectToLogin}
      >
        Log In to Argyle Calculator
      </Button>
    </div>

  </Box>
}
