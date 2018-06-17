import React from 'react';
import Tabs, { Tab } from 'material-ui/Tabs';

import Logo from './images/raw.jpg';

function Header(props) {
    return (
        <div id="header">
            <a href="/"><img id ="headerImg" src={Logo} alt="Logo"/><p>edraw</p></a>

            <div id = "tabs">
                <Tabs value={props.value} onChange={props.handlePage} scrollable scrollButtons="off" indicatorColor="primary">
                    <Tab label = "About" className={props.classes.headerLabels}/>
                    <Tab label = "Feedback" className={props.classes.headerLabels}/>
                    <Tab label = "Logout" className={props.classes.headerLabels}/>
                </Tabs>
            </div>
        </div>
    )
}

export default Header;