import React from "react";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import {NavBarItem} from "./NavBarItem";
import {Divider} from "@material-ui/core";
import SupervisorAccountIcon from '@material-ui/icons/SupervisorAccount';
import PowerSettingsNewIcon from '@material-ui/icons/PowerSettingsNew';
import "../stylesheets/styles-navigation.css"


export const LeftNavBar = () => {
  return <Drawer variant="permanent" anchor={"left"} style={{
    flexShrink: 0,
  }}>
    <List className='menu-container'>
      <NavBarItem link="/accounts/" title="Admin List"
                  icon={<SupervisorAccountIcon/>}/>
      <Divider className="padded-divider"/>
      <NavBarItem link="/auth/logout/" title="Logout"
                  icon={<PowerSettingsNewIcon/>}/>
    </List>
  </Drawer>
}
