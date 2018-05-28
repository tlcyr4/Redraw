import React from 'react';


import BrokenDoor from './images/404Door.png';

function Error(props) {
    return (
        <div>
            <img id="brokenDoor" src={BrokenDoor} alt="404 Error" height={props.window.innerHeight*0.8}/>
            <div id="pageNotFound">
                <h1>Page Not Found</h1>
                <h2>Oh no!</h2>
                <p>Something went terribly wrong!</p>
                <p>Please navigate out of the page and report the issue.</p>
            </div>
        </div>
    )
}

export default Error;